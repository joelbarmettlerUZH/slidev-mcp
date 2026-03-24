import { defineConfig } from "vitepress";
import llmstxt from "vitepress-plugin-llms";

export default defineConfig({
  title: "Slidev MCP",
  description:
    "Generate, render, and host Slidev presentations from any MCP client",

  cleanUrls: true,

  head: [
    [
      "link",
      {
        rel: "icon",
        href: "https://cdn.jsdelivr.net/gh/slidevjs/slidev/assets/favicon.png",
      },
    ],
  ],

  themeConfig: {
    nav: [
      { text: "Guide", link: "/guide/what-is-slidev-mcp" },
      { text: "Clients", link: "/clients/" },
      { text: "Reference", link: "/reference/tools" },
    ],

    sidebar: [
      {
        text: "Introduction",
        items: [
          { text: "What is Slidev MCP?", link: "/guide/what-is-slidev-mcp" },
          { text: "Getting Started", link: "/guide/getting-started" },
        ],
      },
      {
        text: "MCP Clients",
        items: [
          { text: "Overview", link: "/clients/" },
          { text: "Claude Code", link: "/clients/claude-code" },
          { text: "Claude Desktop", link: "/clients/claude-desktop" },
          { text: "Cursor", link: "/clients/cursor" },
          { text: "Windsurf", link: "/clients/windsurf" },
          { text: "VS Code (Copilot)", link: "/clients/vscode" },
          { text: "JetBrains IDEs", link: "/clients/jetbrains" },
          { text: "Zed", link: "/clients/zed" },
          { text: "Opencode", link: "/clients/opencode" },
          { text: "Gemini CLI", link: "/clients/gemini-cli" },
          { text: "ChatGPT", link: "/clients/chatgpt" },
        ],
      },
      {
        text: "Reference",
        items: [
          { text: "Tools", link: "/reference/tools" },
          { text: "Resources", link: "/reference/resources" },
          { text: "Themes", link: "/reference/themes" },
          { text: "Limitations", link: "/reference/limitations" },
        ],
      },
      {
        text: "Hosting",
        items: [
          { text: "Deployment", link: "/guide/deployment" },
          { text: "Configuration", link: "/guide/configuration" },
          { text: "Contributing", link: "/contributing" },
        ],
      },
    ],

    socialLinks: [
      {
        icon: "github",
        link: "https://github.com/joelbarmettler/slidev-mcp",
      },
    ],
  },

  vite: {
    plugins: [llmstxt()],
  },
});
