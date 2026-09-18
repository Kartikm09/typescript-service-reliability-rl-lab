# Evaluation Report: task-004

- Classification: **test_failure**
- Accepted: **false**
- Score: **25/100**
- Acceptance threshold: **80**
- Message: Stage failed: public_tests

## Stage evidence

| Stage | Result | Duration |
| --- | --- | ---: |
| `format` | pass | 18 ms |
| `lint` | pass | 1193 ms |
| `build` | pass | 1170 ms |
| `public_tests` | fail | 1215 ms |

## Changed files

- `CANDIDATE_NOTES.md`
- `src/validator.ts`

## Safety boundary

This report came from local process execution with path checks, timeouts, and output caps.
The evaluator is not a hardened sandbox for untrusted code.
