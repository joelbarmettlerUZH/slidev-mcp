# slidev-theme-vibe

[![NPM version](https://img.shields.io/npm/v/slidev-theme-vibe?color=3AB9D4&label=)](https://www.npmjs.com/package/slidev-theme-vibe)

A premium dark-mode theme for [Slidev](https://github.com/slidevjs/slidev) featuring glassmorphism, neon accents, and sophisticated aesthetics. Inspired by SpaceX cockpit UIs, high-end EV dashboards, and minimalist cyberpunk design.

## Install

Add the following frontmatter to your `slides.md`. Start Slidev then it will prompt you to install the theme automatically.

<pre><code>---
theme: <b>vibe</b>
---</code></pre>

Learn more about [how to use a theme](https://sli.dev/guide/theme-addon#use-theme).

## Layouts

This theme provides the following layouts:

### `cover`

A full-screen title slide with an animated particle background, gradient heading (white to cyan), and fade-in-up entrance animations. Ideal for opening slides.

### `intro`

A full-screen introduction layout with animated background. Similar to `cover` but without uppercase text transformation — better suited for introductory content.

### `default`

The standard content layout with clean heading hierarchy and comfortable padding. Use this for regular text-heavy slides.

### `center`

Centers all content both vertically and horizontally. Good for single statements, key takeaways, or focused messaging.

### `section`

A section divider layout with a left gradient accent bar and slide-in animations. Use it to mark major topic transitions.

![section layout](./examples/section.png)

### `two-cols`

A two-column grid layout with a decorative gradient divider line between the columns. Use the default slot for the left column and the `right` named slot for the right column.

![two-cols layout](./examples/two-column.png)

```md
---
layout: two-cols
---

# Left column

Content here

::right::

# Right column

Content here
```

### `image-right`

Content on the left with an image on the right. The image container has a rounded border, glow effect, and drop shadow. Pass the image URL via the `image` frontmatter prop or use the `image` named slot.

![image-right layout](./examples/image-right.png)

```md
---
layout: image-right
image: /path/to/image.png
---

# Your content here
```

### `image-left`

Mirror of `image-right` — image on the left, content on the right. Accepts the same `image` prop and `image` named slot.

```md
---
layout: image-left
image: /path/to/image.png
---

# Your content here
```

### `quote`

A quote layout with a glass-morphism card, frosted glass effect, and a large decorative quotation mark. The last paragraph is automatically styled as the author attribution.

![quote layout](./examples/quote.png)

```md
---
layout: quote
---

This is the quote text.

Author Name
```

## Components

This theme provides the following components:

### `VibeBackground`

An animated canvas background featuring floating particles and a scrolling grid pattern. Used internally by the `cover` and `intro` layouts. No props required.

### `GlassCard`

A reusable glass-morphism card container with a semi-transparent background, backdrop blur, and a subtle cyan border.

| Prop | Type | Default | Description |
|------|------|---------|-------------|
| `glow` | `boolean` | `false` | Applies a permanent cyan glow shadow |
| `hover` | `boolean` | `true` | Enables border brightening and glow on hover |

```html
<GlassCard>
  Default card with hover effect
</GlassCard>

<GlassCard glow>
  Card with permanent glow
</GlassCard>

<GlassCard :hover="false">
  Static card without hover effect
</GlassCard>
```

## Contributing

- `npm install`
- `npm run dev` to start theme preview of `example.md`
- Edit the `example.md` and style to see the changes
- `npm run export` to generate the preview PDF
- `npm run screenshot` to generate the preview PNG
