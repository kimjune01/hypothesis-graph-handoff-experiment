# Result hypothesis graph: fail-closed shared memory

- `F0` [false, retained]: confirmatory run 1 appeared to kill seven mutants, but one mutant failed during collection and therefore supplied no mutation evidence.
- `E1` [true, bounded]: the declarative protocol preserved all declared invariants across 14,967 states and 39,288 transitions at frozen depth 6; the 20,000-state cap was not hit.
- `C1` [true, basis-scoped]: SQLite matched the independent model after 20 comparisons covering ten distinct API dispositions.
- `R1` [true, schedule-scoped]: same-node double claim, both publish/root-update orders, and the three exact lease-boundary schedules had only permitted outcomes.
- `A1` [true]: both pre-commit subprocess deaths reopened to the complete pre-transition state.
- `M1` [true]: all seven valid source mutants were killed by executed assertion failures.
- `L1` [true, smoke only]: the existing fair-worker deterministic run reached final verification without further root updates.
- `H1` [true, implementation- and boundary-scoped]: versioned, receipt-checked graph memory failed closed against the declared stale, corrupt, duplicate, expiry, invalidation, and interruption faults. Depends on `E1 AND C1 AND R1 AND A1 AND M1`.
- `H2` [supported as a natural extension]: a hypothesis graph can serve as shared semantic memory whose accepted knowledge has explicit dependency, version, and verification entitlement. Depends on `H1` plus the previously demonstrated bounded graph handoffs.
- `X1` [untrue/unclaimed]: hypothesis graphs generally guarantee semantic correctness, Byzantine tolerance, storage durability, or stronger model reasoning.

Retraction rule: retract `H1` and `H2` if any frozen trace produces a projection mismatch, any explored state violates an invariant, either crash leaves a partial transition, or any declared mutant survives or fails to execute.
