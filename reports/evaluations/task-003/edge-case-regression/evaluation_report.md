# Evaluation Report: task-003

- Classification: **test_failure**
- Accepted: **false**
- Score: **25/100**
- Acceptance threshold: **80**
- Message: Stage failed: public_tests

## Stage evidence

| Stage | Result | Duration |
| --- | --- | ---: |
| `format` | pass | 13 ms |
| `lint` | pass | 796 ms |
| `build` | pass | 928 ms |
| `public_tests` | fail | 975 ms |

## Changed files

- `CANDIDATE_NOTES.md`
- `src/domain.ts`
- `src/persistence.ts`
- `src/ports.ts`

## Safety boundary

This report came from local process execution with path checks, timeouts, and output caps.
The evaluator is not a hardened sandbox for untrusted code.
