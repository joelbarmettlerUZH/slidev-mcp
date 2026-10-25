---
description: How to connect ChatGPT to a Slidev MCP server.
---

# ChatGPT

[ChatGPT](https://chatgpt.com) supports MCP servers through its connector system.

## Setup

ChatGPT connects to custom MCP servers through **developer mode**. OpenAI has renamed and moved these menus several times (connectors are now called **Apps** in the UI), and availability depends on your plan, so the exact labels may differ on your account.

1. Open **Settings** and enable **Developer mode** (under the Apps / Connectors **Advanced** settings)
2. In the Apps / Connectors settings, choose **Create** (add a custom connector)
3. Enter a name and the server URL:

```
https://mcp.slidev-mcp.org/mcp
```

4. Set authentication to **No authentication**, accept the notice that custom connectors are not verified by OpenAI, and save

In a new chat, enable the connector for that conversation before asking for a presentation.

::: warning Unverified steps
These steps follow third-party setup guides for ChatGPT developer mode. We could not confirm them against OpenAI's own documentation. If a menu doesn't match, search OpenAI's help for "developer mode MCP".
:::

## Usage

In your ChatGPT conversation, ask:

> Create a presentation about data visualization best practices using the default theme

ChatGPT will use the connected MCP server to render and host the slides.
