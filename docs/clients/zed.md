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
      "settings": {
        "url": "https://your-server.example.com/mcp"
      }
    }
  }
}
```

## Usage

Open the Zed assistant and ask:

> Create a presentation about Rust error handling using the default theme
