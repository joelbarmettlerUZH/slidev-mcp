<p align="center">
  <img src="https://cdn.jsdelivr.net/gh/slidevjs/slidev/assets/favicon.png" width="80" alt="Slidev MCP">
</p>

<h1 align="center">Slidev MCP</h1>

<p align="center">
  Generate, render, and host Slidev presentations from any AI assistant
</p>

<p align="center">
  <a href="https://slidev-mcp.org">Website</a> &middot;
  <a href="https://slidev-mcp.org/guide/getting-started">Getting Started</a> &middot;
  <a href="https://slidev-mcp.org/clients/">MCP Clients</a> &middot;
  <a href="https://slidev-mcp.org/reference/themes">Themes</a>
</p>

<p align="center">
  <a href="https://github.com/joelbarmettler/slidev-mcp/actions/workflows/ci.yml"><img src="https://img.shields.io/github/actions/workflow/status/joelbarmettler/slidev-mcp/ci.yml?label=tests&labelColor=212121" alt="Tests"></a>
  <a href="LICENSE"><img src="https://img.shields.io/badge/license-MIT-blue?labelColor=212121" alt="License"></a>
</p>

---

## What It Does

Connect your AI assistant to a Slidev MCP server, ask it to create a presentation, and get back a live URL — ready to share.

- **30+ themes** to choose from
- **Shareable URLs** — every presentation gets a unique link
- **Iterative updates** — modify slides within the same session, same URL
- **Secure** — builds run in isolated containers with no network access

## Supported MCP Clients

| Client | Type |
|---|---|
| [Claude Code](https://slidev-mcp.org/clients/claude-code) | CLI |
| [Claude Desktop](https://slidev-mcp.org/clients/claude-desktop) | Desktop app |
| [Cursor](https://slidev-mcp.org/clients/cursor) | IDE |
| [Windsurf](https://slidev-mcp.org/clients/windsurf) | IDE |
| [VS Code (Copilot)](https://slidev-mcp.org/clients/vscode) | IDE |
| [JetBrains IDEs](https://slidev-mcp.org/clients/jetbrains) | IDE |
| [Zed](https://slidev-mcp.org/clients/zed) | IDE |
| [Opencode](https://slidev-mcp.org/clients/opencode) | CLI |
| [Gemini CLI](https://slidev-mcp.org/clients/gemini-cli) | CLI |
| [ChatGPT](https://slidev-mcp.org/clients/chatgpt) | Web / Desktop |

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

See the **[full client list](https://slidev-mcp.org/clients/)** for detailed setup instructions.

## Self-Hosting

Slidev MCP is self-hosted. Deploy on your own server with Docker Compose:

```bash
git clone https://github.com/joelbarmettler/slidev-mcp.git
cd slidev-mcp
cp .env.example .env    # Set DOMAIN, POSTGRES_PASSWORD, ACME_EMAIL
docker compose -f docker-compose.yml -f docker-compose.prod.yml up -d
```

See the **[Deployment guide](https://slidev-mcp.org/guide/deployment)** for full instructions.

## How It Works

Your AI assistant sends markdown + a theme name via MCP. The server builds the presentation in an isolated container (no network, read-only filesystem) and serves the result as a static site. No LLM runs on the server — your client generates the markdown, the server just builds and hosts it.

## Development

```bash
make install          # Install Python dependencies
make docker-dev-up    # Start Postgres + Builder
make serve            # Run MCP server locally
make pr-ready         # Lint + format + test
```

## Documentation

Full documentation at **[slidev-mcp.org](https://slidev-mcp.org)**:

- [Getting Started](https://slidev-mcp.org/guide/getting-started): Connect your AI assistant
- [MCP Clients](https://slidev-mcp.org/clients/): Setup guides for 10 clients
- [Themes](https://slidev-mcp.org/reference/themes): 30+ pre-installed themes
- [Tools Reference](https://slidev-mcp.org/reference/tools): Full API documentation
- [Deployment](https://slidev-mcp.org/guide/deployment): Self-host on your own server

## License

MIT
