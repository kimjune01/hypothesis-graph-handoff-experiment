# Result hypothesis graph: concurrent handoff

- `S1` [true]: every run produced exact verified F with no invalid receipt or duplicate node-version acceptance.
- `E1` [true]: every claim sequence began `GD,GA,GB,GC,GE`; D was killed and never claimed.
- `E2` [true, instance-scoped]: GD avoided the frozen D workload of 23,635,954 candidate hashes. Depends on exact D checker replay.
- `C1` [true, weak]: B and C claim intervals overlapped and both published valid receipts.
- `C2` [false]: A, B, and C had a common overlapping claim interval. Killed by immutable timestamps; startup skew serialized A then B on worker 1.
- `T1` [true, descriptive]: concurrent first-claim-to-F time was 34.403 s versus serial 41.198 s.
- `N1` [true]: the no-update control caused no invalidation, cancellation, or recomputation.
- `V1` [true]: rotating A after old JAB progress invalidated exactly `{A,JAB,F}`, cancelled JAB, preserved `{B,C,X}`, and recovered A→JAB→F at version 2.
- `P1` [untrue/unobserved]: graph packets match frozen oracle-curated packets and reduce context transfer. The comparison artifacts and exact emitted packets were not frozen before outcomes.
- `R1` [untrue/unobserved]: priority scheduling has lower regret than a frozen fixed order. No complete comparator order was frozen.
- `F1` [open]: a preregistered gate/frontier barrier may allow all three frontier intervals to overlap.

Retraction: if any final receipt fails replay, retract its run's `S1` support and dependent timing/safety claims; preserve claims rooted in independently passing runs.
