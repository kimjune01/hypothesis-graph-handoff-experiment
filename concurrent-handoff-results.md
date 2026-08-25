# Concurrent graph handoff results

## Verdict

The round demonstrated exact priority scheduling, safe two-worker overlap, and selective versioned recovery. It did **not** pass the preregistered three-frontier concurrency criterion, and the bounded-packet comparison was not validly instantiated.

## Runs

| Run | Exact F | First claim→F | Gate order | D pruned | A/B/C all overlap | Invalidated | Cancelled |
|---|---:|---:|---:|---:|---:|---|---|
| Serial oracle | yes | 41.198 s | exact | yes | no, by design | — | — |
| Concurrent | yes | 34.403 s | exact | yes | **no** | — | — |
| No update | yes | 33.410 s | exact | yes | no | none | none |
| A-root update | yes | 54.767 s | exact | yes | no | A, JAB, F | old JAB claim |

Every accepted receipt passed the exact checker. No node-version was accepted twice and no dependency-invalid publication unlocked a child.

## Economy of search

Every run claimed gates in the frozen priority order `GD, GA, GB, GC, GE` before any expensive workload. GD's cheap composite verdict killed D, which was never claimed.

The deterministic D counterfactual required 23,635,954 candidate hashes and 7.331 seconds in the same local implementation. That work was avoided in every run. This demonstrates the intended cheap, high-uberty move: a cheap discriminating check eliminated an expensive branch before worker occupancy.

The preregistration did not freeze a complete non-priority scheduling order. Scheduling regret against such an order is therefore unobserved and is not reconstructed post hoc.

## Concurrency

The concurrent run completed 6.795 seconds (16.49%) sooner than serial from first claim to F. B and C overlapped, proving that independently claimed work could execute safely in parallel.

However, A completed before B began, and C began after A completed. The required common overlap among A, B, and C was false. Worker startup skew allowed the first worker to clear all five cheap gates and claim A before the other workers entered; it then claimed B immediately after A. The experiment lacked a true start barrier between gate completion and frontier release.

Therefore:

- safe concurrent execution occurred for a two-node overlap;
- the exact final result and dependency safety passed; but
- the preregistered three-frontier concurrency demonstration failed.

The run is not replaced. A corrected barrier would be a separately preregistered follow-up.

## Versioned invalidation

After old-version JAB recorded progress, the trigger rotated A's challenge. The scheduler invalidated exactly `A, JAB, F`, preserved verified `B, C, X`, and changed the active JAB claim to `CANCELLED`. At its next progress call the worker received `StalePublication: cancelled claim`; it did not publish the stale result. One prospective retry rebuilt and verified A, JAB, and F at version 2.

No-update caused no invalidation, cancellation, or recomputation. The versioned recovery mechanism therefore passed in this frozen case.

## Entry packets

The scheduler emitted direct-parent packets during runs, and tests establish their bounded schema. But the oracle-curated packets and full Notes artifact were not frozen before execution, and exact emitted packets were not retained in the event log. The preregistered field-equivalence and byte-transfer audit is therefore unobserved. It must not be reconstructed after outcomes.

## Supported claims

- A graph scheduler can atomically claim and safely publish exactly checked nodes with versioned dependency contracts.
- In this instance, a cheap priority-maximal gate prevented 23,635,954 hashes of unnecessary work.
- Two independent workers overlapped without invalid publication.
- A version change cancelled one active stale join, preserved the independent branch, and recovered exactly the affected subtree.

Unsupported: full three-worker concurrency, bounded-context savings, scheduling regret, scalability, or superiority over curated Notes.
