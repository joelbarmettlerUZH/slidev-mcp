---
description: How to connect VS Code (GitHub Copilot) to a Slidev MCP server.
---

# VS Code (GitHub Copilot)

[VS Code](https://code.visualstudio.com/) supports MCP servers through [GitHub Copilot](https://github.com/features/copilot).

## Setup

Add to `.vscode/mcp.json` in your project root:

```json
{
  "servers": {
    "slidev-mcp": {
      "type": "http",
      "url": "https://mcp.slidev-mcp.org/mcp"
    }
  }
}
```

Or add it to your user settings (`settings.json`):

```json
{
  "mcp": {
    "servers": {
      "slidev-mcp": {
        "type": "http",
        "url": "https://mcp.slidev-mcp.org/mcp"
      }
    }
  }
}
```

## Usage

Open Copilot Chat in agent mode and ask:

> Create a presentation about TypeScript best practices using the seriph theme
