---
description: How to connect Opencode to a Slidev MCP server.
---

# Opencode

[Opencode](https://opencode.ai) is an open-source AI coding assistant with MCP support.

## Setup

Add to your Opencode configuration (`opencode.json`):

```json
{
  "mcp": {
    "slidev-mcp": {
      "type": "http",
      "url": "https://mcp.slidev-mcp.org/mcp"
    }
  }
}
```

## Usage

Ask Opencode:

> Create a presentation about clean code principles using the seriph theme
