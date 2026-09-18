# Test strategy

Run `npm ci && make verify-all`; all existing entry points remain.

- Unit tests cover schemas, adapters, same/different-key work, success caching, failure retry,
  cancellation, duplicate scheduling, invalid budgets and terminal outcomes.
- The integration test exercises request validation and service delivery in process.
  `make http-smoke` separately starts the compiled server and verifies real localhost
  health (200) and missing-route (404) responses; it requires local socket access.
- Node coverage thresholds remain unchanged; no failing assertions are skipped.
- Six evaluator unit tests cover score gates, path restrictions, report redaction and copy isolation.
- Four reference patches must pass; four fixed starting fixtures must fail; eight plausible
  wrong implementations must fail the intended behavioral stage; eight malformed/scope cases
  remain separate. `reports/evaluations` records commands, exit status and assertion evidence.
- Task-004 parses are counted independently, and regression cases protect original validation
  semantics. `python3 scripts/measure_validation.py` compares 1,000 valid inputs over 17 timing
  samples. Operation counts are stable; timings depend on machine/load and are not acceptance gates.
- The property test has seed 20260723. Scheduling uses an injected clock and concurrency uses
  explicit promise barriers. Determinism probes execute real behavior in two processes.

`npm audit --audit-level=high` and the repository secret scan are separate checks. The latter
is a narrow pattern scan, not proof that all possible secrets are absent. Tests use synthetic
records only. Docker/Seatbelt isolation used during development does not qualify this harness
as a hardened executor for hostile submitted code.
