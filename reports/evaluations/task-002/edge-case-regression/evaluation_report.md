# Evaluation Report: task-002

- Classification: **test_failure**
- Accepted: **false**
- Score: **50/100**
- Acceptance threshold: **80**
- Message: Stage failed: held_out_tests

## Stage evidence

| Stage | Result | Duration |
| --- | --- | ---: |
| `format` | pass | 11 ms |
| `lint` | pass | 828 ms |
| `build` | pass | 850 ms |
| `public_tests` | pass | 1355 ms |
| `held_out_tests` | fail | 1438 ms |

## Changed files

- `CANDIDATE_NOTES.md`
- `src/delivery.ts`

## Safety boundary

This report came from local process execution with path checks, timeouts, and output caps.
The evaluator is not a hardened sandbox for untrusted code.
