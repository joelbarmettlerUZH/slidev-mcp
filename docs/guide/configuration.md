---
description: All environment variables and configuration options for Slidev MCP.
---

# Configuration

Slidev MCP is configured via environment variables. Set them in your `.env` file or pass them directly to Docker Compose.

## Environment Variables

### Server

| Variable | Default | Description |
|---|---|---|
| `SERVER_TRANSPORT` | `stdio` | Transport mode: `stdio` or `streamable-http` |
| `SERVER_HOST` | `0.0.0.0` | Bind host (streamable-http mode only) |
| `SERVER_PORT` | `8000` | Bind port (streamable-http mode only) |

### Domain

| Variable | Default | Description |
|---|---|---|
| `DOMAIN` | `localhost` | Public domain for the MCP API |
| `SLIDES_DOMAIN` | *(falls back to `DOMAIN`)* | Separate domain for serving slides. Recommended for production to prevent same-origin XSS from user-generated slide content. |

### Database

| Variable | Default | Description |
|---|---|---|
| `DATABASE_URL` | `postgresql+asyncpg://slidev:slidev@localhost:5432/slidev` | PostgreSQL connection string |
| `POSTGRES_PASSWORD` | — | PostgreSQL password (required for production) |

### Builder

| Variable | Default | Description |
|---|---|---|
| `BUILDER_HOST` | `builder` | Builder HTTP server hostname |
| `BUILDER_PORT` | `3000` | Builder HTTP server port |
| `BUILD_TIMEOUT` | `120` | Maximum seconds per build |
| `MAX_CONCURRENT_BUILDS` | `3` | Not used by the MCP server; concurrency is enforced by the builder (see below) |
| `SLIDES_DIR` | `/data/slides` | Directory for built slide files |

#### Builder limits

These are read by the builder container itself, not the MCP server. Every `slidev` run is stopped when it exceeds its limit (the whole process tree, including Chromium), and stopped early if the client disconnects. When all slots and the queue are full, the builder answers immediately with a "concurrent limit" error instead of piling up work.

| Variable | Default | Description |
|---|---|---|
| `BUILDER_BUILD_TIMEOUT_SECONDS` | `90` | Hard limit for `slidev build` |
| `BUILDER_PREVIEW_TIMEOUT_SECONDS` | `25` | Hard limit for the first-slide preview after a build (best effort) |
| `BUILDER_EXPORT_TIMEOUT_SECONDS` | `170` | Hard limit for a PDF or screenshot export |
| `BUILDER_MAX_CONCURRENT` | `2` | Jobs running at once (the container has 2 CPUs) |
| `BUILDER_MAX_QUEUED` | `8` | Jobs allowed to wait for a slot before new ones are rejected |

Keep the build limits below the MCP server's own timeouts (`BUILD_TIMEOUT` + 5 s for builds, 180 s for exports), or the server gives up first.

### Lifecycle

| Variable | Default | Description |
|---|---|---|
| `SLIDE_TTL_DAYS` | `30` | Days since last update before slides are garbage-collected |
| `GC_INTERVAL_HOURS` | `6` | How often the garbage collector runs |

### Logging

| Variable | Default | Description |
|---|---|---|
| `LOG_LEVEL` | `INFO` | Python log level (`DEBUG`, `INFO`, `WARNING`, `ERROR`) |
| `LOG_FORMAT` | `json` | Log format: `json` or `text` |

### TLS (Production)

| Variable | Default | Description |
|---|---|---|
| `ACME_EMAIL` | — | Email for Let's Encrypt certificate registration |
