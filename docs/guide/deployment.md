---
description: How to deploy Slidev MCP on your own server with Docker Compose.
---

# Deployment

Slidev MCP runs as a Docker Compose stack on a single VM. This guide covers production deployment with Let's Encrypt TLS.

## Prerequisites

- A Linux VM with Docker and Docker Compose v2 installed
- A domain name pointed at the VM's IP address (e.g. `mcp.example.com`)
- Optionally, a second domain for slides (e.g. `slides.example.com`) for [origin isolation](/reference/limitations)

## Quick Start

```bash
# Clone the repository
git clone https://github.com/joelbarmettlerUZH/slidev-mcp.git
cd slidev-mcp

# Create your .env file
cp .env.example .env
```

Edit `.env` with your production values:

```bash
DOMAIN=mcp.example.com
SLIDES_DOMAIN=slides.example.com   # Optional, for origin isolation
POSTGRES_PASSWORD=a-strong-password
ACME_EMAIL=you@example.com
```

Start the stack:

```bash
docker compose -f docker-compose.prod.yml up -d
```

Traefik will automatically obtain TLS certificates via Let's Encrypt. Your MCP server is now available at:

```
https://mcp.example.com/mcp
```

## Services

The stack runs 6 services:

| Service | Purpose |
|---|---|
| **Traefik** | TLS termination, routing, rate limiting |
| **MCP Server** | FastMCP server, build orchestration |
| **Builder** | Isolated Bun + Slidev build container (no network access) |
| **PostgreSQL** | Build metadata and garbage collection |
| **Nginx** | Static file serving for built slides |

## Verify

Check that all services are running:

```bash
docker compose -f docker-compose.prod.yml ps
```

Test the MCP endpoint:

```bash
curl https://mcp.example.com/mcp
```

## Updates

Pull the latest images and restart:

```bash
docker compose -f docker-compose.prod.yml pull
docker compose -f docker-compose.prod.yml up -d
```

## Backups

Back up the PostgreSQL database and slide files:

```bash
# Database
docker compose exec postgres pg_dump -U slidev slidev > backup.sql

# Slide files (optional — they can be rebuilt)
docker compose cp nginx:/data/slides ./slides-backup/
```

See [Configuration](/guide/configuration) for all available environment variables.

## Usage Statistics

The server records anonymous usage events (one row per tool call or resource read) in the `usage_events` table, so you can see how much it is used. Each row holds the tool or resource name, the theme (only names from the allowlist), the MCP client name, latency, response size and an error code. It does **not** store slide markdown, slide UUIDs, IP addresses or session identifiers. Events are kept indefinitely; delete rows yourself if you want a retention window.

The production stack includes an optional read-only dashboard. Set these in `.env` (or as GitHub secrets for the CI/CD deploy) to enable it:

```bash
DASHBOARD_DOMAIN=stats.example.com   # needs a DNS record pointing at your server
DASHBOARD_USER=admin
DASHBOARD_PASSWORD=at-least-12-characters
DASHBOARD_DB_PASSWORD=hex-password-for-the-read-only-db-role
```

The dashboard connects as a separate `dashboard_ro` Postgres role that can only `SELECT` from `usage_events`. Create it once (the deploy workflow does this automatically):

```sql
CREATE ROLE dashboard_ro LOGIN PASSWORD '...';
GRANT CONNECT ON DATABASE slidev TO dashboard_ro;
GRANT USAGE ON SCHEMA public TO dashboard_ro;
GRANT SELECT ON usage_events TO dashboard_ro;
ALTER ROLE dashboard_ro SET default_transaction_read_only = on;
```

Without the two passwords the dashboard container refuses to start; the rest of the stack is unaffected.
