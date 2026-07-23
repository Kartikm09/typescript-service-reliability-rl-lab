import assert from "node:assert/strict";
import test from "node:test";
import type { DeliveryEvent, ContentJob } from "@rl-lab/domain";
import { DeliveryService } from "@rl-lab/jobs";
import { MemoryLogger } from "@rl-lab/observability";
import { MemoryContentRepository } from "@rl-lab/persistence";
import { DeterministicClock } from "@rl-lab/shared-testkit";
const job: ContentJob = {
  id: "scheduled",
  idempotencyKey: "scheduled-key",
  payload: "demo",
};
void test("scheduled delivery retries and emits completion", async () => {
  let calls = 0;
  const events: DeliveryEvent[] = [];
  const clock = new DeterministicClock();
  const service = new DeliveryService(
    new MemoryContentRepository(),
    {
      deliver: () => {
        calls += 1;
        return calls === 1
          ? Promise.reject(new Error("temporary"))
          : Promise.resolve();
      },
    },
    new MemoryLogger(),
  );
  service.schedule(job, 10, clock, { maxAttempts: 2 }, (event) => {
    events.push(event);
  });
  clock.advanceTo(10);
  await new Promise((resolve) => setImmediate(resolve));
  assert.equal(calls, 2);
  assert.deepEqual(
    events.map((event) => event.type),
    ["delivery.scheduled", "delivery.completed"],
  );
});
void test("cancellation prevents pending delivery", async () => {
  let calls = 0;
  const events: DeliveryEvent[] = [];
  const clock = new DeterministicClock();
  const service = new DeliveryService(
    new MemoryContentRepository(),
    {
      deliver: () => {
        calls += 1;
        return Promise.resolve();
      },
    },
    new MemoryLogger(),
  );
  service.schedule(job, 10, clock, { maxAttempts: 1 }, (event) => {
    events.push(event);
  });
  assert.equal(
    service.cancel(job.id, (event) => {
      events.push(event);
    }),
    true,
  );
  assert.equal(
    service.cancel(job.id, (event) => {
      void event;
    }),
    false,
  );
  clock.advanceTo(10);
  await Promise.resolve();
  assert.equal(calls, 0);
  assert.deepEqual(
    events.map((event) => event.type),
    ["delivery.scheduled", "delivery.cancelled"],
  );
});
