# Acceptance Criteria

- Schedule a delivery at an absolute timestamp.
- Cancellation prevents pending delivery.
- Retry policy bounds transport attempts.
- Events use discriminated unions.
- Pending IDs are unique; duplicate scheduling is rejected without replacing the original cancellation handle.
- A retry budget is a positive safe integer; invalid budgets and non-finite times are rejected before enqueueing.
- Exhausted attempts emit one `failed` event and no `completed` event.
- Cancellation applies to pending work; after execution begins `cancel` returns false.
