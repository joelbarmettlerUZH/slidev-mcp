# Slidev Theme Geist

The [Vercel](https://vercel.com) theme for [Slidev](https://github.com/slidevjs/slidev). Based on [Vercel's design system](https://vercel.com/design)

[Demo](https://slidev-theme-geist-demo.vercel.app) | [Documentation](https://slidev-theme-geist-docs.vercel.app) | [Contribution Guide](CONTRIBUTING.md)

[![NPM version](https://img.shields.io/npm/v/slidev-theme-geist)](https://www.npmjs.com/package/slidev-theme-geist)

## Screenshots

![Slide demo with cover page](/example-export/01.png)
![Slide demo with list](/example-export/02.png)
![Slide demo with table](/example-export/03.png)
![Slide demo with code](/example-export/04.png)
![Slide demo with geist components](/example-export/05.png)


---

# Example Slides

The following is the theme's example presentation showing available layouts, components, and features:

````markdown
---
theme: ./
highlighter: shiki
---

# Slidev Theme Geist

The Vercel theme for Slidev

<div class="pt-24">
  Press <KBD>space</KBD> to go to the next page ->
</div>

---

# What is Slidev?

Slidev is a slides maker and presenter designed for developers, consist of the following features

-   📝 **Text-based** - focus on the content with Markdown, and then style them later
-   🎨 **Themeable** - theme can be shared and used with npm packages
-   🧑‍💻 **Developer Friendly** - code highlighting, live coding with autocompletion
-   🤹 **Interactive** - embedding Vue components to enhance your expressions
-   🎥 **Recording** - built-in recording and camera view
-   📤 **Portable** - export into PDF, PNGs, or even a hostable SPA
-   🛠 **Hackable** - anything possible on a webpage

Read more about [Slidev](https://sli.dev)

---

# Navigation

Hover over the bottom-left corner of your screen to see the control panel.

### Keyboard Shortcuts

| shortcut                                             | purpose                     |
| ---------------------------------------------------- | --------------------------- |
| <KBD>space</KBD> / <KBD>tab</KBD> / <KBD>right</KBD> | next animation or slide     |
| <KBD>left</KBD>                                      | previous animation or slide |
| <KBD>up</KBD>                                        | previous slide              |
| <KBD>down</KBD>                                      | next slide                  |

---

# Code

Use `code` snippets and get automatic highlighting!

```ts
// type
interface User {
    id: number;
    firstName: string;
    lastName: string;
    role: string;
}

// function
function updateUser(id: number, update: Partial<User>) {
    const user = getUser(id);
    const newUser = { ...user, ...update };
    saveUser(id, newUser);
}
```

---

# Theme Components

## Button

<Button>Button</Button>

## Keyboard Input

<KBD command shift>P</KBD>

## Note

<Note>Note</Note>

---

# Learn More

[Documentation](https://sli.dev) / [GitHub Repository](https://github.com/slidevjs/slidev)
````
