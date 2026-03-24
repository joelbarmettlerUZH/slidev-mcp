import { copyFile, mkdir, readdir, readFile, rm, writeFile } from "fs/promises";
import { join } from "path";
import { existsSync } from "fs";

interface BuildManifest {
  theme: string;
  uuid: string;
  base_path: string;
}

async function copyDir(src: string, dest: string): Promise<void> {
  await mkdir(dest, { recursive: true });
  const entries = await readdir(src, { withFileTypes: true });
  for (const entry of entries) {
    const srcPath = join(src, entry.name);
    const destPath = join(dest, entry.name);
    if (entry.isDirectory()) {
      await copyDir(srcPath, destPath);
    } else {
      await copyFile(srcPath, destPath);
    }
  }
}

async function main(): Promise<void> {
  const buildDir = process.argv[2];
  if (!buildDir) {
    console.error("Usage: build-job.ts <build-directory>");
    process.exit(1);
  }

  const manifestPath = join(buildDir, "build-manifest.json");
  const slidesPath = join(buildDir, "slides.md");
  const workDir = join(buildDir, "work");
  const distDir = join(buildDir, "dist");

  try {
    // Read manifest
    const manifestRaw = await readFile(manifestPath, "utf-8");
    const manifest: BuildManifest = JSON.parse(manifestRaw);

    // Read user slides
    const slidesContent = await readFile(slidesPath, "utf-8");

    // Copy template into work directory
    const templateDir = "/app/template";
    await copyDir(templateDir, workDir);

    // Patch theme into frontmatter and write slides
    const themedSlides = patchTheme(slidesContent, manifest.theme);
    await writeFile(join(workDir, "slides.md"), themedSlides, "utf-8");

    // Symlink node_modules from the app root so slidev can find themes
    const nodeModulesSrc = "/app/node_modules";
    const nodeModulesDest = join(workDir, "node_modules");
    if (!existsSync(nodeModulesDest)) {
      await Bun.spawn(["ln", "-s", nodeModulesSrc, nodeModulesDest]).exited;
    }

    // Run slidev build
    const proc = Bun.spawn(
      [
        "bunx",
        "slidev",
        "build",
        "--base",
        manifest.base_path,
        "--out",
        distDir,
      ],
      {
        cwd: workDir,
        stdout: "inherit",
        stderr: "inherit",
      }
    );

    const exitCode = await proc.exited;

    if (exitCode !== 0) {
      const errorInfo = {
        exit_code: exitCode,
        stderr: `Build exited with code ${exitCode}`,
      };
      await writeFile(
        join(buildDir, "error.json"),
        JSON.stringify(errorInfo),
        "utf-8"
      );
      process.exit(exitCode);
    }
  } catch (err: any) {
    const errorInfo = {
      exit_code: 1,
      stderr: err.message || String(err),
    };
    await writeFile(
      join(buildDir, "error.json"),
      JSON.stringify(errorInfo),
      "utf-8"
    );
    process.exit(1);
  } finally {
    // Clean up work directory
    if (existsSync(workDir)) {
      await rm(workDir, { recursive: true, force: true });
    }
  }
}

function patchTheme(markdown: string, theme: string): string {
  // If markdown already has frontmatter, patch or add theme field
  const frontmatterRegex = /^---\s*\n([\s\S]*?)\n---/;
  const match = markdown.match(frontmatterRegex);

  if (match) {
    const frontmatter = match[1];
    const themeRegex = /^theme:\s*.*$/m;
    if (themeRegex.test(frontmatter)) {
      // Replace existing theme
      const patched = frontmatter.replace(themeRegex, `theme: ${theme}`);
      return markdown.replace(frontmatterRegex, `---\n${patched}\n---`);
    } else {
      // Add theme to existing frontmatter
      const patched = `theme: ${theme}\n${frontmatter}`;
      return markdown.replace(frontmatterRegex, `---\n${patched}\n---`);
    }
  } else {
    // No frontmatter — prepend one
    return `---\ntheme: ${theme}\n---\n\n${markdown}`;
  }
}

main();
