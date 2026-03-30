---
description: Connect your AI assistant to Slidev MCP and create your first presentation in under a minute.
---

# Getting Started

Slidev MCP lets your AI assistant create, render, and host presentations. Connect once, then ask for slides in natural language.

## Connect in 30 Seconds

### Claude Code (recommended)

```bash
claude mcp add --scope user slidev-mcp --transport streamable-http https://mcp.slidev-mcp.org/mcp
```

### Claude Desktop / claude.ai

Add `mcp.slidev-mcp.org/mcp` as a [custom connector](https://support.anthropic.com/en/articles/11175166-getting-started-with-custom-connectors-using-remote-mcp) in Settings > Connectors.

### Cursor

Add to `.cursor/mcp.json`:

```json
{
  "mcpServers": {
    "slidev-mcp": {
      "url": "https://mcp.slidev-mcp.org/mcp"
    }
  }
}
```

### Other Clients

See [client setup guides](/clients/) for Windsurf, VS Code, JetBrains, Zed, Opencode, Gemini CLI, and ChatGPT. Any client that supports MCP streamable HTTP works with:

```
https://mcp.slidev-mcp.org/mcp
```

::: tip Self-Hosting
Running your own instance? Replace `mcp.slidev-mcp.org` with your server's domain. See the [deployment guide](/guide/deployment) for setup instructions.
:::

## Create Your First Presentation

Once connected, just ask:

> "Create a presentation about the benefits of remote work using the seriph theme"

Your AI assistant will:

1. Read the theme's documentation to learn its layouts and components
2. Write Slidev markdown tailored to the theme
3. Build and host the presentation
4. Return a shareable URL

The whole process takes about 10-15 seconds.

## Update Your Slides

Ask for changes and the same URL updates in place:

> "Add a slide about work-life balance after slide 3"

> "Change the theme to neocarbon"

Just refresh your browser to see the updates.

## Browse Themes

Ask to see what's available:

> "Show me the available themes"

Or describe a style and let the AI pick:

> "I want something dark and modern for a tech talk"

## Share Your Slides

Every presentation gets a permanent URL like:

```
https://slides.slidev-mcp.org/slides/abc123-def456/
```

- Open in any browser &mdash; no login, no app required
- Bookmark it or send it to anyone
- Press `f` for fullscreen presentation mode
- Slides stay available for 30 days after your session ends

While your session is active, you can keep refining the same presentation. Once you disconnect, the slides become a permanent snapshot.

## Available Tools

Your AI assistant has access to these tools:

| Tool | Purpose |
|------|---------|
| `render_slides` | Create or update a presentation |
| `list_session_slides` | See all presentations from this session |
| `list_themes` | Read theme descriptions (for the AI to choose) |
| `browse_themes` | Show a visual theme gallery |
| `get_theme` | Read a specific theme's full documentation |
| `get_slidev_guide` | Learn Slidev markdown syntax |

You don't need to call these directly &mdash; just describe what you want.

## Next Steps

- [Client setup guides](/clients/) &mdash; detailed instructions per client
- [Tool reference](/reference/tools) &mdash; technical tool documentation
- [Themes](/reference/themes) &mdash; browse the full theme gallery
- [Limitations](/reference/limitations) &mdash; what's supported and what isn't
