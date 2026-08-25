# Concurrent handoff follow-up preregistration

Status: frozen after the original concurrency failure and before this follow-up outcome.

## Correction

The original run remains failed on its common A/B/C overlap criterion. This follow-up adds only the diagnosed missing mechanism:

- three distinct workers must register as post-gate ready;
- no PoW workload may be claimed before all three are ready;
- each worker may hold at most one live claim;
- workers poll while the run is pending instead of exiting on temporary emptiness; and
- every semantic entry packet is captured immutably in canonical JSON.

Tests for barrier blocking/release, simultaneous distinct A/B/C claims, polling, and packet immutability pass before this run.

## Run

Initialize a fresh scheduler with difficulty six and `barrier_target=3`. Start three fresh Codex subagents with `fork_turns="none"` and the unchanged worker wrapper. Each invokes the same claim/discover/publish loop. No run is substituted if a worker or infrastructure call fails.

## Exact success criteria

- F is exactly verified and every accepted receipt passes.
- A, B, and C are claimed by three distinct workers.
- Their claimed intervals have a nonempty common intersection.
- No node-version is accepted twice and no invalid parent-version publication unlocks work.
- Gate order is `GD,GA,GB,GC,GE`; D is killed and never claimed.
- The follow-up is reported separately from, not pooled with, the failed original run.

## Frozen packet audit

`artifacts/concurrent-followup/oracle-{A,B,C}.json` are prospectively frozen minimum-sufficient packets. For each corresponding live claim, the scheduler's captured canonical semantic packet must match its oracle file byte-for-byte.

Compare packet byte counts with `artifacts/concurrent-followup/full-notes.md`. Report the fixed worker-wrapper bytes separately. The audit supports only automatic bounded packet production on these three entry points.

## Claim boundary

A pass may establish that the corrected graph scheduler can release three bounded entry points concurrently and provide sufficient packets in this frozen run. It does not erase the first failure or establish general speedup, scaling, or superiority over human-curated packets.
