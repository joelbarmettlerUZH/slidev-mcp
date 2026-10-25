---
description: How to connect Claude Code to a Slidev MCP server.
---

# Claude Code

[Claude Code](https://docs.anthropic.com/en/docs/claude-code) is Anthropic's CLI tool for working with Claude. It has built-in MCP support.

## Setup

Run one command:

```bash
claude mcp add --scope user slidev-mcp --transport http https://mcp.slidev-mcp.org/mcp
```

This adds the server to your user-level MCP configuration. It will be available in all Claude Code sessions.

`http` is Claude Code's name for the MCP Streamable HTTP transport. The older `sse` transport is deprecated, and this server does not offer it.

## Verify

Start a new Claude Code session and ask:

> What MCP tools are available?

You should see `render_slides` and `list_session_slides` listed.

## Usage

Ask Claude to create a presentation:

> Create a presentation about machine learning basics using the default theme

Claude will read the Slidev resources, generate markdown, and return a URL.
