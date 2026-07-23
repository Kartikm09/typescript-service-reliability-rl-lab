# Deterministic Python Evaluator

The evaluator turns each TypeScript task into a candidate-visible workspace,
validates and applies a unified diff, runs staged quality gates, then creates a
separate internal test workspace for held-out tests. It emits six JSON/Markdown
artifacts required for evidence-based review.

```bash
PYTHONPATH=evaluator/src python3 -m rl_evaluator.cli evaluate \
  --repo-root . --task task-001 \
  --patch tasks/task-001/golden/solution.patch \
  --output reports/evaluations/task-001/accepted
```

## Security boundary

Path validation, output caps, timeouts, and workspace separation reduce accidental
risk. They do not isolate system calls, network access, child processes, or resource
exhaustion as a hardened sandbox would. Evaluate only trusted patches on a
credential-free machine, VM, or externally sandboxed runner.
