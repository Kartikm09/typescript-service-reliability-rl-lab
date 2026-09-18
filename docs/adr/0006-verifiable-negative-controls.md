# ADR 6: require behavioral rejection, not any nonzero result

Accepted, 2026-09-18. `scripts/verify_evaluations.py` checks the exact failed stage for eight
plausible wrong patches. Each starts from its task's fixed baseline and includes candidate
notes, avoiding a missing-documentation verdict that masks a test failure. Syntax and scope
controls remain explicitly different. Task-002's unimplemented baseline is intentionally
rejected at compilation because it lacks the required scheduling API; it is not counted as
one of the type-correct behavioral negatives. Reference patches and incorrect patches are
public synthetic examples, not secret benchmark data.
