# Result hypothesis graph: verifiable-memory 2×2

- `P1` [true]: all four primary cells passed the exact grader. Receipt: four `answer.json` files and deterministic grader.
- `P2` [true]: every primary cell reused R1–R3, replayed three checks, and ran zero DLog searches. Depends on primary traces and continuation reports.
- `H1` [false in this pilot]: Graph reduces unnecessary rederivation more than Notes, especially under joint dependency. Killed because both formats had zero rederivation in both rows.
- `H2` [false in this pilot]: Graph has a favorable joint-versus-independent cost interaction. Killed by observed duration interaction `+10.973 s` and cost interaction `+$0.061178`, both unfavorable to Graph.
- `V1` [true, scoped]: both Notes and Graph transmitted the three verified residues as reusable interfaces under the shared protocol. Depends on `P1 AND P2`.
- `R1` [true, scoped diagnostic]: Graph supported targeted retraction and repair of one corrupted checkpoint while preserving independent checkpoints. Depends on corrupted-probe trace and exact pass.
- `L1` [true]: discovery was cheap (0.00–0.01 s per Agent A DLog), limiting ecological sensitivity.
- `L2` [true]: one run per cell and unequal artifact lengths prohibit population or format-efficiency claims.
- `F1` [open]: repeat with tasks whose verified checkpoints are expensive to rediscover and whose downstream chain contains multiple heterogeneous proof interfaces, while matching artifact budgets.

Retraction rule: if any primary answer fails independent replay, retract `P1`, `V1`, and any dependent interpretation; preserve the diagnostic claims whose own receipts still pass.
