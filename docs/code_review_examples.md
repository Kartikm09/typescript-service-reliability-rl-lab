# Constructive Code-Review Examples

**Correctness blocker**

> The retry branch updates the status before persistence succeeds. Could we add a
> regression test for the storage failure and move the transition after commit?

**Concurrency blocker**

> This closes the channel while producers may still send. Please show the
> ownership invariant and add a deterministic cancellation test under the race
> detector or equivalent concurrency checker.

**Performance evidence request**

> The allocation reduction looks promising. Please attach the baseline and
> candidate benchmark commands, sample counts, and variance before we change the
> threshold.

**Non-blocking maintainability suggestion**

> Optional: extracting the error mapping could make the public contract easier to
> scan. This should not block the functionally correct patch.

These are examples of review phrasing, not records of external reviews.
