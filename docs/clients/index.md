---
description: Overview of all MCP clients that work with Slidev MCP and how to connect them.
---

# MCP Clients

Slidev MCP works with any client that supports the [Model Context Protocol](https://modelcontextprotocol.io/). No API keys or authentication required — just point your client at the server URL.

::: tip Quickest Setup
Most clients just need this URL:

```
https://your-server.example.com/mcp
```

Replace with your actual server domain.
:::

## Supported Clients

| Client | Type | Guide |
|---|---|---|
| [Claude Code](/clients/claude-code) | CLI | One command setup |
| [Claude Desktop](/clients/claude-desktop) | Desktop app | JSON config |
| [Cursor](/clients/cursor) | IDE | One-click or JSON config |
| [Windsurf](/clients/windsurf) | IDE | JSON config |
| [VS Code (Copilot)](/clients/vscode) | IDE | JSON config |
| [JetBrains IDEs](/clients/jetbrains) | IDE | UI or JSON config |
| [Zed](/clients/zed) | IDE | JSON config |
| [Opencode](/clients/opencode) | CLI | JSON config |
| [Gemini CLI](/clients/gemini-cli) | CLI | JSON config |
| [ChatGPT](/clients/chatgpt) | Web / Desktop | App connector |

## Other Clients

For any MCP client not listed above, use the **streamable HTTP** transport with your server URL:

```
https://your-server.example.com/mcp
```

Consult your client's MCP documentation for how to add a streamable HTTP server.
