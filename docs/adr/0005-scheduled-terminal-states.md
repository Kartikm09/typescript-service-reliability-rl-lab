# ADR 5: explicit terminal failure and cancellation ownership

Accepted, 2026-09-18. A queued ID owns one cancellation handle. Reject duplicate scheduling
instead of silently replacing the handle. Retry exhaustion emits `delivery.failed` (task
fixture: `failed`) and never completed. The retry count is a positive safe integer and time
must be finite and not in the past. Tests advance a deterministic clock and await an event-loop
turn; they do not sleep for delivery time. Cancellation stops queued work, not an already
running transport. `tests/unit/scheduling.test.ts` and task-002 held-out tests exercise rules.
