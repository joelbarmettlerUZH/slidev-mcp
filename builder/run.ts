/**
 * Run a subprocess under a hard deadline.
 *
 * - The command runs under GNU `timeout`, which signals the whole process
 *   group (slidev -> vite/playwright/chromium), not just the direct child.
 *   TERM first so Playwright can close its browser, then KILL after a grace period.
 * - stdout/stderr are drained while the process runs and only a bounded tail is
 *   kept. Reading them after exit (as before) can block a chatty child forever
 *   once the pipe buffer fills.
 * - An AbortSignal (client disconnected) terminates the run early.
 */

const TAIL_BYTES = 4096;
const KILL_GRACE_SECONDS = 5;

// Exit statuses of GNU `timeout`
const EXIT_TIMED_OUT = 124;
const EXIT_KILLED = 137; // 128 + SIGKILL: forced after the grace period, or OOM-killed

export interface RunOptions {
  cwd: string;
  timeoutSeconds: number;
  signal?: AbortSignal;
}

export interface RunResult {
  exitCode: number;
  timedOut: boolean;
  killed: boolean;
  aborted: boolean;
  stdoutTail: string;
  stderrTail: string;
}

async function drainTail(
  stream: ReadableStream<Uint8Array> | undefined,
  maxBytes: number,
): Promise<string> {
  if (!stream) return "";
  let tail = Buffer.alloc(0);
  for await (const chunk of stream) {
    tail = Buffer.concat([tail, chunk]);
    if (tail.length > maxBytes) tail = tail.subarray(tail.length - maxBytes);
  }
  return tail.toString("utf-8");
}

export async function runCommand(cmd: string[], opts: RunOptions): Promise<RunResult> {
  const proc = Bun.spawn(
    ["timeout", `--kill-after=${KILL_GRACE_SECONDS}s`, `${opts.timeoutSeconds}s`, ...cmd],
    { cwd: opts.cwd, stdout: "pipe", stderr: "pipe" },
  );

  let aborted = false;
  const onAbort = () => {
    aborted = true;
    proc.kill("SIGTERM"); // `timeout` forwards it to the command's process group
  };
  if (opts.signal) {
    if (opts.signal.aborted) onAbort();
    else opts.signal.addEventListener("abort", onAbort, { once: true });
  }

  try {
    const [exitCode, stdoutTail, stderrTail] = await Promise.all([
      proc.exited,
      drainTail(proc.stdout, TAIL_BYTES),
      drainTail(proc.stderr, TAIL_BYTES),
    ]);
    return {
      exitCode,
      timedOut: exitCode === EXIT_TIMED_OUT,
      killed: exitCode === EXIT_KILLED,
      aborted,
      stdoutTail,
      stderrTail,
    };
  } finally {
    opts.signal?.removeEventListener("abort", onAbort);
  }
}
