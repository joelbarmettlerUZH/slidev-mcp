import { copyFile, mkdir, readdir, readFile, rm, writeFile } from "fs/promises";
import { join } from "path";
import { existsSync } from "fs";

export interface ExportParams {
  markdown: string;
  theme: string;
  uuid: string;
  format: "pdf" | "png";
  colorSchema: string;
}

export interface ExportResult {
  uuid: string;
  format: string;
  export_time_seconds: number;
  filename?: string;
  images_base64?: string[];
}

class ExportError extends Error {
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
      continue;
    }
    if (entry.isDirectory()) {
      await copyDir(srcPath, destPath);
    } else {
      await copyFile(srcPath, destPath);
    }
  }
}

function patchFrontmatter(markdown: string, theme: string, colorSchema: string): string {
  const frontmatterRegex = /^---\s*\n([\s\S]*?)\n---/;
  const match = markdown.match(frontmatterRegex);

  const requiredFields: Record<string, string> = {
    theme: theme,
    colorSchema: colorSchema,
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
  }
  const fields = Object.entries(requiredFields)
    .map(([k, v]) => `${k}: ${v}`)
    .join("\n");
  return `---\n${fields}\n---\n\n${markdown}`;
}

async function prepareWorkDir(
  theme: string,
  markdown: string,
  uuid: string,
  colorSchema: string,
): Promise<string> {
  const themeDir = join("/app/themes", theme);
  if (!existsSync(themeDir)) {
    throw new ExportError("theme_not_found", `Theme not found: ${theme}`, 400);
  }

  const workDir = join("/tmp/exports", uuid, "work");
  await copyDir(themeDir, workDir);

  const themedSlides = patchFrontmatter(markdown, theme, colorSchema);
  await writeFile(join(workDir, "slides.md"), themedSlides, "utf-8");

  const nodeModulesSrc = join(themeDir, "node_modules");
  const nodeModulesDest = join(workDir, "node_modules");
  if (!existsSync(nodeModulesDest)) {
    await Bun.spawn(["ln", "-s", nodeModulesSrc, nodeModulesDest]).exited;
  }

  return workDir;
}

export async function runExport(params: ExportParams): Promise<ExportResult> {
  const { markdown, theme, uuid, format, colorSchema } = params;
  const distDir = join("/data/slides", uuid);
  const start = Date.now();

  const workDir = await prepareWorkDir(theme, markdown, uuid, colorSchema);

  try {
    if (format === "pdf") {
      const pdfPath = join(distDir, "slides-export.pdf");

      const proc = Bun.spawn(
        [
          "bunx", "slidev", "export",
          "--output", pdfPath,
          "--timeout", "60000",
        ],
        { cwd: workDir, stdout: "pipe", stderr: "pipe" }
      );

      const exitCode = await proc.exited;
      const elapsed = (Date.now() - start) / 1000;

      if (exitCode !== 0) {
        const stderr = await new Response(proc.stderr).text();
        throw new ExportError(
          "export_failed",
          `PDF export failed (code ${exitCode}): ${stderr.slice(-500)}`
        );
      }

      if (!existsSync(pdfPath)) {
        throw new ExportError("export_failed", "PDF export completed but no file produced");
      }

      return {
        uuid,
        format: "pdf",
        export_time_seconds: Math.round(elapsed * 100) / 100,
        filename: "slides-export.pdf",
      };
    } else {
      // PNG export — returns base64 images of all slides
      const pngDir = join(distDir, "screenshots");

      const proc = Bun.spawn(
        [
          "bunx", "slidev", "export",
          "--format", "png",
          "--output", pngDir,
          "--timeout", "60000",
        ],
        { cwd: workDir, stdout: "pipe", stderr: "pipe" }
      );

      const exitCode = await proc.exited;
      const elapsed = (Date.now() - start) / 1000;

      if (exitCode !== 0) {
        const stderr = await new Response(proc.stderr).text();
        throw new ExportError(
          "export_failed",
          `PNG export failed (code ${exitCode}): ${stderr.slice(-500)}`
        );
      }

      if (!existsSync(pngDir)) {
        throw new ExportError("export_failed", "PNG export completed but no directory produced");
      }

      // Read all PNGs and base64-encode them, sorted by slide number
      const files = (await readdir(pngDir))
        .filter(f => f.endsWith(".png"))
        .sort((a, b) => {
          const numA = parseInt(a.replace(/\D/g, ""), 10);
          const numB = parseInt(b.replace(/\D/g, ""), 10);
          return numA - numB;
        });

      const images_base64: string[] = [];
      for (const file of files) {
        const data = await readFile(join(pngDir, file));
        images_base64.push(Buffer.from(data).toString("base64"));
      }

      return {
        uuid,
        format: "png",
        export_time_seconds: Math.round(elapsed * 100) / 100,
        images_base64,
      };
    }
  } finally {
    const exportTmp = join("/tmp/exports", uuid);
    if (existsSync(exportTmp)) {
      await rm(exportTmp, { recursive: true, force: true });
    }
  }
}
