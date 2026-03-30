# Slidev MCP Server

A self-hosted MCP server that lets AI assistants generate, render, and host Slidev presentations from markdown. An agent connects via MCP, reads resources describing Slidev syntax and themes, calls `render_slides` with markdown + a theme name, and gets back a shareable URL.

## Architecture

The stack runs as a single Docker Compose deployment:

```
MCP Client ──MCP/HTTP──▶ MCP Server (Python/FastMCP)
                              │
                              ├── POST /build ──▶ Builder (Bun HTTP server)
                              │                       │
                              │                  Per-theme Slidev projects
                              │                  (isolated node_modules)
                              │                       │
                              │                  Static HTML output
                              │                       ▼
                              ├── slides-data volume ◀─┘
                              │
                         Nginx serves /slides/{uuid}/
```

**Services** (defined per-environment in `docker-compose.{dev,local,prod}.yml`):

| Service | Image | Purpose |
|---|---|---|
| `mcp-server` | `python:3.13-slim` + uv | FastMCP server, build orchestration via HTTP |
| `builder` | `oven/bun` | Bun HTTP server, per-theme Slidev builds |
| `postgres` | `postgres:17-alpine` | Build metadata, versioned markdown, GC tracking |
| `nginx` | `nginx:alpine` | Static file serving for built slides |
| `traefik` | `traefik:v3.6` | TLS, routing, rate limiting (local + prod only) |

**Key design decisions:**
- Builder communicates via HTTP (port 3000), not Docker socket — no socket mount, no proxy needed
- Each theme is a separate Bun project with its own `package.json`, `node_modules`, and Slidev version
- Builder has outbound internet (`builder-egress` network) for fonts/images during Playwright export, plus `isolated` for MCP server communication. Non-root user, `no-new-privileges`
- Slides use hash-based routing (`routerMode: hash`) so nginx serves static files without SPA fallback
- No base `docker-compose.yml` — each environment file is self-contained

## Repository Structure

```
slidev-mcp/
├── src/slidev_mcp/            # Python MCP server
│   ├── server.py              # FastMCP app, lifespan, tool + resource registration
│   ├── tools.py               # render_slides, list_session_slides (business logic)
│   ├── builder.py             # HTTP client to builder service
│   ├── sessions.py            # In-memory UUID→session map
│   ├── models.py              # SQLAlchemy ORM (Slide, SlideVersion tables)
│   ├── db.py                  # Async engine, session factory
│   ├── resource_registry.py   # Maps resource URIs → files
│   ├── config.py              # pydantic-settings, ALLOWED_THEMES
│   ├── errors.py              # Typed error classes
│   └── resources/             # Hand-authored + fetched resources
│       ├── installed_themes.md
│       ├── theme_guide.md     # Theme selection guide (style, tone, best-for)
│       ├── examples/          # minimal.md, full_demo.md
│       └── themes/            # Per-theme README + example.md (fetched from npm/GitHub)
│
├── builder/                   # Bun-based builder container
│   ├── Dockerfile             # Per-theme project generation, install, validation
│   ├── server.ts              # HTTP server (POST /build, GET /health)
│   ├── build-job.ts           # Build logic: copy theme, patch frontmatter, run slidev build
│   ├── themes.json            # Single source of truth for all themes
│   ├── bunfig.toml            # Disables lifecycle scripts
│   └── scripts/
│       ├── init-themes.ts     # Generates per-theme project dirs from themes.json
│       └── validate-themes.ts # Builds test slide for each theme, removes failures
│
├── docker/
│   ├── Dockerfile.mcp         # MCP server image (multi-stage: vendor docs + Python)
│   └── nginx.conf             # Static file serving config
│
├── docker-compose.dev.yml     # Dev: builder + postgres only, ports exposed
├── docker-compose.local.yml   # Local: full stack with mkcert TLS
├── docker-compose.prod.yml    # Prod: full stack with Let's Encrypt
│
├── docs/                      # VitePress → GitHub Pages
│   ├── .vitepress/
│   │   ├── config.ts          # VitePress config + vitepress-plugin-llms
│   │   ├── themes.ts          # Theme gallery data with preview URLs
│   │   └── theme/components/  # ThemeCard.vue, ThemeGallery.vue
│   ├── clients/               # 10 MCP client setup guides
│   ├── guide/                 # Getting started, deployment, configuration
│   └── reference/             # Tools, resources, themes, limitations
│
├── scripts/
│   ├── bootstrap.sh           # Clone vendor/slidev-docs at pinned ref
│   ├── fetch-theme-readmes.py # Fetch README + example.md from npm/GitHub
│   ├── backup.sh              # pg_dump + slides tar, 7-day rotation
│   └── restore.sh             # Restore from backup
│
├── tests/                     # pytest (59 tests)
│   ├── test_builder.py        # HTTP mock tests for build orchestration
│   ├── test_tools.py          # Tool input/output, UUID validation, errors
│   ├── test_e2e.py            # Full MCP round-trip via FastMCP Client
│   ├── test_sessions.py       # In-memory session map
│   ├── test_config.py         # Settings defaults, theme allowlist
│   ├── test_models.py         # SQLAlchemy model
│   ├── test_resource_registry.py
│   ├── test_server.py         # Tool + resource registration
│   └── test_errors.py
│
├── pyproject.toml             # uv project, ruff, pytest config
├── Makefile                   # Developer commands
├── .github/workflows/         # CI, Docker build+push, docs deploy
└── traefik-dynamic.yml        # mkcert TLS config (local only)
```

## Theme Management

Themes are defined in `builder/themes.json` — the single source of truth:

```json
{
  "slidev_cli_version": "0.50.0",
  "themes": {
    "neocarbon": {
      "package": "slidev-theme-neocarbon",
      "version": "1.0.5",
      "license": "MIT",
      "slidev_cli_version": "52.14.1",
      "repo": "https://github.com/enyineer/slidev-theme-neocarbon"
    },
    "penguin": {
      "package": "slidev-theme-penguin",
      "version": "2.3.1",
      "license": "MIT",
      "repo": "https://github.com/alvarosabu/slidev-theme-penguin",
      "extra_dependencies": {
        "@iconify-json/logos": "^1"
      }
    }
  }
}
```

- `slidev_cli_version` at root is the default; per-theme `slidev_cli_version` overrides it
- `extra_dependencies` adds packages the theme needs but doesn't declare
- At Docker build time: `init-themes.ts` generates per-theme projects, `bun install` runs in parallel, `validate-themes.ts` builds a test slide for each theme and removes failures
- The ALLOWED_THEMES list in `config.py` must match the themes in `themes.json`

**Adding a theme:**
1. Add entry to `builder/themes.json` (package, version, license, repo, optional overrides)
2. Add theme name to `ALLOWED_THEMES` in `src/slidev_mcp/config.py`
3. Add description row to `src/slidev_mcp/resources/installed_themes.md`
4. Add entry to `src/slidev_mcp/resources/theme_guide.md` (style, tone, best-for, key features)
5. Run `python3 scripts/fetch-theme-readmes.py` to fetch README + example.md
6. Add entry to `docs/.vitepress/themes.ts` (with preview URLs if available)
7. Rebuild builder: `docker build -t slidev-mcp-builder -f builder/Dockerfile builder/`
8. Check validation output — if the theme fails, investigate (wrong Slidev version? missing deps?)

## MCP Tools

### `render_slides`
- Parameters: `markdown` (str), `theme` (str), `uuid` (str | None)
- Returns: `ToolResult` with JSON text content (url, uuid, build_time_seconds)
- Annotations: `readOnlyHint=false`, `openWorldHint=false`
- **MCP App:** `app=AppConfig(resourceUri="ui://slidev-mcp/viewer.html")` — clients that support the MCP Apps extension see the built slides embedded inline; non-app clients get the same JSON text response
- Tool description instructs LLMs to read `slidev://themes/{name}` before calling
- UUID validation: `^[0-9a-f]{8}-[0-9a-f]{4}-4[0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}$`

### `list_session_slides`
- No parameters
- Returns: `SessionSlides` dataclass (list of `SlideInfo`)
- Annotations: `readOnlyHint=true`

All parameters use `typing.Annotated` with string descriptions. Errors are returned via `ValueError` with `[error_code] message` format.

### MCP App: Slide Viewer

The `render_slides` tool declares an MCP App (`ui://slidev-mcp/viewer.html`). On clients that support the MCP Apps extension protocol (e.g. Claude Desktop), the built slide deck is rendered in a sandboxed iframe directly in the conversation. The viewer:
- Receives the tool result via `@modelcontextprotocol/ext-apps` SDK
- Embeds the slides URL in an iframe with 16:10 aspect ratio
- Shows a "Building slides..." state while waiting
- Displays a link, UUID, and build time below the preview
- Supports iterative updates (re-renders on each new tool result)

Non-app clients (CLI, most IDEs) receive the same JSON text and are unaffected.

## MCP Resources

| URI pattern | Source |
|---|---|
| `slidev://guide/syntax` | `vendor/slidev-docs/` (pinned upstream) |
| `slidev://guide/animations` | `vendor/slidev-docs/` |
| `slidev://builtin/components` | `vendor/slidev-docs/` |
| `slidev://builtin/layouts` | `vendor/slidev-docs/` |
| `slidev://themes/installed` | `src/slidev_mcp/resources/installed_themes.md` |
| `slidev://themes/guide` | `src/slidev_mcp/resources/theme_guide.md` (style/tone selection guide) |
| `slidev://themes/{name}` | `src/slidev_mcp/resources/themes/{name}.md` (README + example.md merged) |
| `slides://session` | Dynamic — all slides in the current session (theme, markdown, URL) |
| `slides://session/{uuid}` | Dynamic — single slide detail with version history |
| `slidev://examples/minimal` | `src/slidev_mcp/resources/examples/minimal.md` |
| `slidev://examples/full_demo` | `src/slidev_mcp/resources/examples/full_demo.md` |

Per-theme resources are loaded dynamically from the `resources/themes/` directory at startup.
Session slide resources (`slides://`) are dynamic `@mcp.resource` handlers that query the database.

## Environment Variables

| Variable | Default | Description |
|---|---|---|
| `DOMAIN` | `localhost` | Public domain for MCP API |
| `SLIDES_DOMAIN` | *(falls back to DOMAIN)* | Separate domain for slides (origin isolation) |
| `DATABASE_URL` | `postgresql+asyncpg://slidev:slidev@localhost:5432/slidev` | PostgreSQL connection |
| `BUILDER_HOST` | `builder` | Builder HTTP server hostname |
| `BUILDER_PORT` | `3000` | Builder HTTP server port |
| `BUILD_TIMEOUT` | `120` | Max seconds per build |
| `MAX_CONCURRENT_BUILDS` | `3` | Semaphore limit (currently unused — builder handles concurrency) |
| `SLIDE_TTL_DAYS` | `30` | Days before sealed slides are GC'd |
| `GC_INTERVAL_HOURS` | `6` | GC background task interval |
| `SERVER_TRANSPORT` | `stdio` | `stdio` or `streamable-http` |
| `SERVER_HOST` | `0.0.0.0` | Bind host (HTTP mode) |
| `SERVER_PORT` | `8000` | Bind port (HTTP mode) |
| `LOG_LEVEL` | `INFO` | Python log level |
| `LOG_FORMAT` | `json` | `json` or `text` |
| `ACME_EMAIL` | — | Let's Encrypt email (prod only) |
| `POSTGRES_PASSWORD` | — | Required for production |

## Coding Conventions

1. **Pydantic models for data structures.** `BaseModel` with `Annotated[type, Field(description="...")]`. Tool inputs use `Annotated` string descriptions; return types are dataclasses or `ToolResult`.
2. **Async-first.** SQLAlchemy async engine with asyncpg. Builder communication via httpx AsyncClient.
3. **Type-hint everything.** `str | None` not `Optional[str]`. Dataclasses for structured return types.
4. **Fail fast.** Catch specific exceptions at system boundaries. Tool errors returned as structured MCP errors via ValueError.
5. **No heavy frameworks.** No FastAPI, LangChain, or orchestration frameworks. FastMCP handles the server.
6. **Configuration via Settings singleton.** pydantic-settings loads from `.env`.
7. **MCP best practices.** `Annotated` descriptions on all tool parameters. Dataclass return types for structured output. MCP `annotations` (readOnlyHint, openWorldHint, title) on all tools.

## Quality Gates

```bash
make lint          # ruff check .
make format-check  # ruff format --check .
make test          # pytest (59 tests, no live services)
make pr-ready      # lint-fix + format + test
```

CI runs on every PR: `uv sync` → `ruff check` → `ruff format --check` → `pytest`.

## Deployment

**Infrastructure:** Single Infomaniak OpenStack VM, provisioned via `scripts/provision.sh`.

**CI/CD pipeline** (`.github/workflows/deploy.yml`): push to main triggers build → backup → deploy.

```
Push to main
  ↓
Job 1: build
  - Build slidev-mcp-server + slidev-mcp-builder images
  - Push to GHCR with :latest and :sha-${SHA} tags
  ↓
Job 2: backup
  - SSH to server, run pre-deploy backup
  - Download PG dump, encrypt with GPG (AES256)
  - Upload as GitHub artifact (90-day retention)
  ↓
Job 3: deploy
  - SCP docker-compose.prod.yml, nginx.conf, scripts
  - Write .env.production from GitHub Secrets
  - docker compose pull + up -d --remove-orphans
```

**Manual deploy:** `DEPLOY_HOST=x.x.x.x scripts/deploy.sh` (requires `.env.production` already on server).

**Backup:** Daily at 3 AM via cron (`scripts/backup.sh`). PG dump + slides tarball, 7-day rotation.

**Restore:** Trigger `.github/workflows/restore.yml` from Actions tab with a workflow run ID.

**GitHub Secrets required:** `DEPLOY_SSH_KEY`, `DEPLOY_HOST`, `DEPLOY_USER`, `POSTGRES_PASSWORD`, `ACME_EMAIL`, `BACKUP_ENCRYPTION_KEY`.

**GitHub Variables:** `DOMAIN` (default: `slidev-mcp.org`), `DEPLOY_DIR` (default: `/opt/slidev-mcp`).

## Security

- **Builder network:** `isolated` (internal, for MCP server communication) + `builder-egress` (outbound internet for fonts/images during Playwright export). No exposed ports — only outbound connections possible.
- **Builder hardening:** Non-root user (uid 1000), `no-new-privileges`, resource limits (2 CPU, 2GB RAM)
- **No Docker socket:** Builder communicates via HTTP, not docker exec. No socket mount anywhere.
- **Theme allowlist:** Only pre-installed themes. Theme names validated with `^[a-z0-9-]+$` regex + allowlist check.
- **UUID v4 validation:** User-supplied UUIDs validated against UUID v4 regex before any filesystem operations.
- **Origin isolation:** `SLIDES_DOMAIN` serves slides from a separate domain to prevent same-origin XSS.
- **Lifecycle scripts disabled:** `bunfig.toml` with `install.lifecycle.ignore = true` in every theme project.
- **Traefik rate limiting:** 60 req/min average, burst 10, on `/mcp` route (prod).

## Do Not

- Use `npm`, `npx`, or `node` for JS tooling. Use `bun` everywhere (builder, docs, scripts).
- Add FastAPI, Flask, or any web framework. FastMCP handles the server.
- Allow dynamic `bun install` of themes not in the allowlist. Ever.
- Run `bun install` at build time inside the running builder. `node_modules` is baked into the image.
- Expose builder ports or give it inbound network access. Outbound egress for fonts/images is OK.
- Accept user-supplied UUIDs without UUID v4 format validation (path traversal risk).
- Trust theme names from user input without allowlist + regex validation.
- Serve slides from the same origin as the MCP API in production. Use `SLIDES_DOMAIN`.
- Store build artifacts in the database. PG holds metadata only; slides live on the filesystem.
- Edit `uv.lock` manually. Use `uv add/remove`.
- Commit `.env`, `.env.production`, or any secrets.

## Makefile Commands

| Command | Description |
|---|---|
| `make install` | `uv sync` |
| `make bootstrap` | Clone vendor docs + fetch theme READMEs |
| `make lint` / `make lint-fix` | ruff check |
| `make format` / `make format-check` | ruff format |
| `make test` / `make test-all` | pytest (unit / all including integration) |
| `make pr-ready` | lint-fix + format + test |
| `make serve` | Run MCP server locally (stdio) |
| `make docker-build` | Build both Docker images |
| `make docker-dev-up/down` | Dev stack (builder + postgres) |
| `make docker-local-up/down` | Full local stack with mkcert TLS |
| `make docker-prod-up/down` | Production stack with Let's Encrypt |
| `make deploy` | Show deploy info (CI/CD handles deploys) |
| `make deploy-manual` | SSH deploy escape hatch |
| `make docs-dev/build/preview` | VitePress docs |
