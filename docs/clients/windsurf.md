---
description: How to connect Windsurf to a Slidev MCP server.
---

# Windsurf

[Windsurf](https://codeium.com/windsurf) is an AI-powered IDE by Codeium with MCP support.

## Setup

Add to your Windsurf MCP configuration file (`~/.codeium/windsurf/mcp_config.json`):

```json
{
  "mcpServers": {
    "slidev-mcp": {
      "serverUrl": "https://mcp.slidev-mcp.org/mcp"
    }
  }
}
```

Restart Windsurf to apply.

## Usage

In the Windsurf chat, ask:

> Create a presentation about our API design using the default theme
