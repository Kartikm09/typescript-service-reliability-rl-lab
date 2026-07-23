# Repository Reviewer Checklist

- Scope matches the task and allowed-change policy.
- Public and held-out tests evaluate behavior rather than implementation trivia.
- Golden patches are minimal, reproducible, and absent from candidate workspaces.
- Incorrect patches fail for documented reasons.
- Build, runtime, regression, timeout, performance, and malformed-patch paths are
  classified consistently.
- Benchmark claims include before-and-after evidence.
- Reports redact temporary machine paths and cap process output.
- Documentation states sandbox and synthetic-data limitations clearly.
