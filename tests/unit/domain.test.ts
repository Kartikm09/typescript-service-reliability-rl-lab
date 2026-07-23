import assert from "node:assert/strict";
import test from "node:test";
import fc from "fast-check";
import { parseContentJob, ValidationError } from "@rl-lab/domain";
void test("valid synthetic jobs preserve strings", () => {
  fc.assert(
    fc.property(
      fc.string({ minLength: 1 }),
      fc.string({ minLength: 1 }),
      (id, payload) => {
        assert.deepEqual(
          parseContentJob({ id, idempotencyKey: `key-${id}`, payload }),
          { id, idempotencyKey: `key-${id}`, payload },
        );
      },
    ),
  );
});
void test("missing fields are rejected", () => {
  assert.throws(() => parseContentJob({ id: "x" }), ValidationError);
});
