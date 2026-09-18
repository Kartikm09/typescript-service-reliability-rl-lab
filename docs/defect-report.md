# Reproducible defects

Starting service commit: `d0f1cea344df7858fb8393f9df6672dd7e98e4d5`.

TS-001 (high for the advertised contract): create one `DeliveryService`, await `process(job)`
twice with the same key, and count transport calls. Expected 1; observed 2. The old unit suite
only checked concurrent calls. Regression: `completed idempotency key is reused after the first
promise settles` in `tests/unit/delivery.test.ts`.

TS-002 (high for scheduling reliability): schedule a job with a transport that rejects every
attempt and a budget of 2, advance the injected clock and observe the next event-loop turn.
Expected one terminal failure, two calls and no completion. Observed unhandled `Error: offline`.
Regressions also exposed accepted zero retry budgets and overwritten duplicate scheduling
handles. See `tests/unit/scheduling.test.ts`.

A supplementary isolated Node 24.18.0 transform-types probe reproduced all four failures
before implementation and all four passed after correction. The production verification
remains `npm ci && make verify-all`, which compiles TypeScript, lints, tests service/API/coverage,
and executes task evaluation controls. To reproduce the defects on the starting commit,
apply only the test additions from this change, then run `npm ci && npm run build && npm test`.
Do not apply the implementation changes when reproducing the old behavior.

The old task fixtures intentionally remain broken; a rejected starting fixture is an expected
negative case, not a newly introduced application defect. The task-002 reference patch is
updated to satisfy the newly explicit failed-event and duplicate-ID rules.

TS-004: inject a logger that throws after transport success. The original completion cache
was set after logging, so a retry delivered again and threw again. The regression observes
the first logging error, then requires a cached successful retry and exactly one transport
call. Record completion at transport acknowledgement, before logging.

TS-005: `npm audit --audit-level=high` identified a high severity expansion denial of service
in the old transitive `brace-expansion` 5.0.7 lock entry (GHSA-mh99-v99m-4gvg and
GHSA-rgw5-rvv9-x895). Updating only that entry to 5.0.12 produced zero audit findings after
a fresh `npm ci`.

TS-006: starting the compiled API with APP_PORT=0 correctly bound an ephemeral port but
printed 0. The new localhost smoke asserted the actual port and failed before the fix.
Readiness now reports the socket address, enabling health/404 requests without a fixed-port
collision. This server exposes no delivery HTTP endpoint.
