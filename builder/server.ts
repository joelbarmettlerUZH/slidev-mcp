/**
 * Lightweight HTTP server for the Slidev builder.
 * Accepts build requests from the MCP server and returns results.
 *
 * POST /build  — Build slides from markdown
 *   Body: { markdown: string, theme: string, uuid: string, base_path: string }
 *   Returns: { uuid, build_time_seconds } or { error, details }
 *
 * GET /health  — Health check
 */

import { runBuild } from "./build-job";
import { runExport } from "./export-job";

const PORT = Number(process.env.BUILDER_PORT || 3000);

const server = Bun.serve({
  port: PORT,
  async fetch(req) {
    const url = new URL(req.url);

    if (req.method === "GET" && url.pathname === "/health") {
      return Response.json({ status: "ok" });
    }

    if (req.method === "POST" && url.pathname === "/build") {
      try {
        const body = await req.json();
        const { markdown, theme, uuid, base_path, color_schema } = body;

        if (!markdown || !theme || !uuid || !base_path) {
          return Response.json(
            { error: "missing_fields", details: "Required: markdown, theme, uuid, base_path" },
            { status: 400 }
          );
        }

        const result = await runBuild({
          markdown, theme, uuid, basePath: base_path,
          colorSchema: color_schema || "light",
        });
        return Response.json(result);
      } catch (err: any) {
        const status = err.status || 500;
        return Response.json(
          { error: err.code || "build_failed", details: err.message || String(err) },
          { status }
        );
      }
    }

    if (req.method === "POST" && url.pathname === "/export") {
      try {
        const body = await req.json();
        const { markdown, theme, uuid, format, color_schema } = body;

        if (!markdown || !theme || !uuid) {
          return Response.json(
            { error: "missing_fields", details: "Required: markdown, theme, uuid" },
            { status: 400 }
          );
        }

        const result = await runExport({
          markdown, theme, uuid,
          format: format === "png" ? "png" : "pdf",
          colorSchema: color_schema || "light",
        });
        return Response.json(result);
      } catch (err: any) {
        const status = err.status || 500;
        return Response.json(
          { error: err.code || "export_failed", details: err.message || String(err) },
          { status }
        );
      }
    }

    return new Response("Not found", { status: 404 });
  },
});

console.log(`Builder server listening on port ${PORT}`);
