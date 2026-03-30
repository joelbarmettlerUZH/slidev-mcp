---
description: Reference documentation for all Slidev MCP tools.
---

# Tools

Slidev MCP provides 8 tools. You don't call them directly &mdash; your AI assistant uses them behind the scenes. This page documents their behavior for reference.

## render_slides

Render a Slidev presentation from markdown and return its hosted URL.

### Parameters

| Parameter | Type | Required | Description |
|---|---|---|---|
| `markdown` | `string` | Yes | Full Slidev markdown including frontmatter |
| `theme` | `string` | Yes | Theme name (e.g. `seriph`, `default`, `apple-basic`) |
| `uuid` | `string \| null` | No | UUID of an existing presentation to update. Omit to create a new one. |
| `color_schema` | `string` | No | Color scheme: `light` (default), `dark`, or `auto`. Controls whether slides render in light or dark mode. |

### Returns

```json
{
  "url": "https://mcp.slidev-mcp.org/slides/abc123-def456/",
  "uuid": "abc123-def456",
  "build_time_seconds": 7.42
}
```

A base64-encoded PNG preview image is also returned as an image content block (visible on clients that support image rendering).

### Errors

| Code | Description |
|---|---|
| `theme_not_allowed` | Theme name is not in the allowlist or has an invalid format |
| `invalid_uuid` | UUID does not match UUID v4 format |
| `uuid_sealed` | UUID exists but belongs to a closed session (immutable) |
| `uuid_foreign` | UUID belongs to a different active session |
| `build_failed` | Slidev build failed (includes error details) |
| `build_timeout` | Build exceeded the timeout (default 120s) |
| `markdown_too_large` | Markdown exceeds the size limit (default 1 MB) |
| `concurrent_limit` | Too many builds running simultaneously; retry later |

### Notes

- Images must be **remote URLs** or **base64-encoded inline**. Local file paths are not supported.
- The `theme` parameter is validated against the [installed themes](/reference/themes). Only pre-installed themes are allowed.
- When `uuid` is provided, the presentation is updated in-place. The URL stays the same.
- UUIDs are tied to your session. Once you disconnect, your presentations become immutable.

## export_slides

Export a presentation as a downloadable PDF.

### Parameters

| Parameter | Type | Required | Description |
|---|---|---|---|
| `uuid` | `string` | Yes | UUID of the presentation to export. Must be from the current session. |

### Returns

```json
{
  "pdf_url": "https://mcp.slidev-mcp.org/slides/abc123-def456/slidev-exported.pdf",
  "uuid": "abc123-def456",
  "export_time_seconds": 12.3
}
```

### Errors

| Code | Description |
|---|---|
| `uuid_foreign` | UUID does not belong to this session |
| `not_found` | Slide or markdown version not found |
| `export_failed` | PDF export failed (includes error details) |

### Notes

- The presentation must have been created in the current session.
- PDF export uses Playwright to render slides server-side, so the result matches what you see in the browser.

## screenshot_slides

Render all slides as PNG images and return them for visual review.

### Parameters

| Parameter | Type | Required | Description |
|---|---|---|---|
| `uuid` | `string` | Yes | UUID of the presentation to screenshot. |

### Returns

One PNG image per slide, returned as image content blocks. Use this to visually review a presentation and give specific feedback on individual slides.

### Errors

| Code | Description |
|---|---|
| `uuid_foreign` | UUID does not belong to this session |
| `not_found` | Slide or markdown version not found |
| `export_failed` | Screenshot rendering failed |

### Notes

- The presentation must have been created in the current session.
- Returns one image per slide, so multi-model AI clients can see exactly what each slide looks like.

## list_session_slides

List all presentations created in the current session.

### Parameters

None.

### Returns

```json
{
  "slides": [
    {
      "uuid": "abc123-def456",
      "url": "https://mcp.slidev-mcp.org/slides/abc123-def456/",
      "theme": "seriph",
      "created_at": "2026-03-23T14:12:00+00:00",
      "updated_at": "2026-03-23T14:15:30+00:00",
      "version_count": 3
    }
  ]
}
```

## list_themes

Get a list of all available themes with style descriptions and recommendations. Used by the AI to decide which theme to use &mdash; does not display anything to the user.

### Parameters

None.

### Returns

Markdown text with a quick reference table and categorized theme recommendations (dark, academic, modern, playful, etc.).

## browse_themes

Show the user a visual theme gallery with preview images. On clients that support MCP Apps (claude.ai, Claude Desktop), this renders an interactive gallery in the conversation.

### Parameters

| Parameter | Type | Required | Description |
|---|---|---|---|
| `themes` | `list[string] \| null` | No | Theme names to show. If omitted, all 24 themes are displayed. |

### Returns

JSON with the theme filter. The visual gallery is rendered by the MCP App.

### Notes

- Pass a filtered list to show only specific themes (e.g. only dark themes)
- The AI typically calls `list_themes` first to identify matches, then passes the filtered names here

## get_theme

Get full documentation for a specific theme: layouts, components, frontmatter options, and example slides.

### Parameters

| Parameter | Type | Required | Description |
|---|---|---|---|
| `theme` | `string` | Yes | Theme name (e.g. `seriph`, `neocarbon`, `field-manual`) |

### Returns

Markdown text with the theme's README and example slides.

### Notes

- The AI calls this before `render_slides` to learn the theme's unique features
- Returns an error message if the theme is not found

## get_slidev_guide

Get the Slidev syntax guide: frontmatter, slide separators, speaker notes, layouts, code blocks, and an example deck.

### Parameters

None.

### Returns

Markdown text combining the Slidev syntax reference, built-in layout documentation, and a minimal example deck.
