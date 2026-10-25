---
description: How to connect JetBrains IDEs (IntelliJ, WebStorm, PyCharm, etc.) to a Slidev MCP server.
---

# JetBrains IDEs

JetBrains IDEs (IntelliJ IDEA, WebStorm, PyCharm, GoLand, etc.) support MCP servers through their AI Assistant.

## Setup

1. Open **Settings** > **Tools** > **AI Assistant** > **Model Context Protocol (MCP)**
2. Click **Add** to open the New MCP Server dialog
3. Select the **HTTP** connection type and paste:

```json
{
  "mcpServers": {
    "slidev-mcp": {
      "url": "https://mcp.slidev-mcp.org/mcp"
    }
  }
}
```

4. Choose the level (global or current project), then click **OK** and **Apply**
5. Check that the server shows as connected in the **Status** column

## Usage

Open the AI Assistant chat and ask:

> Create a presentation about our microservices architecture using the apple-basic theme
