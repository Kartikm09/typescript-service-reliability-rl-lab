# Evaluation Report: task-003

- Classification: **test_failure**
- Accepted: **false**
- Score: **50/100**
- Acceptance threshold: **80**
- Message: Stage failed: held_out_tests

## Stage evidence

| Stage | Result | Duration |
| --- | --- | ---: |
| `format` | pass | 69 ms |
| `lint` | pass | 1387 ms |
| `build` | pass | 1353 ms |
| `public_tests` | pass | 1167 ms |
| `held_out_tests` | fail | 1292 ms |

## Changed files

- `CANDIDATE_NOTES.md`

## Safety boundary

This report came from local process execution with path checks, timeouts, and output caps.
The evaluator is not a hardened sandbox for untrusted code.
