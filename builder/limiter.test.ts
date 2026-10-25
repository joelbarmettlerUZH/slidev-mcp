import { describe, expect, test } from "bun:test";
import { AbortedError, BusyError, Limiter } from "./limiter";

const sleep = (ms: number) => new Promise((r) => setTimeout(r, ms));

/** A job that stays running until released. */
function gate() {
  let release!: () => void;
  const done = new Promise<void>((r) => (release = r));
  return { done, release };
}

describe("Limiter", () => {
  test("never runs more than maxConcurrent jobs at once", async () => {
    const limiter = new Limiter(2, 10);
    let running = 0;
    let peak = 0;
    const job = async () => {
      running++;
      peak = Math.max(peak, running);
      await sleep(20);
      running--;
    };
    await Promise.all(Array.from({ length: 8 }, () => limiter.run(job)));
    expect(peak).toBe(2);
    expect(limiter.stats).toEqual({ active: 0, queued: 0 });
  });

  test("rejects with BusyError once the queue is full", async () => {
    const limiter = new Limiter(1, 1);
    const g = gate();
    const first = limiter.run(() => g.done); // running
    const second = limiter.run(async () => "queued"); // waiting
    await sleep(5);
    await expect(limiter.run(async () => "overflow")).rejects.toBeInstanceOf(BusyError);
    g.release();
    await first;
    expect(await second).toBe("queued");
  });

  test("a queued job whose client disconnected never runs", async () => {
    const limiter = new Limiter(1, 5);
    const g = gate();
    const first = limiter.run(() => g.done);
    const ctl = new AbortController();
    let ran = false;
    const waiting = limiter.run(async () => {
      ran = true;
    }, ctl.signal);
    await sleep(5);
    expect(limiter.stats.queued).toBe(1);
    ctl.abort();
    await expect(waiting).rejects.toBeInstanceOf(AbortedError);
    expect(limiter.stats.queued).toBe(0);
    g.release();
    await first;
    expect(ran).toBe(false);
    expect(limiter.stats).toEqual({ active: 0, queued: 0 });
  });

  test("a slot is released when a job throws", async () => {
    const limiter = new Limiter(1, 1);
    await expect(
      limiter.run(async () => {
        throw new Error("boom");
      }),
    ).rejects.toThrow("boom");
    expect(await limiter.run(async () => "ok")).toBe("ok");
    expect(limiter.stats).toEqual({ active: 0, queued: 0 });
  });

  test("an already-aborted request is rejected without taking a slot", async () => {
    const limiter = new Limiter(1, 1);
    const ctl = new AbortController();
    ctl.abort();
    await expect(limiter.run(async () => "x", ctl.signal)).rejects.toBeInstanceOf(AbortedError);
    expect(limiter.stats).toEqual({ active: 0, queued: 0 });
  });
});
