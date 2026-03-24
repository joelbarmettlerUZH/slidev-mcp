export interface ThemeInfo {
  id: string
  name: string
  description: string
  previews: string[]
  repo?: string
  tags?: string[]
}

export const official: ThemeInfo[] = [
  {
    id: "default",
    name: "Default",
    description: "The minimalism default theme for Slidev",
    repo: "https://github.com/slidevjs/themes/tree/main/packages/theme-default",
    previews: [
      "https://cdn.jsdelivr.net/gh/slidevjs/themes@main/screenshots/theme-default/01.png",
      "https://cdn.jsdelivr.net/gh/slidevjs/themes@main/screenshots/theme-default/02.png",
      "https://cdn.jsdelivr.net/gh/slidevjs/themes@main/screenshots/theme-default/06.png",
      "https://cdn.jsdelivr.net/gh/slidevjs/themes@main/screenshots/theme-default/08.png",
    ],
    tags: ["minimalism", "dark", "light"],
  },
  {
    id: "seriph",
    name: "Seriph",
    description: "A more formal looking theme using Serif fonts",
    repo: "https://github.com/slidevjs/themes/tree/main/packages/theme-seriph",
    previews: [
      "https://cdn.jsdelivr.net/gh/slidevjs/themes@main/screenshots/theme-seriph/01.png",
      "https://cdn.jsdelivr.net/gh/slidevjs/themes@main/screenshots/theme-seriph/02.png",
      "https://cdn.jsdelivr.net/gh/slidevjs/themes@main/screenshots/theme-seriph/03.png",
      "https://cdn.jsdelivr.net/gh/slidevjs/themes@main/screenshots/theme-seriph/08.png",
    ],
    tags: ["minimalism", "dark", "light"],
  },
  {
    id: "apple-basic",
    name: "Apple Basic",
    description: "Inspired by the Basic Black/White theme from Apple Keynote",
    repo: "https://github.com/slidevjs/themes/tree/main/packages/theme-apple-basic",
    previews: [
      "https://cdn.jsdelivr.net/gh/slidevjs/themes@main/screenshots/theme-apple-basic/01.png",
      "https://cdn.jsdelivr.net/gh/slidevjs/themes@main/screenshots/theme-apple-basic/02.png",
      "https://cdn.jsdelivr.net/gh/slidevjs/themes@main/screenshots/theme-apple-basic/03.png",
      "https://cdn.jsdelivr.net/gh/slidevjs/themes@main/screenshots/theme-apple-basic/09.png",
    ],
    tags: ["minimalism", "dark", "light"],
  },
  {
    id: "bricks",
    name: "Bricks",
    description: "Building bricks",
    repo: "https://github.com/slidevjs/themes/tree/main/packages/theme-bricks",
    previews: [
      "https://cdn.jsdelivr.net/gh/slidevjs/themes@main/screenshots/theme-bricks/01.png",
      "https://cdn.jsdelivr.net/gh/slidevjs/themes@main/screenshots/theme-bricks/04.png",
      "https://cdn.jsdelivr.net/gh/slidevjs/themes@main/screenshots/theme-bricks/06.png",
      "https://cdn.jsdelivr.net/gh/slidevjs/themes@main/screenshots/theme-bricks/05.png",
    ],
    tags: ["light"],
  },
  {
    id: "shibainu",
    name: "Shibainu",
    description: "Meow!",
    repo: "https://github.com/slidevjs/themes/tree/main/packages/theme-shibainu",
    previews: [
      "https://cdn.jsdelivr.net/gh/slidevjs/themes@main/screenshots/theme-shibainu/01.png",
      "https://cdn.jsdelivr.net/gh/slidevjs/themes@main/screenshots/theme-shibainu/03.png",
      "https://cdn.jsdelivr.net/gh/slidevjs/themes@main/screenshots/theme-shibainu/04.png",
      "https://cdn.jsdelivr.net/gh/slidevjs/themes@main/screenshots/theme-shibainu/09.png",
    ],
    tags: ["dark"],
  },
]

export const community: ThemeInfo[] = [
  {
    id: "academic",
    name: "Academic",
    description: "Academic presentations with Slidev made simple",
    repo: "https://github.com/alexanderdavide/slidev-theme-academic",
    previews: [
      "https://cdn.jsdelivr.net/gh/alexanderdavide/slidev-theme-academic@assets/example-export/01.png",
      "https://cdn.jsdelivr.net/gh/alexanderdavide/slidev-theme-academic@assets/example-export/02.png",
      "https://cdn.jsdelivr.net/gh/alexanderdavide/slidev-theme-academic@assets/example-export/08.png",
      "https://cdn.jsdelivr.net/gh/alexanderdavide/slidev-theme-academic@assets/example-export/04.png",
    ],
    tags: ["dark", "light"],
  },
  {
    id: "geist",
    name: "Vercel / Geist",
    description: "A theme based on Vercel's design system",
    repo: "https://github.com/nico-bachner/slidev-theme-geist",
    previews: [
      "https://cdn.jsdelivr.net/gh/nico-bachner/slidev-theme-geist@main/example-export/01.png",
      "https://cdn.jsdelivr.net/gh/nico-bachner/slidev-theme-geist@main/example-export/02.png",
      "https://cdn.jsdelivr.net/gh/nico-bachner/slidev-theme-geist@main/example-export/03.png",
      "https://cdn.jsdelivr.net/gh/nico-bachner/slidev-theme-geist@main/example-export/04.png",
    ],
    tags: ["dark", "light"],
  },
  {
    id: "light-icons",
    name: "Light Icons",
    description: "A simple, light and elegant theme with creative layouts and custom components",
    repo: "https://github.com/lightvue/slidev-theme-light-icons",
    previews: [
      "https://cdn.jsdelivr.net/gh/lightvue/slidev-theme-light-icons@master/screenshot/1-layout-intro.png",
      "https://cdn.jsdelivr.net/gh/lightvue/slidev-theme-light-icons@master/screenshot/2-layout-image-header-intro-light.png",
      "https://cdn.jsdelivr.net/gh/lightvue/slidev-theme-light-icons@master/screenshot/3-layout-dynamic-image-light.png",
      "https://cdn.jsdelivr.net/gh/lightvue/slidev-theme-light-icons@master/screenshot/5-layout-dynamic-image-light.png",
    ],
    tags: ["dark", "light"],
  },
  {
    id: "neversink",
    name: "Neversink",
    description: "Education and academia oriented theme with whimsical elements",
    repo: "https://github.com/gureckis/slidev-theme-neversink",
    previews: [
      "https://gureckis.github.io/slidev-theme-neversink/screenshots/2.png",
      "https://gureckis.github.io/slidev-theme-neversink/screenshots/6.png",
      "https://gureckis.github.io/slidev-theme-neversink/screenshots/8.png",
      "https://gureckis.github.io/slidev-theme-neversink/screenshots/15.png",
    ],
    tags: ["light", "academic"],
  },
  {
    id: "penguin",
    name: "Penguin",
    description: "A Penguin theme for Slidev",
    repo: "https://github.com/alvarosabu/slidev-theme-penguin",
    previews: [
      "https://cdn.jsdelivr.net/gh/alvarosaburido/slidev-theme-penguin@master/screenshots/dark/01.png",
      "https://cdn.jsdelivr.net/gh/alvarosaburido/slidev-theme-penguin@master/screenshots/light/02.png",
      "https://cdn.jsdelivr.net/gh/alvarosaburido/slidev-theme-penguin@master/screenshots/light/06.png",
      "https://cdn.jsdelivr.net/gh/alvarosaburido/slidev-theme-penguin@master/screenshots/light/05.png",
    ],
    tags: ["dark", "light"],
  },
  {
    id: "purplin",
    name: "Purplin",
    description: "Theme with bar bottom component, based on purple color",
    repo: "https://github.com/moudev/slidev-theme-purplin",
    previews: [
      "https://i.imgur.com/BX3TpEc.png",
      "https://i.imgur.com/mqqRi1F.png",
      "https://i.imgur.com/fwm2785.png",
      "https://i.imgur.com/m8eemKt.png",
    ],
    tags: ["dark", "light"],
  },
  {
    id: "the-unnamed",
    name: "The Unnamed",
    description: "A theme based on The unnamed VS Code theme",
    repo: "https://github.com/estruyf/slidev-theme-the-unnamed",
    previews: [
      "https://cdn.jsdelivr.net/gh/estruyf/slidev-theme-the-unnamed@main/assets/cover.png",
      "https://cdn.jsdelivr.net/gh/estruyf/slidev-theme-the-unnamed@main/assets/about-me.png",
      "https://cdn.jsdelivr.net/gh/estruyf/slidev-theme-the-unnamed@main/assets/default.png",
      "https://cdn.jsdelivr.net/gh/estruyf/slidev-theme-the-unnamed@main/assets/section.png",
    ],
    tags: ["dark"],
  },
  {
    id: "nord",
    name: "Nord",
    description: "Based on the Nord color palette",
    repo: "https://github.com/oller/slidev-theme-nord",
    previews: [
      "https://raw.githubusercontent.com/oller/slidev-theme-nord/HEAD/example-export/1.png",
      "https://raw.githubusercontent.com/oller/slidev-theme-nord/HEAD/example-export/2.png",
      "https://raw.githubusercontent.com/oller/slidev-theme-nord/HEAD/example-export/3.png",
      "https://raw.githubusercontent.com/oller/slidev-theme-nord/HEAD/example-export/4.png",
    ],
    tags: ["dark", "light"],
  },
  {
    id: "scholarly",
    name: "Scholarly",
    description: "LaTeX Beamer-style styling for scholarly presentations",
    repo: "https://github.com/jxpeng98/slidev-theme-scholarly",
    previews: [
      "https://raw.githubusercontent.com/jxpeng98/slidev-theme-scholarly/HEAD/images/themes/classic-blue/1.png",
      "https://raw.githubusercontent.com/jxpeng98/slidev-theme-scholarly/HEAD/images/themes/oxford/1.png",
      "https://raw.githubusercontent.com/jxpeng98/slidev-theme-scholarly/HEAD/images/themes/cambridge/1.png",
      "https://raw.githubusercontent.com/jxpeng98/slidev-theme-scholarly/HEAD/images/themes/princeton/1.png",
    ],
    tags: ["academic"],
  },
  {
    id: "field-manual",
    name: "Field Manual",
    description: "A 24-layout theme modeled on vintage military field manuals",
    repo: "https://github.com/pjdoland/slidev-theme-field-manual",
    previews: [
      "https://raw.githubusercontent.com/pjdoland/slidev-theme-field-manual/main/screenshots/1.jpg",
      "https://raw.githubusercontent.com/pjdoland/slidev-theme-field-manual/main/screenshots/2.jpg",
      "https://raw.githubusercontent.com/pjdoland/slidev-theme-field-manual/main/screenshots/3.jpg",
      "https://raw.githubusercontent.com/pjdoland/slidev-theme-field-manual/main/screenshots/4.jpg",
    ],
    tags: ["light", "dark", "vintage"],
  },
]

// Themes that are installed but don't have upstream preview screenshots
export const additional: { id: string; name: string; description: string }[] = [
  { id: "ehl2022", name: "EHL 2022", description: "EHL China default presentation template with UnoCSS" },
  { id: "cobalt", name: "Cobalt", description: "Deep cobalt blue color scheme with framed layouts" },
  { id: "meetup", name: "Meetup", description: "Theme designed for meetup and conference talks" },
  { id: "nmt", name: "NMT", description: "Theme based on The unnamed VS Code theme by Elio Struyf" },
  { id: "nearform", name: "NearForm", description: "NearForm corporate theme for technical presentations" },
  { id: "mistica", name: "Mistica", description: "Telefonica Mistica design system theme" },
  { id: "alchemmist", name: "Alchemmist", description: "Alchemmist-styled presentation theme" },
  { id: "whulug", name: "WHULUG", description: "Community theme with a clean, modern aesthetic" },
  { id: "one-purple-unicorn-pro", name: "One Purple Unicorn Pro", description: "Purple/indigo focused with clean macOS style" },
  { id: "vibe", name: "Vibe", description: "Dark-mode theme with glassmorphism and neon accents" },
  { id: "greycat", name: "GreyCat", description: "GreyCat-branded data-centric theme" },
  { id: "neocarbon", name: "Neocarbon", description: "Premium dark theme with cinematic animations and glass morphism" },
  { id: "umn", name: "UMN", description: "Theme inspired by University of Minnesota branding" },
  { id: "scorpion", name: "Scorpion", description: "Scorpion-styled presentation theme" },
  { id: "ucsf", name: "UCSF", description: "UCSF-inspired presentation theme" },
  { id: "dataerai", name: "DataErai", description: "Data-focused professional theme" },
  { id: "measurelab", name: "Measurelab", description: "Measurelab branded analytics presentation theme" },
  { id: "academic-schober", name: "Academic Schober", description: "Academic presentations variant with personal styling" },
  { id: "swiss-ai-hub", name: "Swiss AI Hub", description: "Professional theme with Swiss AI-Hub branding" },
]
