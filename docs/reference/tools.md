---
description: Reference documentation for all Slidev MCP tools — render_slides and list_session_slides.
---

# Tools

Slidev MCP provides two tools that your AI assistant can call.

## render_slides

Render a Slidev presentation from markdown and return its hosted URL.

### Parameters

| Parameter | Type | Required | Description |
|---|---|---|---|
| `markdown` | `string` | Yes | Full Slidev markdown including frontmatter |
| `theme` | `string` | Yes | Theme name (e.g. `seriph`, `default`, `apple-basic`) |
| `uuid` | `string \| null` | No | UUID of an existing presentation to update. Omit to create a new one. |

### Returns

```json
{
  "url": "https://your-server.example.com/slides/abc123-def456/",
  "uuid": "abc123-def456",
  "build_time_seconds": 7.42
}
```

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
      "url": "https://your-server.example.com/slides/abc123-def456/",
      "theme": "seriph",
      "created_at": "2026-03-23T14:12:00+00:00",
      "updated_at": "2026-03-23T14:15:30+00:00"
    }
  ]
}
```
