# Evaluation Report: task-001

- Classification: **test_failure**
- Accepted: **false**
- Score: **25/100**
- Acceptance threshold: **80**
- Message: Stage failed: public_tests

## Stage evidence

| Stage | Result | Duration |
| --- | --- | ---: |
| `format` | pass | 19 ms |
| `lint` | pass | 1359 ms |
| `build` | pass | 1321 ms |
| `public_tests` | fail | 1637 ms |

## Changed files

- `CANDIDATE_NOTES.md`
- `src/content-service.ts`

## Safety boundary

This report came from local process execution with path checks, timeouts, and output caps.
The evaluator is not a hardened sandbox for untrusted code.
