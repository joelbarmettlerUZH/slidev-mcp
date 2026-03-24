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
| `slidev://themes/gallery` | Community themes gallery from the Slidev ecosystem |
| `slidev://themes/use` | How to configure and use themes |
| `slidev://themes/installed` | Which themes are pre-installed and available on this server |

### Examples

| Resource URI | Content |
|---|---|
| `slidev://examples/minimal` | A minimal 3-slide deck to use as a starting point |
| `slidev://examples/full_demo` | A 10-slide deck showcasing layouts, code blocks, and animations |

## How Resources Work

When your AI assistant is asked to create a presentation, it typically:

1. Reads `slidev://themes/installed` to see which themes are available
2. Reads `slidev://guide/syntax` to understand the markdown format
3. Optionally reads `slidev://examples/minimal` or `slidev://examples/full_demo` for reference
4. Generates the markdown and calls `render_slides`

The resources are sourced from the [official Slidev documentation](https://sli.dev/) pinned to the Slidev version running in the builder.
