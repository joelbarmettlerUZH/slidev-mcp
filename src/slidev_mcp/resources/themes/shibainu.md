# @slidev/theme-shibainu

[![NPM version](https://img.shields.io/npm/v/@slidev/theme-shibainu?color=3AB9D4&label=)](https://www.npmjs.com/package/@slidev/theme-shibainu)

Shibainu theme for [Slidev](https://github.com/slidevjs/slidev).

## Install

Add the following frontmatter to your `slides.md`. Start Slidev then it will prompt you to install the theme automatically.

<pre><code>---
theme: <b>shibainu</b>
---</code></pre>

Learn more about [how to use a theme](https://sli.dev/themes/use).

## Layouts

### `cover`

![](https://cdn.jsdelivr.net/gh/slidevjs/themes@main/screenshots/theme-shibainu/01.png)

### `default`

![](https://cdn.jsdelivr.net/gh/slidevjs/themes@main/screenshots/theme-shibainu/02.png)

### `center`

![](https://cdn.jsdelivr.net/gh/slidevjs/themes@main/screenshots/theme-shibainu/03.png)

### `section`

![](https://cdn.jsdelivr.net/gh/slidevjs/themes@main/screenshots/theme-shibainu/04.png)

### `default-2`

![](https://cdn.jsdelivr.net/gh/slidevjs/themes@main/screenshots/theme-shibainu/05.png)

### `default-3`

![](https://cdn.jsdelivr.net/gh/slidevjs/themes@main/screenshots/theme-shibainu/06.png)

### `right`

![](https://cdn.jsdelivr.net/gh/slidevjs/themes@main/screenshots/theme-shibainu/07.png)

### `section-2`

![](https://cdn.jsdelivr.net/gh/slidevjs/themes@main/screenshots/theme-shibainu/08.png)

### `default-4`

![](https://cdn.jsdelivr.net/gh/slidevjs/themes@main/screenshots/theme-shibainu/09.png)

### `default-5`

![](https://cdn.jsdelivr.net/gh/slidevjs/themes@main/screenshots/theme-shibainu/10.png)

### `default-6`

![](https://cdn.jsdelivr.net/gh/slidevjs/themes@main/screenshots/theme-shibainu/11.png)

### `default-7`

![](https://cdn.jsdelivr.net/gh/slidevjs/themes@main/screenshots/theme-shibainu/12.png)

### `section-3`

![](https://cdn.jsdelivr.net/gh/slidevjs/themes@main/screenshots/theme-shibainu/13.png)

### `quote`

![](https://cdn.jsdelivr.net/gh/slidevjs/themes@main/screenshots/theme-shibainu/14.png)

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
layout: cover
---

# Presentation title

Presentation subtitle

---

# Layout `default`

Slide Subtitle

* Slide bullet text
  * Slide bullet text
  * Slide bullet text
* Slide bullet text
* Slide bullet text

---
layout: center
---

# Layout `center`

Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.

---
layout: section
---

# Layout `section`

---
layout: default-2
---

# Layout `default-2`

Colons can be used to align columns.

| Tables        | Are           | Cool  |
| ------------- |:-------------:| -----:|
| col 3 is      | right-aligned | $1600 |
| col 2 is      | centered      |   $12 |
| zebra stripes | are neat      |    $1 |

---
layout: default-3
class: 'grid text-center h-full content-center'
---

<div class="grid grid-cols-3 gap-4 text-center w-140 m-auto">

<div class="m-auto w-35 h-35 rounded-full bg-[#bf926b]"></div>
<div class="m-auto w-35 h-35 rounded-full bg-[#bf926b]"></div>
<div class="m-auto w-35 h-35 rounded-full bg-[#bf926b]"></div>

<div>Lorem</div>
<div>Ipsum</div>
<div>Dolor</div>

</div>

<br>

Layout `default-3`

---
layout: right
---

# Layout `right`

Lorem ipsum dolor sit amet, consectetur adipiscing elit.

Sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.

---
layout: section-2
---

# Section 2

---
layout: default-4
---

# Layout `default-4`

Lorem ipsum dolor sit amet, consectetur adipiscing elit.

Sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.

---
layout: default-5
---

# Layout `default-5`

Lorem ipsum dolor sit amet, consectetur adipiscing elit.

Sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.

---
layout: default-6
---

# Layout `default-6`

Lorem ipsum dolor sit amet, consectetur adipiscing elit.

Sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.

---
layout: default-7
---

# Layout `default-7`

Lorem ipsum dolor sit amet, consectetur adipiscing elit.

Sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.

---
layout: section-3
---

# Section 3

---
layout: quote
---

# Thanks
````
