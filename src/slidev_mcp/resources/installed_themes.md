# Installed Themes

The following themes are pre-installed in the Slidev MCP builder and available for use with the `render_slides` tool. Use the theme name in the `theme` parameter.

Each theme has been individually verified: license checked (all MIT or Apache-2.0), pinned to a specific version, and validated to build correctly with its corresponding Slidev version.

## Official Themes

| Theme | Description |
|-------|-------------|
| `default` | Clean, minimal theme that ships with Slidev |
| `seriph` | Elegant theme with serif typography and subtle animations |
| `apple-basic` | Apple keynote-inspired clean presentation style |
| `bricks` | Colorful theme with a brick-like layout pattern |
| `shibainu` | Playful theme with warm tones and rounded elements |

## Community Themes

| Theme | Description |
|-------|-------------|
| `academic` | Formal theme suited for academic presentations and lectures |
| `cobalt` | Deep cobalt blue color scheme with framed layouts |
| `dracula` | Dark theme based on the popular Dracula color scheme |
| `eloc` | Focus on writing, present in a concise style |
| `field-manual` | Vintage US Army field manual aesthetic (1950s-1980s) |
| `frankfurt` | Inspired by the LaTeX Beamer theme Frankfurt |
| `geist` | Vercel-inspired minimalist theme with modern typography |
| `neocarbon` | Premium dark theme with cinematic animations and glass morphism |
| `neversink` | Education/academia oriented theme with whimsical elements |
| `nord` | Theme based on the Nord color palette (arctic, north-bluish) |
| `penguin` | Clean and professional theme with blue accents |
| `purplin` | Vibrant purple-themed design with gradient accents |
| `scholarly` | LaTeX Beamer-style styling for scholarly presentations |
| `swiss-ai-hub` | Professional theme with Swiss AI-Hub branding and gradient backgrounds |
| `the-unnamed` | Dark theme based on The unnamed VS Code theme |
| `unicorn` | Based on Dawntraoz website design with dark/light modes |
| `vibe` | Dark-mode theme with glassmorphism and neon accents |
| `vuetiful` | A Vue-inspired theme for Slidev |
| `zhozhoba` | A zhozhoba theme with dark/light mode support |

## Usage

Set the theme in the `theme` parameter of `render_slides`. The theme will be applied to the frontmatter automatically.

**Important:** Only themes listed above are available. Requesting any other theme will result in a `theme_not_allowed` error. No dynamic theme installation is supported.
