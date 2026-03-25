![repository-banner.png](https://res.cloudinary.com/alvarosaburido/image/upload/v1612193118/as-portfolio/Repo_Banner_kexozw.png)

# slidev-theme-penguin

[![NPM version](https://img.shields.io/npm/v/slidev-theme-penguin?color=3AB9D4&label=)](https://www.npmjs.com/package/slidev-theme-penguin)

A Penguin 🐧  theme for [Slidev](https://github.com/slidevjs/slidev).

This theme is based on my personal brand, but it can be easily use and customized for your own.

<!--
run `npm run dev` to check out the slides for more details of how to start writing a theme
-->

<!--
put some screenshots here to demonstrate your theme,
-->

Live demo: [here](https://slidev-theme-penguin.alvarosaburido.dev/)

## You can help me keep working on this project 💚

- [Become a Sponsor on GitHub](https://github.com/sponsors/alvarosaburido)
- [One-time donation via PayPal](https://paypal.me/alvarosaburido)

<h4 align="center">Generous Unicorns 🦄</h4>

<p align="center">
  <a href="https://github.com/OmgImAlexis" target="_blank" rel="noopener noreferrer" ">
    <img src="https://avatars.githubusercontent.com/u/6525926?v=4" height="72px"  style="border-radius: 100%; overflow: hidden; border: 4px solid #5EDCAE" alt="OmgImAlexis">
  </a>
</p>

## Install

Add the following frontmatter to your `slides.md`. Start Slidev then it will prompt you to install the theme automatically.

<pre><code>---
theme: <b>penguin</b>
---</code></pre>

It is also required to install the npm package `vite-svg-loader` and adding a vite.config.js in your project with the following:

```js
import svgLoader from 'vite-svg-loader'

export default {
  plugins: [svgLoader()],
}
```

Learn more about [how to use a theme](https://sli.dev/themes/use).

## Layouts

This theme provides the following layouts:

### Header and footer

By default any layout will not contain a header and a footer

But you can add this properties to add header and footer

```
---
themeConfig:
  logoHeader: '/logo.svg'
  eventLogo: 'https://img2.storyblok.com/352x0/f/84560/2388x414/23d8eb4b8d/vue-amsterdam-with-name.png'
  eventUrl: 'https://vuejs.amsterdam/'
  twitter: '@alvarosabu'
  twitterUrl: 'https://twitter.com/alvarosabu'
---
```
With properties            | Without properties
:-------------------------:|:-------------------------:
![introDark](./screenshots/dark/intro.png) | ![introLight](./screenshots/dark/04.png)

---

Date on footer is automatic

### Intro `intro`

Usage:

- Add `intro` in the layout field.

```
---
layout: intro
---
```

Dark                       | Light
:-------------------------:|:-------------------------:
![introDark](./screenshots/dark/intro.png) | ![introLight](./screenshots/light/intro.png)

---

### Presenter `presenter`

Usage:

- Add `presenter` in the layout field.
- Add `presenterImage` for the speaker image.

```
---
layout: presenter
presenterImage: 'https://res.cloudinary.com/alvarosaburido/image/upload/v1622370075/as-portfolio/alvaro_saburido.jpg'
---
```

Dark                       | Light
:-------------------------:|:-------------------------:
![presenterDark](./screenshots/dark/presenter.png) | ![presenterLight](./screenshots/light/presenter.png)

---

### New Section `new-section`

Usage:

- Add `new-section` in the layout field.

```
---
layout: new-section
---
```

Dark                       | Light
:-------------------------:|:-------------------------:
![newSectionDark](./screenshots/dark/new-section.png) | ![newSectionLight](./screenshots/light/new-section.png)

---

### Text Image `text-image`

Usage:

- Add `text-image` in the layout field and add the image url on the `media` field.

```
---
layout: text-image
media: 'https://media.giphy.com/media/VkMV9TldsPd28/giphy.gif'
---
```

Dark                       | Light
:-------------------------:|:-------------------------:
![textImageDark](./screenshots/dark/text-image.png) | ![textImageLight](./screenshots/light/text-image.png)

- Add `reverse:true` to reverse the order of the layout

```
---
layout: text-image
media: 'https://media.giphy.com/media/VkMV9TldsPd28/giphy.gif'
reverse: true
---
```
Dark                       | Light
:-------------------------:|:-------------------------:
![textImageDark](./screenshots/dark/text-image-reverse.png) | ![textImageLight](./screenshots/light/text-image-reverse.png)
---

### Text Window `text-window`

Usage:

- Add `text-window` in the layout field.

```
---
layout: text-window
---
```

Dark                       | Light
:-------------------------:|:-------------------------:
![textWindowDark](./screenshots/dark/text-window.png) | ![textWindowLight](./screenshots/light/text-window.png)

- Add `reverse:true` to reverse the order of the layout

```
---
layout: text-window
reverse: true
---
```
Dark                       | Light
:-------------------------:|:-------------------------:
![textWindowDark](./screenshots/dark/text-window-reverse.png) | ![textWindowLight](./screenshots/light/text-window-reverse.png)

To set the content inside the window console, just use the syntax sugar `::window::` for slot name:

```
---
layout: text-window
---

# Consoles

Use code snippets and get the highlighting directly into a nice looking window!

::window::

I go inside the window

```

## Components

This theme provides the following components:

### Auto-favicon fancy link `fancy-link`

`FancyLink` Component will allow you to automatically add the favicon just aside your link.

![auto-favicon](./screenshots/fancy-link-component.png)

To use it you just need to add it to your `examples.md` like this:

```markdown
Say hi at <fancy-link href="https://twitter.com/alvarosabu">@alvarosabu</fancy-link>
```

### Console window `the-console`

```html
<TheConsole>
  <iframe
    height="300"
    style="width: 100%"
    scrolling="no"
    title="Text Clock"
    src="https://codepen.io/searleb/embed/pvQaJB?default-tab=html%2Cresult"
    frameborder="no"
    loading="lazy"
    allowtransparency="true"
    allowfullscreen="true"
  >
    See the Pen <a href="https://codepen.io/searleb/pen/pvQaJB"> Text Clock</a> by Bill Searle (<a
      href="https://codepen.io/searleb"
      >@searleb</a
    >) on <a href="https://codepen.io">CodePen</a>.
  </iframe>
</TheConsole>
```

> TODO:

## Contributing

- `npm install`
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
colorSchema: 'auto'
layout: intro
# https://sli.dev/custom/highlighters.html
highlighter: shiki
title: Slidev Penguin Theme
themeConfig:
  logoHeader: '/avatar.png'
  eventLogo: 'https://img2.storyblok.com/352x0/f/84560/2388x414/23d8eb4b8d/vue-amsterdam-with-name.png'
  eventUrl: 'https://vuejs.amsterdam/'
  twitter: '@alvarosabu'
  twitterUrl: 'https://twitter.com/alvarosabu'
---

# A penguin Slidev Theme

🐧 slides for developers

<div class="pt-12">
  <span @click="next" class="px-2 p-1 rounded cursor-pointer hover:bg-white hover:bg-opacity-10">
    Press Space for next page <carbon:arrow-right class="inline"/>
  </span>
</div>

---
layout: presenter
eventLogo: 'https://img2.storyblok.com/352x0/f/84560/2388x414/23d8eb4b8d/vue-amsterdam-with-name.png'
eventUrl: 'https://vuejs.amsterdam/'
twitter: '@alvarosabu'

twitterUrl: 'https://twitter.com/alvarosabu'
presenterImage: 'https://res.cloudinary.com/alvarosaburido/image/upload/v1666351649/b_w_egfb4v.png'
---

# Alvaro Saburido

DX at <a  href="https://www.storyblok.com/"><logos-storyblok-icon  mr-1/>Storyblok</a>

- Barcelona, Spain 🇪🇸
- I often write at <a href="https://dev.to/alvarosaburido"> dev.to/@alvarosabu</a>
- Creating content on <a href="https://www.youtube.com/channel/AlvaroDevLabs" ><logos-youtube-icon mr-1 />AlvaroDevLabs</a>
- Blog & Portfolio <a href="https://alvarosaburido.dev">alvarosaburido.dev</a>
- Say hi at <a href="https://twitter.com/alvarosabu"><logos-twitter mr-1 />@alvarosabu</a>

---
layout: text-image
media: 'https://media.giphy.com/media/VkMV9TldsPd28/giphy.gif'
caption: 'I am a penguin'
---

# This is a peguin 🐧

Arepa ipsum dolor amet jalabola! aenean sit tequeños se prendio esta chamito;? Nisl nojoda eu amet in? Nisl cuál es la guachafita ni lava ni presta la batea háblame cloro gravida sifrino macundal panita; Sed háblame cloro nunc empanada ac coroto Na webona vladimil parchita?

- Cacique panita sit Se prendio la labia gravida Praesent tequeño.
- Qué paso mi pana?! elit parchita molleja aguacate vergación, háblame mollejúo chamito est burda mauris morbi;

---
layout: text-image
reverse: true
media: 'https://media.giphy.com/media/VkMV9TldsPd28/giphy.gif'
---

# This is a reverse peguin

Arepa ipsum dolor amet jalabola! aenean sit tequeños se prendio esta mierdaa menool ladilla chamito;? Nisl nojoda eu amet in? Nisl cuál es la guachafita ni lava ni presta la batea háblame cloro gravida sifrino macundal panita; Sed háblame cloro nunc empanada ac coroto Na webona vladimil parchita? Cacique ladilla sit Se prendio el peo labia gravida Praesent tequeño. Qué paso mi pana?! elit parchita molleja aguacate vergación, háblame mollejúo chamito est burda mauris morbi;
---

# What is Slidev?

Slidev is a slides maker and presenter designed for developers `devs`, consist of the following features

- 📝 **Text-based** - focus on the content with Markdown, and then style them later
- 🎨 **Themable** - theme can be shared and used with npm packages
- 🧑‍💻 **Developer Friendly** - code highlighting, live coding with autocompletion
- 🤹 **Interactive** - embedding Vue components to enhance your expressions
- 🎥 **Recording** - built-in recording and camera view
- 📤 **Portable** - export into PDF, PNGs, or even a hostable SPA
- 🛠 **Hackable** - anything possible on a webpage

<br>
<br>

Read more about [Why Slidev?](https://sli.dev/guide/why)

---

# Navigation

Hover on the bottom-left corner to see the navigation's controls panel

### Keyboard Shortcuts

|                                                      |                             |
| ---------------------------------------------------- | --------------------------- |
| <kbd>space</kbd> / <kbd>tab</kbd> / <kbd>right</kbd> | next animation or slide     |
| <kbd>left</kbd>                                      | previous animation or slide |
| <kbd>up</kbd>                                        | previous slide              |
| <kbd>down</kbd>                                      | next slide                  |

---
layout: new-section

---

# New wild section appeared

![penguin-work](https://media.giphy.com/media/VkMV9TldsPd28/giphy.gif)

---
eventLogo: 'https://img2.storyblok.com/352x0/f/84560/2388x414/23d8eb4b8d/vue-amsterdam-with-name.png'
eventUrl: 'https://vuejs.amsterdam/'
twitter: '@alvarosabu'
twitterUrl: 'https://twitter.com/alvarosabu'

---

# Code

Use code snippets and get the highlighting directly!

```vue
<script setup>
import { TresCanvas } from '@tresjs/core'
</script>

<template>
  <TresCanvas
    clear-color="”#82DBC5”"
    window-size
  >
    <TresPerspectiveCamera />
    <TresMesh
      @click="onClick"
    >
      <TresBoxGeometry :args="[1, 1, 1]" />
      <TresMeshNormalMaterial />
    </TresMesh>
  </TresCanvas>
</template>
```

---
layout: two-cols
---
Awiwiiw

```vue
// Model.vue
<script setup lang="ts">
import { useAnimations, useGLTF } from '@tresjs/cientos'

const { scene: model, animations } = await useGLTF(
  'models/ugly-bunny.gltf',
)

const { actions, mixer } = useAnimations(animations, model)
const currentAction = ref(actions.Greeting)
currentAction.value.play()
</script>

<template>
  <primitive :object="model" />
</template>
```

::right::

```vue
<template>
  <TresCanvas
    clear-color="”#82DBC5”"
    window-size
  >
    <TresPerspectiveCamera />
    <Suspense>
      <Model />
    </Suspense>
  </TresCanvas>
</template>
```

---
layout: two-thirds
---
Awiwiiw

```vue
// Model.vue
<script setup lang="ts">
import { useAnimations, useGLTF } from '@tresjs/cientos'

const { scene: model, animations } = await useGLTF(
  'models/ugly-bunny.gltf',
)

const { actions, mixer } = useAnimations(animations, model)
const currentAction = ref(actions.Greeting)
currentAction.value.play()
</script>

<template>
  <primitive :object="model" />
</template>
```

::right::

```vue
<template>
  <TresCanvas
    clear-color="”#82DBC5”"
    window-size
  >
    <TresPerspectiveCamera />
    <Suspense>
      <Model />
    </Suspense>
  </TresCanvas>
</template>
```
---
layout: text-window

---

# Consoles

Use code snippets and get the highlighting directly into a nice looking window!

::window::

```ts
// main.ts

import { createDynamicForms } from '@asigloo/vue-dynamic-forms'
import { createApp } from 'vue'

const VueDynamicForms = createDynamicForms({
  // Global Options go here
})

export const app = createApp(App)

app.use(VueDynamicForms)
```
---
layout: text-window
reverse: true
logoHeader: '/logo.svg'
eventLogo: 'https://img2.storyblok.com/352x0/f/84560/2388x414/23d8eb4b8d/vue-amsterdam-with-name.png'
eventUrl: 'https://vuejs.amsterdam/'
twitter: '@alvarosabu'
twitterUrl: 'https://twitter.com/alvarosabu'
---

# Embedded stuff

Use window to show a live demo of any page, or even a sub component!

::window::

<div class="overflow-hidden relative w-full aspect-16-9">
<iframe height="300" style="width: 100%;" scrolling="no" title="Text Clock" src="https://codepen.io/searleb/embed/pvQaJB?default-tab=html%2Cresult" frameborder="no" loading="lazy" allowtransparency="true" allowfullscreen="true">
  See the Pen <a href="https://codepen.io/searleb/pen/pvQaJB">
  Text Clock</a> by Bill Searle (<a href="https://codepen.io/searleb">@searleb</a>)
  on <a href="https://codepen.io">CodePen</a>.
</iframe>
</div>
---
class: 'grid text-center align-self-center justify-self-center'
---

# Gracias totales

[Documentations](https://sli.dev) / [GitHub Repo](https://github.com/slidevjs/slidev)
````
