import { describe, expect, test } from "bun:test";
import { runCommand } from "./run";

const cwd = "/tmp";

describe("runCommand", () => {
  test("returns exit code and output tails", async () => {
    const r = await runCommand(["sh", "-c", "echo out; echo err >&2; exit 3"], {
      cwd,
      timeoutSeconds: 10,
    });
    expect(r.exitCode).toBe(3);
    expect(r.timedOut).toBe(false);
    expect(r.stdoutTail.trim()).toBe("out");
    expect(r.stderrTail.trim()).toBe("err");
  });

  test("stops a command that exceeds the deadline", async () => {
    const t = Date.now();
    const r = await runCommand(["sleep", "30"], { cwd, timeoutSeconds: 1 });
    expect(r.timedOut).toBe(true);
    expect(Date.now() - t).toBeLessThan(8000);
  });

  test("kills grandchildren too, not just the direct child", async () => {
    const marker = `grandchild-${Date.now()}`;
    // The shell spawns a long-lived grandchild and waits for it.
    const t = Date.now();
    const r = await runCommand(["sh", "-c", `sleep 60 & echo ${marker}; wait`], {
      cwd,
      timeoutSeconds: 1,
    });
    expect(r.timedOut).toBe(true);
    // If only the shell were killed, the pipe held open by the grandchild would
    // keep draining until `sleep 60` ended.
    expect(Date.now() - t).toBeLessThan(10000);
  });

  test("drains output far larger than a pipe buffer without hanging", async () => {
    // 8 MB on stdout and stderr: a process whose pipes are read only after exit blocks here.
    const r = await runCommand(
      ["sh", "-c", "head -c 8000000 /dev/zero | tr '\\0' 'x'; head -c 8000000 /dev/zero | tr '\\0' 'e' >&2"],
      { cwd, timeoutSeconds: 20 },
    );
    expect(r.exitCode).toBe(0);
    expect(r.stdoutTail.length).toBeLessThanOrEqual(4096);
    expect(r.stderrTail.length).toBeLessThanOrEqual(4096);
  });

  test("an abort signal terminates the run early", async () => {
    const ctl = new AbortController();
    const t = Date.now();
    setTimeout(() => ctl.abort(), 300);
    const r = await runCommand(["sleep", "30"], { cwd, timeoutSeconds: 60, signal: ctl.signal });
    expect(r.aborted).toBe(true);
    expect(Date.now() - t).toBeLessThan(8000);
  });

  test("an already-aborted signal never lets the command run long", async () => {
    const ctl = new AbortController();
    ctl.abort();
    const t = Date.now();
    const r = await runCommand(["sleep", "30"], { cwd, timeoutSeconds: 60, signal: ctl.signal });
    expect(r.aborted).toBe(true);
    expect(Date.now() - t).toBeLessThan(8000);
  });
});
