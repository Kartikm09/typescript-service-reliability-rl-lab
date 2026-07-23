import type { Clock } from "@rl-lab/jobs";
interface Scheduled {
  readonly at: number;
  readonly callback: () => void;
  cancelled: boolean;
}
export class DeterministicClock implements Clock {
  readonly #scheduled: Scheduled[] = [];
  constructor(private current = 0) {}
  now(): number {
    return this.current;
  }
  schedule(at: number, callback: () => void): { cancel(): void } {
    const item: Scheduled = { at, callback, cancelled: false };
    this.#scheduled.push(item);
    this.#scheduled.sort((a, b) => a.at - b.at);
    return {
      cancel: () => {
        item.cancelled = true;
      },
    };
  }
  advanceTo(at: number): void {
    this.current = at;
    for (const item of this.#scheduled) {
      if (!item.cancelled && item.at <= at) {
        item.cancelled = true;
        item.callback();
      }
    }
  }
}
