# slidev-theme-unicorn

[![NPM version](https://img.shields.io/npm/v/slidev-theme-unicorn?color=3AB9D4&label=)](https://www.npmjs.com/package/slidev-theme-unicorn)

A Unicorn theme for [Slidev](https://github.com/slidevjs/slidev).

This theme is based on [dawntraoz.com](https://www.dawntraoz.com/) website design.

Live demo: https://unicorn-theme.dawntraoz.com/

## Install

Add the following frontmatter to your `slides.md`. Start Slidev then it will prompt you to install the theme automatically.

<pre><code>---
theme: <b>unicorn</b>
---</code></pre>

Learn more about [how to use a theme](https://sli.dev/themes/use).

## Layouts

This theme provides the following layouts:

### Common properties

By default any layout will contain a header and a footer expecting:

```
---
logoHeader: 'https://www.dawntraoz.com/images/logo.svg'
website: 'dawntraoz.com'
handle: 'dawntraoz'
---
```

If you don't add this property it will be an empty slide expecting your content:

With properties            | Without properties 
:-------------------------:|:-------------------------:
![introDark](https://raw.githubusercontent.com/Dawntraoz/slidev-theme-unicorn/master/screenshots/dark-theme-center.png) | ![introLight](https://raw.githubusercontent.com/Dawntraoz/slidev-theme-unicorn/master/screenshots/dark-theme-center-without-header-footer.png)

---

### Intro `intro`

Usage:

- Add `intro` in the layout field.
- Add your profile image in the `introImage` field.

```
---
layout: intro
introImage: 'https://img2.storyblok.com/312x312/filters:format(webp)/f/79165/400x400/1082ff0d24/dawntraoz-alba-silvente.jpg'
---
```

Dark                       | Light
:-------------------------:|:-------------------------:
![introDark](https://raw.githubusercontent.com/Dawntraoz/slidev-theme-unicorn/master/screenshots/dark-theme-intro.png) | ![introLight](https://raw.githubusercontent.com/Dawntraoz/slidev-theme-unicorn/master/screenshots/light-theme-intro.png)

---

### Default `cover`

Cover is the default layout when none is specified.

Usage:

```
---
layout: cover
---
```

Dark                       | Light
:-------------------------:|:-------------------------:
![introDark](https://raw.githubusercontent.com/Dawntraoz/slidev-theme-unicorn/master/screenshots/dark-theme-cover.png) | ![introLight](https://raw.githubusercontent.com/Dawntraoz/slidev-theme-unicorn/master/screenshots/light-theme-cover.png)

---

### Presentation `cover-logos`

Usage:

- Add `cover-logos` in the layout field.
- Add an Array of logo URLs in the `logos` field.

```
---
layout: cover-logos
logos: [
  'https://img2.storyblok.com/588x0/filters::format(webp)/f/86387/x/21aa32ed18/logo-normal.svg',
  'https://nuxtjs.org/logos/nuxt-emoji.png',
]
---
```

Dark                       | Light
:-------------------------:|:-------------------------:
![introDark](https://raw.githubusercontent.com/Dawntraoz/slidev-theme-unicorn/master/screenshots/dark-theme-cover-logos.png) | ![introLight](https://raw.githubusercontent.com/Dawntraoz/slidev-theme-unicorn/master/screenshots/light-theme-cover-logos.png)

---

### Table of contents `table-contents`

Usage:

- Add `table-contents` in the layout field.
- Add an Array of hexadecimal colours in the `gradientColors` field to fill the illustration.

```
---
layout: table-contents
gradientColors: ['#8EC5FC', '#E0C3FC']
---
```

Dark (added gradient)      | Light (default gradient)
:-------------------------:|:-------------------------:
![introDark](https://raw.githubusercontent.com/Dawntraoz/slidev-theme-unicorn/master/screenshots/dark-theme-table-content.png) | ![introLight](https://raw.githubusercontent.com/Dawntraoz/slidev-theme-unicorn/master/screenshots/light-theme-table-content.png)

---

### New section slide `new-section`

> Always in dark version

Usage:

- Add `new-section` in the layout field.

```
---
layout: new-section
---
```

Dark                       | Light
:-------------------------:|:-------------------------:
![introDark](https://raw.githubusercontent.com/Dawntraoz/slidev-theme-unicorn/master/screenshots/new-section.png) | ![introLight](https://raw.githubusercontent.com/Dawntraoz/slidev-theme-unicorn/master/screenshots/new-section.png)

---

### Image Centered `image-center`

The content will be place before the image, you can add a title, subtitle to give context to the image.

```
---
layout: image-center
image: 'https://source.unsplash.com/collection/94734566/1920x1080'
imageWidth: '450'
imageHeight: '950'
---
```

Dark                       | Light
:-------------------------:|:-------------------------:
![introDark](https://raw.githubusercontent.com/Dawntraoz/slidev-theme-unicorn/master/screenshots/dark-theme-image-centered.png) | ![introLight](https://raw.githubusercontent.com/Dawntraoz/slidev-theme-unicorn/master/screenshots/light-theme-image-center.png)

---

### Text centered `center`

```
---
layout: center
---
```

Dark                       | Light
:-------------------------:|:-------------------------:
![introDark](https://raw.githubusercontent.com/Dawntraoz/slidev-theme-unicorn/master/screenshots/dark-theme-center.png) | ![introLight](https://raw.githubusercontent.com/Dawntraoz/slidev-theme-unicorn/master/screenshots/light-theme-center.png)

---

## Contributing

- `pnpm install`
- `pnpm dev` to start theme preview of `example.md`
- Edit the `example.md` and style to see the changes
- `pnpm export` to generate the preview PDF
- `pnpm screenshot` to generate the preview PNG


---

# Example Slides

The following is the theme's example presentation showing available layouts, components, and features:

````markdown
---
theme: ./
colorSchema: 'light'
layout: intro
logoHeader: '/logo.svg'
website: 'dawntraoz.com'
handle: 'dawntraoz'
introImage: 'https://img2.storyblok.com/312x312/filters:format(webp)/f/79165/400x400/1082ff0d24/dawntraoz-alba-silvente.jpg'
---

# Unicorn slidev theme

Presentation slides for developers


<div class="pt-12">
  <span @click="$slidev.nav.next" class="px-2 p-1 rounded cursor-pointer" hover="bg-white bg-opacity-10">
    Press Space for next page <carbon:arrow-right class="inline"/>
  </span>
</div>

---
logoHeader: '/logo.svg'
website: 'dawntraoz.com'
handle: 'dawntraoz'
layout: cover-logos
logos: [
  'https://img2.storyblok.com/256x0/filters:format(webp)/f/86387/x/4cf6a70a8c/logo-white-text.svg',
  '/nuxt-emoji-white.png',
  '/storyblok.png'
]
---

Frontend Developer Consultant at **@passionpeopleNL**
Blogger, speaker and open source lover

Ambassador at **@nuxt_js** and **@storyblok**

---
logoHeader: '/logo.svg'
website: 'dawntraoz.com'
handle: 'dawntraoz'
layout: table-contents
gradientColors: ['#A21CAF', '#5B21B6']
---

# What is Slidev?

Slidev is a slides maker and presenter designed for developers, consist of the following features
  
- 📝 **Text-based** - focus on the content with Markdown
- 🎨 **Themable** - create your theme
- 🧑‍💻 **Developer Friendly** - code highlighting, live coding
- 🤹 **Interactive** - embedding Vue components
- 🎥 **Recording** - built-in recording and camera view
- 📤 **Portable** - export into PDF, PNGs, or even a host it
- 🛠 **Hackable** - anything possible on a webpage

---
logoHeader: '/logo.svg'
website: 'dawntraoz.com'
handle: 'dawntraoz'
layout: new-section
sectionImage: 'https://images.unsplash.com/photo-1711091189179-53ec364d4bf3?q=80&w=3054&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D'
---

# This is a new section
Some content to explain

<!--
Add some notes to your slides!
-->

---
logoHeader: '/logo.svg'
website: 'dawntraoz.com'
handle: 'dawntraoz'
---

# Navigation

Hover on the bottom-left corner to see the navigation's controls panel

### Keyboard Shortcuts

|     |     |
| --- | --- |
| <kbd>space</kbd> / <kbd>tab</kbd> / <kbd>right</kbd> | next animation or slide |
| <kbd>left</kbd> | previous animation or slide |
| <kbd>up</kbd> | previous slide |
| <kbd>down</kbd> | next slide |

---
logoHeader: '/logo.svg'
website: 'dawntraoz.com'
handle: 'dawntraoz'
layout: image-center
image: 'https://source.unsplash.com/collection/94734566/1920x1080'
imageWidth: '450'
imageHeight: '950'
---

# Image centered

Making use of `image-center` layout.

---
logoHeader: '/logo.svg'
website: 'dawntraoz.com'
handle: 'dawntraoz'
layout: cover
---

# Code

Use code snippets and get the highlighting directly!

```ts
interface User {
  id: number
  firstName: string
  lastName: string
  role: string
}

function updateUser(id: number, update: Partial<User>) {
  const user = getUser(id)
  const newUser = {...user, ...update}  
  saveUser(id, newUser)
}
```

---
layout: center
---

# Thank you

[Documentations](https://sli.dev) / [GitHub Repo](https://github.com/slidevjs/slidev)
````
