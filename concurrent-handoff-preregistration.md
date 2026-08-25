# Concurrent graph handoff preregistration

Status: frozen before serial or concurrent worker outcomes.

## System and DAG

The tested system is the executable versioned scheduler in `concurrency_scheduler.py`, with node work in `concurrency_work.py` and the worker client in `concurrency_worker.py`.

Verified root `R0` opens five gates. Frozen gate order by expected decisive yield/cost is `GD`, `GA`, `GB`, `GC`, `GE`; stable ties use committed `tie_order`. `GD` checks composite 21 and kills expensive child D. The other prime checks open A, B, C, and X. A and B unlock JAB; JAB, C, and X unlock F.

All PoW nodes use committed challenge `frozen:{node}` and six leading hexadecimal zeroes. Pre-run calibration observed: A 8,641,801 candidates/2.715 s; B 44,853,054/14.413 s; C 18,331,937/5.789 s; X 4,028,979/1.285 s; JAB 10,321,645/3.272 s; F 19,179,632/5.964 s. These observations fixed difficulty; no alternate challenge was selected.

## Runs

1. **Serial oracle:** one fresh Codex worker invokes the claim/discover/publish loop until F verifies.
2. **Concurrent entry:** three fresh Codex workers with `fork_turns="none"` invoke the identical loop against one new scheduler database.
3. **No-update control:** three fresh workers; after JAB records at least 10,000 candidates, observe without rotating a root. No claim may be cancelled.
4. **Invalidation:** three fresh workers; after JAB is live and records at least 10,000 candidates, change A's challenge to `frozen:A:v2`. Expected invalidation is exactly A, JAB, F; B, C, and X remain verified. A stale JAB publication must not be accepted. Workers then recover to one valid F.

Fresh worker prompts contain only the fixed wrapper and command. Workers acquire task-local packets through atomic claims. Filesystem isolation is behavioral because all subagents share the workspace.

## Exact criteria

Concurrency safety passes if F verifies, all accepted receipts pass, every accepted node had verified parents at its claimed versions, no node is accepted twice, and A/B/C claimed intervals overlap.

Economy of search passes if every claim is priority-maximal at claim time, all five gates are claimed before any workload, D is killed and never claimed, and the fixed-order counterfactual cost of D is reported as avoided.

Invalidation passes if scheduler events show exact affected set `{A,JAB,F}`, preservation `{B,C,X}`, cancellation/rejection of old-version JAB, and exact recovery to F. No-update passes if no cancellation, invalidation, or recomputation occurs.

## Packet audit

For every accepted claim, mechanically reconstruct the graph packet and compare it with a frozen oracle-curated packet field-for-field. Report canonical UTF-8 bytes of full Notes, oracle packet, graph packet, and fixed wrapper separately. This audit establishes automatic bounded packet production, not superiority to human curation.

## Measurements and claims

Record scheduler events, node intervals, candidate hashes, wall time, worker/model usage where available, prompt and packet bytes, stale rejections, cancellations, avoided D work, and setup cost.

One round supports only existence claims: safe concurrency occurred; priority scheduling pruned one expensive branch; bounded packets were emitted; or versioned recovery localized one stale subtree. No significance test, scaling claim, or general Notes comparison is permitted.

No failed run is replaced. Infrastructure failures and model routing remain in the work log.
