# ADR 0001: Isolated candidate workspaces

**Status:** Accepted

The evaluator first creates a candidate-visible workspace containing only the
task baseline and public tests. It applies the patch there, then makes a separate
internal evaluation copy and overlays held-out tests. Golden material and scoring
internals are never copied into the candidate-visible workspace.

This separation makes leakage tests straightforward. It does not turn local
process execution into a hardened security sandbox.
