---
description: How to contribute to Slidev MCP — development setup, testing, adding themes.
---

# Contributing

## Development Setup

```bash
# Clone and install
git clone https://github.com/joelbarmettlerUZH/slidev-mcp.git
cd slidev-mcp
make install

# Start infrastructure (Postgres + Builder)
make docker-dev-up

# Run the MCP server locally
make serve
```

## Quality Checks

Every PR must pass:

```bash
make pr-ready    # Runs: lint-fix, format, test
```

Individual commands:

| Command | What it does |
|---|---|
| `make lint` | Run ruff linter |
| `make lint-fix` | Auto-fix lint issues |
| `make format` | Format code with ruff |
| `make format-check` | Check formatting without changing files |
| `make test` | Run unit tests |
| `make test-all` | Run all tests including integration |

## Adding a Theme

1. Add the theme package to `builder/package.json`
2. Add the theme name to `ALLOWED_THEMES` in `src/slidev_mcp/config.py`
3. Add a description row to `src/slidev_mcp/resources/installed_themes.md`
4. Rebuild the builder image: `make docker-build`
5. Run `make pr-ready`

## Verifying Builder Isolation

After bringing up the stack, verify the builder container has no internet access:

The builder runs on an `internal: true` Docker network with no external egress. It cannot reach the internet by design.

## Project Structure

```
src/slidev_mcp/       # Python MCP server
builder/              # Bun + Slidev builder container
docker/               # MCP server Dockerfile + nginx config
docs/                 # This documentation (VitePress)
tests/                # Unit and integration tests
scripts/              # Bootstrap, deploy, backup scripts
```
