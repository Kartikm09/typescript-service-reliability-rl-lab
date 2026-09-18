# Evaluation Report: task-004

- Classification: **regression_failure**
- Accepted: **false**
- Score: **70/100**
- Acceptance threshold: **80**
- Message: Stage failed: regression_tests

## Stage evidence

| Stage | Result | Duration |
| --- | --- | ---: |
| `format` | pass | 15 ms |
| `lint` | pass | 1049 ms |
| `build` | pass | 899 ms |
| `public_tests` | pass | 1082 ms |
| `held_out_tests` | pass | 996 ms |
| `regression_tests` | fail | 1175 ms |

## Changed files

- `CANDIDATE_NOTES.md`
- `src/validator.ts`

## Safety boundary

This report came from local process execution with path checks, timeouts, and output caps.
The evaluator is not a hardened sandbox for untrusted code.
