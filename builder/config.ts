/**
 * Builder limits, tunable via environment variables.
 *
 * The MCP server gives up after BUILD_TIMEOUT (default 120s) + 5s for builds and
 * 180s for exports, so the per-step budgets below must stay under those.
 */

function intFromEnv(name: string, fallback: number): number {
  const raw = process.env[name];
  if (raw === undefined || raw === "") return fallback;
  const value = Number(raw);
  if (!Number.isInteger(value) || value < 1) {
    throw new Error(`${name} must be a positive integer, got "${raw}"`);
  }
  return value;
}

export const config = {
  /** `slidev build` hard limit, seconds. */
  buildTimeoutSeconds: intFromEnv("BUILDER_BUILD_TIMEOUT_SECONDS", 90),
  /** First-slide preview export after a build, seconds (best effort). */
  previewTimeoutSeconds: intFromEnv("BUILDER_PREVIEW_TIMEOUT_SECONDS", 25),
  /** PDF / PNG export hard limit, seconds. */
  exportTimeoutSeconds: intFromEnv("BUILDER_EXPORT_TIMEOUT_SECONDS", 170),
  /** Jobs running at once (the container has 2 CPUs). */
  maxConcurrent: intFromEnv("BUILDER_MAX_CONCURRENT", 2),
  /** Jobs allowed to wait for a slot before new ones are rejected. */
  maxQueued: intFromEnv("BUILDER_MAX_QUEUED", 8),
};
