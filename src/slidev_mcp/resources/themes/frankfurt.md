# slidev-theme-frankfurt

[![NPM version](https://img.shields.io/npm/v/slidev-theme-frankfurt?color=3AB9D4&label=)](https://www.npmjs.com/package/slidev-theme-frankfurt)

A theme for [Slidev](https://github.com/slidevjs/slidev),
inspired by the Frankfurt theme in [Beamer](https://github.com/josephwright/beamer),
well-suited for academic talks.

![](screenshots/01.png)

## Install

Add the following frontmatter to your `slides.md`.
Start Slidev and then it will prompt you to install the theme automatically.

```yaml
---
theme: frankfurt
infoLine: true # on by default, can be turned off
author: 'Your name here' # shows in infoLine
title: 'Title' # shows in infoLine
date: '2023/01/01' # shows in infoLine, defaults to the current date
---
```

Learn more about [how to use a theme](https://sli.dev/guide/theme-addon#use-theme).

## Using sections

The main feature of Frankfurt theme is the section and progress indicators on top.
To divide your slides into sections,
add the following frontmatter to the first page of each section:

```yaml
---
section: 'Section title'
---
```

## Components

This theme provides the following component:

```html
<Item title="Title of your thing">
	Create a box for definitions, lemmas, theorems, etc.
</Item>
```

![](screenshots/06.png)

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
colorSchema: auto
author: Mu-Tsun Tsai
date: 2023/01/01
transition: slide-left
---

# Slidev Theme Frankfurt

Presentation slides for developers

<div class="pt-12">
  <span @click="next" class="px-2 p-1 rounded cursor-pointer hover:bg-white hover:bg-opacity-10">
    Press Space for next page <carbon:arrow-right class="inline"/>
  </span>
</div>

---
section: Introduction
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


---

# Navigation

Hover on the bottom-left corner to see the navigation's controls panel

## Keyboard Shortcuts

|     |     |
| --- | --- |
| <kbd>space</kbd> / <kbd>tab</kbd> / <kbd>right</kbd> | next animation or slide |
| <kbd>left</kbd>  / <kbd>shift</kbd><kbd>space</kbd> | previous animation or slide |
| <kbd>up</kbd> | previous slide |
| <kbd>down</kbd> | next slide |

---
layout: image-right
image: 'https://source.unsplash.com/collection/94734566/1920x1080'
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
  const newUser = { ...user, ...update }
  saveUser(id, newUser)
}
```

---
section: Frankfurt
src: section.md
---

---
section: Final words
layout: center
class: "text-center"
---

# Learn More

[Documentations](https://sli.dev) / [GitHub Repo](https://github.com/slidevjs/slidev)
````
