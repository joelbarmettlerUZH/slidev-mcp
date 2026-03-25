# slidev-theme-neocarbon

[![NPM version](https://img.shields.io/npm/v/slidev-theme-neocarbon?color=E30613)](https://www.npmjs.com/package/slidev-theme-neocarbon)

A **premium dark Slidev theme** with cinematic animations, glassmorphism, and animated data visualizations. Built for high-fidelity corporate pitch decks, tech talks, and product showcases.

## Features

- 🎬 **22 Layouts** — Cover, section, fact, quote, statement, comparison, code, math, diagram, spotlight, browser, and more
- 🧩 **25 Components** — Charts, timelines, progress bars, terminals, feature grids, radar charts, heatmaps, flip cards, and more
- ✨ **Cinematic Animations** — Staggered entrances, shimmer highlights, pulsing glows, floating particles
- 🎨 **Fully Themeable** — Override `--nc-accent` to re-skin the entire theme in one line
- 🌗 **Dark-only** — Designed for maximum contrast and visual impact
- 📊 **Mermaid / KaTeX / Monaco** — First-class dark-theme styling for all Slidev features
- 📄 **PDF-ready** — Print styles with `print-color-adjust: exact`

## Slide Examples

<table>
<tr>
<td><img src="examples/0.png" width="400" /></td>
<td><img src="examples/1.png" width="400" /></td>
<td><img src="examples/2.png" width="400" /></td>
</tr>
<tr>
<td><img src="examples/3.png" width="400" /></td>
<td><img src="examples/4.png" width="400" /></td>
<td><img src="examples/5.png" width="400" /></td>
</tr>
<tr>
<td><img src="examples/6.png" width="400" /></td>
<td><img src="examples/7.png" width="400" /></td>
<td><img src="examples/8.png" width="400" /></td>
</tr>
<tr>
<td><img src="examples/9.png" width="400" /></td>
<td><img src="examples/10.png" width="400" /></td>
<td><img src="examples/11.png" width="400" /></td>
</tr>
<tr>
<td><img src="examples/12.png" width="400" /></td>
<td><img src="examples/13.png" width="400" /></td>
<td><img src="examples/14.png" width="400" /></td>
</tr>
<tr>
<td><img src="examples/15.png" width="400" /></td>
<td><img src="examples/16.png" width="400" /></td>
<td><img src="examples/17.png" width="400" /></td>
</tr>
<tr>
<td><img src="examples/18.png" width="400" /></td>
<td><img src="examples/19.png" width="400" /></td>
<td><img src="examples/20.png" width="400" /></td>
</tr>
<tr>
<td><img src="examples/21.png" width="400" /></td>
<td><img src="examples/22.png" width="400" /></td>
<td><img src="examples/23.png" width="400" /></td>
</tr>
<tr>
<td><img src="examples/24.png" width="400" /></td>
<td><img src="examples/25.png" width="400" /></td>
<td><img src="examples/26.png" width="400" /></td>
</tr>
<tr>
<td><img src="examples/27.png" width="400" /></td>
<td><img src="examples/28.png" width="400" /></td>
<td><img src="examples/29.png" width="400" /></td>
</tr>
<tr>
<td><img src="examples/30.png" width="400" /></td>
<td></td>
<td></td>
</tr>
</table>

## Installation

```bash
npm i slidev-theme-neocarbon
```

In your `slides.md` frontmatter:

```yaml
---
theme: slidev-theme-neocarbon
---
```

For local development:

```yaml
---
theme: ./slidev-theme-neocarbon
---
```

## Design Tokens

Override any token in your own CSS or frontmatter `style` block:

```css
:root {
  /* Brand accent — changes the entire palette */
  --nc-accent: #E30613;
  --nc-accent-rgb: 227, 6, 19;

  /* Surfaces */
  --nc-bg: #0c0c0c;
  --nc-surface: #161616;
  --nc-border: rgba(255, 255, 255, 0.06);

  /* Text */
  --nc-text: #f0f0f0;
  --nc-text-muted: rgba(255, 255, 255, 0.45);
  --nc-text-dim: rgba(255, 255, 255, 0.25);

  /* Semantic colors */
  --nc-success: #4ade80;
  --nc-warning: #fbbf24;
  --nc-danger: #ea580c;
  --nc-info: #60a5fa;

  /* Typography */
  --nc-font: 'Inter', system-ui, -apple-system, sans-serif;
}
```

---

## Layouts (22)

### `cover`

Full-screen hero/title slide with centered content.

```markdown
---
layout: cover
---
# My Presentation
A subtitle goes here
```

### `default`

Standard content slide with 2.5rem padding and staggered entrance animations.

```markdown
---
layout: default
---
# Slide Title
Content here...
```

### `section`

Chapter divider with centered heading and accent underline.

```markdown
---
layout: section
---
# Chapter Name
Optional subtitle
```

### `center`

Simple centered layout for statements or quotes.

```markdown
---
layout: center
---
# Centered Content
```

### `two-cols`

Left/right content split using named slots.

```markdown
---
layout: two-cols
---
::left::
Left content

::right::
Right content
```

### `comparison`

Side-by-side comparison with distinct visual treatments — dark surface on the left, success-tinted gradient on the right.

```markdown
---
layout: comparison
---
::left::
### ❌ Before
Old way

::right::
### ✅ After
New way
```

### `split-heading`

Magazine-style layout with a big heading pinned on the left and content flowing on the right. A gradient accent divider separates the two sections.

```markdown
---
layout: split-heading
---
::left::
# Big Heading
Subtitle text

::right::
Content body with cards, charts, or any markup.
```

### `fact`

A single powerful statistic centered with a glowing ring animation.

```markdown
---
layout: fact
---
# 47.5M €
Estimated savings over 3 years
```

### `quote`

Cinematic quote with oversized quotation marks, radial glow, and attribution styling.

```markdown
---
layout: quote
---
The best way to predict the future is to invent it.

— Alan Kay
```

### `statement`

Dramatic full-screen statement with text-shadow glow and a breathing radial background.

```markdown
---
layout: statement
---
# We need to act now.
Good design is invisible.
```

### `intro`

Speaker introduction with a glowing side accent bar and styled bullet points.

```markdown
---
layout: intro
---
# Jane Doe
**Lead Engineer** at Acme Corp

- 10+ years software architecture
- AI & ML specialist
```

### `metrics`

Row of metric cards with auto-grid and a content area below.

```markdown
---
layout: metrics
---
# Key Metrics

::metrics::
<div class="nc-metric">
  <p style="font-size: 1.1rem; font-weight: 900; color: white;">99.9%</p>
  <p style="font-size: 0.6rem; color: rgba(255,255,255,0.4);">Uptime</p>
</div>
```

### `image-right`

Content on the left, framed image/visual on the right with glow and entrance animation.

```markdown
---
layout: image-right
---
::default::
# Feature X
Description text

::right::
<img src="/screenshot.png" />
```

### `image-left`

Mirror of `image-right` — image on the left, content on the right.

```markdown
---
layout: image-left
---
::left::
<img src="/screenshot.png" />

::default::
# Feature X
Description text
```

### `code`

Optimized for Monaco editor and code blocks. Automatically wraps code in a macOS-style window frame with traffic-light dots via CSS — no special markup needed.

```markdown
---
layout: code
---
# API Handler

\`\`\`ts
export async function handler(req: Request) {
  return Response.json({ ok: true })
}
\`\`\`
```

### `diagram`

Split layout for Mermaid diagrams — content description on the left, diagram on the right with a subtle grid background. Includes deep CSS overrides to restyle Mermaid SVGs to match the dark theme.

```markdown
---
layout: diagram
---
::left::
# Architecture
High-level overview

::right::
\`\`\`mermaid
graph TD
  A[Client] --> B[API]
  B --> C[Database]
\`\`\`
```

### `math`

Centered layout for KaTeX formulas with a glassmorphic formula card and shimmer effect.

```markdown
---
layout: math
---
# Euler's Identity

$$
e^{i\pi} + 1 = 0
$$

The most beautiful equation in mathematics.
```

### `showcase`

Heading area above a flexible content zone with built-in grid utilities.

```markdown
---
layout: showcase
---
# Feature Highlights

<div class="nc-showcase-grid">
  <div class="nc-showcase-item">
    <img src="/screen1.png" />
    <p>Dashboard</p>
  </div>
</div>
```

### `full`

Edge-to-edge content with zero padding, no entrance animations. Ideal for background images or custom compositions.

```markdown
---
layout: full
---
<img src="/bg.jpg" style="width:100%; height:100%; object-fit:cover;" />
```

### `spotlight`

Dramatic dark stage with an animated spotlight cone illuminating centered content. Background drops to near-black for maximum contrast.

```markdown
---
layout: spotlight
---
# We just raised €50M
Series B led by top-tier venture capital
```

### `browser`

Content rendered inside a Safari-style browser frame with traffic-light dots, URL bar with green lock icon, and navigation buttons. Pass `url` as a frontmatter property.

```markdown
---
layout: browser
url: https://app.example.com/dashboard
---
Dashboard content rendered inside the browser frame.
```

### `end`

Closing/CTA slide with centered content and dimmed footnote styling.

```markdown
---
layout: end
---
# Thank You
Built with ❤️ using Slidev + NeoCarbon
```

---

## Components (25)

### `<NcAnimatedCounter>`

Animated number counter with eased animation.

| Prop | Type | Default | Description |
|------|------|---------|-------------|
| `to` | `number` | — | Target value |
| `duration` | `number` | `2000` | Animation duration (ms) |
| `decimals` | `number` | `0` | Decimal places |
| `separator` | `string` | `','` | Thousands separator |
| `prefix` | `string` | `''` | Prefix (e.g. `'€'`) |
| `suffix` | `string` | `''` | Suffix (e.g. `' M€'`) |

```html
<NcAnimatedCounter :to="47.5" :decimals="1" suffix=" Mio. €" separator="." />
```

### `<NcBarChart>`

Bar chart using Chart.js with dark theme styling.

| Prop | Type | Default | Description |
|------|------|---------|-------------|
| `labels` | `string[]` | — | X-axis labels |
| `data` | `number[]` | — | Data values |
| `colors` | `string[]` | `['#E30613']` | Bar colors |
| `title` | `string` | `''` | Chart title |
| `horizontal` | `boolean` | `false` | Horizontal orientation |
| `height` | `number` | `240` | Chart height (px) |

```html
<NcBarChart title="Revenue" :labels="['Q1','Q2','Q3','Q4']" :data="[2,4,5,7]" />
```

### `<NcPieChart>`

Pie/doughnut chart using Chart.js.

| Prop | Type | Default | Description |
|------|------|---------|-------------|
| `labels` | `string[]` | — | Segment labels |
| `data` | `number[]` | — | Segment values |
| `colors` | `string[]` | `['#E30613']` | Segment colors |
| `title` | `string` | `''` | Chart title |
| `type` | `string` | `'doughnut'` | `'pie'` or `'doughnut'` |
| `height` | `number` | `240` | Chart height (px) |

```html
<NcPieChart title="Budget" :labels="['Eng','Ops']" :data="[60,40]" />
```

### `<NcLineChart>`

Line/area chart with gradient fill and multi-dataset support.

| Prop | Type | Default | Description |
|------|------|---------|-------------|
| `labels` | `string[]` | — | X-axis labels |
| `data` | `number[]` | — | Single dataset values |
| `datasets` | `Array` | — | Multi-dataset mode: `[{ label, data, color }]` |
| `colors` | `string[]` | `['#E30613']` | Line colors |
| `title` | `string` | `''` | Chart title |
| `yLabel` | `string` | `''` | Y-axis label |
| `fill` | `boolean` | `true` | Show gradient fill |
| `smooth` | `boolean` | `true` | Smooth curves |
| `height` | `number` | `240` | Chart height (px) |

```html
<NcLineChart
  title="Growth"
  :labels="['Jan','Feb','Mar']"
  :datasets="[
    { label: 'Revenue', data: [2,4,7], color: '#E30613' },
    { label: 'Costs', data: [3,2.8,2.5], color: '#60a5fa' },
  ]"
/>
```

### `<NcRoiCard>`

Premium ROI / financial metric card with gradient hero value, structured key-value metrics, ambient glow, and hover lift.

| Prop | Type | Default | Description |
|------|------|---------|-------------|
| `label` | `string` | — | Scenario label (e.g. "Konservativ (10%)") |
| `roi` | `string` | — | Hero ROI value (e.g. "6,2×") |
| `color` | `string` | accent | Theme color for accents and gradients |
| `icon` | `string` | — | Optional emoji before the label |
| `source` | `string` | — | Optional source/description text |
| `metrics` | `Array<{ label, value }>` | — | Key-value metric rows |

```html
<NcRoiCard
  icon="🔸" label="Konservativ (10%)"
  source="GitHub/Microsoft-Studie: 8–13%"
  roi="6,2×" color="#fbbf24"
  :metrics="[
    { label: 'Einsparung/Jahr', value: '15,84 Mio. €' },
    { label: 'Einsparung/3J', value: '47,5 Mio. €' },
  ]"
/>
```

### `<NcStatCard>`

Pre-styled KPI card with accent top border and entrance animation.

| Prop | Type | Default | Description |
|------|------|---------|-------------|
| `value` | `string` | — | Display value |
| `label` | `string` | — | Description label |
| `color` | `string` | `'white'` | Value text color |
| `borderColor` | `string` | accent | Top border color |
| `icon` | `string` | — | Optional emoji icon |

```html
<NcStatCard value="99.9%" label="Uptime" icon="🟢" color="var(--nc-success)" />
```

### `<NcProgress>`

Animated progress bar with shimmer effect.

| Prop | Type | Default | Description |
|------|------|---------|-------------|
| `value` | `number` | — | Percentage (0–100) |
| `label` | `string` | — | Label text |
| `color` | `string` | accent | Fill color |
| `showValue` | `boolean` | `true` | Show percentage value |

```html
<NcProgress label="TypeScript" :value="92" color="var(--nc-info)" />
```

### `<NcTimeline>`

Horizontal or vertical timeline with animated nodes.

| Prop | Type | Default | Description |
|------|------|---------|-------------|
| `items` | `Array` | — | `[{ label?, title, description?, color?, active? }]` |
| `vertical` | `boolean` | `false` | Vertical orientation |

```html
<NcTimeline :items="[
  { label: 'Q1', title: 'Research', color: '#E30613' },
  { label: 'Q2', title: 'Build', active: true },
  { label: 'Q3', title: 'Launch', color: '#4ade80' },
]" />
```

### `<NcSteps>`

Numbered vertical step indicator with connector lines and done/active states.

| Prop | Type | Default | Description |
|------|------|---------|-------------|
| `steps` | `Array` | — | `[{ title, description?, done?, active? }]` |

```html
<NcSteps :steps="[
  { title: 'Plan', description: 'Define requirements', done: true },
  { title: 'Build', description: 'Develop MVP', active: true },
  { title: 'Ship', description: 'Deploy to prod' },
]" />
```

### `<NcCallout>`

Styled alert/info box with 5 semantic types.

| Prop | Type | Default | Description |
|------|------|---------|-------------|
| `type` | `string` | `'accent'` | `'info'`, `'success'`, `'warning'`, `'danger'`, `'accent'` |
| `title` | `string` | — | Callout title |
| `icon` | `string` | — | Custom emoji icon |

```html
<NcCallout type="warning" title="Attention">
  Resource utilization is approaching **85%**.
</NcCallout>
```

### `<NcBadge>`

Small status badge / tag pill.

| Prop | Type | Default | Description |
|------|------|---------|-------------|
| `type` | `string` | `'accent'` | `'accent'`, `'success'`, `'warning'`, `'danger'`, `'info'`, `'neutral'` |
| `glow` | `boolean` | `false` | Add glow effect |

```html
<NcBadge type="success">Done</NcBadge>
<NcBadge type="danger" glow>Critical</NcBadge>
```

### `<NcWindow>`

macOS-style window chrome wrapper with traffic-light dots.

| Prop | Type | Default | Description |
|------|------|---------|-------------|
| `title` | `string` | — | Window title / filename |
| `dark` | `boolean` | `false` | Darker body background |

```html
<NcWindow title="api/handler.ts">
  <pre>const x = 42;</pre>
</NcWindow>
```

### `<NcTerminal>`

Terminal/console display with blinking cursor and semantic color classes.

| Prop | Type | Default | Description |
|------|------|---------|-------------|
| `title` | `string` | `'Terminal'` | Title bar text |

Available CSS classes for child elements: `nc-term-prompt`, `nc-term-success`, `nc-term-error`, `nc-term-warn`, `nc-term-info`, `nc-term-dim`.

```html
<NcTerminal title="~/project">
  <div><span class="nc-term-prompt">$</span> npm run build</div>
  <div><span class="nc-term-success">✓ Build complete</span></div>
</NcTerminal>
```

### `<NcGlow>`

Adds a pulsing accent glow behind any child content.

| Prop | Type | Default | Description |
|------|------|---------|-------------|
| `color` | `string` | accent | Glow color (CSS color value) |
| `intensity` | `number` | `0.12` | Glow opacity |
| `size` | `number` | `250` | Glow diameter (px) |

```html
<NcGlow :size="200" :intensity="0.15">
  <h1>🚀</h1>
</NcGlow>
```

### `<NcKbd>`

Styled keyboard shortcut display.

```html
Press <NcKbd>⌘</NcKbd> + <NcKbd>K</NcKbd> to search
```

### `<NcFeatureGrid>`

Auto-layout grid of feature items with emoji icons, staggered entrance, and hover lift.

| Prop | Type | Default | Description |
|------|------|---------|-------------|
| `features` | `Array` | — | `[{ icon?, title, description?, color? }]` |
| `columns` | `number` | auto | Number of columns |

```html
<NcFeatureGrid :features="[
  { icon: '🚀', title: 'Fast', description: 'Sub-second builds' },
  { icon: '🔒', title: 'Secure', description: 'Zero-trust' },
]" :columns="3" />
```

### `<NcMarquee>`

Infinitely scrolling horizontal marquee with fade-edge masking.

| Prop | Type | Default | Description |
|------|------|---------|-------------|
| `items` | `string[]` | — | Items to display |
| `speed` | `number` | `30` | Animation duration (seconds) |
| `reverse` | `boolean` | `false` | Reverse scroll direction |

```html
<NcMarquee :items="['React', 'Vue', 'TypeScript', 'Rust']" :speed="25" />
```

### `<NcIconCard>`

Pre-assembled icon-card component (icon + title + description).

| Prop | Type | Default | Description |
|------|------|---------|-------------|
| `icon` | `string` | — | Iconify component name |
| `title` | `string` | — | Card title |
| `description` | `string` | — | Description text |
| `color` | `string` | accent | Icon background color |
| `highlighted` | `boolean` | `false` | Accent highlight background |
| `small` | `boolean` | `false` | Smaller icon |

```html
<NcIconCard icon="carbon-flash" title="Lightning Fast" description="Sub-second response times" />
```

### `<NcDivider>`

Themed horizontal divider with optional centered label.

| Prop | Type | Default | Description |
|------|------|---------|-------------|
| `label` | `string` | — | Centered label text |
| `accent` | `boolean` | `false` | Use accent color |

```html
<NcDivider />
<NcDivider label="OR" />
<NcDivider label="Section" accent />
```

### `<NcTypewriter>`

Text that types itself character by character with blinking cursor.

| Prop | Type | Default | Description |
|------|------|---------|-------------|
| `text` | `string` | — | Single line text |
| `lines` | `string[]` | — | Multi-line text |
| `speed` | `number` | `50` | Ms per character |
| `delay` | `number` | `500` | Initial delay (ms) |
| `cursor` | `boolean` | `true` | Show cursor |
| `loop` | `boolean` | `false` | Loop animation |

```html
<NcTypewriter :lines="['$ npm run build', '✓ Done in 1.2s']" :speed="40" />
```

### `<NcSpeechBubble>`

iMessage-style chat bubbles with avatar and alignment.

| Prop | Type | Default | Description |
|------|------|---------|-------------|
| `from` | `string` | — | Sender name |
| `avatar` | `string` | — | Avatar emoji |
| `side` | `string` | `'left'` | `'left'` or `'right'` |
| `accent` | `boolean` | `false` | Accent-tinted bubble |
| `delay` | `number` | `0` | Stagger index for entrance animation (0, 1, 2…) |

```html
<NcSpeechBubble from="Alice" avatar="👩" side="left" :delay="0">
  This product is amazing!
</NcSpeechBubble>
<NcSpeechBubble from="Bot" avatar="🤖" side="right" accent :delay="1">
  Thank you!
</NcSpeechBubble>
```

### `<NcFlipCard>`

3D card that flips on hover to reveal a back side.

| Prop | Type | Default | Description |
|------|------|---------|-------------|
| `width` | `string` | `'180px'` | Card width |
| `height` | `string` | `'200px'` | Card height |

```html
<NcFlipCard>
  <template #front><h2>🔒</h2></template>
  <template #back><h2>SOC 2</h2></template>
</NcFlipCard>
```

### `<NcOrbit>`

Items orbiting around a central element (solar system style).

| Prop | Type | Default | Description |
|------|------|---------|-------------|
| `center` | `string` | `'⚛️'` | Center emoji |
| `centerLabel` | `string` | — | Label below center |
| `items` | `string[]` | — | Orbiting items |
| `size` | `number` | `260` | Diagram size (px) |
| `speed` | `number` | `30` | Rotation duration (s) |

```html
<NcOrbit center="🧠" centerLabel="Core" :items="['📊','🔒','🚀','🌍']" />
```

### `<NcHeatmap>`

GitHub-style contribution/activity heatmap grid.

| Prop | Type | Default | Description |
|------|------|---------|-------------|
| `data` | `number[]` | — | Cell values |
| `columns` | `number` | `7` | Grid columns |
| `headers` | `string[]` | — | Grid-aligned column headers |
| `label` | `string` | — | Header label |
| `cellSize` | `number` | `28` | Cell size in px |
| `colors` | `string[]` | accent scale | 5-level color scale |

```html
<NcHeatmap
  :data="[0,1,3,2,4,1,0,1,2,4,3,5,2,0]"
  :columns="7"
  :headers="['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']"
/>
```

### `<NcTicker>`

Bloomberg-style financial ticker bar with change indicators.

| Prop | Type | Default | Description |
|------|------|---------|-------------|
| `items` | `Array` | — | `[{ label, value, change?, unit? }]` |

```html
<NcTicker :items="[
  { label: 'Revenue', value: '€47.5M', change: 12.4 },
  { label: 'Churn', value: '0.8%', change: -15.1 },
]" />
```

### `<NcRadarChart>`

Pure SVG spider/radar chart (no Chart.js needed).

| Prop | Type | Default | Description |
|------|------|---------|-------------|
| `labels` | `string[]` | — | Axis labels |
| `datasets` | `Array` | — | `[{ label?, data, color? }]` |
| `max` | `number` | `5` | Max axis value |
| `size` | `number` | `220` | Chart size (px) |
| `levels` | `number` | `5` | Grid levels |

```html
<NcRadarChart
  :labels="['Speed','Security','Scale','Cost','UX']"
  :datasets="[
    { label: 'Current', data: [2,3,2,4,2], color: '#ff4444' },
    { label: 'Target', data: [5,5,4,4,5], color: '#4ade80' },
  ]"
/>
```

---

## CSS Utility Classes

### Cards & Surfaces

| Class | Description |
|-------|-------------|
| `nc-card` | Dark surface card with hover lift and accent glow |
| `nc-glass` | Glassmorphism panel with backdrop blur |
| `nc-highlight` | Accent-gradient card with shimmer animation |
| `nc-metric` | Compact KPI metric card |

### Text Colors

| Class | Color |
|-------|-------|
| `nc-text-accent` | Brand accent (`--nc-accent`) |
| `nc-text-success` | Green (`--nc-success`) |
| `nc-text-warning` | Amber (`--nc-warning`) |
| `nc-text-danger` | Orange-red (`--nc-danger`) |
| `nc-text-info` | Blue (`--nc-info`) |
| `nc-text-muted` | 60% white |
| `nc-text-dim` | 25% white |

### Other

| Class | Description |
|-------|-------------|
| `nc-label` | Uppercase accent label (0.65rem, tracking) |
| `nc-icon` | 36px accent icon badge with pulse animation |
| `nc-icon-sm` | 28px compact icon badge |
| `nc-showcase-grid` | Auto-fit responsive grid for showcase items |
| `nc-showcase-item` | Card with hover lift for grid items |

---

## Slidev Feature Integration

### Mermaid Diagrams

All Mermaid diagrams are automatically restyled to match the dark theme — nodes use `--nc-surface` fill with accent-colored strokes, edges use semi-transparent accent, and labels use white text. No configuration needed.

### KaTeX Math

KaTeX formulas render with white text on the dark background. Use the `math` layout for dedicated formula slides with glassmorphic cards and shimmer effects.

### Monaco Editor

Monaco code editor and Shiki code blocks get rounded corners, dark backgrounds, and themed borders. Use the `code` layout for a full macOS-window-frame presentation.

---

## Ambient Background

The theme includes a `global-bottom.vue` with:

- **Gradient orbs** — Two soft accent-colored radial gradients
- **Floating particles** — 30 animated dots with randomized motion
- **Grid overlay** — Subtle 60px engineering grid, center-masked
- **Grain texture** — Film noise via SVG `<feTurbulence>`
- **Vignette** — Darkened edges for depth

And a `global-top.vue` with an animated accent line at the top of every slide.

---

## Customization Example

Re-skin to your brand in one CSS block:

```css
:root {
  --nc-accent: #0066FF;
  --nc-accent-rgb: 0, 102, 255;
  --nc-font: 'Outfit', sans-serif;
}
```

---

## Development

```bash
cd slidev-theme-neocarbon
bun install
bun run dev    # Opens demo at localhost:3030
```

## License

MIT
