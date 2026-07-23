import assert from "node:assert/strict";
import test from "node:test";
import { DeliveryService, type Transport } from "@rl-lab/jobs";
import { MemoryLogger } from "@rl-lab/observability";
import { MemoryContentRepository } from "@rl-lab/persistence";
void test("concurrent idempotent work shares one side effect", async () => {
  let calls = 0;
  const transport: Transport = {
    deliver: async () => {
      calls += 1;
      await Promise.resolve();
    },
  };
  const service = new DeliveryService(
    new MemoryContentRepository(),
    transport,
    new MemoryLogger(),
  );
  const job = { id: "job-1", idempotencyKey: "same", payload: "synthetic" };
  assert.deepEqual(
    await Promise.all([service.process(job), service.process(job)]),
    ["job-1", "job-1"],
  );
  assert.equal(calls, 1);
});
