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

To make it available in every workspace, run **MCP: Open User Configuration** from the Command Palette and add the same `servers` entry there. You can also run **MCP: Add Server**, choose **HTTP**, and enter the URL.

VS Code tries Streamable HTTP first and only falls back to the deprecated SSE transport for servers that don't support it.

## Usage

Open Copilot Chat in agent mode and ask:

> Create a presentation about TypeScript best practices using the seriph theme
