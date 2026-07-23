# Architecture

TypeScript project references enforce dependency direction. `domain` owns contracts;
`persistence` implements ports; `observability` owns structured records; `jobs` owns
idempotency and scheduling; `api` maps HTTP-style inputs and responses; `shared-testkit`
supplies deterministic clocks. All packages emit ESM and declarations.

Task candidates receive baseline and public tests only. The Python evaluator builds a
separate internal copy before held-out tests are overlaid. See `DECISIONS.md`.
