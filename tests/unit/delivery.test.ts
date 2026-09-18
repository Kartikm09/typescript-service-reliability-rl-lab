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

void test("completed idempotency key is reused after the first promise settles", async () => {
  let calls = 0;
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
  const job = { id: "done", idempotencyKey: "done-key", payload: "synthetic" };
  assert.equal(await service.process(job), "done");
  assert.equal(await service.process(job), "done");
  assert.equal(calls, 1);
});

void test("distinct keys begin before either transport completes", async () => {
  const started: string[] = [];
  const releases: (() => void)[] = [];
  let bothStarted!: () => void;
  const ready = new Promise<void>((resolve) => {
    bothStarted = resolve;
  });
  const service = new DeliveryService(
    new MemoryContentRepository(),
    {
      deliver: (job) =>
        new Promise<void>((resolve) => {
          started.push(job.id);
          releases.push(resolve);
          if (started.length === 2) bothStarted();
        }),
    },
    new MemoryLogger(),
  );
  const first = service.process({ id: "a", idempotencyKey: "a", payload: "a" });
  const second = service.process({
    id: "b",
    idempotencyKey: "b",
    payload: "b",
  });
  await ready;
  assert.deepEqual(started, ["a", "b"]);
  for (const release of releases) release();
  await Promise.all([first, second]);
});

void test("failure clears the key and permits one successful retry", async () => {
  let calls = 0;
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
  const job = {
    id: "retry",
    idempotencyKey: "retry-key",
    payload: "synthetic",
  };
  await assert.rejects(service.process(job), /temporary/);
  assert.equal(await service.process(job), "retry");
  assert.equal(calls, 2);
});

void test("completed transport is not repeated when logging fails", async () => {
  let calls = 0;
  const service = new DeliveryService(
    new MemoryContentRepository(),
    {
      deliver: () => {
        calls += 1;
        return Promise.resolve();
      },
    },
    {
      write: () => {
        throw new Error("logger unavailable");
      },
    },
  );
  const job = {
    id: "logged",
    idempotencyKey: "logged-key",
    payload: "synthetic",
  };
  await assert.rejects(service.process(job), /logger unavailable/);
  assert.equal(await service.process(job), "logged");
  assert.equal(calls, 1);
});
