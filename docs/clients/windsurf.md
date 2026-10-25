---
description: How to connect Windsurf to a Slidev MCP server.
---

# Windsurf

[Windsurf](https://codeium.com/windsurf) is an AI-powered IDE by Codeium with MCP support.

## Setup

In the Cascade panel, click the `...` (Actions) menu, then **Open MCP config file** in the MCPs section, and add:

```json
{
  "mcpServers": {
    "slidev-mcp": {
      "serverUrl": "https://mcp.slidev-mcp.org/mcp"
    }
  }
}
```

Save the file and the server appears in the MCPs list, where you can toggle it on. The file lives at `~/.codeium/windsurf/mcp_config.json` in classic Windsurf installs. Newer versions that follow the Devin layout use `~/.config/devin/mcp_config.json`; opening it from the menu always gets you the right one.

## Usage

In the Windsurf chat, ask:

> Create a presentation about our API design using the default theme
