---
description: All pre-installed Slidev themes available on the server — with visual previews.
---

<script setup>
import ThemeGallery from '../.vitepress/theme/components/ThemeGallery.vue'
import { additional } from '../.vitepress/themes'
</script>

# Themes

Slidev MCP ships with over 30 pre-installed themes. Specify the theme name in your request and the server handles the rest.

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

## Additional Themes

The following themes are also pre-installed but don't have preview images available:

<table>
  <thead>
    <tr><th>Theme ID</th><th>Name</th><th>Description</th></tr>
  </thead>
  <tbody>
    <tr v-for="t in additional" :key="t.id">
      <td><code>{{ t.id }}</code></td>
      <td>{{ t.name }}</td>
      <td>{{ t.description }}</td>
    </tr>
  </tbody>
</table>

## Usage

Specify the theme name when asking your AI assistant to create a presentation:

> Create a presentation about our roadmap using the **seriph** theme

Or pass it directly in the `theme` parameter of `render_slides`.

::: warning
Only themes listed on this page are available. Requesting any other theme returns a `theme_not_allowed` error. No dynamic theme installation is supported — this is a security measure to prevent supply chain attacks.
:::
