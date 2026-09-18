# RFC: executable reliability evidence

Implemented locally on 18 September 2026; synthetic portfolio fixtures only.

The service and four coding tasks retain their IDs and public commands. Each `task.yaml`
now identifies starting commit `d0f1cea344df7858fb8393f9df6672dd7e98e4d5`; each baseline
manifest hashes every starting file. Reference patches can evolve with acceptance tests
without silently replacing the broken starting state.

The service keeps both in-flight and successfully completed results per idempotency key.
An unsuccessful transport clears its pending entry so a retry can execute. A successful
transport acknowledgement is cached before logging; a logging error reaches the first caller
without making a retry repeat delivery. Different keys have independent promises. This is in-memory, process-local deduplication, with no durable
cross-process exactly-once guarantee or eviction policy.

Scheduled work has four events: scheduled, cancelled, completed and failed. Only pending
work can be cancelled. A duplicate pending ID is rejected, preserving the first handle.
A positive safe-integer retry budget and finite time are checked before scheduling. Exhaustion
emits failed exactly once instead of rejecting an unobserved promise. Event listeners are
trusted synchronous consumers; callers must not throw from them.

`make verify-all` executes one reference, the fixed starting state, two type-correct behavioral
negative patches and two syntax/scope controls for each task. Behavioral negatives must fail
the named public, held-out or regression stage, so compiler/setup errors cannot masquerade
as rejection evidence. Original malformed/prohibited controls remain separate.

The previous determinism script printed a constant string. The trusted verifier now executes
real candidate behavior in `verifiers/determinism.mjs` and compares results across fresh
processes. Task 004 additionally counts actual `JSON.parse` calls independently of the
candidate's reported metric; semantic tests cover null, arrays, scalar JSON, empty strings,
malformed JSON and field-error priority.

The evaluator is for trusted synthetic patches. Candidate and internal copies separate
execution stages, but they share an OS process environment with repository fixtures. Public
verifiers are inspectable; neither this evaluator nor Docker alone hides the golden assets
from hostile code. Use a separately hardened executor for unknown submissions.
