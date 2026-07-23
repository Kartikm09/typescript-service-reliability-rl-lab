# Acceptance Criteria

- Concurrent same-key calls execute one side effect.
- All callers receive the same result.
- Different keys may run concurrently.
- Failures clear in-flight state for retry.
