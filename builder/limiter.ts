/**
 * Bounded concurrency with a bounded wait queue.
 *
 * At most `maxConcurrent` jobs run at once and at most `maxQueued` wait for a
 * slot; anything beyond that is rejected immediately with BusyError so callers
 * can answer "retry later" instead of piling up unbounded work. A waiting job
 * whose signal aborts (client went away) leaves the queue without ever running.
 */

export class BusyError extends Error {
  constructor() {
    super("Builder is busy; retry later");
  }
}

export class AbortedError extends Error {
  constructor() {
    super("Request aborted by client");
  }
}

export class Limiter {
  private active = 0;
  private waiters: Array<() => void> = [];

  constructor(
    private readonly maxConcurrent: number,
    private readonly maxQueued: number,
  ) {}

  get stats(): { active: number; queued: number } {
    return { active: this.active, queued: this.waiters.length };
  }

  async run<T>(fn: () => Promise<T>, signal?: AbortSignal): Promise<T> {
    if (signal?.aborted) throw new AbortedError();

    if (this.active < this.maxConcurrent) {
      this.active++;
    } else {
      if (this.waiters.length >= this.maxQueued) throw new BusyError();
      await this.waitForSlot(signal);
    }

    try {
      return await fn();
    } finally {
      this.release();
    }
  }

  private waitForSlot(signal?: AbortSignal): Promise<void> {
    return new Promise<void>((resolve, reject) => {
      const onAbort = () => {
        const i = this.waiters.indexOf(waiter);
        if (i !== -1) this.waiters.splice(i, 1);
        reject(new AbortedError());
      };
      // The slot is handed over by release(): `active` is not decremented.
      const waiter = () => {
        signal?.removeEventListener("abort", onAbort);
        resolve();
      };
      this.waiters.push(waiter);
      signal?.addEventListener("abort", onAbort, { once: true });
    });
  }

  private release(): void {
    const next = this.waiters.shift();
    if (next) next();
    else this.active--;
  }
}
