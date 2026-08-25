# Fail-closed shared memory experiment

Status: prospective design; no new fault-testing outcome has been generated.

## Claim under test

> Within a declared bounded fault model, the hypothesis graph preserves replay, version, publication, and selective-invalidation invariants under concurrent agent use.

This is a reliability claim about the shared-memory protocol, not a claim that models reason better. “Fail-closed” means an unsupported or stale result cannot enter verified memory or unlock downstream work; the system may refuse progress rather than accept an unentitled claim.

The experiment tests the executable state machine, not LLM judgment. Workers are modeled as untrusted clients that may fail, retry, delay, duplicate, corrupt, or reorder requests.

## System under test

The SQLite-backed scheduler in `concurrency_scheduler.py`:

- versioned nodes and parent-version vectors;
- atomic claim tokens and leases;
- exact receipt checking;
- idempotent publication;
- dependency-directed opening;
- transitive invalidation and cancellation; and
- immutable event and packet records.

Use a pure in-memory reference model implementing the same public contract independently. Every generated action is applied to both the reference model and the SQLite implementation; observable state and invariant verdicts are compared after every step.

## Safety invariants

Check after every transition:

1. **Receipt entitlement:** every `VERIFIED` non-root node has a receipt that passes its current checker.
2. **Version entitlement:** every accepted publication's parent-version vector equals the currently verified parent versions at acceptance.
3. **Dependency closure:** a `VERIFIED` node has all required parents verified at the recorded versions.
4. **Unique publication:** at most one publication is accepted for each `(node, version)`.
5. **Stale exclusion:** an expired, cancelled, unknown, or stale-parent claim never changes a node to `VERIFIED` and never unlocks a child.
6. **Exact invalidation:** changing root `r` invalidates every reachable descendant and no unreachable node.
7. **Independent preservation:** unaffected verified nodes retain version, receipt, and verified state byte-for-byte.
8. **Claim exclusivity:** at most one live claim exists per node-version and per worker-run pair.
9. **Idempotency:** repeating a successful publish returns the original result without a second state transition.
10. **Audit monotonicity:** committed event and packet records cannot be changed or deleted through the public protocol.
11. **Priority safety:** priority changes which eligible node is claimed, never whether an ineligible node becomes claimable.
12. **Fail-closed recovery:** after a rejected action, the graph remains in a state satisfying invariants 1–11.

Liveness is separate. Under a fair worker that eventually submits valid receipts and without further root changes, every reachable open frontier should eventually reach the terminal verified result. This conditional property must not be conflated with safety: refusing progress still passes fail-closed safety.

## Declared fault model

### Included

- worker fail-stop before claim, during work, after progress, before publish, and after publish response loss;
- duplicate, delayed, retried, and reordered claim/progress/publish requests;
- unknown, expired, reused, and cancelled claim tokens;
- missing, malformed, corrupted, wrong-node, and wrong-root receipts;
- lease expiry immediately before progress or publication;
- one or two root rotations before, during, and after descendant work;
- stale publication after invalidation;
- simultaneous claim races from multiple workers;
- simultaneous publication and invalidation transactions;
- duplicate invalidation and retry after database reopen;
- process termination at transaction boundaries followed by SQLite reopen;
- gates that pass, fail, or change version while descendants are pending;
- independent branches sharing one ancestor.

### Excluded

- a malicious client with direct write access to the SQLite database or scheduler process;
- corruption of the checker, task specification, scheduler binary, SQLite engine, or operating system;
- disk loss, undetected storage corruption, compromised cryptographic hashes, or rollback of the entire database;
- distributed multi-primary databases, network partitions, or clocks outside the single-host lease assumptions;
- semantic inadequacy of a correctly replayed predicate.

These exclusions bound the claim. The protocol guards against untrusted workers, not a compromised verifier or storage root.

## Test architecture

### Layer 1: deterministic unit and transition tests

Cover every public transition and rejection path individually. Target 100% transition coverage, not line coverage as a proxy.

Required cases include claim race, valid publish, every invalid receipt form, idempotent retry, expiry, cancellation, reopening, gate kill, root rotation, exact closure, preserved branch, stale publish, and terminal state.

### Layer 2: bounded exhaustive model exploration

Use a minimal diamond graph `R→A,B; A,B→J` with two workers. Enumerate every enabled action and included fault through a frozen depth sufficient to contain claim, invalidation, expiry, retry, and recovery cycles. Canonicalize equivalent states to avoid exploring action-order permutations that yield the same state.

Freeze before execution:

- graph and initial versions;
- action alphabet;
- maximum depth and state cap;
- state-canonicalization rule; and
- exact invariant checker.

Report explored states, transitions, pruned equivalent states, and whether the cap was reached. Call this exhaustive only within those explicit bounds.

### Layer 3: stateful property-based testing

Use Hypothesis stateful testing against larger generated DAGs.

Prospective defaults:

- 10,000 examples;
- up to 200 state-machine steps per example;
- 2–8 workers;
- 4–25 nodes;
- fixed CI seed plus a second non-derandomized exploratory run;
- deadline disabled; and
- persistence of every minimized counterexample.

Bias generation toward boundary events: publication at lease expiry, invalidation immediately before publish, two roots changing across a shared descendant, response loss after commit, and stale retry after reopen.

The confirmatory run uses frozen settings and is never silently rerun after failure. Hypothesis shrinking supplies the minimal receipt for any violation.

### Layer 4: concurrency and crash integration

Run real threads/processes against SQLite WAL mode:

- synchronized double-claim races;
- publish-versus-invalidate races;
- kill worker processes at frozen checkpoints;
- close and reopen the database after each injected crash; and
- repeat accepted publication after simulated response loss.

Use a frozen race count and process count. Record transaction results and full event logs. Do not infer exhaustive concurrency coverage from stress testing.

## Mutation sensitivity

Create isolated test-only mutants, one at a time:

1. remove receipt validation;
2. omit the parent-version comparison;
3. permit two live claims;
4. accept an expired token;
5. under-invalidate one descendant;
6. over-invalidate an independent branch;
7. allow duplicate node-version acceptance;
8. let stale publication unlock children; and
9. make packets or events mutable.

The experiment is sensitive only if the suite kills every declared mutant with the expected invariant. Surviving mutants are evidence of a coverage gap, even if the unmutated implementation passes.

## Preregistered outcome

The strong claim passes only if:

- all deterministic transition tests pass;
- bounded exploration finishes without invariant violation or clearly reports reaching its cap;
- the confirmatory 10,000-example stateful run has zero invariant violations;
- all frozen crash/race cases preserve safety;
- the conditional liveness checks pass under their fair-worker assumptions; and
- every declared mutant is killed.

Any invariant violation fails the claim for the declared model. Fixes require a new version and separately preregistered rerun; the failing trace remains published.

## Evidence and reporting

Publish:

- fault-model manifest;
- reference model and SUT adapter;
- invariant definitions;
- generator settings and seeds;
- state/transition counts;
- minimized counterexamples;
- race/crash event logs;
- mutation matrix;
- code and artifact hashes; and
- append-only work log.

The permitted conclusion is:

> Version X preserved all declared safety invariants across Y bounded states, Z stateful interleavings, the frozen crash/race suite, and all declared fault mutants.

Do not shorten this to “the graph is safe” or extend it beyond the included faults and trusted computing base.

## Relationship to an ecological demonstration

The state-machine experiment is load-bearing for reliability. A later real coding-agent case is useful for ecological relevance, but it is not required to establish the bounded protocol invariant. Keep that case separate so model behavior cannot weaken or inflate the systems guarantee.

## Execution order

1. Freeze the fault model and trusted computing base.
2. Write invariant and mutant-sensitivity tests before changing the scheduler.
3. Implement the independent reference model and SUT adapter.
4. Run deterministic tests and bounded exploration.
5. Freeze property settings, seeds, and crash schedule.
6. Commit and push the preregistration before confirmatory outcomes.
7. Run stateful, concurrency/crash, liveness, and mutation suites.
8. Publish every failure and minimized trace; do not replace runs.
