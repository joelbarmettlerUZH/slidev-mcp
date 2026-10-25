---
description: How to connect Gemini CLI to a Slidev MCP server.
---

# Gemini CLI

[Gemini CLI](https://github.com/google-gemini/gemini-cli) is Google's command-line tool for Gemini with MCP support.

## Setup

One command:

```bash
gemini mcp add --transport http slidev-mcp https://mcp.slidev-mcp.org/mcp
```

Or add it to your Gemini CLI settings file (`~/.gemini/settings.json`). Use `httpUrl` for Streamable HTTP; the `url` key is for the deprecated SSE transport, which this server does not offer:

```json
{
  "mcpServers": {
    "slidev-mcp": {
      "httpUrl": "https://mcp.slidev-mcp.org/mcp"
    }
  }
}
```

## Usage

Ask Gemini:

> Create a presentation about cloud architecture using the apple-basic theme
