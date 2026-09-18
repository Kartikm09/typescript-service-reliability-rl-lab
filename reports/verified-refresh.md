# Reliability verification, 2026-09-18

The original commit `d0f1cea344df7858fb8393f9df6672dd7e98e4d5` passed its existing
`make verify-all` suite in a clean source copy. New failure-first probes exposed gaps
in sequential deduplication, scheduling validation, terminal failure handling and
logging after delivery. The [defect report](../docs/defect-report.md) gives reproduction steps.

The repaired source was installed from the lockfile with `npm ci` in a fresh source copy,
then checked using Node 24.18.1, npm 11.16.0 and Python 3.12 on macOS arm64 under
credential-free Seatbelt isolation. CI separately uses the declared Node 24.18.0 pin.
No database, messaging provider or model credentials were used.

`make verify-all` passed after review: 13 unit tests, one in-process API contract test,
six evaluator unit tests and 24 task controls (four references accepted; four starting
states, eight behavioral negatives and eight malformed/scope controls rejected).
Coverage was 100% of instrumented lines and 95.83% of branches.

`npm run test:smoke` passed real localhost health/404 requests; `npm audit --audit-level=high`
reported zero vulnerabilities. `npm run benchmark` completed, and
`python3 scripts/measure_validation.py` measured 3,000 baseline versus 1,000 reference
JSON.parse calls for the same 1,000 valid inputs, with no errors. See
[measured results](measured-validation.json) for timestamps and machine-specific timings.
[Structured evidence](verified-refresh.json) includes exact tested source hashes.

The full reviewed run completed on 2026-09-18 in 117.35 seconds. Private execution logs
include failure-first regressions and command exit codes; published task reports contain
sanitized commands, assertion outcomes, classifications and scores. The previous Docker run hit a task
compile timeout under host memory contention; this was not classified as a source defect.

The fixture corpus is synthetic and public. Evaluation consistency, task behavior and
path allowlists are tested; this does not establish hostile-code containment or benchmark
calibration across machines. The historical July Docker evidence remains historical.
