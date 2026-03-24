---
description: How to connect JetBrains IDEs (IntelliJ, WebStorm, PyCharm, etc.) to a Slidev MCP server.
---

# JetBrains IDEs

JetBrains IDEs (IntelliJ IDEA, WebStorm, PyCharm, GoLand, etc.) support MCP servers through their AI Assistant.

## Setup

1. Open **Settings** > **Tools** > **AI Assistant** > **MCP Servers**
2. Click **Add** > **As JSON**
3. Paste:

```json
{
  "slidev-mcp": {
    "type": "http",
    "url": "https://your-server.example.com/mcp"
  }
}
```

4. Click **OK** and restart the IDE.

## Usage

Open the AI Assistant chat and ask:

> Create a presentation about our microservices architecture using the apple-basic theme
