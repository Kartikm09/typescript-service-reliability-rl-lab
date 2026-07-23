# ADR 0002: Deterministic reward model

**Status:** Accepted

Stage weights are explicit in each `evaluator_config.json`. Functional build,
correctness, and regression evidence dominate the score. Formatting, static
analysis, documentation, and performance receive smaller bounded weights.
Commands use fixed fixtures and seeds; timing thresholds are avoided when a
deterministic work metric can express the requirement more reliably.
