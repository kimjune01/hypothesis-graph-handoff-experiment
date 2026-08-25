# Concurrent handoff experiment round

Status: prospective design only; no instance or outcome has been generated.

## Thesis under test

> Verifiable handoff makes concurrent inquiry safe. Graph-addressable handoff makes it scalable by exposing independently claimable entry points with bounded dependency closures, without transferring the entire inquiry to every worker.

This separates three mechanisms:

1. **Reuse:** workers inherit verified prerequisites instead of rediscovering them.
2. **Concurrency:** independent frontier nodes can be worked simultaneously.
3. **Coordination:** entry-point assignment, publication, joins, and invalidation operate on addressable nodes.

Previous rounds tested single-agent reuse and recovery. They did not test concurrency or coordination.

## Experimental task

Construct one frozen, exactly graded inquiry DAG:

```text
                 R0
          /       |       \
        A1        B1       C1       D1
         \       /          \       /
           JAB                JCD
              \              /
                       F
```

- `R0` is a shared verified root.
- `A1`–`D1` are four independently actionable, expensive-to-discover checkpoints.
- `JAB` and `JCD` require their two parents.
- `F` requires both joins.
- Every node has pinned roots, an executable receipt, a kill condition, and a deterministic output contract.

Use heterogeneous bounded certificate tasks rather than six identical hashes if construction remains exactly gradeable: for example, one SAT witness, one bounded counterexample search, one optimization certificate, and one deterministic proof-of-work checkpoint. Verification must be much cheaper than discovery. If heterogeneous cost cannot be matched prospectively, use calibrated deterministic PoW and state that the demonstration concerns coordination rather than semantic reasoning.

Four workers start concurrently on `A1`–`D1`; join workers become eligible only after their prerequisites verify. A coordinator or scheduler owns assignment and publication. No worker may receive an answer for its own open node.

## Conditions

### 1. Shared Notes

Every worker receives the same complete chronological inquiry notes, including all verified facts and dependency statements. The coordinator announces assignments in prose. Workers must locate their own prerequisite closure and report completion back through the shared log.

### 2. Curated note packets

A coordinator reads the chronological notes and manually prepares a task-local packet for each worker: objective, verified prerequisite closure, checks, output contract, and publication target. This is the strongest non-graph handoff and controls for the benefit of bounded context alone.

Packet-production time, coordinator tokens, and omissions are included in total cost.

### 3. Graph entry packets

A mechanical scheduler queries open nodes, atomically claims one per worker, computes its prerequisite closure, and emits the same packet fields from the graph. Verified publications automatically unlock joins. Workers receive no full graph unless requested.

The intervention includes graph-native addressability, closure queries, claiming, unlocking, and invalidation. It is not merely graph-shaped prose.

## Experiment A: concurrency mechanism

Compare one worker executing the frozen graph serially with four workers executing independent frontier nodes concurrently using Graph entry packets.

Primary existence criterion:

- both produce the exact certified final result; and
- concurrent wall time from frontier release to all four branch publications is less than serial wall time, with CPU/API contention reported.

This demonstrates that independently verifiable handoffs permit safe parallel execution. It does not establish a general speedup.

## Experiment B: entry-point scalability

Run Shared Notes, Curated Packets, and Graph Packets with the same four-worker topology.

Primary measurements:

- exact final certification and prerequisite compliance;
- context bytes/tokens delivered to each worker before its first useful action;
- total context transferred across workers;
- time and cost to produce entry packets;
- time to first useful action per worker;
- duplicate node work and conflicting claims;
- invalid early starts at `JAB`, `JCD`, or `F`;
- wall-clock critical-path completion;
- coordinator messages, tokens, and interventions.

The graph supports a scalability claim only if it matches the curated-packet condition on worker correctness and context while reducing packet-production or coordination cost. Beating Shared Notes alone shows that selective handoff helps, not that a graph is necessary.

## Experiment C: concurrent invalidation

After `A1` and `C1` publish and while downstream work is active, rotate one pinned root of `A1`. Freeze the event time by a task-state trigger, not wall-clock timing.

The correct response is to:

- invalidate `A1`, `JAB`, and `F`;
- preserve `B1`, `C1`, `D1`, and `JCD`;
- cancel or reject publications rooted in stale `A1`;
- reassign only the invalid frontier; and
- resume joins after replacement receipts verify.

Measure propagation latency, wasted worker actions/tokens, over- and under-invalidation, stale publication acceptance, coordinator interventions, and recovery wall time.

## Controls

- Same underlying Agent A trajectory and substantive facts projected into all conditions.
- Same worker prompts, models, tools, budgets, start barrier, and node assignments where the condition permits assignments.
- Exact graders for every node and final join; no LLM judge for correctness.
- Packet content parity test: Graph and Curated packets must expose the same claims, receipts, roots, and contracts.
- No-update control to detect unnecessary cancellations.
- Serial oracle schedule to establish the correctness and critical-path ceiling.
- Log all failed launches and infrastructure/model-routing changes without replacement.

## Preregistered claims

One frozen round can support only existence claims:

- **Concurrency:** verifiable node handoffs can support correct concurrent execution on this DAG.
- **Bounded transfer:** graph queries can produce sufficient worker entry packets smaller than the full inquiry context.
- **Coordination:** graph-native scheduling can claim, unlock, and selectively invalidate work correctly on this run.

It cannot establish typical speedup, scaling curves, or superiority across tasks. Those require multiple DAG sizes and repetitions.

## Falsification

- If concurrent Graph execution violates dependencies or fails exact grading, the safety demonstration fails.
- If Curated Packets match Graph including coordinator production cost, the graph-specific scalability claim is null.
- If Graph wins only because its workers receive less substantive information, the comparison is invalid.
- If all conditions are dominated by model startup latency or local CPU contention, wall-clock conclusions are withheld while correctness and context-transfer results remain reportable.

## Recommended execution order

1. Build and test the exact DAG, scheduler, claim lock, and graders.
2. Calibrate node costs before freezing the instance.
3. Run the serial oracle and no-update control.
4. Freeze Agent A trajectory and all three projections.
5. Randomize the three concurrent conditions.
6. Run Experiment B, then the independently preregistered invalidation probes.
7. Publish raw per-worker traces, packet contents, scheduler events, exact grades, and an append-only work log.
