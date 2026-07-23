import { performance } from "node:perf_hooks";
import { parseContentJob } from "../packages/domain/dist/index.js";
const fixtures = Array.from({ length: 10_000 }, (_, index) => ({
  id: `job-${index}`,
  idempotencyKey: `key-${index}`,
  payload: "synthetic",
}));
const started = performance.now();
for (const fixture of fixtures) parseContentJob(fixture);
const elapsed = performance.now() - started;
console.log(
  JSON.stringify({
    benchmark: "parse-content-job",
    operations: fixtures.length,
    elapsedMs: Number(elapsed.toFixed(3)),
    opsPerSecond: Math.round(fixtures.length / (elapsed / 1000)),
  }),
);
