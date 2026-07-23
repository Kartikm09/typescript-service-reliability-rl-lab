import type {
  ContentJob,
  ContentRepository,
  DeliveryEvent,
} from "@rl-lab/domain";
import type { Logger } from "@rl-lab/observability";

export interface Clock {
  now(): number;
  schedule(at: number, callback: () => void): { cancel(): void };
}
export interface Transport {
  deliver(job: ContentJob): Promise<void>;
}
export interface RetryPolicy {
  readonly maxAttempts: number;
}

export class DeliveryService {
  readonly #inFlight = new Map<string, Promise<string>>();
  readonly #scheduled = new Map<string, { cancel(): void }>();
  constructor(
    private readonly repository: ContentRepository,
    private readonly transport: Transport,
    private readonly logger: Logger,
  ) {}
  process(job: ContentJob): Promise<string> {
    const existing = this.#inFlight.get(job.idempotencyKey);
    if (existing !== undefined) return existing;
    const operation = this.execute(job).finally(() =>
      this.#inFlight.delete(job.idempotencyKey),
    );
    this.#inFlight.set(job.idempotencyKey, operation);
    return operation;
  }
  schedule(
    job: ContentJob,
    at: number,
    clock: Clock,
    policy: RetryPolicy,
    onEvent: (event: DeliveryEvent) => void,
  ): void {
    if (at < clock.now()) throw new RangeError("delivery time is in the past");
    const handle = clock.schedule(at, () => {
      this.#scheduled.delete(job.id);
      void this.deliverWithRetry(job, policy).then((attempts) => {
        onEvent({ type: "delivery.completed", jobId: job.id, attempts });
      });
    });
    this.#scheduled.set(job.id, handle);
    onEvent({ type: "delivery.scheduled", jobId: job.id, at });
  }
  cancel(jobId: string, onEvent: (event: DeliveryEvent) => void): boolean {
    const handle = this.#scheduled.get(jobId);
    if (handle === undefined) return false;
    handle.cancel();
    this.#scheduled.delete(jobId);
    onEvent({ type: "delivery.cancelled", jobId });
    return true;
  }
  private async execute(job: ContentJob): Promise<string> {
    await this.repository.save(job);
    await this.transport.deliver(job);
    this.logger.write({
      event: "delivery.completed",
      fields: { jobId: job.id },
    });
    return job.id;
  }
  private async deliverWithRetry(
    job: ContentJob,
    policy: RetryPolicy,
  ): Promise<number> {
    let error: unknown;
    for (let attempt = 1; attempt <= policy.maxAttempts; attempt++) {
      try {
        await this.process(job);
        return attempt;
      } catch (caught) {
        error = caught;
      }
    }
    throw error;
  }
}
