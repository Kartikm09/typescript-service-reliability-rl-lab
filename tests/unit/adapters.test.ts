import assert from "node:assert/strict";
import test from "node:test";
import { MemoryLogger } from "@rl-lab/observability";
import { MemoryContentRepository } from "@rl-lab/persistence";
void test("memory adapters return defensive snapshots", async () => {
  const repository = new MemoryContentRepository();
  const job = { id: "1", idempotencyKey: "k", payload: "p" };
  await repository.save(job);
  assert.deepEqual(await repository.find("1"), job);
  assert.equal(await repository.find("missing"), undefined);
  const logger = new MemoryLogger();
  logger.write({ event: "test", fields: { count: 1 } });
  assert.deepEqual(logger.records(), [{ event: "test", fields: { count: 1 } }]);
});
