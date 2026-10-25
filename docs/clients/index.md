---
description: Overview of all MCP clients that work with Slidev MCP and how to connect them.
---

# MCP Clients

Slidev MCP works with any client that supports the [Model Context Protocol](https://modelcontextprotocol.io/). No API keys or authentication required — just point your client at the server URL.

::: tip Quickest Setup
Most clients just need this URL:

```
https://mcp.slidev-mcp.org/mcp
```

Self-hosting? Replace with your own server domain.
:::

## Supported Clients

| Client | Type | Guide |
|---|---|---|
| [Claude Code](/clients/claude-code) | CLI | One command setup |
| [Claude Desktop](/clients/claude-desktop) | Desktop app | Custom connector (UI) |
| [Cursor](/clients/cursor) | IDE | One-click or JSON config |
| [Windsurf](/clients/windsurf) | IDE | JSON config |
| [VS Code (Copilot)](/clients/vscode) | IDE | JSON config |
| [JetBrains IDEs](/clients/jetbrains) | IDE | UI or JSON config |
| [Zed](/clients/zed) | IDE | JSON config |
| [Opencode](/clients/opencode) | CLI | JSON config |
| [Gemini CLI](/clients/gemini-cli) | CLI | JSON config |
| [ChatGPT](/clients/chatgpt) | Web / Desktop | Custom connector (developer mode) |

## Other Clients

For any MCP client not listed above, use the **streamable HTTP** transport with your server URL:

```
https://mcp.slidev-mcp.org/mcp
```

Consult your client's MCP documentation for how to add a streamable HTTP server.

## About Transports

Slidev MCP serves **Streamable HTTP** at `/mcp`. This is the remote transport defined by the current [MCP specification](https://modelcontextprotocol.io/specification/latest/basic/transports) (revision 2026-07-28), which only defines stdio and Streamable HTTP. The older HTTP+SSE transport is deprecated and there is no `/sse` endpoint, so if your client asks you to choose, pick **HTTP** / **Streamable HTTP**, not SSE. Clients that try Streamable HTTP first and fall back to SSE (Claude Code, VS Code) will work without changes.

Configuration key names differ per client (`url`, `serverUrl`, `httpUrl`, `type: "remote"`), so use the exact format from your client's guide.
