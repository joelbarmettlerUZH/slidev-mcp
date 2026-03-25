import { copyFile, mkdir, readdir, rm, writeFile } from "fs/promises";
import { join } from "path";
import { existsSync } from "fs";

export interface BuildParams {
  markdown: string;
  theme: string;
  uuid: string;
  basePath: string;
}

export interface BuildResult {
  uuid: string;
  build_time_seconds: number;
}

class BuildError extends Error {
  code: string;
  status: number;
  constructor(code: string, message: string, status = 500) {
    super(message);
    this.code = code;
    this.status = status;
  }
}

async function copyDir(src: string, dest: string): Promise<void> {
  await mkdir(dest, { recursive: true });
  const entries = await readdir(src, { withFileTypes: true });
  for (const entry of entries) {
    const srcPath = join(src, entry.name);
    const destPath = join(dest, entry.name);
    if (entry.name === "node_modules" || entry.name === "dist-test") {
      continue; // Skip — we symlink node_modules separately
    }
    if (entry.isDirectory()) {
      await copyDir(srcPath, destPath);
    } else {
      await copyFile(srcPath, destPath);
    }
  }
}

function patchFrontmatter(markdown: string, theme: string): string {
  const frontmatterRegex = /^---\s*\n([\s\S]*?)\n---/;
  const match = markdown.match(frontmatterRegex);

  const requiredFields: Record<string, string> = {
    theme: theme,
    routerMode: "hash",
  };

  if (match) {
    let frontmatter = match[1];
    for (const [key, value] of Object.entries(requiredFields)) {
      const fieldRegex = new RegExp(`^${key}:\\s*.*$`, "m");
      if (fieldRegex.test(frontmatter)) {
        frontmatter = frontmatter.replace(fieldRegex, `${key}: ${value}`);
      } else {
        frontmatter = `${key}: ${value}\n${frontmatter}`;
      }
    }
    return markdown.replace(frontmatterRegex, `---\n${frontmatter}\n---`);
  } else {
    const fields = Object.entries(requiredFields)
      .map(([k, v]) => `${k}: ${v}`)
      .join("\n");
    return `---\n${fields}\n---\n\n${markdown}`;
  }
}

export async function runBuild(params: BuildParams): Promise<BuildResult> {
  const { markdown, theme, uuid, basePath } = params;

  // Locate the theme's project directory
  const themeDir = join("/app/themes", theme);
  if (!existsSync(themeDir)) {
    throw new BuildError("theme_not_found", `Theme directory not found: ${theme}`, 400);
  }

  const workDir = join("/tmp/builds", uuid, "work");
  const distDir = join("/data/slides", uuid);
  const start = Date.now();

  try {
    // Copy theme project into work directory (excludes node_modules)
    await copyDir(themeDir, workDir);

    // Patch theme + routerMode into frontmatter and write slides
    const themedSlides = patchFrontmatter(markdown, theme);
    await writeFile(join(workDir, "slides.md"), themedSlides, "utf-8");

    // Symlink node_modules from the theme's own install
    const nodeModulesSrc = join(themeDir, "node_modules");
    const nodeModulesDest = join(workDir, "node_modules");
    if (!existsSync(nodeModulesDest)) {
      await Bun.spawn(["ln", "-s", nodeModulesSrc, nodeModulesDest]).exited;
    }

    // Clean existing slides directory if overwriting
    if (existsSync(distDir)) {
      await rm(distDir, { recursive: true, force: true });
    }

    // Run slidev build
    const proc = Bun.spawn(
      ["bunx", "slidev", "build", "--base", basePath, "--out", distDir],
      {
        cwd: workDir,
        stdout: "pipe",
        stderr: "pipe",
      }
    );

    const exitCode = await proc.exited;
    const elapsed = (Date.now() - start) / 1000;

    if (exitCode !== 0) {
      const stderr = await new Response(proc.stderr).text();
      throw new BuildError(
        "build_failed",
        `Build exited with code ${exitCode}: ${stderr.slice(-500)}`
      );
    }

    if (!existsSync(join(distDir, "index.html"))) {
      throw new BuildError("build_failed", "Build completed but no index.html produced");
    }

    return { uuid, build_time_seconds: Math.round(elapsed * 100) / 100 };
  } finally {
    // Clean up work directory
    const buildTmp = join("/tmp/builds", uuid);
    if (existsSync(buildTmp)) {
      await rm(buildTmp, { recursive: true, force: true });
    }
  }
}
