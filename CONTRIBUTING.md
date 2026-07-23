# Contributing to TypeScript Service Reliability RL Lab

Thank you for considering a contribution. This repository is an independent,
synthetic proof-of-work project. Contributions must remain defensive,
reproducible, and free of confidential material.

## Workflow

1. Open or select a scoped issue before substantial work.
2. Create a branch from `main` using `type/short-description`.
3. Keep one concern per pull request and add or update tests.
4. Run `make verify-all` and include the commands and relevant output in the PR.
5. Update documentation, fixtures, and `CHANGELOG.md` when behavior changes.
6. Request review only after the pull-request checklist is complete.

## Task-environment changes

Changes to held-out tests, scoring, golden patches, or allowed paths receive
additional review. A task change must explain why the reward remains
deterministic and why the candidate workspace does not reveal evaluation-only
assets.

## Review standard

Reviewers prioritize correctness, regression safety, deterministic evidence,
and security boundaries. Style feedback is important but cannot outweigh
functional correctness in evaluation scoring.

By participating, you agree to follow `CODE_OF_CONDUCT.md`.
