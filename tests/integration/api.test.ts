import assert from "node:assert/strict";
import test from "node:test";
import { handleCreate } from "@rl-lab/api";
import { DeliveryService } from "@rl-lab/jobs";
import { MemoryLogger } from "@rl-lab/observability";
import { MemoryContentRepository } from "@rl-lab/persistence";
void test("API contract returns accepted synthetic ID", async () => {
  const service = new DeliveryService(
    new MemoryContentRepository(),
    { deliver: () => Promise.resolve() },
    new MemoryLogger(),
  );
  const response = await handleCreate(
    { id: "job-1", idempotencyKey: "key-1", payload: "demo" },
    service,
  );
  assert.deepEqual(response, { status: 202, body: { id: "job-1" } });
});
