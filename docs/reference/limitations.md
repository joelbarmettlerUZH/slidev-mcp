---
description: Known limitations of Slidev MCP — images, PDF export, live preview, and more.
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
| **PDF export** | Only static HTML is generated | Use your browser's print-to-PDF on the slide URL |
| **Live preview** | Each change requires a full build (7-30s) | Iterate by asking your assistant to update specific slides |
| **Presenter mode** | Not included in the static build | View slides directly in the browser |
| **Custom CSS/JS files** | No file upload support | Use inline `<style>` and `<script setup>` blocks in markdown |
| **Custom fonts** | No file upload support | Use web fonts via URL imports in `<style>` blocks |

## Limits

| Limit | Default | Description |
|---|---|---|
| Markdown size | 1 MB | Maximum size of the markdown input |
| Build timeout | 120 seconds | Maximum time for a single build |
| Concurrent builds | 3 | Maximum simultaneous builds on the server |
| Slide TTL | 30 days | Slides are automatically deleted after this period |

## Session Behavior

- You can update a presentation as many times as you want **within the same session**.
- Once your session ends (you disconnect), all your presentations become **immutable** — they can still be viewed but not modified.
- If the server restarts, all active sessions are terminated. Existing slides remain viewable.

## Theme Set

The available themes are fixed at build time. You cannot install custom themes at runtime. See the [full theme list](/reference/themes).
