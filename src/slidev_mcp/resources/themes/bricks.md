# @slidev/theme-bricks

[![NPM version](https://img.shields.io/npm/v/@slidev/theme-bricks?color=3AB9D4&label=)](https://www.npmjs.com/package/@slidev/theme-bricks)

Bricks theme for [Slidev](https://github.com/slidevjs/slidev).

## Install

Add the following frontmatter to your `slides.md`. Start Slidev then it will prompt you to install the theme automatically.

<pre><code>---
theme: <b>bricks</b>
---</code></pre>

Learn more about [how to use a theme](https://sli.dev/themes/use).

## Layouts

### `cover`

![](https://cdn.jsdelivr.net/gh/slidevjs/themes@main/screenshots/theme-bricks/01.png)

### `intro`

![](https://cdn.jsdelivr.net/gh/slidevjs/themes@main/screenshots/theme-bricks/02.png)

### `default`

![](https://cdn.jsdelivr.net/gh/slidevjs/themes@main/screenshots/theme-bricks/03.png)

### `section`

![](https://cdn.jsdelivr.net/gh/slidevjs/themes@main/screenshots/theme-bricks/04.png)

### `items`

![](https://cdn.jsdelivr.net/gh/slidevjs/themes@main/screenshots/theme-bricks/05.png)

### `quote`

![](https://cdn.jsdelivr.net/gh/slidevjs/themes@main/screenshots/theme-bricks/06.png)

### `fact`

![](https://cdn.jsdelivr.net/gh/slidevjs/themes@main/screenshots/theme-bricks/07.png)

### `statement`

![](https://cdn.jsdelivr.net/gh/slidevjs/themes@main/screenshots/theme-bricks/08.png)

## Components

This theme provided a few components for each polygon used in the theme.

`<Polygon1/>` to `<Polygon11/>`

![](https://cdn.jsdelivr.net/gh/slidevjs/themes@main/screenshots/theme-bricks/05.png)

## Example

See [example.md](./example.md)

## License

MIT License © 2021 [iiiiiiinès](https://github.com/iiiiiiines)


---

# Example Slides

The following is the theme's example presentation showing available layouts, components, and features:

````markdown
---
theme: ./
---

# Presentation title

Presentation subtitle

---
layout: intro
---

# Slidev Theme Bricks

---

# Slide Title

Slide Subtitle

* Slide bullet text
  * Slide bullet text
* Slide bullet text

---
layout: section
---

# Lorem ipsum dolor sit

::right::

## Dolore magna

Lorem ipsum dolor sit amet, consectetuer adipiscing elit, sed diam

## Dolore magna

Lorem ipsum dolor sit amet, consectetuer adipiscing elit, sed diam

---
layout: items
cols: 4
---

# Lorem ipsum

::items::

<Polygon7 w="20" h="20" m="auto"/>
<Polygon2 w="20" h="20" m="auto"/>
<Polygon3 w="20" h="20" m="auto"/>
<Polygon4 w="20" h="20" m="auto"/>

Polygon7

Polygon2

Polygon3

Polygon4

---
layout: quote
---

# Lorem ipsum

---
layout: fact
---

# Lorem ipsum

---
layout: statement
---

# Thanks
````
