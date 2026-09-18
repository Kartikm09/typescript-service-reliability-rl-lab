# Evaluation Report: task-004

- Classification: **test_failure**
- Accepted: **false**
- Score: **50/100**
- Acceptance threshold: **80**
- Message: Stage failed: held_out_tests

## Stage evidence

| Stage | Result | Duration |
| --- | --- | ---: |
| `format` | pass | 14 ms |
| `lint` | pass | 985 ms |
| `build` | pass | 1176 ms |
| `public_tests` | pass | 1360 ms |
| `held_out_tests` | fail | 1226 ms |

## Changed files

- `CANDIDATE_NOTES.md`

## Safety boundary

This report came from local process execution with path checks, timeouts, and output caps.
The evaluator is not a hardened sandbox for untrusted code.
