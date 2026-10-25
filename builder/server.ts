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
import { config } from "./config";
import { AbortedError, BusyError, Limiter } from "./limiter";

const PORT = Number(process.env.BUILDER_PORT || 3000);
const limiter = new Limiter(config.maxConcurrent, config.maxQueued);

/** Map failures to the JSON error shape the MCP server expects. */
function errorResponse(err: any, fallbackCode: string): Response {
  if (err instanceof BusyError) {
    return Response.json(
      { error: "concurrent_limit", details: err.message },
      { status: 503, headers: { "Retry-After": "10" } },
    );
  }
  if (err instanceof AbortedError) {
    return Response.json({ error: "aborted", details: err.message }, { status: 499 });
  }
  return Response.json(
    { error: err.code || fallbackCode, details: err.message || String(err) },
    { status: err.status || 500 },
  );
}

const server = Bun.serve({
  port: PORT,
  async fetch(req) {
    const url = new URL(req.url);

    if (req.method === "GET" && url.pathname === "/health") {
      return Response.json({ status: "ok", ...limiter.stats });
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

        const result = await limiter.run(
          () => runBuild({
            markdown, theme, uuid, basePath: base_path,
            colorSchema: color_schema || "light",
            signal: req.signal,
          }),
          req.signal,
        );
        return Response.json(result);
      } catch (err: any) {
        return errorResponse(err, "build_failed");
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

        const result = await limiter.run(
          () => runExport({
            markdown, theme, uuid,
            format: format === "png" ? "png" : "pdf",
            colorSchema: color_schema || "light",
            signal: req.signal,
          }),
          req.signal,
        );
        return Response.json(result);
      } catch (err: any) {
        return errorResponse(err, "export_failed");
      }
    }

    return new Response("Not found", { status: 404 });
  },
});

console.log(`Builder server listening on port ${PORT}`);
