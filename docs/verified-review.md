# Internal code-review example

This is a review of synthetic portfolio code, not an accepted external contribution.

**Finding TS-001 — completed work loses deduplication.** `DeliveryService.process` originally
removed its only per-key entry in `finally`. Concurrent requests shared work, but a subsequent
request after completion delivered twice. The task-001 reference cached successful results;
the demonstration service did not. Preserve completed results separately and still clear
failures. Tests must assert sequential reuse and retry, not only concurrent same-key calls.

**Finding TS-002 — scheduled failures become unhandled rejections.** `schedule` attached a
success handler to `deliverWithRetry`, discarded its promise and provided no terminal failure
handler. Exhausting the retry budget could terminate the process. The fix emits a typed
failure event, validates the budget and preserves cancellation ownership on duplicate IDs.
Returning a successful completed event after exhaustion would make the UI appear healthy
while delivery failed, so the negative tests inspect event types and attempt counts.

**Finding TS-003 — negative controls can fail for the wrong reason.** The old runner accepted
any non-accepted result. Missing notes masked failure classification; wrong task-002 and
004 examples could fail before behavioral tests. New controls compile successfully and fail
a named assertion stage. The verifier also measures `JSON.parse` calls rather than trusting
a candidate's performance number. Reference acceptance, not patch similarity, is required.

**Finding TS-004 — logging failure can duplicate a successful effect.** Independent review
reproduced two transport calls when logging threw after the first successful delivery. The
completed map now records transport acknowledgement before invoking the logger. The new
regression keeps the first logging error visible and verifies retry returns the cached ID
with one transport call; the existing transport-failure test still verifies two attempts.

**Finding TS-005 — dependency expansion denial of service.** A fresh audit identified
`brace-expansion` 5.0.7 as vulnerable. A targeted lockfile-only update to 5.0.12 removes the
reported advisory without changing direct dependency pins. Clean installation and audit
reported zero vulnerabilities; this is a point-in-time dependency check.

Review limits: OS-level hostile-code isolation, durable storage, idempotency expiry and
throwing event listeners remain outside this small demonstration. No external reviewer
acceptance or production operation is claimed.

The first GitHub history scan flagged two provenance SHA256 values as generic API keys.
Both values were recomputed from their public source files and matched. `.gitleaksignore`
records only those exact commit/file/rule/line fingerprints; complete-history scanning stays
enabled without a rule-wide, path-wide or arbitrary-hash exclusion.
