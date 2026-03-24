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
| `DOCKER_HOST` | — | Docker API endpoint. Set to `tcp://docker-socket-proxy:2375` in Docker Compose. |
| `BUILDER_CONTAINER_NAME` | `builder` | Name of the builder container for `docker exec` |
| `BUILD_TIMEOUT` | `120` | Maximum seconds per build |
| `MAX_CONCURRENT_BUILDS` | `3` | Maximum simultaneous builds |
| `SLIDES_DIR` | `/data/slides` | Directory for built slide files |
| `BUILD_INBOX_DIR` | `/data/builds` | Staging area for build inputs/outputs |

### Lifecycle

| Variable | Default | Description |
|---|---|---|
| `SLIDE_TTL_DAYS` | `30` | Days before sealed slides are garbage-collected |
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
