---
description: How to connect Cursor to a Slidev MCP server.
---

# Cursor

[Cursor](https://cursor.com) is an AI-powered code editor with built-in MCP support.

## Setup

Add to `.cursor/mcp.json` in your project root (or globally at `~/.cursor/mcp.json`):

```json
{
  "mcpServers": {
    "slidev-mcp": {
      "url": "https://your-server.example.com/mcp"
    }
  }
}
```

Cursor will detect the configuration automatically.

## Verify

Open the Cursor chat and ask:

> What MCP tools are available?

You should see `render_slides` and `list_session_slides` listed.

## Usage

In the Cursor chat, ask:

> Create a presentation about the architecture of this project using the seriph theme
