---
description: Known limitations of Slidev MCP — images, live preview, custom assets, and more.
---

# Limitations

Slidev MCP is designed to be simple and secure. Some Slidev features are not available in the current version.

## Images

| Image source | Supported? | Notes |
|---|---|---|
| Remote URLs (`![](https://...)`) | Yes | Browser fetches the image when viewing the slides |
| Base64 inline (`![](data:image/png;base64,...)`) | Yes | Works but inflates markdown size (1 MB limit) |
| Local file paths (`![](./images/photo.png)`) | No | No mechanism to upload files to the builder |

**Recommendation:** Use remote image URLs. If you need to embed an image without hosting it, use base64 encoding.

## Features Not Available

| Feature | Why | Workaround |
|---|---|---|
| **Live preview** | Each change requires a full build (7-30s) | Iterate by asking your assistant to update specific slides |
| **Presenter mode** | Not included in the static build | View slides directly in the browser |
| **Custom CSS/JS files** | No file upload support | Use inline `<style>` and `<script setup>` blocks in markdown |
| **Custom fonts** | No file upload support | Use web fonts via URL imports in `<style>` blocks |

## Export

PDF export and slide screenshots are fully supported:

| Feature | Tool | Notes |
|---|---|---|
| **PDF export** | `export_slides` | Server-side Playwright rendering; returns a download URL |
| **Slide screenshots** | `screenshot_slides` | Returns one PNG per slide for visual review |

Both tools take the UUID of the presentation.

## Limits

| Limit | Default | Description |
|---|---|---|
| Markdown size | 1 MB | Maximum size of the markdown input |
| Build timeout | 120 seconds | Maximum time for a single build |
| Concurrent builds | 3 | Maximum simultaneous builds on the server |
| Slide TTL | 30 days | Slides are automatically deleted after this period without an update |

## Access Model

The server has no accounts and no per-connection state, because the current MCP protocol (`2026-07-28`) is stateless. A presentation's **UUID is its only credential**:

- Anyone who has the UUID can update, export, or screenshot the presentation. The UUID is part of the slide URL (`/slides/{uuid}/`), so **treat the URL like an edit link**: sharing it shares edit access through this server.
- UUIDs are random v4 values and cannot be guessed or listed. The server has no way to enumerate other people's presentations.
- A presentation can be updated from any connection, in any conversation, and across server restarts, for as long as it exists.
- `list_session_slides` only looks up UUIDs you pass in; keep the UUIDs returned by `render_slides`.

## Theme Set

The available themes are fixed at build time. Each theme is individually curated — license-checked, version-pinned, and build-validated. You cannot install custom themes at runtime. See the [full theme list](/reference/themes).
