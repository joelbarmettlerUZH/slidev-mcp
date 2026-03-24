---
description: How to connect Claude Desktop to a Slidev MCP server.
---

# Claude Desktop

[Claude Desktop](https://claude.ai/download) is Anthropic's desktop application for Claude.

## Setup

Open your Claude Desktop configuration file:

- **macOS:** `~/Library/Application Support/Claude/claude_desktop_config.json`
- **Windows:** `%APPDATA%\Claude\claude_desktop_config.json`

Add the server:

```json
{
  "mcpServers": {
    "slidev-mcp": {
      "type": "http",
      "url": "https://your-server.example.com/mcp"
    }
  }
}
```

Restart Claude Desktop to apply the changes.

## Verify

Open a new conversation and ask:

> What MCP tools do you have access to?

You should see `render_slides` and `list_session_slides`.

## Usage

Ask Claude to create a presentation:

> Create a 10-slide presentation about our product roadmap using the apple-basic theme
