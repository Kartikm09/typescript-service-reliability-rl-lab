# Release Process

1. Confirm `main` is clean and all release changes are reviewed.
2. Run `make verify-all`, `make benchmark`, evaluator acceptance/rejection checks,
   the secret scan, and Docker verification.
3. Update `CHANGELOG.md` and `docs/release-notes-v0.1.0.md`.
4. Verify CI on the release commit.
5. Create an annotated semantic-version tag and GitHub release.
6. Re-check the public URL, release assets, and documented commands.

A tag is not created when a required gate is unverified.
