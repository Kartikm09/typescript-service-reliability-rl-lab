# Benchmark Evidence

Recorded on 2026-07-23 with Node.js 24.18.0 and TypeScript 6.0.3 on an Apple M1 host.
These local measurements are reproducibility evidence, not cross-machine guarantees.

## Application Benchmark

Command: `npm run benchmark`

```json
{"benchmark":"parse-content-job","operations":10000,"elapsedMs":2.621,"opsPerSecond":3815156}
```

## Task 004 Before And After

| Workspace | `parse_passes` | Result |
| --- | ---: | --- |
| Published baseline | 300 | Reproduced with `scripts/run_benchmark.sh` |
| Golden patch | 100 | Accepted; configured threshold is at most 100 |

The deterministic parse counter records redundant validation work. The accepted report
in `reports/evaluations/task-004/solution/result.json` also passed strict compilation,
public, held-out, regression, formatting, and determinism stages.
