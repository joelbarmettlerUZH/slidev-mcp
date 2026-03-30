"""Theme gallery data and HTML for the MCP App viewer."""

import json

THEMES = [
    {
        "id": "default",
        "name": "Default",
        "description": "Clean, minimal theme that ships with Slidev",
        "tags": ["light", "dark", "minimalism"],
        "previews": [
            "https://cdn.jsdelivr.net/gh/slidevjs/themes@main/screenshots/theme-default/01.png",
            "https://cdn.jsdelivr.net/gh/slidevjs/themes@main/screenshots/theme-default/02.png",
            "https://cdn.jsdelivr.net/gh/slidevjs/themes@main/screenshots/theme-default/06.png",
            "https://cdn.jsdelivr.net/gh/slidevjs/themes@main/screenshots/theme-default/08.png",
        ],
    },
    {
        "id": "seriph",
        "name": "Seriph",
        "description": "Elegant theme with serif typography and subtle animations",
        "tags": ["light", "dark", "minimalism"],
        "previews": [
            "https://cdn.jsdelivr.net/gh/slidevjs/themes@main/screenshots/theme-seriph/01.png",
            "https://cdn.jsdelivr.net/gh/slidevjs/themes@main/screenshots/theme-seriph/02.png",
            "https://cdn.jsdelivr.net/gh/slidevjs/themes@main/screenshots/theme-seriph/03.png",
            "https://cdn.jsdelivr.net/gh/slidevjs/themes@main/screenshots/theme-seriph/08.png",
        ],
    },
    {
        "id": "apple-basic",
        "name": "Apple Basic",
        "description": "Apple Keynote-inspired clean presentation style",
        "tags": ["light", "dark", "minimalism"],
        "previews": [
            "https://cdn.jsdelivr.net/gh/slidevjs/themes@main/screenshots/theme-apple-basic/01.png",
            "https://cdn.jsdelivr.net/gh/slidevjs/themes@main/screenshots/theme-apple-basic/02.png",
            "https://cdn.jsdelivr.net/gh/slidevjs/themes@main/screenshots/theme-apple-basic/03.png",
            "https://cdn.jsdelivr.net/gh/slidevjs/themes@main/screenshots/theme-apple-basic/09.png",
        ],
    },
    {
        "id": "bricks",
        "name": "Bricks",
        "description": "Colorful theme with a brick-like layout pattern",
        "tags": ["light"],
        "previews": [
            "https://cdn.jsdelivr.net/gh/slidevjs/themes@main/screenshots/theme-bricks/01.png",
            "https://cdn.jsdelivr.net/gh/slidevjs/themes@main/screenshots/theme-bricks/04.png",
            "https://cdn.jsdelivr.net/gh/slidevjs/themes@main/screenshots/theme-bricks/06.png",
            "https://cdn.jsdelivr.net/gh/slidevjs/themes@main/screenshots/theme-bricks/05.png",
        ],
    },
    {
        "id": "shibainu",
        "name": "Shibainu",
        "description": "Playful theme with warm tones and rounded elements",
        "tags": ["dark"],
        "previews": [
            "https://cdn.jsdelivr.net/gh/slidevjs/themes@main/screenshots/theme-shibainu/01.png",
            "https://cdn.jsdelivr.net/gh/slidevjs/themes@main/screenshots/theme-shibainu/03.png",
            "https://cdn.jsdelivr.net/gh/slidevjs/themes@main/screenshots/theme-shibainu/04.png",
            "https://cdn.jsdelivr.net/gh/slidevjs/themes@main/screenshots/theme-shibainu/09.png",
        ],
    },
    {
        "id": "academic",
        "name": "Academic",
        "description": "Formal theme suited for academic presentations and lectures",
        "tags": ["dark", "light"],
        "previews": [
            "https://cdn.jsdelivr.net/gh/alexanderdavide/slidev-theme-academic@assets/example-export/01.png",
            "https://cdn.jsdelivr.net/gh/alexanderdavide/slidev-theme-academic@assets/example-export/02.png",
            "https://cdn.jsdelivr.net/gh/alexanderdavide/slidev-theme-academic@assets/example-export/08.png",
            "https://cdn.jsdelivr.net/gh/alexanderdavide/slidev-theme-academic@assets/example-export/04.png",
        ],
    },
    {
        "id": "cobalt",
        "name": "Cobalt",
        "description": "Deep cobalt blue color scheme with framed layouts",
        "tags": ["dark"],
        "previews": [],
    },
    {
        "id": "dracula",
        "name": "Dracula",
        "description": "Dark theme based on the popular Dracula color scheme",
        "tags": ["dark", "minimalism"],
        "previews": [
            "https://cdn.jsdelivr.net/gh/jd-solanki/slidev-theme-dracula/screenshots/screenshot-1.png",
            "https://cdn.jsdelivr.net/gh/jd-solanki/slidev-theme-dracula/screenshots/screenshot-2.png",
            "https://cdn.jsdelivr.net/gh/jd-solanki/slidev-theme-dracula/screenshots/screenshot-3.png",
            "https://cdn.jsdelivr.net/gh/jd-solanki/slidev-theme-dracula/screenshots/screenshot-4.png",
        ],
    },
    {
        "id": "eloc",
        "name": "Eloc",
        "description": "Focus on writing, present in a concise style",
        "tags": ["dark", "light"],
        "previews": [
            "https://cdn.jsdelivr.net/gh/zthxxx/slides@master/packages/slidev-theme-eloc/screenshot/01.png",
            "https://cdn.jsdelivr.net/gh/zthxxx/slides@master/packages/slidev-theme-eloc/screenshot/02.png",
            "https://cdn.jsdelivr.net/gh/zthxxx/slides@master/packages/slidev-theme-eloc/screenshot/03.png",
            "https://cdn.jsdelivr.net/gh/zthxxx/slides@master/packages/slidev-theme-eloc/screenshot/04.png",
        ],
    },
    {
        "id": "field-manual",
        "name": "Field Manual",
        "description": "Vintage US Army field manual aesthetic (1950s-1980s), 30+ layouts",
        "tags": ["light", "dark", "vintage"],
        "previews": [
            "https://raw.githubusercontent.com/pjdoland/slidev-theme-field-manual/main/screenshots/1.jpg",
            "https://raw.githubusercontent.com/pjdoland/slidev-theme-field-manual/main/screenshots/2.jpg",
            "https://raw.githubusercontent.com/pjdoland/slidev-theme-field-manual/main/screenshots/3.jpg",
            "https://raw.githubusercontent.com/pjdoland/slidev-theme-field-manual/main/screenshots/4.jpg",
        ],
    },
    {
        "id": "frankfurt",
        "name": "Frankfurt",
        "description": "Inspired by the LaTeX Beamer theme Frankfurt",
        "tags": ["dark", "light"],
        "previews": [
            "https://cdn.jsdelivr.net/gh/MuTsunTsai/slidev-theme-frankfurt/screenshots/01.png",
            "https://cdn.jsdelivr.net/gh/MuTsunTsai/slidev-theme-frankfurt/screenshots/04.png",
            "https://cdn.jsdelivr.net/gh/MuTsunTsai/slidev-theme-frankfurt/screenshots/06.png",
            "https://cdn.jsdelivr.net/gh/MuTsunTsai/slidev-theme-frankfurt/screenshots/07.png",
        ],
    },
    {
        "id": "geist",
        "name": "Vercel / Geist",
        "description": "Vercel-inspired minimalist theme with modern typography",
        "tags": ["dark", "light"],
        "previews": [
            "https://cdn.jsdelivr.net/gh/nico-bachner/slidev-theme-geist@main/example-export/01.png",
            "https://cdn.jsdelivr.net/gh/nico-bachner/slidev-theme-geist@main/example-export/02.png",
            "https://cdn.jsdelivr.net/gh/nico-bachner/slidev-theme-geist@main/example-export/03.png",
            "https://cdn.jsdelivr.net/gh/nico-bachner/slidev-theme-geist@main/example-export/04.png",
        ],
    },
    {
        "id": "neocarbon",
        "name": "Neocarbon",
        "description": "Premium dark theme with cinematic animations and glassmorphism",
        "tags": ["dark"],
        "previews": [],
    },
    {
        "id": "neversink",
        "name": "Neversink",
        "description": "Education-oriented theme with whimsical elements",
        "tags": ["light", "academic"],
        "previews": [
            "https://gureckis.github.io/slidev-theme-neversink/screenshots/2.png",
            "https://gureckis.github.io/slidev-theme-neversink/screenshots/6.png",
            "https://gureckis.github.io/slidev-theme-neversink/screenshots/8.png",
            "https://gureckis.github.io/slidev-theme-neversink/screenshots/15.png",
        ],
    },
    {
        "id": "nord",
        "name": "Nord",
        "description": "Theme based on the Nord color palette (arctic, north-bluish)",
        "tags": ["dark", "light"],
        "previews": [
            "https://raw.githubusercontent.com/oller/slidev-theme-nord/HEAD/example-export/1.png",
            "https://raw.githubusercontent.com/oller/slidev-theme-nord/HEAD/example-export/2.png",
            "https://raw.githubusercontent.com/oller/slidev-theme-nord/HEAD/example-export/3.png",
            "https://raw.githubusercontent.com/oller/slidev-theme-nord/HEAD/example-export/4.png",
        ],
    },
    {
        "id": "penguin",
        "name": "Penguin",
        "description": "Clean and professional theme with blue accents",
        "tags": ["dark", "light"],
        "previews": [
            "https://cdn.jsdelivr.net/gh/alvarosaburido/slidev-theme-penguin@master/screenshots/dark/01.png",
            "https://cdn.jsdelivr.net/gh/alvarosaburido/slidev-theme-penguin@master/screenshots/light/02.png",
            "https://cdn.jsdelivr.net/gh/alvarosaburido/slidev-theme-penguin@master/screenshots/light/06.png",
            "https://cdn.jsdelivr.net/gh/alvarosaburido/slidev-theme-penguin@master/screenshots/light/05.png",
        ],
    },
    {
        "id": "purplin",
        "name": "Purplin",
        "description": "Vibrant purple-themed design with gradient accents",
        "tags": ["dark", "light"],
        "previews": [
            "https://i.imgur.com/BX3TpEc.png",
            "https://i.imgur.com/mqqRi1F.png",
            "https://i.imgur.com/fwm2785.png",
            "https://i.imgur.com/m8eemKt.png",
        ],
    },
    {
        "id": "scholarly",
        "name": "Scholarly",
        "description": "LaTeX Beamer-style styling for scholarly presentations",
        "tags": ["academic"],
        "previews": [
            "https://raw.githubusercontent.com/jxpeng98/slidev-theme-scholarly/HEAD/images/themes/classic-blue/1.png",
            "https://raw.githubusercontent.com/jxpeng98/slidev-theme-scholarly/HEAD/images/themes/oxford/1.png",
            "https://raw.githubusercontent.com/jxpeng98/slidev-theme-scholarly/HEAD/images/themes/cambridge/1.png",
            "https://raw.githubusercontent.com/jxpeng98/slidev-theme-scholarly/HEAD/images/themes/princeton/1.png",
        ],
    },
    {
        "id": "swiss-ai-hub",
        "name": "Swiss AI Hub",
        "description": "Professional theme with Swiss AI-Hub branding and gradient backgrounds",
        "tags": ["dark"],
        "previews": [],
    },
    {
        "id": "the-unnamed",
        "name": "The Unnamed",
        "description": "Dark theme based on The unnamed VS Code theme",
        "tags": ["dark"],
        "previews": [
            "https://cdn.jsdelivr.net/gh/estruyf/slidev-theme-the-unnamed@main/assets/cover.png",
            "https://cdn.jsdelivr.net/gh/estruyf/slidev-theme-the-unnamed@main/assets/about-me.png",
            "https://cdn.jsdelivr.net/gh/estruyf/slidev-theme-the-unnamed@main/assets/default.png",
            "https://cdn.jsdelivr.net/gh/estruyf/slidev-theme-the-unnamed@main/assets/section.png",
        ],
    },
    {
        "id": "unicorn",
        "name": "Unicorn",
        "description": "Based on Dawntraoz website design with dark/light modes",
        "tags": ["dark", "light"],
        "previews": [
            "https://cdn.jsdelivr.net/gh/Dawntraoz/slidev-theme-unicorn@master/screenshots/dark-theme-intro.png",
            "https://cdn.jsdelivr.net/gh/Dawntraoz/slidev-theme-unicorn@master/screenshots/light-theme-cover.png",
            "https://cdn.jsdelivr.net/gh/Dawntraoz/slidev-theme-unicorn@master/screenshots/dark-theme-image-centered.png",
            "https://cdn.jsdelivr.net/gh/Dawntraoz/slidev-theme-unicorn@master/screenshots/dark-theme-center-without-header-footer.png",
        ],
    },
    {
        "id": "vibe",
        "name": "Vibe",
        "description": "Dark-mode theme with glassmorphism and neon accents",
        "tags": ["dark"],
        "previews": [],
    },
    {
        "id": "vuetiful",
        "name": "Vuetiful",
        "description": "A Vue-inspired theme for Slidev",
        "tags": ["dark", "light"],
        "previews": [
            "https://cdn.jsdelivr.net/gh/LinusBorg/slidev-theme-vuetiful@main/screenshots/cover-alt.png",
            "https://cdn.jsdelivr.net/gh/LinusBorg/slidev-theme-vuetiful@main/screenshots/section.png",
            "https://cdn.jsdelivr.net/gh/LinusBorg/slidev-theme-vuetiful@main/screenshots/big-points.png",
            "https://cdn.jsdelivr.net/gh/LinusBorg/slidev-theme-vuetiful@main/screenshots/quote.png",
        ],
    },
    {
        "id": "zhozhoba",
        "name": "Zhozhoba",
        "description": "A zhozhoba theme with dark/light mode support",
        "tags": ["dark", "light"],
        "previews": [
            "https://cdn.jsdelivr.net/gh/thatoranzhevyy/slidev-theme-zhozhoba@master/slides-export/01.png",
            "https://cdn.jsdelivr.net/gh/thatoranzhevyy/slidev-theme-zhozhoba@master/.github/dark.png",
            "https://cdn.jsdelivr.net/gh/thatoranzhevyy/slidev-theme-zhozhoba@master/slides-export/02.png",
            "https://cdn.jsdelivr.net/gh/thatoranzhevyy/slidev-theme-zhozhoba@master/slides-export/03.png",
        ],
    },
]


def build_gallery_html() -> str:
    """Build the theme gallery HTML with baked-in theme data."""
    themes_json = json.dumps(THEMES)
    return (
        """\
<!DOCTYPE html>
<html>
<head>
  <meta charset="utf-8">
  <meta name="color-scheme" content="light dark">
  <style>
    * { box-sizing: border-box; margin: 0; padding: 0; }
    html, body { height: auto; overflow: visible; }
    body {
      font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto,
                   Helvetica, Arial, sans-serif;
      padding: 16px; background: transparent;
    }
    h1 { font-size: 18px; margin-bottom: 12px; }
    .grid {
      display: grid;
      grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
      gap: 16px;
    }
    .card {
      border: 1px solid rgba(128,128,128,0.2);
      border-radius: 10px; overflow: hidden;
      background: rgba(128,128,128,0.05);
      transition: box-shadow 0.2s;
    }
    .card:hover { box-shadow: 0 4px 16px rgba(0,0,0,0.15); }
    .preview {
      aspect-ratio: 16/9; background: #111;
      position: relative; overflow: hidden;
    }
    .preview img {
      width: 100%; height: 100%; object-fit: cover;
      position: absolute; top: 0; left: 0;
      opacity: 0; transition: opacity 0.5s;
    }
    .preview img.active { opacity: 1; }
    .no-preview {
      width: 100%; height: 100%;
      display: flex; align-items: center; justify-content: center;
      color: rgba(255,255,255,0.3); font-size: 14px;
    }
    .info { padding: 12px; }
    .info h2 { font-size: 15px; margin-bottom: 4px; }
    .info .id { font-size: 12px; opacity: 0.5; font-family: monospace; }
    .info p { font-size: 13px; opacity: 0.7; margin: 6px 0; line-height: 1.4; }
    .tags { display: flex; gap: 4px; flex-wrap: wrap; }
    .tag {
      font-size: 11px; padding: 2px 8px;
      border-radius: 99px; background: rgba(128,128,128,0.15);
      opacity: 0.7;
    }
  </style>
</head>
<body>
  <h1 id="title">Theme Gallery</h1>
  <div class="grid" id="grid"></div>
  <script type="module">
    import { App } from
      "https://unpkg.com/@modelcontextprotocol/ext-apps@0.4.0/app-with-deps";

    const allThemes = """
        + themes_json
        + """;

    function renderThemes(themeList) {
      const grid = document.getElementById("grid");
      grid.innerHTML = "";
      // Set body min-height to 0 so ResizeObserver reports actual content height
      document.body.style.minHeight = "0";
      for (const t of themeList) {
        const card = document.createElement("div");
        card.className = "card";

        let previewHtml;
        if (t.previews.length > 0) {
          previewHtml = t.previews.map((url, i) =>
            `<img src="${url}" alt="${t.name}" class="${i === 0 ? 'active' : ''}">`
          ).join("");
        } else {
          previewHtml = `<div class="no-preview">No preview</div>`;
        }

        const tagsHtml = (t.tags || []).map(tag =>
          `<span class="tag">${tag}</span>`
        ).join("");

        card.innerHTML = `
          <div class="preview" data-theme="${t.id}">${previewHtml}</div>
          <div class="info">
            <h2>${t.name}</h2>
            <span class="id">${t.id}</span>
            <p>${t.description}</p>
            <div class="tags">${tagsHtml}</div>
          </div>
        `;
        grid.appendChild(card);
      }
    }

    // Rotate preview images every 3 seconds
    setInterval(() => {
      document.querySelectorAll(".preview").forEach(el => {
        const imgs = el.querySelectorAll("img");
        if (imgs.length < 2) return;
        const active = el.querySelector("img.active");
        if (!active) return;
        active.classList.remove("active");
        const next = active.nextElementSibling?.tagName === "IMG"
          ? active.nextElementSibling : imgs[0];
        next.classList.add("active");
      });
    }, 3000);

    const app = new App(
      { name: "Theme Gallery", version: "1.0.0" },
      {},
      { autoResize: false }
    );

    function reportSize() {
      requestAnimationFrame(() => {
        app.sendSizeChanged({
          width: document.documentElement.scrollWidth,
          height: document.documentElement.scrollHeight,
        });
      });
    }

    app.ontoolresult = ({ content }) => {
      const text = content?.find(c => c.type === "text");
      if (!text) { renderThemes(allThemes); return; }
      let data;
      try { data = JSON.parse(text.text); } catch { renderThemes(allThemes); return; }

      const filter = data.themes;
      if (filter && Array.isArray(filter) && filter.length > 0) {
        const filterSet = new Set(filter.map(s => s.toLowerCase()));
        const filtered = allThemes.filter(t => filterSet.has(t.id));
        document.getElementById("title").textContent =
          `Showing ${filtered.length} of ${allThemes.length} themes`;
        renderThemes(filtered);
      } else {
        renderThemes(allThemes);
      }

      // Report actual content size to host after rendering
      reportSize();
    };

    await app.connect();
    reportSize();
  </script>
</body>
</html>"""
    )
