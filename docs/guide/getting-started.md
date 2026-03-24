---
description: How to connect your MCP client to a Slidev MCP server and create your first presentation.
---

# Getting Started

To use Slidev MCP, you need access to a running Slidev MCP server. If your team already hosts one, you just need the server URL. If not, see the [Deployment guide](/guide/deployment) to set one up.

## Connect Your Client

The server URL follows this pattern:

```
https://your-server.example.com/mcp
```

Replace `your-server.example.com` with your actual server domain.

### Claude Code

One command:

```bash
claude mcp add --scope user slidev-mcp --transport streamable-http https://your-server.example.com/mcp
```

### Cursor

Add to `.cursor/mcp.json`:

```json
{
  "mcpServers": {
    "slidev-mcp": {
      "url": "https://your-server.example.com/mcp"
    }
  }
}
```

### Other Clients

See the [MCP Clients](/clients/) section for detailed setup instructions for all supported clients.

## Create Your First Presentation

Once connected, ask your AI assistant to create a presentation:

> Create a 5-slide presentation about our Q3 results using the seriph theme

The assistant will:
1. Read the Slidev syntax and theme resources from the server
2. Generate the markdown
3. Call `render_slides` with the markdown and theme
4. Return a URL like `https://your-server.example.com/slides/abc123-def456/`

Open the URL in your browser to see your slides.

## Update Your Slides

Within the same session, you can ask the assistant to modify the presentation:

> Change slide 3 to include a bar chart and update the title

The assistant will re-render the slides using the same UUID. The URL stays the same — just refresh your browser.

## What's Available

| Type | What it does |
|---|---|
| [**Tools**](/reference/tools) | Render slides, list session slides |
| [**Resources**](/reference/resources) | Slidev syntax, animations, layouts, components, themes, examples |
| [**Themes**](/reference/themes) | 30+ pre-installed themes to choose from |

## Next Steps

- [MCP Clients](/clients/) — Setup guides for all supported clients
- [Tools reference](/reference/tools) — Full tool documentation
- [Themes](/reference/themes) — Browse available themes
- [Limitations](/reference/limitations) — What to know before you start
