---
description: Reference documentation for all Slidev MCP resources — syntax guides, theme docs, and examples.
---

# Resources

Slidev MCP exposes documentation as MCP resources. Your AI assistant reads these automatically to understand Slidev syntax, available themes, and best practices.

You don't need to interact with resources directly — your assistant uses them behind the scenes when generating presentations.

## Available Resources

### Slidev Syntax & Features

| Resource URI | Content |
|---|---|
| `slidev://guide/syntax` | Slide separators, frontmatter, speaker notes, comments |
| `slidev://guide/animations` | Click animations (`<v-click>`), transitions, motion |
| `slidev://builtin/components` | Built-in components reference |
| `slidev://builtin/layouts` | Built-in layout reference (cover, two-cols, image, etc.) |

### Themes

| Resource URI | Content |
|---|---|
| `slidev://themes/installed` | Which themes are pre-installed and available on this server |
| `slidev://themes/guide` | Theme selection guide with style categories, tone, and "best for" recommendations |
| `slidev://themes/{name}` | Per-theme README with layouts, components, and usage examples (e.g. `slidev://themes/swiss-ai-hub`) |

### Session Slides

| Resource URI | Content |
|---|---|
| `slides://session` | All slides created in the current session with their themes, URLs, and latest markdown |
| `slides://session/{uuid}` | Details for a specific slide: theme, URL, current markdown, and version history |

Session slide resources let the assistant read back previous presentations to reference, modify, or continue iterating on them.

### Examples

| Resource URI | Content |
|---|---|
| `slidev://examples/minimal` | A minimal 3-slide deck to use as a starting point |
| `slidev://examples/full_demo` | A 10-slide deck showcasing layouts, code blocks, and animations |

## How Resources Work

When your AI assistant is asked to create a presentation, it typically:

1. Reads `slidev://themes/guide` to understand which theme fits the user's request
2. Reads `slidev://themes/{name}` for the chosen theme's layouts and components
3. Reads `slidev://guide/syntax` to understand the markdown format
4. Generates the markdown and calls `render_slides`

When updating an existing presentation, the assistant reads `slides://session/{uuid}` to get the current markdown, modifies it, and calls `render_slides` with the same UUID.

The resources are sourced from the [official Slidev documentation](https://sli.dev/) pinned to the Slidev version running in the builder.

## Resources vs Tools

Some MCP clients (like Claude Code) support reading resources automatically. Others (like claude.ai) only support tools. Slidev MCP provides equivalent tools for the most important resources:

| Resource | Equivalent Tool |
|----------|----------------|
| `slidev://themes/guide` | `list_themes` |
| `slidev://themes/{name}` | `get_theme` |
| `slidev://guide/syntax` + layouts + examples | `get_slidev_guide` |

The AI assistant uses whichever method is available on your client.
