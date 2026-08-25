# Corrected concurrent handoff follow-up results

## Outcome

Follow-up 2 passed every preregistered correctness, concurrency, economy-gate, and packet criterion. It remains separate from both the original failed overlap run and Follow-up 1's launch failure.

## Concurrent entry

- A claimed by `followup2-3` at `t=0.000000` relative to the first frontier claim.
- B claimed by `followup2-2` 1.643 ms later.
- C claimed by `followup2-1` 7.699 ms after A.
- All three intervals overlapped from C's claim until A's acceptance: 3.443 seconds.
- Every node receipt passed, F verified, no node-version was accepted twice, and no stale dependency publication unlocked work.

The readiness barrier corrected the diagnosed launch defect. All three workers registered after gate completion before any PoW frontier claim; one-live-claim enforcement distributed A, B, and C across distinct workers.

First frontier claim to F took 40.445 seconds. The earlier serial oracle took 41.198 seconds, a descriptive reduction of only 0.753 seconds (1.83%). CPU contention and the long B node dominated the critical path. The result demonstrates safe concurrency, not useful speedup.

## Economy of search

Gate claims remained exactly `GD,GA,GB,GC,GE` before workloads. GD killed D, which was never claimed, preserving the previous exact avoided-work receipt of 23,635,954 candidates. This is cheap discrimination before expensive branch release; it is not evidence about an unfrozen scheduling-regret comparator.

## Bounded entry packets

The scheduler immutably captured canonical packets for all claims. Prospectively frozen A/B/C oracle packets matched their emitted packets byte-for-byte.

| Entry | Worker | Graph packet | Oracle match |
|---|---|---:|---:|
| A | followup2-3 | 554 bytes | yes |
| B | followup2-2 | 554 bytes | yes |
| C | followup2-1 | 554 bytes | yes |

Full chronological Notes were 1,283 bytes. A task-local packet was 729 bytes (56.82%) smaller. Across three initial workers, payload transfer was 1,662 bytes rather than 3,849, avoiding 2,187 bytes. The fixed worker wrapper was 880 bytes per worker and is reported separately; assignment-message and model-token accounting were not exposed canonically.

The packets contain objective, direct verified prerequisite receipt and version, exact work root, check, kill condition, and output contract. They contain no open-node answer. This establishes that graph queries automatically produced sufficient bounded entry points on this DAG. It does not show that a human could not curate the same packets; indeed, the oracle files demonstrate equivalence.

## Integrity history

- Original concurrent run: exact final pass but failed common A/B/C overlap because no barrier existed.
- Follow-up 1: infrastructure failure before claims because worker 1 received an accidental trailing `.` argument; workers 2/3 were interrupted at the barrier.
- Follow-up 2: separately preregistered command-format correction; passed.

No result was overwritten or pooled.

## Supported existence claims

On this frozen DAG, a versioned graph scheduler can:

- release three independently claimable frontiers to distinct concurrent workers;
- enforce prerequisite/version safety through exact publication;
- issue sufficient entry packets 56.82% smaller than the full Notes artifact; and
- run cheap discriminating gates before expensive branch release.

Unsupported: material wall-time speedup, asymptotic scalability, typical context savings, or superiority over curated packets.
