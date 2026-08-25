# Fail-closed shared memory experiment

Status: revised prospectively after independent subagent audit; not yet implemented or run.

## Claim under test

> The declarative graph protocol is fail-closed over its frozen bounded state space, and scheduler commit `f88647bb5bcf0647c7d94f5ec702d5816841ce67` conforms on a transition/disposition-complete basis while preserving the same declared invariants under the frozen SQLite races, crash points, and fault mutants.

“Fail-closed” means unsupported or stale results cannot enter verified memory or unlock downstream work. Refusing progress is safe. Liveness is evaluated separately and is not required for this safety claim.

This is an implementation- and boundary-specific claim about shared memory, not model capability or semantic correctness.

## Trusted computing base

Trusted:

- receipt checker and task specification;
- root-admission and root-update authority;
- scheduler process and installed code;
- SQLite engine and transaction semantics;
- operating system, clock source supplied to the scheduler, and storage root; and
- cryptographic hash behavior.

Untrusted workers may crash, retry, delay, reorder, duplicate, corrupt, or omit requests. Direct database writes, checker compromise, scheduler compromise, database rollback, disk loss, and specification inadequacy are excluded.

Root admission is not ordinary worker publication. The implementation must either validate roots under a declared root checker or expose root admission as an explicit trusted operation that cannot target non-root nodes.

## Required observability changes before preregistration

Do not run confirmatory tests until the implementation records enough information to adjudicate its invariants:

1. Claims record `node_version` as well as the parent-version vector.
2. An immutable publication table records claim token, node, node version, parent-version vector, receipt digest, acceptance sequence, and result.
3. Accepted publication events carry the same version information or link to the publication record.
4. Event immutability is either enforced with database triggers and tested, or removed from the protocol guarantee and treated as trusted storage behavior.
5. `progress()` enforces live lease and token status.
6. Accepted-token replay after later invalidation has an explicit rule. Recommended: return the historical accepted result marked `superseded`, never represent it as current entitlement, and never unlock work.
7. Receipt validation uses the claimed node version's frozen work roots, not whichever work happens to be current later.
8. Invalidation scope is defined: root updates are authoritative; internal invalidation is either prohibited or separately specified. Killed-branch reopening semantics are explicit.

The scheduler must also support deterministic testing through an injected logical clock, deterministic token source, and declarative arbitrary-DAG fixtures.

## Observable-state projection

Freeze a projection used to compare a pure reference model with SQLite after every action:

- node ID, state, version, current receipt digest, and frozen work-root digest;
- edges and required parent versions;
- live/expired/cancelled/accepted claim status with node version;
- immutable accepted publication records;
- killed nodes and reopen eligibility; and
- ordered semantic transition kinds.

Exclude random UUID spelling, wall-clock timestamps, SQLite row IDs, JSON whitespace, and other incidental representation. Freeze the equivalence relation before execution.

The reference model is derived from a declarative transition table, not translated line-by-line from scheduler code. Invariant checks are implemented separately from both systems. Complete bounded exploration validates the protocol specification; it is not represented as complete exploration of SQLite. Scheduler correspondence is tested separately by the frozen conformance basis below.

## Load-bearing safety invariants

Check after every transition:

1. **Receipt entitlement:** every verified non-root node has a receipt valid for its accepted node version and frozen work roots.
2. **Version entitlement:** an accepted publication records its claimed node version and the exact currently verified parent versions at acceptance.
3. **Dependency closure:** a verified node's required parents were verified at its recorded versions when accepted.
4. **Unique acceptance:** at most one current acceptance exists for each `(node, version)`; idempotent replay creates no second publication.
5. **Stale exclusion:** unknown, expired, cancelled, superseded, wrong-version, or stale-parent claims cannot verify a node or unlock a child.
6. **Claim exclusivity:** at most one live claim exists per node-version and per worker-run pair.
7. **Exact invalidation:** a root update invalidates every reachable descendant and no unreachable node.
8. **Independent preservation:** unreachable verified nodes retain state, version, and receipt byte-for-byte.
9. **Atomic publication:** claim acceptance, node verification, publication record, and all resulting state/event changes are committed or none are.
10. **Fail-closed rejection:** every rejected or interrupted action leaves invariants 1–9 true.

Audit-record immutability is a separate storage-integrity property unless the revised implementation enforces it explicitly. Priority order is excluded; it is scheduling policy, not fail-closed memory.

## Declared worker fault model

- fail-stop before claim, during work, after progress, before publish, and after commit but before response;
- duplicate, delayed, retried, and reordered public API calls;
- malformed, missing, wrong-node, corrupted, stale-work, and wrong-version receipts;
- unknown, expired, reused, cancelled, and superseded tokens;
- root update before claim, during live descendant work, immediately before publish, and after acceptance;
- two root updates sharing one descendant;
- simultaneous claim races;
- publish-versus-invalidate and expiry-versus-publish races;
- duplicate invalidation and retry after reopen; and
- pass/fail gates with pending, killed, and independent branches.

## Load-bearing evidence

### 1. Deterministic transition suite

Test every permitted transition and rejection path individually, including historical accepted-token replay after invalidation and root admission boundaries. Target complete transition/fault coverage rather than line coverage.

### 2. Complete bounded exploration

Use logical time and deterministic tokens on the frozen diamond DAG `R→A,B; A,B→J` with two workers.

Frozen settings: `initial_diamond(lease_ticks=2)`, two workers, the action alphabet implemented by `_actions`, maximum depth 6, and 20,000 unique states. State canonicalization is `project()`. The model hash is `9a149be6d7ad4f2189980339cb1781f1948e5c1c40e085c6fe2c8a96b76088d3`; explorer hash is `af978deba57a5dfbde127940f056564f099fa8ca7654b6c9e9171742c8d121eb`.

Enumerate every enabled action/fault to the frozen depth, deduplicating equivalent projected states. Report states, transitions, equivalent states pruned, maximum depth reached, and counterexamples.

Hitting the state cap is an inconclusive/failing layer, never a pass. “Exhaustive” always means only within the frozen DAG, alphabet, and depth.

### 3. Frozen model–SQLite conformance basis

Run the two deterministic traces in `fail_closed_conformance.py`: 18 public actions, 20 comparisons after actions and initial states, and exactly these ten dispositions: claimed, not-claimable, unknown-token, invalid-receipt, accepted, current replay, expired, cancelled, root-updated, and superseded replay. Any projected-state mismatch fails. Conformance adapter hash: `b54bacc3d1ff16a787fbd0baf558a906842524680ff4d736766f04431c32fbaf`.

### 4. Frozen real races

Against SQLite WAL mode, run each exact forced schedule once:

- same-node double claim with a two-thread barrier;
- publish-before-root-update and root-update-before-publish; and
- publication immediately before, exactly at, and immediately after lease expiry.

These exact linearizations replace noisy repetition. Assert the permitted outcome and invariants after every schedule. Adversarial test hash: `9bd94e0e94c7a42709b6b7cbfd6d5265e5be0e53b405d140edc29abcb6003316`.

### 5. Pre-commit crash failpoints

Terminate a subprocess at exactly two frozen failpoints: `publication_after_node_write` and `invalidation_after_first_node_write`. Reopen SQLite and require the complete pre-transition state, never a partial publication or invalidation.

Transaction-boundary termination alone is insufficient evidence.

### 6. Exact mutation sensitivity

Run the seven exact isolated source transformations in `fail_closed_mutations.py`: receipt bypass, node/parent-version entitlement bypass, expired-token acceptance, claim-exclusivity loss, under-invalidation, over-invalidation, and split publication transaction. A mutant counts as killed only when its selected test executes and fails (`pytest` exit code 1); collection, usage, interruption, or infrastructure errors fail the layer. Follow-up runner hash: `aad9a73dc56bfcd5acfc7c9ed2b03f5ca810f74c6548057cdaa68c764e381d8c`.

Every mutant must be killed. A surviving mutant is a coverage failure even if the unmodified scheduler passes.

## Cost boundary

This is a bounded mechanism demonstration, not general scheduler certification. Do not add
randomized trials merely to increase a sample count. The confirmatory evidence is limited to:

- one tiny diamond graph explored completely to its frozen depth;
- one deterministic test for each distinct transition or rejection rule;
- the three races above, repeated only enough to exercise both permitted orderings;
- only pre-commit failpoints that separate writes within the publication or invalidation transaction; and
- the seven frozen mutants above.

Generated-DAG property testing is explicitly deferred. It may broaden robustness later, but it
does not carry the present conclusion. Expand the suite only when a new case exposes a distinct
failure mode or trusted-boundary assumption.

## Separate liveness result

Under a frozen fair-worker policy, no further root updates, valid discoverable receipts, and unexpired/reissued leases, test that every reachable frontier eventually reaches terminal verification. Report separately. Safety can pass while liveness fails.

## Pass rule

The fail-closed claim passes only if:

- all deterministic transition tests pass;
- bounded exploration completes below its cap with zero invariant violations;
- every frozen real race has a permitted atomic outcome;
- every pre-commit crash reopens to a complete before/after state;
- every declared mutant is killed; and
- all failures and minimized traces are retained.

Any invariant violation fails this scheduler version. A fix requires a separately preregistered version and rerun.

## Permitted conclusion

> The declarative graph protocol preserved its declared invariants over Y completely explored bounded states. Scheduler commit `f88647b` matched the frozen conformance basis and preserved those invariants across six forced race/boundary schedules, two pre-commit process deaths, and all seven declared mutants under a trusted checker, scheduler process, SQLite engine, operating system, clock, and storage root.

Even after a pass, do not claim that hypothesis graphs are generally safe, Byzantine-fault tolerant, semantically correct, durable under storage rollback, or automatically confer these guarantees on arbitrary applications.

## Execution order

1. Implement observability, deterministic dependencies, arbitrary fixtures, and semantics test-first.
2. Freeze the transition table, projection, invariants, exhaustive bounds, races, failpoints, and exact mutant patches.
3. Commit and push the preregistration before confirmatory outcomes.
4. Run deterministic and bounded-exploration layers.
5. Run races, crashes, and mutants.
6. Run the separate liveness suite.
7. Publish every trace, state count, mutation result, and work-log decision.
