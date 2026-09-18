# ADR 4: cache completion per key in the demonstration service

Accepted, 2026-09-18. `packages/jobs/src/index.ts` retains successful IDs in a completed map,
while failures remove only the in-flight promise. The prior map forgot a completed result,
so sequential repeats caused duplicate effects. A global lock would suppress concurrency
between different keys, so maps remain key-scoped. Tests use a controlled transport barrier
and check concurrent, completed and failed/retried requests. Memory retention and restart
loss are documented limitations, not claims of durable exactly-once delivery.

Completion is recorded immediately after transport success, before logging. If logging
throws, the first caller observes the error, but a retry reuses the known successful ID
instead of repeating the external effect. A transport rejection still clears in-flight work
and permits another attempt. The retry counter counts processing attempts, not necessarily
transport calls. This acknowledgement boundary is process-local; it cannot settle ambiguous
remote outcomes when a transport rejects after an unobservable remote commit.
