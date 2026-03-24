# Slidev MCP Server — Implementation Plan

## 1. What We're Building

A self-hosted MCP server that lets LLM agents generate, render, and host Slidev presentations from markdown. An agent
connects via MCP, reads resources describing Slidev syntax and available themes, then calls a tool with markdown + a
theme name. The server delegates the build to an isolated builder container running Bun + Slidev, which produces a
static site deployed to a public URL. The tool returns the link. During the same MCP session the agent can update the
deck by re-submitting markdown with the same UUID. Once the session ends, the UUID is sealed and immutable.

The entire stack runs on a single Infomaniak OpenStack VM as one Docker Compose deployment: Traefik (TLS + routing),
FastMCP (Python 3.13, `streamable-http` transport), a dedicated builder container (Bun + Slidev, no network access),
PostgreSQL (build metadata + GC), Nginx (static file serving). Documentation lives in a VitePress site deployed to
GitHub Pages.

Reference architecture: see `slidev-mcp-architecture.md`.


---

## 2. Specifications

### 2.1 MCP Resources

Resources are served from the **upstream Slidev documentation**, cloned from
`https://github.com/slidevjs/slidev` (sparse checkout of the `docs/` subtree). This avoids maintaining hand-written
copies that drift from the actual docs. At bootstrap time, the repo is cloned into `vendor/slidev-docs/`. The server
reads selected files at startup and registers them as MCP resources.

A thin resource registry in `src/slidev_mcp/resource_registry.py` maps resource URIs to filesystem paths within the
cloned docs. Only a curated subset of the docs tree is exposed — not the entire repo.

| Resource URI | Source path (relative to `vendor/slidev-docs/`) | Content |
|---|---|---|
| `slidev://guide/syntax` | `guide/syntax.md` | Slide separators, frontmatter, notes, comments |
| `slidev://guide/animations` | `guide/animations.md` | `<v-click>`, transitions, motion |
| `slidev://builtin/components` | `builtin/components.md` | Built-in components reference |
| `slidev://builtin/layouts` | `builtin/layouts.md` | Built-in layout reference |
| `slidev://themes/gallery` | `themes/gallery.md` | Community themes gallery |
| `slidev://themes/use` | `themes/use.md` | How to configure and use themes |
| `slidev://themes/installed` | `src/slidev_mcp/resources/installed_themes.md` | **Ours.** Which themes are pre-installed in our builder |
| `slidev://examples/{name}` | `src/slidev_mcp/resources/examples/` | **Ours.** Hand-written example decks |

**What stays hand-authored:** Only the `examples/` directory (working slide decks for the LLM to reference) and
`installed_themes.md` (listing which themes are pre-installed and available without dynamic install). Everything else
comes from upstream.

**Versioning:** The cloned docs are pinned to a git tag or commit matching the Slidev version in `slidev-template/
package.json`. When we bump Slidev, we bump the pinned docs ref. `make bootstrap` handles the clone + checkout.

**Docker:** The `vendor/slidev-docs/` directory is copied into the MCP server image at build time. No git operations
at runtime.

### 2.2 MCP Tools

#### `render_slides`

| Parameter | Type | Required | Description |
|---|---|---|---|
| `markdown` | `str` | yes | Full Slidev markdown (including frontmatter) |
| `theme` | `str` | yes | Theme package name (e.g. `seriph`, `apple-basic`, `default`) |
| `uuid` | `str \| None` | no | If provided and owned by current session, overwrites. If `None`, generates new. |

Returns: `{ url: str, uuid: str, build_time_seconds: float }`

Errors (returned as structured MCP tool errors, not raised exceptions):
- `theme_not_allowed` — theme name failed validation (not in allowlist or malformed).
- `invalid_uuid` — UUID does not match UUID v4 format (`^[0-9a-f]{8}-...-[0-9a-f]{12}$`).
- `uuid_sealed` — UUID exists but belongs to a closed session.
- `uuid_foreign` — UUID exists but belongs to a different active session.
- `build_failed` — Bun/Slidev build exited non-zero. Include stderr excerpt in error message.
- `build_timeout` — Build exceeded the configured timeout (default 120s).
- `markdown_too_large` — Markdown exceeds size limit (default 1 MB).
- `concurrent_limit` — Build semaphore is full; retry later.

#### `list_session_slides`

No parameters. Returns `{ slides: list[{ uuid, url, theme, created_at, updated_at }] }`.

### 2.3 Session & UUID Lifecycle

**Session management is handled entirely by FastMCP.** FastMCP v3 natively tracks sessions via its transport layer
(each streamable-http or SSE connection has a session ID). We do not reimplement session tracking.

**UUID ownership is tracked in-memory** in a simple dict: `dict[str, str]` mapping `uuid → session_id`. This is
sufficient because:
- Session-scoped mutability is a convenience feature, not a durability guarantee.
- If the server restarts, all active sessions are gone anyway, so in-memory state is consistent.
- The only invariant that must survive restarts is "sealed UUIDs cannot be overwritten," which is enforced by checking
  PostgreSQL: if a UUID exists in the `slides` table and is not in the in-memory active map, it is sealed by definition.

**Lifecycle:**

```
Session connects (FastMCP assigns session_id)
  │
  ├─ render_slides(markdown, theme)
  │    → generate uuid, add to in-memory map: {uuid: session_id}
  │    → insert row in PG: (uuid, session_id, theme, created_at)
  │    → build → return URL
  │
  ├─ render_slides(markdown, theme, uuid=same)
  │    → in-memory map confirms ownership → overwrite build → update PG row
  │
Session disconnects
  │
  └─ FastMCP fires session cleanup → remove all entries for this session_id from in-memory map
     (PG rows remain; uuid is now implicitly sealed because it's in PG but not in the active map)
```

**On server restart:** The in-memory map is empty. All previously created UUIDs exist in PG and are therefore sealed.
No data loss, no inconsistency.

### 2.4 Build Pipeline & Isolation

Builds run in a **dedicated builder container** — not as a subprocess in the MCP server process. This provides:
- **Security isolation:** The builder has no network access, no access to the MCP server's filesystem or database.
  Even if user-provided markdown contains malicious Vue components that execute at build time, the blast radius is
  contained to a disposable, network-less container with limited CPU/memory.
- **Resource limits:** Docker `--memory`, `--cpus`, `--pids-limit` enforced at the container level.
- **Clean environment:** Each build gets a fresh(ish) container filesystem. No cross-contamination between builds.

**How it works:**

The builder container runs a long-lived lightweight process (a simple HTTP server or Unix socket listener) that accepts
build requests from the MCP server. Alternatively, the MCP server uses `docker exec` or the Docker API to run build
commands inside the builder container. The simpler approach:

1. The MCP server writes `slides.md` and a `build-manifest.json` (containing theme name, uuid, base path) to a
   **build-inbox volume** at `/data/builds/{uuid}/`.
2. The MCP server calls `docker exec builder bun run build-job /data/builds/{uuid}` (or sends a request to a minimal
   HTTP endpoint inside the builder).
3. The builder reads the manifest, copies the pre-warmed template, writes `slides.md`, patches the theme, runs
   `slidev build --base /slides/{uuid}/`, and writes output to `/data/builds/{uuid}/dist/`.
4. The MCP server detects build completion (by polling for `dist/index.html` or via the exec exit code), moves
   `dist/` to `/data/slides/{uuid}/`, and cleans up the inbox.
5. Nginx serves `/data/slides/{uuid}/` immediately.

**Volume layout:**

| Volume | Mounted in | Access | Purpose |
|---|---|---|---|
| `slides-data` | MCP (rw), Nginx (ro) | Final built slides | `/data/slides/{uuid}/` |
| `build-inbox` | MCP (rw), Builder (rw) | Build input + output staging | `/data/builds/{uuid}/` |

**Concurrency:** The MCP server holds an `asyncio.Semaphore(MAX_CONCURRENT_BUILDS)`. The builder container can handle
concurrent builds (each in its own `/data/builds/{uuid}/` directory). If more isolation is needed later, we can switch
to ephemeral builder containers per build — but a single long-lived builder with directory-level isolation is sufficient
for v1.

### 2.5 Theme Validation & Security

User-provided theme names are **untrusted input**. A malicious or careless theme name could:
- Trigger `bun install` of an arbitrary npm package (supply chain attack).
- Execute arbitrary code via `postinstall` scripts.
- Install a package that is not a Slidev theme at all.

**Mitigations (all mandatory for v1):**

1. **Allowlist only.** The builder ships with a fixed set of pre-installed themes. The MCP server validates the `theme`
   parameter against this allowlist before dispatching a build. No dynamic `bun install` of unknown packages. The
   allowlist is defined in `config.py` and also documented in the `slidev://themes/installed` resource.

2. **No `bun install` at build time.** The builder's `node_modules/` is baked into the image. The build script must
   never run `bun install`, `npm install`, or any package manager command. If a theme is not pre-installed, the tool
   returns a `theme_not_allowed` error.

3. **`--ignore-scripts` in the builder image.** When building the Docker image, all `bun install` commands use
   `--ignore-scripts` (or the Bun equivalent: `--no-install-scripts` / `bunfig.toml` with
   `install.lifecycle.ignore = true`) to prevent `postinstall` scripts from running even for pre-installed themes.

4. **Builder has no network.** The builder container is on an `internal` Docker network with no external access
   (`internal: true`). Even if code execution occurs during `slidev build`, it cannot reach the internet.

5. **Builder runs as non-root.** The Dockerfile creates a dedicated `builder` user. All build operations run under
   this user with limited filesystem permissions.

6. **Theme name format validation.** Before even checking the allowlist, reject theme names that don't match
   `^[a-z0-9-]+$` (lowercase alphanumeric + hyphens only). This prevents path traversal, command injection, and other
   shenanigans.

7. **UUID v4 format validation.** User-supplied UUIDs are validated against
   `^[0-9a-f]{8}-[0-9a-f]{4}-4[0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}$` before any filesystem operations. This
   prevents path traversal via crafted UUIDs (e.g. `../../etc`). Implemented in `tools.py`.

8. **Docker socket proxy.** The MCP server does **not** mount `/var/run/docker.sock` directly. Instead, a
   [Tecnativa docker-socket-proxy](https://github.com/Tecnativa/docker-socket-proxy) sits between the MCP server and
   the Docker daemon, exposing only `CONTAINERS` + `EXEC` + `POST` endpoints. This limits blast radius if the MCP
   server is compromised — an attacker cannot create arbitrary containers or mount host paths.

9. **Origin isolation for served slides.** Slidev output contains user-controlled JavaScript (Vue components,
   `<script setup>` blocks). To prevent same-origin XSS from slides reaching the `/mcp` endpoint, slides should be
   served from a **separate domain** (configured via `SLIDES_DOMAIN` env var, e.g. `slides.example.com` vs
   `mcp.example.com`). When `SLIDES_DOMAIN` is unset, it falls back to `DOMAIN` for backward compatibility.

10. **Builder filesystem hardening.** The builder container runs with `read_only: true` (immutable root filesystem),
    `tmpfs` for `/tmp`, and `security_opt: ["no-new-privileges:true"]`. This limits what a compromised build process
    can do even within the container.

### 2.6 Image & Asset Limitations

Slidev markdown can reference images in several ways. Each has different implications for our architecture:

| Image source | Works in our setup? | Notes |
|---|---|---|
| **Remote URLs** (`![](https://...)`) | Yes | Slidev embeds them as `<img src="...">`. Browser fetches at view time. |
| **Local relative paths** (`![](./images/foo.png)`) | **No (v1)** | Would require file upload support. No mechanism to get binary files into the build. |
| **Base64 inline** (`![](data:image/png;base64,...)`) | Yes | Works but inflates markdown size. Subject to the 1 MB limit. |
| **Unsplash/URL shorthand** (Slidev-specific) | Yes | Resolved at build time by Slidev (builder needs network? No — resolved to URL in HTML). |

**v1 stance:** Only remote URLs and base64 inline images are supported. Local image paths will produce broken images
in the built deck. The `slidev://guide/syntax` resource and our example decks must document this limitation clearly.
The `render_slides` tool description should state: "Images must be remote URLs or base64-encoded inline. Local file
paths are not supported."

**Future (v2+):** Add an `upload_asset` tool that accepts base64-encoded images and writes them to the build inbox
alongside `slides.md`. The builder would then copy them into the Slidev project's `public/` directory before building.
This requires changes to the build manifest and the inbox volume layout, but is architecturally straightforward.

### 2.7 Non-Functional Requirements

- Build time target: under 30s for a typical 20-slide deck on a 4-vCPU VM. The pre-warmed template + no `bun install`
  should make this achievable. Measure and optimize in Phase 3.
- Slide hosting: static HTML served with gzip and Brotli, 1h cache, no authentication.
- Availability: single-VM, best-effort. `restart: unless-stopped` on all services.
- Storage: 80 GB disk. Each build produces ~2–10 MB. At 30-day TTL, supports thousands of decks.


---

## 3. Tech Stack & Tooling

### 3.1 Runtime

| Component | Version | Purpose |
|---|---|---|
| Python | 3.13 | MCP server runtime |
| uv | latest | Package management, virtual environments, lockfile |
| FastMCP | v3 (latest) | MCP protocol (streamable-http transport), session management |
| SQLAlchemy | 2.x (async) | ORM for PostgreSQL |
| asyncpg | latest | Async PostgreSQL driver (used by SQLAlchemy async engine) |
| pydantic-settings | latest | Configuration from env vars |
| PostgreSQL | 17-alpine | Build metadata, GC tracking |
| Bun | latest | Slidev build runner (in builder container) |
| Slidev | latest stable | Slide rendering engine |
| Traefik | v3.6+ | Reverse proxy, TLS (Let's Encrypt), rate limiting |
| Nginx | alpine | Static file serving |
| Docker Compose | v2 | Orchestration |

### 3.2 Quality & CI

| Tool | Config Location | Purpose |
|---|---|---|
| ruff | `pyproject.toml` `[tool.ruff]` | Linting + formatting (replaces black, isort, flake8) |
| pytest + pytest-asyncio | `pyproject.toml` `[tool.pytest]` | Unit + integration tests |
| GitHub Actions | `.github/workflows/` | CI (lint + test), image build + push, docs deploy |
| Makefile | `Makefile` | Developer UX: single commands for all tasks |

### 3.3 Ruff Configuration

Mirrors the vue-docs-mcp project. In root `pyproject.toml`:

```toml
[tool.ruff]
line-length = 100
target-version = "py313"

[tool.ruff.lint]
select = ["E", "W", "F", "I", "UP", "B", "SIM", "TCH", "RUF"]

[tool.ruff.lint.isort]
known-first-party = ["slidev_mcp"]

[tool.ruff.format]
quote-style = "double"
```

### 3.4 Pytest Configuration

```toml
[tool.pytest.ini_options]
asyncio_mode = "auto"
testpaths = ["tests"]
markers = [
    "integration: requires live services (PostgreSQL, builder container)",
]
addopts = "-m 'not integration'"
```


---

## 4. Repository Structure

```
slidev-mcp/
├── pyproject.toml                 # uv project, ruff, pytest config
├── uv.lock
├── .python-version                # 3.13
├── Makefile                       # Developer commands
├── README.md
├── .env.example
├── .gitignore
│
├── src/
│   └── slidev_mcp/
│       ├── __init__.py
│       ├── server.py              # FastMCP app, lifespan, tool + resource registration
│       ├── tools.py               # render_slides, list_session_slides
│       ├── builder.py             # Build dispatch: write inbox, exec in builder, collect output
│       ├── sessions.py            # In-memory UUID→session map, ownership checks
│       ├── models.py              # SQLAlchemy ORM models (Slide table)
│       ├── db.py                  # Async engine, session factory, create_tables()
│       ├── resource_registry.py   # Maps resource URIs → vendor/slidev-docs/ file paths
│       ├── config.py              # pydantic-settings: Settings singleton, theme allowlist
│       ├── errors.py              # Typed error classes for tool responses
│       └── resources/             # Hand-authored resources (only what we own)
│           ├── installed_themes.md
│           └── examples/
│               ├── minimal.md
│               └── full_demo.md
│
├── vendor/
│   └── slidev-docs/               # Sparse checkout of slidevjs/slidev docs/ (gitignored, created by make bootstrap)
│
├── builder/                       # Everything for the builder container
│   ├── Dockerfile                 # Bun + Slidev + pre-installed themes, non-root user, no network
│   ├── bunfig.toml                # install.lifecycle.ignore = true (disable postinstall scripts)
│   ├── build-job.ts               # Entrypoint script: read manifest, copy template, patch theme, build
│   ├── package.json               # @slidev/cli + all allowlisted themes
│   ├── bun.lock
│   └── template/                  # Minimal Slidev project skeleton
│       ├── package.json           # References parent node_modules (workspace or symlink)
│       └── slides.md              # Placeholder
│
├── docker/
│   ├── Dockerfile.mcp             # Python 3.13 + uv + vendor/slidev-docs baked in
│   └── nginx.conf                 # Static file serving config
│
├── docker-compose.yml             # Shared base (volumes, networks)
├── docker-compose.dev.yml         # Dev: postgres exposed, no Traefik
├── docker-compose.local.yml       # Local: Traefik with mkcert TLS
├── docker-compose.prod.yml        # Prod: Traefik with Let's Encrypt
│
├── docs/                          # VitePress → GitHub Pages
│   ├── package.json
│   ├── .vitepress/
│   │   └── config.ts
│   ├── index.md
│   ├── guide/
│   │   ├── getting-started.md
│   │   ├── architecture.md
│   │   ├── deployment.md
│   │   └── configuration.md
│   ├── reference/
│   │   ├── tools.md
│   │   ├── resources.md
│   │   ├── themes.md
│   │   └── limitations.md         # Image limitations, known constraints
│   └── contributing.md
│
├── scripts/
│   ├── bootstrap.sh               # Clone/update vendor/slidev-docs at pinned ref
│   ├── setup-vm.sh                # OpenStack VM bootstrap
│   ├── deploy.sh                  # SSH deploy: pull + restart
│   ├── backup.sh                  # pg_dump + slides tarball, 7-day rotation
│   └── restore.sh                 # Restore from backup
│
├── .github/
│   └── workflows/
│       ├── ci.yml                 # Lint + test on PRs
│       ├── build-and-push.yml     # Build Docker images, push to GHCR on main
│       └── deploy-docs.yml        # Build VitePress, deploy to GitHub Pages
│
└── tests/
    ├── conftest.py                # Shared fixtures (mock context, in-memory session map)
    ├── test_builder.py            # Build dispatch unit tests (mocks docker exec)
    ├── test_sessions.py           # In-memory ownership, sealing on disconnect
    ├── test_tools.py              # Tool input/output contracts, theme validation
    ├── test_config.py             # Settings loading, theme allowlist
    ├── test_models.py             # SQLAlchemy model constraints
    ├── test_resource_registry.py  # Resource URI resolution
    └── test_integration.py        # Full round-trip (marked integration)
```


---

## 5. Coding Conventions

Aligned with the team's existing conventions from the vue-docs-mcp project.

1. **Pydantic models for all data structures.** Use `BaseModel` with `Annotated[type, Field(description="...")]`. Tool
   inputs and outputs are Pydantic models, not raw dicts.

2. **Async-first.** All I/O operations use `async`/`await`. SQLAlchemy uses the async engine (`create_async_engine`
   with `asyncpg`). Docker exec uses `asyncio.create_subprocess_exec`. Use `asyncio.Semaphore` for concurrency.

3. **Type-hint everything.** Return types mandatory. Modern syntax: `str | None` not `Optional[str]`, `list[str]` not
   `List[str]`.

4. **Fail fast.** No broad try/except. Catch specific exceptions at system boundaries (subprocess calls, DB ops, Docker
   exec). Let everything else propagate. Tool errors are returned as structured error responses, not raised exceptions.

5. **No heavy frameworks.** No LangChain, no FastAPI (FastMCP handles the server). Direct `asyncio.subprocess` for
   Docker exec. Keep the dependency tree shallow.

6. **Configuration via Settings singleton.** `slidev_mcp.config.Settings` loads from `.env` via pydantic-settings.
   All tunables (domain, paths, timeouts, concurrency limits, TTL, theme allowlist) are env vars with sensible defaults.

7. **Server state via lifespan.** FastMCP v3 lifespan context initializes the DB engine, session map, and build
   semaphore. Start the GC background task. On shutdown: dispose the engine, cancel background tasks.

8. **SQLAlchemy ORM for PostgreSQL.** ORM models in `slidev_mcp.models`. Async engine + `AsyncSession`. Tables created
   via `Base.metadata.create_all()` (wrapped in `run_sync`). No separate migration tool.

9. **In-memory session tracking.** A plain `dict[str, str]` mapping `uuid → session_id`, protected by nothing (Python
   GIL is sufficient for dict ops in a single-process async server). FastMCP's session lifecycle hooks manage
   insertions and cleanup.

10. **Resource files from vendor.** The `resource_registry.py` maps URIs to `Path` objects. At startup, it verifies
    all paths exist. If a path is missing (e.g. Slidev docs restructured), the server logs a warning and skips that
    resource — it does not crash.


---

## 6. Quality Gates

### 6.1 Every PR Must Pass

| Gate | Command | What It Checks |
|---|---|---|
| Lint | `make lint` | `ruff check` — no warnings, no errors |
| Format | `make format-check` | `ruff format --check` — code is formatted |
| Unit tests | `make test` | `pytest` — all non-integration tests pass |
| No manual style | — | Don't manually fix style. Run `make lint-fix && make format`. |

### 6.2 Before Merging to Main

| Gate | Command | What It Checks |
|---|---|---|
| Full check | `make pr-ready` | `make lint-fix && make format && make test` |
| Docker build | `make docker-build` | Both images build successfully |

### 6.3 CI Pipeline (GitHub Actions)

**`ci.yml`** (on every PR):
1. `uv sync`
2. `ruff check .`
3. `ruff format --check .`
4. `pytest` (unit tests only — no live services)

**`build-and-push.yml`** (on push to `main`):
1. Build both Docker images (`Dockerfile.mcp` + `builder/Dockerfile`)
2. Push to GHCR
3. Optionally trigger deploy via `scripts/deploy.sh`

**`deploy-docs.yml`** (on push to `main`, `docs/**` path filter):
1. Install deps in `docs/`
2. Build VitePress
3. Deploy to GitHub Pages

### 6.4 Makefile Commands

```makefile
.PHONY: install bootstrap lint lint-fix format format-check test test-all pr-ready \
        serve docker-build docker-dev-up docker-dev-down docker-prod-up docker-prod-down

install:
	uv sync

bootstrap:
	scripts/bootstrap.sh

lint:
	uv run ruff check .

lint-fix:
	uv run ruff check --fix .

format:
	uv run ruff format .

format-check:
	uv run ruff format --check .

test:
	uv run pytest

test-all:
	uv run pytest -m ""

test-integration:
	docker compose -f docker-compose.yml -f docker-compose.dev.yml up -d
	uv run pytest -m integration
	docker compose -f docker-compose.yml -f docker-compose.dev.yml down

pr-ready: lint-fix format test

serve:
	uv run python -m slidev_mcp.server

docker-build:
	docker build -t slidev-mcp-server -f docker/Dockerfile.mcp .
	docker build -t slidev-mcp-builder -f builder/Dockerfile builder/

docker-dev-up:
	docker compose -f docker-compose.yml -f docker-compose.dev.yml up -d

docker-dev-down:
	docker compose -f docker-compose.yml -f docker-compose.dev.yml down

docker-local-up:
	docker compose -f docker-compose.yml -f docker-compose.local.yml up -d

docker-local-down:
	docker compose -f docker-compose.yml -f docker-compose.local.yml down

docker-prod-up:
	docker compose -f docker-compose.yml -f docker-compose.prod.yml up -d

docker-prod-down:
	docker compose -f docker-compose.yml -f docker-compose.prod.yml down
```


---

## 7. Docker Compose Architecture

### 7.1 Services

| Service | Image | Network | Volumes | Purpose |
|---|---|---|---|---|
| `traefik` | `traefik:v3.6` | `web` | `traefik-certs` | TLS termination, routing, rate limiting |
| `docker-socket-proxy` | `tecnativa/docker-socket-proxy` | `isolated` | docker socket (ro) | Restricted Docker API proxy (CONTAINERS+EXEC+POST only) |
| `mcp-server` | `ghcr.io/.../slidev-mcp-server` | `web`, `internal`, `isolated` | `slides-data` (rw), `build-inbox` (rw) | FastMCP server, build orchestration |
| `builder` | `ghcr.io/.../slidev-mcp-builder` | `isolated` (internal, no egress) | `build-inbox` (rw), `slides-data` (rw) | Bun + Slidev builds (read_only, no-new-privileges) |
| `postgres` | `postgres:17-alpine` | `internal` | `pg-data` | Build metadata, GC tracking |
| `nginx` | `nginx:alpine` | `web` | `slides-data` (ro) | Static file serving |

### 7.2 Networks

| Network | External access | Services |
|---|---|---|
| `web` | Yes (via Traefik) | traefik, mcp-server, nginx |
| `internal` | No | mcp-server, postgres |
| `isolated` | No, `internal: true` | mcp-server, builder, docker-socket-proxy |

The builder is on the `isolated` network which has `internal: true` set in Docker Compose. This means containers on
this network cannot reach the internet — only other containers on the same network. The MCP server is on both
`internal` (to reach PG) and `isolated` (to reach the builder). The builder cannot reach PG, Traefik, or the internet.

### 7.3 Volumes

| Volume | Purpose |
|---|---|
| `traefik-certs` | ACME certificates |
| `slides-data` | Final built slides (`/data/slides/{uuid}/`) |
| `build-inbox` | Build staging area (`/data/builds/{uuid}/`) |
| `pg-data` | PostgreSQL data |

### 7.4 Simplified Compose (prod)

```yaml
services:
  traefik:
    image: traefik:v3.6
    ports: ["80:80", "443:443"]
    networks: [web]
    volumes:
      - /var/run/docker.sock:/var/run/docker.sock:ro
      - traefik-certs:/certs
    command:
      - --providers.docker=true
      - --providers.docker.exposedbydefault=false
      - --entrypoints.web.address=:80
      - --entrypoints.websecure.address=:443
      - --certificatesresolvers.le.acme.httpchallenge.entrypoint=web
      - --certificatesresolvers.le.acme.email=${ACME_EMAIL}
      - --certificatesresolvers.le.acme.storage=/certs/acme.json

  docker-socket-proxy:
    image: tecnativa/docker-socket-proxy:latest
    networks: [isolated]
    volumes:
      - /var/run/docker.sock:/var/run/docker.sock:ro
    environment:
      CONTAINERS: 1
      EXEC: 1
      POST: 1

  mcp-server:
    image: ghcr.io/${GITHUB_REPO}/slidev-mcp-server:latest
    networks: [web, internal, isolated]
    labels:
      - traefik.enable=true
      - traefik.http.routers.mcp.rule=Host(`${DOMAIN}`) && PathPrefix(`/mcp`)
      - traefik.http.routers.mcp.entrypoints=websecure
      - traefik.http.routers.mcp.tls.certresolver=le
      - traefik.http.services.mcp.loadbalancer.server.port=8000
      - traefik.http.middlewares.mcp-rate.ratelimit.average=60
      - traefik.http.middlewares.mcp-rate.ratelimit.burst=10
      - traefik.http.routers.mcp.middlewares=mcp-rate
    volumes:
      - slides-data:/data/slides
      - build-inbox:/data/builds
    environment:
      - DOMAIN=${DOMAIN}
      - SLIDES_DOMAIN=${SLIDES_DOMAIN:-}
      - DATABASE_URL=postgresql+asyncpg://slidev:${POSTGRES_PASSWORD}@postgres:5432/slidev
      - SERVER_TRANSPORT=streamable-http
      - DOCKER_HOST=tcp://docker-socket-proxy:2375
    depends_on:
      postgres: { condition: service_healthy }
      builder: { condition: service_started }
      docker-socket-proxy: { condition: service_started }

  builder:
    image: ghcr.io/${GITHUB_REPO}/slidev-mcp-builder:latest
    networks: [isolated]
    volumes:
      - build-inbox:/data/builds
      - slides-data:/data/slides
    user: "1000:1000"
    read_only: true
    tmpfs:
      - /tmp
    security_opt:
      - "no-new-privileges:true"
    deploy:
      resources:
        limits: { cpus: "2", memory: 2G }
    command: ["sleep", "infinity"]

  postgres:
    image: postgres:17-alpine
    networks: [internal]
    volumes:
      - pg-data:/var/lib/postgresql/data
    environment:
      - POSTGRES_DB=slidev
      - POSTGRES_USER=slidev
      - POSTGRES_PASSWORD=${POSTGRES_PASSWORD}
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U slidev"]
      interval: 5s
      retries: 5

  nginx:
    image: nginx:alpine
    networks: [web]
    labels:
      - traefik.enable=true
      - traefik.http.routers.slides.rule=Host(`${DOMAIN}`) && PathPrefix(`/slides`)
      - traefik.http.routers.slides.entrypoints=websecure
      - traefik.http.routers.slides.tls.certresolver=le
      - traefik.http.services.slides.loadbalancer.server.port=8080
    volumes:
      - slides-data:/data/slides:ro

networks:
  web:
  internal:
  isolated:
    internal: true   # No external egress

volumes:
  traefik-certs:
  slides-data:
  build-inbox:
  pg-data:
```


---

## 8. Implementation Phases

### Phase 1 — Project Skeleton, Config & Data Layer

**Goal:** A working Python project with uv, ruff, pytest, SQLAlchemy models, and a PostgreSQL connection. No MCP yet,
no builder, no Docker. Just the data layer and project scaffolding.

**Deliverables:**

1. Initialize repo: `uv init`, `.python-version` → `3.13`, `pyproject.toml` with ruff + pytest config (sections 3.3
   and 3.4 of this doc).
2. Create `src/slidev_mcp/` package: `__init__.py`, `config.py`, `models.py`, `db.py`, `errors.py`, `sessions.py`.
3. **`config.py`:** `Settings` model via pydantic-settings. Fields: `domain`, `database_url`, `slides_dir`,
   `build_inbox_dir`, `build_timeout` (120), `max_concurrent_builds` (3), `slide_ttl_days` (30), `gc_interval_hours`
   (6), `server_transport` (`stdio`), `server_host`, `server_port`, `log_level`, `log_format`. Plus
   `ALLOWED_THEMES: list[str]` as a class-level constant (not env var) listing all pre-installed theme names.
4. **`models.py`:** SQLAlchemy 2.x declarative ORM model:
   ```python
   class Slide(Base):
       __tablename__ = "slides"
       uuid: Mapped[str] = mapped_column(String, primary_key=True)
       session_id: Mapped[str] = mapped_column(String, nullable=False, index=True)
       theme: Mapped[str] = mapped_column(String, nullable=False)
       created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
       updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
   ```
5. **`db.py`:** `create_async_engine`, `async_sessionmaker`, `async def create_tables()` (uses `run_sync` +
   `Base.metadata.create_all`), `async def get_session()` context manager.
6. **`sessions.py`:** `SessionMap` class:
   - `_active: dict[str, str]` — uuid → session_id.
   - `def register(uuid, session_id)`, `def owns(uuid, session_id) -> bool`,
     `def remove_session(session_id) -> list[str]` (returns removed UUIDs), `def is_active(uuid) -> bool`.
   - Pure in-memory, no I/O, trivially testable.
7. **`errors.py`:** `ThemeNotAllowed`, `UuidSealed`, `UuidForeign`, `BuildFailed`, `BuildTimeout`,
   `MarkdownTooLarge`, `ConcurrentLimitReached`. All inherit from a base `SlidevMcpError`.
8. **Tests:**
   - `test_config.py`: Settings loads defaults, respects env overrides.
   - `test_sessions.py`: register, ownership check, removal on disconnect, is_active for unknown uuid.
   - `test_models.py`: Slide model instantiation, constraint validation.
9. `Makefile` with `install`, `lint`, `lint-fix`, `format`, `format-check`, `test`, `pr-ready`.
10. `.github/workflows/ci.yml`: lint + format check + unit tests.

**Quality gate:** `make pr-ready` passes.

**Estimated effort:** 2 days.

---

### Phase 2 — Builder Container & Build Pipeline

**Goal:** A working builder container and the MCP server's build orchestration module. Given markdown + theme, produces
a static Slidev site on disk. Tested end-to-end locally via Docker.

**Deliverables:**

1. **`builder/` directory:**
   - `Dockerfile`: `FROM oven/bun:latest`. Create non-root `builder` user (uid 1000). Copy `package.json`, `bun.lock`,
     `bunfig.toml`. Run `bun install --frozen-lockfile` (lifecycle scripts are already disabled via `bunfig.toml`).
     Copy `template/` and `build-job.ts`. Set `USER builder`. `CMD ["sleep", "infinity"]`.
   - `bunfig.toml`: `[install.lifecycle] ignore = true` — disables all postinstall/preinstall scripts.
   - `package.json`: `@slidev/cli` + all themes from the allowlist as direct dependencies.
   - `template/`: minimal Slidev project (`package.json` that references the shared `node_modules`, empty `slides.md`).
   - `build-job.ts`: a Bun script that:
     - Takes a single argument: build directory path (e.g. `/data/builds/{uuid}`).
     - Reads `build-manifest.json` from that directory (`{ theme, uuid, base_path }`).
     - Copies the template into a `work/` subdirectory of the build dir.
     - Writes `slides.md` from the build directory into `work/slides.md`.
     - Patches the theme into frontmatter.
     - Runs `bunx slidev build --base {base_path} --out ../dist` from the `work/` directory.
     - On success: `dist/` is written to `{build_dir}/dist/`.
     - On failure: writes exit code + stderr to `{build_dir}/error.json`.
     - Cleans up `work/`.

2. **`src/slidev_mcp/builder.py`:** `BuildOrchestrator` class:
   - `async def build(markdown, theme, uuid) -> BuildResult`:
     - Validates theme against `Settings.ALLOWED_THEMES`. Raises `ThemeNotAllowed` if not found.
     - Validates theme name format: `^[a-z0-9-]+$`. Raises `ThemeNotAllowed` if malformed.
     - Validates markdown size against limit. Raises `MarkdownTooLarge`.
     - Writes `slides.md` and `build-manifest.json` to `/data/builds/{uuid}/`.
     - Runs `docker exec builder bun run /app/build-job.ts /data/builds/{uuid}` via
       `asyncio.create_subprocess_exec` with timeout.
     - On success: moves `/data/builds/{uuid}/dist/` to `/data/slides/{uuid}/`. Returns `BuildResult`.
     - On failure: reads `error.json`, raises `BuildFailed` with stderr excerpt.
     - On timeout: kills subprocess, raises `BuildTimeout`.
     - Always cleans up `/data/builds/{uuid}/` in a `finally` block.
   - Holds reference to `asyncio.Semaphore` for concurrency control.

3. **`docker-compose.dev.yml`:** Add `builder` and `postgres` services. Builder mounts `build-inbox` and `slides-data`.
   Postgres with health check.

4. **Tests:**
   - `test_builder.py` (unit): Mock `asyncio.create_subprocess_exec`. Test theme validation, markdown size check,
     manifest writing, dist directory moving, error/timeout handling.
   - `test_builder.py` (integration, marked): Actually run a build via Docker. Requires
     `make docker-dev-up` to have the builder running.

5. **Performance baseline:** Time a build of the `minimal.md` example. Record in the PR. Target: < 15s for a 3-slide
   deck. If slower, investigate: is `copytree` slow? Is `slidev build` slow? Profile and document findings.

6. Add `make docker-build` (builds both images), `make docker-dev-up/down`.

**Quality gate:** `make pr-ready` passes. Integration test builds a real Slidev deck and produces `index.html`.
Build time for `minimal.md` is documented.

**Estimated effort:** 3–4 days.

---

### Phase 3 — FastMCP Server, Tools & Resources

**Goal:** A fully functional MCP server. Connects to PostgreSQL, tracks sessions in-memory, dispatches builds to the
builder container, serves upstream Slidev docs as resources. End-to-end testable with Claude Desktop.

**Deliverables:**

1. **`scripts/bootstrap.sh`:**
   - Sparse-clones `https://github.com/slidevjs/slidev` into `vendor/slidev-docs/`, checking out only the `docs/`
     subtree at the pinned git ref.
   - Idempotent: if already cloned, does `git fetch` + `git checkout {ref}`.
   - The pinned ref is defined as a variable at the top of the script, matching the Slidev version in
     `builder/package.json`.

2. **`src/slidev_mcp/resource_registry.py`:**
   - `RESOURCE_MAP: dict[str, Path]` — maps URI strings to filesystem paths.
   - Upstream resources point into `vendor/slidev-docs/`.
   - Hand-authored resources point into `src/slidev_mcp/resources/`.
   - `def load_resources(vendor_dir: Path, package_dir: Path) -> dict[str, str]` — reads all files, returns
     `{uri: content}`. Logs warnings for missing files, does not crash.

3. **Hand-authored resources:**
   - `src/slidev_mcp/resources/installed_themes.md`: list of themes in the allowlist with one-line descriptions.
   - `src/slidev_mcp/resources/examples/minimal.md`: 3-slide deck (title, content, end). Uses only remote image URLs.
   - `src/slidev_mcp/resources/examples/full_demo.md`: 10-slide deck showcasing layouts, code blocks, animations,
     components. Documents image limitations inline.

4. **`server.py`:**
   - FastMCP app with `streamable-http` or `stdio` transport based on `Settings.server_transport`.
   - **Lifespan:** create async engine, `create_tables()`, instantiate `SessionMap`, `BuildOrchestrator`,
     `asyncio.Semaphore`. Load resources via `resource_registry`. Start GC background task. On shutdown: cancel GC
     task, dispose engine.
   - **Resources:** Register each resource from the loaded map as a FastMCP resource.
   - **Session hooks:** Use FastMCP's session lifecycle to call `session_map.remove_session(session_id)` on disconnect.
   - **Tools:** Register `render_slides` and `list_session_slides`.
   - **GC background task:** Every `gc_interval_hours`, query PG for slides where `created_at < now - ttl_days` AND
     uuid is not in the active session map. Delete PG rows + filesystem directories.

5. **`tools.py`:**
   - `render_slides`: extract `session_id` from FastMCP context. Check in-memory map for UUID ownership. If new UUID,
     acquire semaphore, call `builder.build()`, register in session map + insert PG row. If existing UUID and owned,
     acquire semaphore, rebuild, update PG row. Return `{url, uuid, build_time_seconds}`.
   - `list_session_slides`: query PG for rows matching current `session_id`.
   - All errors caught and returned as structured MCP tool errors.

6. **Tests:**
   - `test_tools.py`: Mock builder + session map + DB. Test all happy paths and error conditions from Section 2.2.
   - `test_resource_registry.py`: Verify resource loading with a fixture vendor dir. Test missing file warning.
   - `test_server.py`: Verify all resources and tools are registered.

7. `make bootstrap` added to Makefile. `make serve` runs the server in stdio mode.

**Quality gate:** `make pr-ready` passes. Manual end-to-end test with Claude Desktop: connect → read resource → render
slides → verify URL → update → verify update → disconnect → verify seal.

**Estimated effort:** 3–4 days.

---

### Phase 4 — Docker Compose & Networking

**Goal:** The full stack runs in Docker Compose with all three network tiers (web, internal, isolated). Local dev with
mkcert TLS. Production-ready with Let's Encrypt.

**Deliverables:**

1. **`docker/Dockerfile.mcp`** (multi-stage):
   - Stage 1 (`vendor`): `FROM alpine/git`. Clone Slidev docs at pinned ref.
   - Stage 2 (`runtime`): `FROM python:3.13-slim`. Install uv. Copy `pyproject.toml` + `uv.lock` → `uv sync --frozen`.
     Copy vendor docs from stage 1. Copy `src/`. Create `/data/slides` and `/data/builds`. Non-root user.
   - `CMD ["uv", "run", "python", "-m", "slidev_mcp.server"]`.
   - **Note:** Unlike the previous plan, Bun is NOT installed in this image. Builds happen in the builder container.

2. **`docker/nginx.conf`:** Gzip + Brotli (if available), `try_files`, cache headers, security headers
   (`X-Frame-Options`, `X-Content-Type-Options`).

3. **`docker-compose.yml`** (base): Define all volumes and networks.

4. **`docker-compose.dev.yml`:** Postgres + builder only. Ports exposed for local development. MCP server runs on host
   via `make serve`.

5. **`docker-compose.local.yml`:** All services. Traefik with mkcert file provider. For full local stack testing.

6. **`docker-compose.prod.yml`:** All services. Traefik with Let's Encrypt. Rate limiting. `restart: unless-stopped`.
   `.env.production.example` with all required vars.

7. **Builder networking verification:** After `docker compose up`, verify that the builder container cannot reach the
   internet: `docker exec builder ping -c1 8.8.8.8` must fail. Document this check in `contributing.md`.

8. **Build dispatch mechanism:** The MCP server runs `docker exec` commands in the builder container via a
   **Docker socket proxy** (Tecnativa). The proxy is the only service that mounts `/var/run/docker.sock` and only
   exposes the `CONTAINERS`, `EXEC`, and `POST` API endpoints. The MCP server connects to the proxy via
   `DOCKER_HOST=tcp://docker-socket-proxy:2375`. This prevents the MCP server from creating arbitrary containers,
   mounting host paths, or escalating to root on the host — even if compromised.

9. `make docker-build`, `make docker-local-up/down`, `make docker-prod-up/down`.

**Quality gate:** `make docker-build` succeeds. `make docker-local-up` starts all 5 services. End-to-end test via
MCP client against `https://$DOMAIN/mcp`. Builder network isolation verified.

**Estimated effort:** 2–3 days.

---

### Phase 5 — CI/CD & GitHub Actions

**Goal:** Automated quality on PRs. Automated image builds and deployment on merge.

**Deliverables:**

1. **`.github/workflows/ci.yml`** (on PR):
   ```yaml
   steps:
     - uses: actions/checkout@v4
     - uses: astral-sh/setup-uv@v5
     - run: uv sync
     - run: uv run ruff check .
     - run: uv run ruff format --check .
     - run: uv run pytest
   ```

2. **`.github/workflows/build-and-push.yml`** (on push to `main`, paths-ignore `docs/**`):
   - Build `docker/Dockerfile.mcp` → push `ghcr.io/{repo}/slidev-mcp-server:{sha}` + `:latest`.
   - Build `builder/Dockerfile` → push `ghcr.io/{repo}/slidev-mcp-builder:{sha}` + `:latest`.

3. **`.github/workflows/deploy-docs.yml`** (on push to `main`, paths `docs/**`):
   - Build VitePress → deploy to GitHub Pages.

4. **Optional:** Add deploy job to `build-and-push.yml` that SSHs to the VM and runs `scripts/deploy.sh`.

**Quality gate:** CI passes on a test PR. Images pushed to GHCR on merge.

**Estimated effort:** 1 day.

---

### Phase 6 — VitePress Documentation

**Goal:** Public docs site on GitHub Pages.

**Deliverables:**

1. `docs/package.json`, `docs/.vitepress/config.ts`.
2. Pages:
   - `index.md`: hero, feature highlights, quick-start.
   - `guide/getting-started.md`: prerequisites, clone, bootstrap, serve, connect Claude Desktop.
   - `guide/architecture.md`: diagram, component responsibilities, build pipeline, network isolation.
   - `guide/deployment.md`: VM setup, DNS, `.env.production`, `make docker-prod-up`.
   - `guide/configuration.md`: full table of all env vars.
   - `reference/tools.md`: tool schemas, parameters, return values, error codes.
   - `reference/resources.md`: all resource URIs with descriptions.
   - `reference/themes.md`: installed themes with descriptions.
   - `reference/limitations.md`: **Image limitations** (Section 2.6 of this doc, adapted for end-users). Other known
     constraints (markdown size limit, concurrent builds, TTL).
   - `contributing.md`: dev setup, `make pr-ready`, adding themes, adding resources, network isolation verification.

**Quality gate:** Docs build without warnings. GitHub Actions deploys.

**Estimated effort:** 2 days.

---

### Phase 7 — Production Hardening & Observability

**Goal:** Safe, observable, and resilient for public use.

**Deliverables:**

1. **Security hardening (implemented):**
   - Builder container: `user: "1000:1000"`, `deploy.resources.limits` (2 CPU, 2 GB RAM), `read_only: true` with
     tmpfs for `/tmp`. `security_opt: ["no-new-privileges:true"]`.
   - Docker socket proxy (Tecnativa): MCP server does not mount raw socket. Proxy allows only CONTAINERS+EXEC+POST.
   - Origin isolation: `SLIDES_DOMAIN` config for serving slides from a separate domain.
   - UUID v4 format validation in `tools.py`: `^[0-9a-f]{8}-[0-9a-f]{4}-4[0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}$`.
   - Builder Dockerfile uses `bun install --frozen-lockfile` for reproducible builds.
   - Traefik rate limiting: 60 req/min average, burst 10, on `/mcp` route.
   - Nginx security headers: `X-Frame-Options: SAMEORIGIN`, `X-Content-Type-Options: nosniff`.

2. **Observability:**
   - Structured JSON logging via `structlog` or Python's `logging` with a JSON formatter.
   - Log every build: uuid, session_id, theme, duration, success/failure, markdown size.
   - Health endpoint: `GET /health` — checks PG connection and returns build semaphore availability.
   - Traefik access logs enabled.

3. **Resilience:**
   - `restart: unless-stopped` on all services.
   - Graceful shutdown: on SIGTERM, cancel GC task, wait for in-progress builds (with timeout), dispose DB engine.
   - GC background task tested with synthetic data.

4. **Backup:**
   - `scripts/backup.sh`: `pg_dump` + optional `tar` of `/data/slides`, 7-day rotation.
   - `scripts/restore.sh`: restore from backup.

**Quality gate:** Rate limiting verified with `wrk`. Health endpoint returns meaningful JSON. GC deletes old slides.
Builder cannot reach the internet. Logs are parseable JSON.

**Estimated effort:** 2–3 days.


---

## 9. Testing Strategy

### Unit Tests (run on every PR, no external deps)

| File | What It Tests |
|---|---|
| `test_builder.py` | Theme validation (allowlist + regex), markdown size check, manifest writing, subprocess mocking, error/timeout handling |
| `test_sessions.py` | In-memory map: register, owns, remove_session, is_active |
| `test_tools.py` | Tool input validation, error responses, happy paths. Mocks builder + session map + DB. |
| `test_config.py` | Settings loads defaults, env overrides, theme allowlist is populated |
| `test_models.py` | SQLAlchemy Slide model constraints |
| `test_resource_registry.py` | URI → path resolution, missing file handling |

### Integration Tests (require `make docker-dev-up`)

| Scope | What It Tests | Requires |
|---|---|---|
| Build round-trip | Markdown in → `index.html` out | Builder container running |
| DB persistence | Insert slide row → query it back | PostgreSQL running |
| GC | Create expired slide → run GC → verify deleted from PG + disk | PostgreSQL + filesystem |
| Theme rejection | Non-allowlisted theme → `theme_not_allowed` error | Builder container |

### Manual Acceptance Tests (before production deploy)

1. Connect Claude Desktop to the server (stdio mode locally, or streamable-http via Docker).
2. Ask Claude to read the Slidev syntax resource.
3. Ask Claude to create a 5-slide presentation. Verify the returned URL works in a browser.
4. Ask Claude to update slide 3 and re-render. Verify the URL reflects the change.
5. Disconnect and reconnect. Ask Claude to overwrite the old UUID. Verify it's rejected.
6. Verify the builder cannot reach the internet (`docker exec builder ping -c1 8.8.8.8` fails).
7. Verify a non-allowlisted theme is rejected without any `bun install` attempt.

### Mocking Patterns

- `unittest.mock.AsyncMock` for FastMCP context (provides session_id).
- `unittest.mock.patch` on `asyncio.create_subprocess_exec` to mock Docker exec.
- SQLAlchemy async in-memory SQLite for DB tests (`sqlite+aiosqlite://`), or mock the session factory.
- Helper functions (`_mock_ctx(session_id)`, `_make_slide(...)`) in `conftest.py` — prefer helpers over fixtures.


---

## 10. Key Technical Decisions

| Decision | Rationale |
|---|---|
| **Upstream docs as MCP resources** | Avoids maintaining hand-written copies that drift. Pin to the Slidev version we ship. |
| **PostgreSQL over SQLite** | Consistent with the team's stack (vue-docs-mcp). Runs in its own container, proper backup via `pg_dump`, no file-locking surprises. |
| **SQLAlchemy async ORM** | Team convention. Typed models, `create_tables()` for schema, async engine with asyncpg. |
| **In-memory session tracking** | FastMCP manages sessions natively. UUID→session is a convenience map, not durable state. PG is the source of truth for "does this UUID exist"; the in-memory map only answers "is it currently mutable." |
| **Isolated builder container** | User markdown can contain arbitrary Vue/JS that executes at Slidev build time. Builder has no network, limited resources, non-root user. Blast radius is contained. |
| **Theme allowlist (no dynamic install)** | Eliminates supply chain attacks via `bun install` of arbitrary packages. The allowlist is a compile-time constant. |
| **`--ignore-scripts` / `bunfig.toml` lifecycle ignore** | Even pre-installed themes shouldn't run postinstall. Defense in depth. |
| **Bun over npm/pnpm** | Fastest install + build times. |
| **Pre-warmed template** | No `bun install` at build time. Template with `node_modules` is baked into the builder image. |
| **Nginx behind Traefik** | Traefik for TLS + routing + rate limiting. Nginx for fast static serving with gzip/Brotli. |
| **Docker socket proxy for build dispatch** | MCP server uses `docker exec` via a Tecnativa socket proxy (not a raw socket mount). Proxy only allows CONTAINERS+EXEC+POST — limits blast radius if MCP server is compromised. |
| **Origin isolation for slides** | Slides contain user-controlled JS. Serving from a separate `SLIDES_DOMAIN` prevents same-origin XSS from reaching the `/mcp` API endpoint. |
| **No LLM at build time** | The MCP client generates the markdown. Our server just builds and serves. Zero per-request API costs. |


---

## 11. Known Limitations (v1)

Document these in `docs/reference/limitations.md` and in the `render_slides` tool description.

| Limitation | Impact | Future mitigation |
|---|---|---|
| **No local images** | `![](./image.png)` produces broken images. Only remote URLs and base64 inline work. | Add `upload_asset` tool that stages files in the build inbox. |
| **No custom CSS/JS files** | Only what's expressible in Slidev markdown (inline `<style>`, `<script setup>`). | Same as above — asset upload. |
| **No PDF export** | Only static HTML output. | Add `export_pdf` tool using `slidev export` + Playwright in the builder. |
| **No live preview** | Every change requires a full static build (10–30s). | Run `slidev dev --remote` in a persistent container, proxy via Traefik. |
| **Theme set is fixed** | Only pre-installed themes. No dynamic install. | Expand the allowlist by rebuilding the builder image. Possibly add a vetted-install mechanism. |
| **No presenter mode** | Static build doesn't include Slidev's presenter view. | Could be enabled with `slidev build --with-presenter`. Verify security implications. |
| **In-memory session map lost on restart** | All UUIDs become sealed. Active sessions are disconnected. | Acceptable — sessions are ephemeral by design. PG remains consistent. |
| **Single-VM, single builder** | Max ~3 concurrent builds. No HA. | Scale with multiple builder containers or move to K8s. |


---

## 12. Environment Variables

| Variable | Default | Description |
|---|---|---|
| `SERVER_TRANSPORT` | `stdio` | `stdio` or `streamable-http` |
| `SERVER_HOST` | `0.0.0.0` | Bind host (streamable-http mode) |
| `SERVER_PORT` | `8000` | Bind port (streamable-http mode) |
| `DOMAIN` | `localhost` | Public domain for MCP API |
| `SLIDES_DOMAIN` | `` (falls back to `DOMAIN`) | Separate domain for serving slides (origin isolation) |
| `DOCKER_HOST` | — | Set to `tcp://docker-socket-proxy:2375` in Docker Compose |
| `DATABASE_URL` | `postgresql+asyncpg://slidev:slidev@localhost:5432/slidev` | SQLAlchemy async connection string |
| `SLIDES_DIR` | `/data/slides` | Where built slides are served from |
| `BUILD_INBOX_DIR` | `/data/builds` | Staging area for builder input/output |
| `BUILDER_CONTAINER_NAME` | `builder` | Docker container name for `docker exec` |
| `BUILD_TIMEOUT` | `120` | Max seconds per build |
| `MAX_CONCURRENT_BUILDS` | `3` | Semaphore limit |
| `SLIDE_TTL_DAYS` | `30` | Days before sealed slides are garbage-collected |
| `GC_INTERVAL_HOURS` | `6` | GC background task interval |
| `LOG_LEVEL` | `INFO` | Python log level |
| `LOG_FORMAT` | `json` | `json` or `text` |
| `ACME_EMAIL` | — | Required for production TLS |
| `POSTGRES_PASSWORD` | — | Required for production PG |


---

## 13. Do Not

- Add FastAPI, Flask, or any web framework. FastMCP handles the server.
- Use LangChain, LlamaIndex, or orchestration frameworks.
- Store build artifacts in the database. PG holds metadata only; slides live on the filesystem.
- Allow dynamic `bun install` of themes not in the allowlist. Ever.
- Run `bun install` at build time inside the builder. `node_modules` is baked into the image.
- Give the builder container network access. The `isolated` network must have `internal: true`.
- Mount `/var/run/docker.sock` directly into the MCP server. Use the Docker socket proxy instead.
- Serve slides from the same origin as the MCP API in production. Use `SLIDES_DOMAIN`.
- Accept user-supplied UUIDs without UUID v4 format validation (path traversal risk).
- Trust theme names from user input without allowlist + regex validation.
- Reimplement session tracking. Use FastMCP's native session lifecycle hooks.
- Persist the UUID→session map to disk or database. In-memory is correct and intentional.
- Edit `uv.lock` manually. Use `uv add/remove`.
- Commit `.env`, `.env.production`, or any secrets.
- Serve slides through the Python process. Nginx exists for this reason.
- Write migration scripts for PG. `Base.metadata.create_all()` is the schema source of truth (1 table).
- Maintain hand-written copies of Slidev documentation. Clone upstream and pin to a ref.
- Use `npm`, `npx`, or `node` for JS tooling. Use `bun` everywhere (builder, docs, scripts).
