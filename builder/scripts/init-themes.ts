/**
 * Generates per-theme project directories from themes.json.
 * Each theme gets its own package.json, slides.md placeholder, and bunfig.toml.
 * Run: bun run scripts/init-themes.ts
 */
import { mkdir, writeFile, copyFile } from "fs/promises";
import { join } from "path";

const ROOT = import.meta.dir.replace("/scripts", "");

interface ThemeEntry {
  package: string;
  version: string;
  license: string;
  repo: string;
  slidev_cli_version?: string; // Per-theme override
  extra_dependencies?: Record<string, string>; // Additional packages needed
}

interface ThemesConfig {
  slidev_cli_version: string; // Default Slidev version
  themes: Record<string, ThemeEntry>;
}

async function main() {
  const config: ThemesConfig = await Bun.file(join(ROOT, "themes.json")).json();
  const themesDir = join(ROOT, "themes");

  let count = 0;

  for (const [name, entry] of Object.entries(config.themes)) {
    const dir = join(themesDir, name);
    await mkdir(dir, { recursive: true });

    // Use per-theme Slidev version if specified, otherwise use the default
    const slidevVersion = entry.slidev_cli_version || config.slidev_cli_version;

    // package.json — pinned @slidev/cli + pinned theme + singlefile plugin + any extras
    const pkg = {
      name: `slidev-theme-project-${name}`,
      private: true,
      dependencies: {
        "@slidev/cli": slidevVersion,
        [entry.package]: entry.version,
        "vite-plugin-singlefile": "2.3.2",
        ...(entry.extra_dependencies || {}),
      },
    };
    await writeFile(join(dir, "package.json"), JSON.stringify(pkg, null, 2) + "\n");

    // vite.config.ts — enable single-file output (inline all JS/CSS into index.html)
    // Slidev sets manualChunks which conflicts with singlefile's inlineDynamicImports.
    // A configResolved hook removes manualChunks after all config merges.
    const viteConfig = `import { defineConfig } from "vite";
import { viteSingleFile } from "vite-plugin-singlefile";

export default defineConfig({
  plugins: [
    viteSingleFile({ useRecommendedBuildConfig: true }),
    {
      name: "force-no-manual-chunks",
      enforce: "post" as const,
      configResolved(config) {
        const output = config.build?.rollupOptions?.output;
        if (output) {
          if (Array.isArray(output)) {
            output.forEach((o: any) => { delete o.manualChunks; });
          } else {
            delete (output as any).manualChunks;
          }
        }
      },
    },
  ],
});
`;
    await writeFile(join(dir, "vite.config.ts"), viteConfig);

    // slides.md — minimal placeholder for validation builds
    const slides = [
      "---",
      `theme: ${name}`,
      "---",
      "",
      "# Test",
      "",
      `Validation slide for theme \`${name}\`.`,
      "",
    ].join("\n");
    await writeFile(join(dir, "slides.md"), slides);

    // bunfig.toml — disable lifecycle scripts
    await copyFile(join(ROOT, "bunfig.toml"), join(dir, "bunfig.toml"));

    count++;
    console.log(`  Created: themes/${name} (slidev@${slidevVersion}, ${entry.package}@${entry.version})`);
  }

  console.log(`\nGenerated ${count} theme projects in ${themesDir}`);
}

main();
