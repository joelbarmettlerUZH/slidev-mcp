---
description: How to connect Zed to a Slidev MCP server.
---

# Zed

[Zed](https://zed.dev) is a high-performance code editor with MCP support.

## Setup

Add to your Zed settings (`~/.config/zed/settings.json`):

```json
{
  "context_servers": {
    "slidev-mcp": {
      "url": "https://mcp.slidev-mcp.org/mcp"
    }
  }
}
```

You can also add it through **Settings > AI > MCP Servers > Add Server**; Zed writes the same entry for you.

## Usage

Open the Zed assistant and ask:

> Create a presentation about Rust error handling using the default theme
