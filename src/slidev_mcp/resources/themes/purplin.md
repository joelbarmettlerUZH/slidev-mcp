# slidev-theme-purplin

[![NPM version](https://img.shields.io/npm/v/slidev-theme-purplin?color=3AB9D4&label=)](https://www.npmjs.com/package/slidev-theme-purplin)

[![Netlify Status](https://api.netlify.com/api/v1/badges/c011b5f3-5d1f-4c16-a1df-929b1e503724/deploy-status)](https://app.netlify.com/sites/slidev-theme-purplin/deploys)

A (...) theme for [Slidev](https://github.com/slidevjs/slidev).

<!--
run `npm run dev` to check out the slides for more details of how to start writing a theme
-->

<!--
put some screenshots here to demonstrate your theme,
-->

Live demo: https://slidev-theme-purplin.netlify.app/

## Install

Add the following frontmatter to your `slides.md`. Start Slidev then it will prompt you to install the theme automatically.

<pre><code>---
theme: <b>purplin</b>
---</code></pre>

Learn more about [how to use a theme](https://sli.dev/themes/use).

## Layouts

This theme provides the following layouts:

### quote

Usage:

```markdown
---
layout: quote
position: center
---

# "layout: quote"
position: center

'position' variants: left (default), center, right
```

![quote-layout](https://user-images.githubusercontent.com/13499566/118434542-dd60d500-b6a2-11eb-9f4e-1759abe19349.png)

---

### image-x

Usage:

```markdown
---
layout: image-x
image: 'https://source.unsplash.com/collection/94734566/600x600'
imageOrder: 1
---

# layout: image-x

imageOrder: 1

image 600x600
```

![image-x-1](https://user-images.githubusercontent.com/13499566/118434655-07b29280-b6a3-11eb-902c-3b142d57a770.png)

```markdown
---
layout: image-x
image: 'https://source.unsplash.com/collection/94734566/1080x1920'
imageOrder: 2
---

# layout: image-x

imageOrder: 2

image 1080x1920
```

![image-x-2](https://user-images.githubusercontent.com/13499566/118434696-1a2ccc00-b6a3-11eb-9655-e740b330b2de.png)

## Components

This theme provides the following components:

### `<BarBottom />`

This component displays a bar at the bottom of the slide.

The component needs to be added to each slide where we want to display it.

Receives a `title` prop that is the text displayed on the left.

This component uses `slots` to add items on the right. Exist an `<Item />` component that receives a `text` prop and uses `slots` to add the icon/image.

Exist a large [list of icon collections](https://icones.js.org/collection) available that you can use. These icons are imported automatically by _slidev_, you don't need to configure anything else to use them.

Usage:

```markdown
---
layout: intro
---

# Slidev Theme Purplin

Presentation slides for developers

<div class="pt-12">
  <span @click="next" class="px-2 p-1 rounded cursor-pointer hover:bg-white hover:bg-opacity-10">
    Press Space for next page <carbon:arrow-right class="inline"/>
  </span>
</div>

<BarBottom  title="Slidev theme purplin">
  <Item text="slidevjs/slidev">
    <carbon:logo-github />
  </Item>
  <Item text="Slidevjs">
    <carbon:logo-twitter />
  </Item>
  <Item text="sli.dev">
    <carbon:link />
  </Item>
</BarBottom>
```

This example uses [carbon collection](https://icones.js.org/collection/carbon).

![barBottom-component](https://user-images.githubusercontent.com/13499566/118434724-287ae800-b6a3-11eb-8e7c-b52d5765245a.png)

**How to use other available icons**

You have to go to the [icon list](https://icones.js.org/collection) and select a collection, click on an icon a copy its name. You don't need to do anything else, only copy the name and use an `<Item />` component and the icon will be automatically imported from the collections.

**How to use custom icon/image**

You can use your own icons/images if you want, you only need to add an `<Item />` component and use `slots` features.

Also, you can use [Windi CSS](https://windicss.org/) to add style to the icon, for example, adjust the width o height.

Usage:

```markdown
---
layout: intro
---

# Slidev Theme Purplin

Presentation slides for developers

<div class="pt-12">
  <span @click="next" class="px-2 p-1 rounded cursor-pointer hover:bg-white hover:bg-opacity-10">
    Press Space for next page <carbon:arrow-right class="inline"/>
  </span>
</div>

<BarBottom  title="Slidev theme purplin">
  <Item text="slidevjs/slidev">
    <carbon:logo-github />
  </Item>
  <Item text="Slidevjs">
    <carbon:logo-twitter />
  </Item>
  <Item text="sli.dev">
    <img
      src="https://d33wubrfki0l68.cloudfront.net/273aa82ec83b3e4357492a201fb68048af1c3e6a/8f657/logo.svg"
      class="w-4"
    />
  </Item>
</BarBottom>
```

![barBottom-component](https://user-images.githubusercontent.com/13499566/139119534-4398a2ff-4f83-4282-9d12-bf5f27b99174.png)

## Contributing

- `npm install`
- `npm run dev` to start theme preview of `example.md`
- Edit the `example.md` and style to see the changes
- `npm run export` to genreate the preview PDF
- `npm run screenshot` to genrate the preview PNG


---

# Example Slides

The following is the theme's example presentation showing available layouts, components, and features:

````markdown
---
# replace "./" with "purplin"
# when you copy this example.md file over
# to your own slidev environment and install
# purplin as a module
theme: ./
---

# Slidev Theme Purplin

Presentation slides for developers

<div class="pt-12">
  <span @click="next" class="px-2 p-1 rounded cursor-pointer hover:bg-white hover:bg-opacity-10">
    Press Space for next page <carbon:arrow-right class="inline"/>
  </span>
</div>

<BarBottom  title="Slidev theme purplin">
  <Item text="slidevjs/slidev">
    <carbon:logo-github />
  </Item>
  <Item text="Slidevjs">
    <carbon:logo-twitter />
  </Item>
  <Item text="sli.dev">
    <carbon:link />
  </Item>
</BarBottom>

---
layout: intro
---

## `<BarBottom />` component

<br />
<br />

<div class="grid grid-cols-2 gap-x-4">
<div>
This component displays a bar at the bottom of the slide. The component needs to be added to each slide where we want to display it.

Receives a `title` prop that is the text displayed on the left.

This component uses `slots` to add items on the right. Exist an `<Item />` component that receives a `text` prop and uses `slots` to add the icon/image.

Exist a large [list of icon collections](https://icones.js.org/collection) available that you can use. These icons are imported automatically by _slidev_, you don't need to configure anything else to use them.

</div>
<div>

### Slide example

```markdown
---
layout: intro
---

# Content

<BarBottom  title="Slidev theme purplin">
  <Item text="slidevjs/slidev">
    <carbon:logo-github />
  </Item>
  <Item text="Slidevjs">
    <carbon:logo-twitter />
  </Item>
  <Item text="sli.dev">
    <carbon:link />
  </Item>
</BarBottom>
```

</div>
</div>

<BarBottom  title="Slidev theme purplin">
  <Item text="slidevjs/slidev">
    <carbon:logo-github />
  </Item>
  <Item text="Slidevjs">
    <carbon:logo-twitter />
  </Item>
  <Item text="sli.dev">
    <carbon:link />
  </Item>
</BarBottom>

---
layout: intro
---

## `<BarBottom />` with custom icons/images

<br />
<br />

<div class="grid grid-cols-2 gap-x-4">
<div>

You can use your own icons/images if you want.

Only need to add an `<Item />` component and use `slots` features.

Also, you can use [Windi CSS](https://windicss.org/) to add style to the icon, for example, adjust the width o height.

</div>
<div>

### Slide example

```markdown
---
layout: intro
---

# Content

<BarBottom  title="Slidev theme purplin">
  <Item text="slidevjs/slidev">
    <carbon:logo-github />
  </Item>
  <Item text="Slidevjs">
    <carbon:logo-twitter />
  </Item>
  <Item text="sli.dev">
    <img
      src="https://d33wubrfki0l68.cloudfront.net/273aa82ec83b3e4357492a201fb68048af1c3e6a/8f657/logo.svg"
      class="w-4"
    />
  </Item>
</BarBottom>
```

</div>
</div>

<BarBottom  title="Slidev theme purplin">
  <Item text="slidevjs/slidev">
    <carbon:logo-github />
  </Item>
  <Item text="Slidevjs">
    <carbon:logo-twitter />
  </Item>
  <Item text="sli.dev">
    <img
      src="https://d33wubrfki0l68.cloudfront.net/273aa82ec83b3e4357492a201fb68048af1c3e6a/8f657/logo.svg"
      class="w-4"
    />
  </Item>
</BarBottom>

---
layout: image-x
image: 'https://user-images.githubusercontent.com/13499566/138951075-018e65d5-b5fe-4200-9ea7-34315b1764da.jpg'
imageOrder: 1
---

# layout: image-x

imageOrder: 1

image 600x600

<BarBottom  title="Slidev theme purplin">
  <Item text="slidevjs/slidev">
    <carbon:logo-github />
  </Item>
  <Item text="Slidevjs">
    <carbon:logo-twitter />
  </Item>
  <Item text="sli.dev">
    <carbon:link />
  </Item>
</BarBottom>

---
layout: image-x
image: 'https://user-images.githubusercontent.com/13499566/138950866-7d2addb2-fe3f-41f5-aab6-d35688516612.jpg'
imageOrder: 2
---

# layout: image-x

imageOrder: 2

image 1080x1920

<BarBottom  title="Slidev theme purplin">
  <Item text="slidevjs/slidev">
    <carbon:logo-github />
  </Item>
  <Item text="Slidevjs">
    <carbon:logo-twitter />
  </Item>
  <Item text="sli.dev">
    <carbon:link />
  </Item>
</BarBottom>

---
layout: quote
position: center
---

# "layout: quote"
position: center

'position' variants: left (default), center, right

<BarBottom  title="Slidev theme purplin">
  <Item text="slidevjs/slidev">
    <carbon:logo-github />
  </Item>
  <Item text="Slidevjs">
    <carbon:logo-twitter />
  </Item>
  <Item text="sli.dev">
    <carbon:link />
  </Item>
</BarBottom>

---

# What is Slidev?

Slidev is a slides maker and presenter designed for developers, consist of the following features
  
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

<BarBottom  title="Slidev theme purplin">
  <Item text="slidevjs/slidev">
    <carbon:logo-github />
  </Item>
  <Item text="Slidevjs">
    <carbon:logo-twitter />
  </Item>
  <Item text="sli.dev">
    <carbon:link />
  </Item>
</BarBottom>

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

<BarBottom  title="Slidev theme purplin">
  <Item text="slidevjs/slidev">
    <carbon:logo-github />
  </Item>
  <Item text="Slidevjs">
    <carbon:logo-twitter />
  </Item>
  <Item text="sli.dev">
    <carbon:link />
  </Item>
</BarBottom>

---
layout: image-right
image: 'https://user-images.githubusercontent.com/13499566/138950614-52ec045b-aa93-4d52-91df-b782cc9c7143.jpg'
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

<BarBottom  title="Slidev theme purplin">
  <Item text="slidevjs/slidev">
    <carbon:logo-github />
  </Item>
  <Item text="Slidevjs">
    <carbon:logo-twitter />
  </Item>
  <Item text="sli.dev">
    <carbon:link />
  </Item>
</BarBottom>

---
layout: center
class: "text-center"
---

# Learn More

[Documentations](https://sli.dev) / [GitHub Repo](https://github.com/slidevjs/slidev)

<BarBottom  title="Slidev theme purplin">
  <Item text="slidevjs/slidev">
    <carbon:logo-github />
  </Item>
  <Item text="Slidevjs">
    <carbon:logo-twitter />
  </Item>
  <Item text="sli.dev">
    <carbon:link />
  </Item>
</BarBottom>
````
