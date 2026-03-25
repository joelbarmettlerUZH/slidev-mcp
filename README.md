<p align="center">
  <img src="https://cdn.jsdelivr.net/gh/slidevjs/slidev/assets/favicon.png" width="80" alt="Slidev MCP">
</p>

<h1 align="center">Slidev MCP</h1>

<p align="center">
  Generate, render, and host Slidev presentations from any AI assistant
</p>

<p align="center">
  <a href="https://github.com/joelbarmettlerUZH/slidev-mcp">GitHub</a> &middot;
  <a href="#quick-start">Getting Started</a> &middot;
  <a href="#supported-mcp-clients">MCP Clients</a> &middot;
  <a href="#themes">Themes</a>
</p>

<p align="center">
  <a href="https://github.com/joelbarmettlerUZH/slidev-mcp/actions/workflows/ci.yml"><img src="https://img.shields.io/github/actions/workflow/status/joelbarmettlerUZH/slidev-mcp/ci.yml?label=tests&labelColor=212121" alt="Tests"></a>
  <a href="LICENSE.md"><img src="https://img.shields.io/badge/license-FSL--1.1--ALv2-blue?labelColor=212121" alt="License"></a>
</p>

---

## What It Does

Connect your AI assistant to a Slidev MCP server, ask it to create a presentation, and get back a live URL — ready to share.

- **24 curated themes** — all MIT/Apache-2.0 licensed, version-pinned, build-validated
- **Shareable URLs** — every presentation gets a unique link
- **Iterative updates** — modify slides within the same session, same URL
- **Secure** — builds run in isolated containers with no network access

## Supported MCP Clients

| Client | Type |
|---|---|
| [Claude Code](#claude-code) | CLI |
| [Claude Desktop](#other-clients) | Desktop app |
| [Cursor](#cursor) | IDE |
| [Windsurf](#other-clients) | IDE |
| [VS Code (Copilot)](#other-clients) | IDE |
| [JetBrains IDEs](#other-clients) | IDE |
| [Zed](#other-clients) | IDE |
| [Opencode](#other-clients) | CLI |
| [Gemini CLI](#other-clients) | CLI |
| [ChatGPT](#other-clients) | Web / Desktop |

Works with any client that supports [MCP](https://modelcontextprotocol.io/) streamable HTTP.

## Quick Start

### Claude Code

```bash
claude mcp add --scope user slidev-mcp --transport streamable-http https://your-server.example.com/mcp
```

### Cursor

Add to `.cursor/mcp.json`:

```json
{
  "mcpServers": {
    "slidev-mcp": {
      "url": "https://your-server.example.com/mcp"
    }
  }
}
```

### Other Clients

Any MCP client that supports streamable HTTP works with:

```
https://your-server.example.com/mcp
```

## Self-Hosting

Slidev MCP is self-hosted. Deploy on your own server with Docker Compose:

```bash
git clone https://github.com/joelbarmettlerUZH/slidev-mcp.git
cd slidev-mcp
cp .env.example .env    # Set DOMAIN, POSTGRES_PASSWORD, ACME_EMAIL
docker compose -f docker-compose.prod.yml up -d
```

## Themes

24 pre-installed themes (5 official + 19 community), each individually verified:

**Official:** `default`, `seriph`, `apple-basic`, `bricks`, `shibainu`

**Community:** `academic`, `cobalt`, `dracula`, `eloc`, `field-manual`, `frankfurt`, `geist`, `neocarbon`, `neversink`, `nord`, `penguin`, `purplin`, `scholarly`, `swiss-ai-hub`, `the-unnamed`, `unicorn`, `vibe`, `vuetiful`, `zhozhoba`

Each theme has its own isolated project with pinned dependencies — no cross-theme conflicts.

## How It Works

Your AI assistant sends markdown + a theme name via MCP. The server builds the presentation in an isolated container (no network access, non-root user, resource-limited) and serves the result as a static site. No LLM runs on the server — your client generates the markdown, the server just builds and hosts it.

## Development

```bash
make install          # Install Python dependencies
make docker-dev-up    # Start Postgres + Builder
make serve            # Run MCP server locally
make pr-ready         # Lint + format + test
```

## License

[FSL-1.1-ALv2](LICENSE.md) — Functional Source License, converting to Apache 2.0 after two years.
