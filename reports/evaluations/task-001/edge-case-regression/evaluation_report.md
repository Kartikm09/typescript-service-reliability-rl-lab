# Evaluation Report: task-001

- Classification: **test_failure**
- Accepted: **false**
- Score: **50/100**
- Acceptance threshold: **80**
- Message: Stage failed: held_out_tests

## Stage evidence

| Stage | Result | Duration |
| --- | --- | ---: |
| `format` | pass | 24 ms |
| `lint` | pass | 1426 ms |
| `build` | pass | 1958 ms |
| `public_tests` | pass | 1732 ms |
| `held_out_tests` | fail | 1453 ms |

## Changed files

- `CANDIDATE_NOTES.md`
- `src/content-service.ts`

## Safety boundary

This report came from local process execution with path checks, timeouts, and output caps.
The evaluator is not a hardened sandbox for untrusted code.
