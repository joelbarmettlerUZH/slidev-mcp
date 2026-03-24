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
git clone https://github.com/joelbarmettler/slidev-mcp.git
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
docker compose -f docker-compose.yml -f docker-compose.prod.yml up -d
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
| **Docker Socket Proxy** | Restricted Docker API proxy for build dispatch |

## Verify

Check that all services are running:

```bash
docker compose -f docker-compose.yml -f docker-compose.prod.yml ps
```

Test the MCP endpoint:

```bash
curl https://mcp.example.com/mcp
```

## Updates

Pull the latest images and restart:

```bash
docker compose -f docker-compose.yml -f docker-compose.prod.yml pull
docker compose -f docker-compose.yml -f docker-compose.prod.yml up -d
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
