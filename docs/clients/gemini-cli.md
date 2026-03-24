---
description: How to connect Gemini CLI to a Slidev MCP server.
---

# Gemini CLI

[Gemini CLI](https://github.com/google-gemini/gemini-cli) is Google's command-line tool for Gemini with MCP support.

## Setup

Add to your Gemini CLI settings file (`~/.gemini/settings.json`):

```json
{
  "mcpServers": {
    "slidev-mcp": {
      "httpUrl": "https://your-server.example.com/mcp"
    }
  }
}
```

## Usage

Ask Gemini:

> Create a presentation about cloud architecture using the apple-basic theme
