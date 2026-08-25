# Result hypothesis graph: corrected concurrency follow-up

- `O1` [false in original]: original A/B/C intervals lacked common overlap because no readiness barrier existed.
- `I1` [false/infrastructure]: Follow-up 1 performed no claim after a malformed command argument; two workers waited and were interrupted.
- `B1` [true]: Follow-up 2 released no workload until three distinct workers were ready.
- `C1` [true]: distinct workers claimed A, B, C within 7.699 ms and shared 3.443 s of common overlap.
- `S1` [true]: every accepted receipt and final F passed; no node-version duplicated or invalid dependency unlocked.
- `T1` [true, descriptive]: Follow-up 2 took 40.445 s versus serial 41.198 s, only 1.83% less.
- `P1` [true]: emitted A/B/C packets each matched prospectively frozen oracle packets byte-for-byte.
- `P2` [true, artifact-scoped]: each 554-byte packet was 56.82% smaller than 1,283-byte full Notes, avoiding 2,187 payload bytes across three workers.
- `E1` [true]: priority gates ran before workloads and GD prevented D from being claimed.
- `H1` [true, existence-scoped]: graph-addressable handoff supported safe three-worker entry with bounded sufficient packets on this DAG. Depends on `B1 AND C1 AND S1 AND P1`.
- `H2` [untrue/unobserved]: concurrency materially reduces completion time. The observed difference was only 0.753 s and no threshold was preregistered.
- `F1` [open]: repeat on a DAG whose parallel branches dominate model startup, barrier, and join overhead.

Retraction: if any captured packet differs from its frozen oracle or any receipt fails replay, retract the corresponding packet/safety node and all dependent claims.
