---
description: Overview of Slidev MCP — what it is, how it works, and why you'd use it.
---

# What is Slidev MCP?

Slidev MCP is a self-hosted [Model Context Protocol](https://modelcontextprotocol.io/) (MCP) server that lets AI assistants generate, render, and host [Slidev](https://sli.dev/) presentations from markdown.

You connect your MCP client (Claude Code, Cursor, VS Code, etc.) to the server, ask your AI assistant to create a presentation, and it returns a live URL with your slides — ready to share.

## How It Works

1. **Connect** your MCP client to a Slidev MCP server.
2. **Ask** your AI assistant to create a presentation on any topic.
3. The assistant reads the available [resources](/reference/resources) to learn Slidev syntax and themes.
4. It calls the [`render_slides`](/reference/tools#render-slides) tool with markdown and a theme name.
5. The server builds the presentation and returns a **shareable URL**.
6. You can **update** the same presentation within your session — the URL stays the same.

## What You Get

- A hosted, interactive HTML presentation at a unique URL
- Support for Slidev features: layouts, animations, code highlighting, LaTeX, Mermaid diagrams
- [24 curated themes](/reference/themes) to choose from — all MIT-licensed and build-validated
- The ability to iterate on your slides within the same session

## Who Is This For?

- **Anyone using an MCP-compatible AI assistant** who wants to create presentations quickly
- **Teams** who want a shared slide generation service
- **Developers** who prefer markdown over drag-and-drop slide editors

## Self-Hosted

Slidev MCP is designed to be self-hosted. You deploy it on your own server and connect your MCP clients to it. See the [Deployment guide](/guide/deployment) for setup instructions.
