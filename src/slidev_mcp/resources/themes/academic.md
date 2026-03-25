# slidev-theme-academic [![npm](https://img.shields.io/npm/v/slidev-theme-academic?color=blue)](https://www.npmjs.com/package/slidev-theme-academic) ![npm](https://img.shields.io/npm/dw/slidev-theme-academic?color=blue) [![https://img.shields.io/badge/Conventional%20Commits-1.0.0-yellow.svg](https://img.shields.io/badge/Conventional%20Commits-1.0.0-yellow.svg)](https://www.conventionalcommits.org/)

Simplifies creating academic presentations with [Slidev](https://github.com/slidevjs/slidev) by providing the necessary components and layouts.

## Install

Add the following frontmatter to your `slides.md`. Start Slidev then it will prompt you to install the theme automatically.

```
---
theme: academic
---
```

Learn more about [how to use a theme](https://sli.dev/themes/use).

## Layouts

### cover

| **Parameter**              | **Type**      | **Default**                       | **Notes**                                                                         |
| -------------------------- | ------------- | --------------------------------- | --------------------------------------------------------------------------------- |
| `coverAuthor`              | Array, String | `undefined`                       | -                                                                                 |
| `coverAuthorUrl`           | Array, String | `undefined`                       | -                                                                                 |
| `coverBackgroundUrl`       | String        | `undefined`                       | Adapt the text color with the built-in `class` attribute in the same frontmatter. |
| `coverBackgroundSource`    | String        | `undefined`                       | -                                                                                 |
| `coverBackgroundSourceUrl` | String        | `undefined`                       | -                                                                                 |
| `coverDate`                | String        | `new Date().toLocaleDateString()` | -                                                                                 |

![cover](../assets/example-export/01.png)

### table-of-contents

`table-of-contents` puts custom content above the table of contents. If none is given, the content defaults to `<h1>Table of Contents</h1>`.

![table-of-contents](../assets/example-export/02.png)

### index

`index` can be used as a general list for figures, references, tables etc..

`index` puts custom content above the list. If none is given, the content defaults to `<h1>Index</h1>`.

| **Parameter**               | **Type**                                      | **Default** | **Notes**                                                                              |
| --------------------------- | --------------------------------------------- | ----------- | -------------------------------------------------------------------------------------- |
| `indexEntries`<sup>\*</sup> | `{ title: string, uri?: number \| string }[]` | `undefined` | Specify `uri` as a page number or optional URL in accordance with `indexRedirectType`. |
| `indexRedirectType`         | `external \| internal`                        | `internal`  | -                                                                                      |

![index](../assets/example-export/08.png)

### figure

| **Parameter**            | **Type** | **Default** | **Notes**                |
| ------------------------ | -------- | ----------- | ------------------------ |
| `figureCaption`          | String   | `undefined` | -                        |
| `figureFootnoteNumber`   | Number   | `undefined` | Align with a `Footnote`. |
| `figureUrl`<sup>\*</sup> | String   | `undefined` | -                        |

![figure](../assets/example-export/04.png)

### figure-side

| **Parameter**            | **Type** | **Values**   | **Default** | **Notes**                |
| ------------------------ | -------- | ------------ | ----------- | ------------------------ |
| `figureCaption`          | String   | -            | `undefined` | -                        |
| `figureFootnoteNumber`   | Number   | -            | `undefined` | Align with a `Footnote`. |
| `figureUrl`<sup>\*</sup> | String   | -            | `undefined` | -                        |
| `figureX`                | String   | `'l'`, `'r'` | `'r'`       | -                        |

![figure-side](../assets/example-export/05.png)

## Components

### Footnotes

`Footnotes` is to be used as parent of `Footnote` children.

| **Parameter** | **Type** | **Values**       | **Default** | **Notes**                                                       |
|---------------|----------|------------------|-------------|-----------------------------------------------------------------|
| `filled`      | Boolean  | `true`, `false`  | `false`     | Overlay subordinate content that may puts itself in background. |
| `separator`   | Boolean  | `true`, `false`  | `false`     | -                                                               |
| `x`           | String   | `'l'`, `'r'`     | `'r'`       | -                                                               |
| `y`           | String   | `'col'`, `'row'` | `'row'`     |                                                                 |

### Footnote

`Footnote` is to be used as children of a `Footnotes` parent.

| **Parameter** | **Type** | **Notes**                                        |
| ------------- | -------- | ------------------------------------------------ |
| `number`      | Number   | Align with an attribution in the pages' content. |

![Footnotes & Footnote](../assets/example-export/06.png)

### Pagination

`Pagination` is rendered globally by default. The global configuration can be defined using [`themeConfig`](#themeconfig).

If certain pages need individual configuration of `Pagination`, exclude them from global rendering of `Pagination` using [`themeConfig`](#themeconfig) and add `Pagination` manually.

| **Parameter** | **Type**      | **Values**   | **Default** | **Notes**                                                                                    |
| ------------- | ------------- | ------------ | ----------- | -------------------------------------------------------------------------------------------- |
| `classNames`  | Array, String | -            | `undefined` | `Pagination` by default uses the color given by the color schema currently active in Slidev. |
| `x`           | String        | `'l'`, `'r'` | `'r'`       | -                                                                                            |
| `y`           | String        | `'b'`, `'t'` | `'t'`       | -                                                                                            |

![Pagination](../assets/example-export/07.png)

## themeConfig

Global parameters of the theme can be set using the `themeConfig` block in the frontmatter of the first page.

Be aware that defining the `themeConfig` block initializes all parameters as `undefined`; hence you may need to set parameters albeit using defaults.

| **Parameter**             | **Type** | **Values**   | **Default** | **Notes**                                                                                                                                          |
| ------------------------- | -------- | ------------ | ----------- | -------------------------------------------------------------------------------------------------------------------------------------------------- |
| `paginationPagesDisabled` | Array    | -            | `undefined` | Disable global rendering of `Pagination` for pages having individual `Pagination`.                                                                 |
| `paginationX`             | String   | `'l'`, `'r'` | `'r'`       | To disable global default rending, set both `paginationX` and `paginationY` to `undefined`. `Pagination` can then still be used on selected pages. |
| `paginationY`             | String   | `'b'`, `'t'` | `'t'`       | To disable global default rending, set both `paginationX` and `paginationY` to `undefined`. `Pagination` can then still be used on selected pages. |

## Contributing

- `npm run setup`
- `npm run dev` to start theme preview of `example.md`
- Edit the `example.md` and style to see the changes
- `npm run export` to generate the preview PDF
- `npm run screenshot` to generate the preview PNG


---

# Example Slides

The following is the theme's example presentation showing available layouts, components, and features:

````markdown
---
theme: ./
layout: cover
class: text-white
coverAuthor: [alexanderdavide, contributors]
coverAuthorUrl: [https://www.alexeble.de, https://github.com/alexanderdavide/slidev-theme-academic/graphs/contributors]
coverBackgroundUrl: /presentation.jpg
coverBackgroundSource: unsplash
coverBackgroundSourceUrl: https://images.unsplash.com/photo-1594122230689-45899d9e6f69?ixlib=rb-1.2.1&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=1170&q=80
fonts:
  local: Montserrat, Roboto Mono, Roboto Slab # local fonts are used for legal reasons for deployment to https://slidev-theme-academic.alexeble.de and only set up for the example project, remove this line for your project to automatically have fonts imported from Google
hideInToc: true
themeConfig:
  paginationX: r
  paginationY: t
  paginationPagesDisabled: [1]
title: slidev-theme-academic
info: |
  # slidev-theme-academic

  Created and maintained by [Alexander Eble](https://www.alexeble.de).

  - [GitHub](https://github.com/alexanderdavide/slidev-theme-academic)
  - [npm](https://www.npmjs.com/package/slidev-theme-academic)

  slidev-theme-academic is licensed under [MIT](https://github.com/alexanderdavide/slidev-theme-academic/blob/master/LICENSE).

  <ul>
    <li>
      <a href="https://www.alexeble.de/impressum/" target="_blank">Legal information of this website</a>
    </li>
    <li>
      <a href="https://www.alexeble.de/datenschutz/" target="_blank">Privacy policy of this website</a>
    </li>
  </ul>
---

# cover

## slidev-theme-academic

<Pagination classNames="text-gray-300" />

---
layout: table-of-contents
hideInToc: false
---

# table-of-contents

---
layout: index
indexEntries:
  - { title: "Curated cover image for Slidev", uri: 4 }
  - { title: "Curated cover image for Slidev", uri: 5 }
---

# index

`index` used as list of figures

---
layout: figure
figureCaption: Curated cover image for Slidev
figureFootnoteNumber: 1
figureUrl: https://picsum.photos/1920/1080
---

# figure

<Footnotes separator>
  <Footnote :number=1><a href="https://picsum.photos/" rel="noreferrer" target="_blank">Picsum</a></Footnote>
</Footnotes>

---
layout: figure-side
figureCaption: Curated cover image for Slidev
figureFootnoteNumber: 1
figureUrl: https://picsum.photos/1024/768
---

# figure-side

- Ensures figures are displayed nicely out of the box
- Allows placing the figure on the left or right
- Features an optional figure caption

<Footnotes separator>
  <Footnote :number=1><a href="https://picsum.photos/" rel="noreferrer" target="_blank">Picsum</a></Footnote>
</Footnotes>

---
layout: center
class: "text-center"
---

# Footnotes & Footnote

<span class="font-extralight">
  <q>Give credit where credit is due</q>
  <sup>1</sup>
</span>

<Footnotes separator>
  <Footnote :number=1>Smart person</Footnote>
</Footnotes>

---
layout: center
class: "text-center"
---

# Pagination

<span class="font-extralight">Enabled by default</span>

<img
  class="absolute transform rotate-z-180 -top-0.9 -right-21.5 w-36"
  src="/box.svg"
/>

<p class="absolute font-extralight right-14 transform rotate-8 top-4">Here!</p>

---
layout: index
indexEntries:
  - { title: "GitHub", uri: "https://github.com/alexanderdavide/slidev-theme-academic" }
  - { title: "npm", uri: "https://www.npmjs.com/package/slidev-theme-academic" }
  - { title: "Slidev", uri: "https://sli.dev" }
indexRedirectType: external
---

# index

`index` used as a list of references
````
