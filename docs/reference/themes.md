---
description: All 24 pre-installed Slidev themes — 5 official and 19 community. Each is license-checked, version-pinned, and build-validated.
---

<script setup>
import ThemeGallery from '../.vitepress/theme/components/ThemeGallery.vue'
</script>

# Themes

Slidev MCP ships with 24 pre-installed themes — 5 official and 19 community. Each has been individually verified: license checked (all MIT or Apache-2.0), version pinned, and build validated.

::: tip
You don't need to remember these names. Just ask your AI assistant to "list available themes" and it will read the theme resource from the server.
:::

## Official Themes

<ClientOnly>
  <ThemeGallery collection="official" />
</ClientOnly>

## Community Themes

<ClientOnly>
  <ThemeGallery collection="community" />
</ClientOnly>

## Usage

Specify the theme name when asking your AI assistant to create a presentation:

> Create a presentation about our roadmap using the **seriph** theme

Or pass it directly in the `theme` parameter of `render_slides`.

::: warning
Only themes listed on this page are available. Requesting any other theme returns a `theme_not_allowed` error. No dynamic theme installation is supported — this is a security measure to prevent supply chain attacks.
:::
