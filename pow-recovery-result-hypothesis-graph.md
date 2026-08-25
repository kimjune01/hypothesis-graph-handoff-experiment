# Result hypothesis graph: expensive-checkpoint recovery

- `A1` [true]: Agent A produced the exact frozen six-node v1 bundle after 6,292,520 candidate hashes. Receipt: Agent A trace, program, measurements, and hidden reconstruction.
- `C1` [true]: the N1 authoritative salt changed from v1 to v2.
- `D1` [true]: under the frozen DAG, `C1` invalidates exactly `{N1,D12,E}` and leaves `{N2,N3,D23}` independently entitled. Receipt: tested transitive-closure rule and exact challenges.
- `N1R` [true]: Notes recovered the exact retraction, preservation, recomputation sets and final bundle with 1,781,267 candidate hashes.
- `G1R` [true]: Graph recovered the same exact sets and bundle with 1,781,267 candidate hashes.
- `M1` [true, existence-scoped]: verifiable memory can perform selective recovery from a stale expensive checkpoint while preserving an independent branch. Depends on `C1 AND D1 AND (N1R OR G1R)`.
- `S1` [true, instance-scoped]: selective recovery avoided 3,674,424 of 5,455,691 full-rebuild candidate hashes (67.35%). Depends on exact deterministic nonces.
- `H1` [false in this instance]: explicit Graph organization improves recovery over equally informative Notes. Killed because exact outcomes and candidate hashes tied while Graph used more wall time and cost.
- `K1` [true]: without corruption, the receiver preserved all six checkpoints and rebuilt none.
- `A2` [untrue/unobserved]: unverifiable attestations force full rebuilding. The planned run failed with HTTP 403 before task work, so no outcome is entitled.
- `F1` [open]: test heterogeneous semantic proof checkpoints whose dependencies are difficult to reconstruct from concise prose.

Retraction rule: if hidden replay invalidates either primary final bundle, retract the corresponding recovery node and any claim depending solely on it. Preserve the other independently passing run.
