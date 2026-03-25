/**
 * Validates that every theme can actually build a slide deck.
 * Run during Docker image build to catch broken themes early.
 * Usage: bun run scripts/validate-themes.ts [--remove-broken]
 *
 * With --remove-broken: removes themes that fail to build (for CI).
 * Without: exits non-zero if any theme fails (for local dev).
 */
import { readdir, rm } from "fs/promises";
import { join } from "path";
import { existsSync } from "fs";

const ROOT = import.meta.dir.replace("/scripts", "");
const THEMES_DIR = join(ROOT, "themes");
const removeBroken = process.argv.includes("--remove-broken");

interface Result {
  theme: string;
  success: boolean;
  duration: number;
  error?: string;
}

async function validateTheme(name: string): Promise<Result> {
  const themeDir = join(THEMES_DIR, name);
  const outDir = join(themeDir, "dist-test");
  const start = Date.now();

  try {
    const proc = Bun.spawn(
      ["bunx", "slidev", "build", "--base", `/test/${name}/`, "--out", outDir],
      {
        cwd: themeDir,
        stdout: "pipe",
        stderr: "pipe",
      }
    );

    const exitCode = await proc.exited;
    const duration = (Date.now() - start) / 1000;

    if (exitCode !== 0) {
      const stderr = await new Response(proc.stderr).text();
      return { theme: name, success: false, duration, error: stderr.slice(-500) };
    }

    // Check that index.html was produced
    if (!existsSync(join(outDir, "index.html"))) {
      return { theme: name, success: false, duration, error: "No index.html in output" };
    }

    return { theme: name, success: true, duration };
  } catch (err: any) {
    return { theme: name, success: false, duration: (Date.now() - start) / 1000, error: err.message };
  } finally {
    // Clean up test output
    if (existsSync(outDir)) {
      await rm(outDir, { recursive: true, force: true });
    }
  }
}

async function main() {
  const entries = await readdir(THEMES_DIR, { withFileTypes: true });
  const themes = entries.filter((e) => e.isDirectory()).map((e) => e.name).sort();

  console.log(`Validating ${themes.length} themes...\n`);

  const results: Result[] = [];

  // Run sequentially to avoid resource contention
  for (const theme of themes) {
    const result = await validateTheme(theme);
    const icon = result.success ? "OK" : "FAIL";
    console.log(`  [${icon}] ${theme} (${result.duration.toFixed(1)}s)`);
    if (!result.success && result.error) {
      console.log(`         ${result.error.split("\n").pop()}`);
    }
    results.push(result);
  }

  const passed = results.filter((r) => r.success);
  const failed = results.filter((r) => !r.success);

  console.log(`\n${passed.length} passed, ${failed.length} failed\n`);

  if (failed.length > 0 && removeBroken) {
    console.log("Removing broken themes:");
    for (const r of failed) {
      const themeDir = join(THEMES_DIR, r.theme);
      await rm(themeDir, { recursive: true, force: true });
      console.log(`  Removed: ${r.theme}`);
    }
    // Write the validated theme list
    const validThemes = passed.map((r) => r.theme);
    await Bun.write(
      join(ROOT, "validated-themes.json"),
      JSON.stringify(validThemes, null, 2) + "\n"
    );
    console.log(`\nWrote validated-themes.json with ${validThemes.length} themes`);
  } else if (failed.length > 0) {
    process.exit(1);
  }
}

main();
