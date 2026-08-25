# Fail-closed shared memory experiment

Status: revised prospectively after independent subagent audit; not yet implemented or run.

## Claim under test

> This scheduler version preserves declared replay, version, publication, and selective-invalidation safety invariants over a frozen bounded state space, race schedules, crash points, and fault mutants.

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

The reference model is derived from a declarative transition table, not translated line-by-line from scheduler code. Invariant checks are implemented separately from both systems.

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
9. **Atomic publication:** claim acceptance, node verification, publication record, and unlock event are all committed or none are.
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

Before execution freeze:

- exact initial state and versions;
- complete action alphabet and preconditions;
- exact maximum depth;
- maximum unique-state cap;
- state canonicalization and equivalence relation; and
- invariant checker hash.

Enumerate every enabled action/fault to the frozen depth, deduplicating equivalent projected states. Report states, transitions, equivalent states pruned, maximum depth reached, and counterexamples.

Hitting the state cap is an inconclusive/failing layer, never a pass. “Exhaustive” always means only within the frozen DAG, alphabet, and depth.

### 3. Frozen real races

Against SQLite WAL mode, use barriers to run:

- double claim;
- publish versus root invalidation; and
- lease expiry versus publication.

Freeze repetitions and process/thread counts. Assert exact permitted outcomes and invariants after every race. These tests cover real concurrency that the serialized state model does not.

### 4. Pre-commit crash failpoints

Add test-only process failpoints after individual publication/invalidation writes but before commit. Terminate a subprocess at each frozen failpoint, reopen SQLite, and require either the complete transition or the complete pre-transition state—never a partial publication or invalidation.

Transaction-boundary termination alone is insufficient evidence.

### 5. Exact mutation sensitivity

Freeze isolated test-only patches and the invariant expected to kill each:

1. remove receipt validation;
2. omit parent-version comparison;
3. split claim/publication writes outside one transaction;
4. accept an expired token;
5. under-invalidate one descendant;
6. over-invalidate an independent branch;
7. return accepted-token replay after invalidation as current entitlement;
8. validate a receipt against stale rather than claimed-version work; and
9. partially commit invalidation.

Every mutant must be killed. A surviving mutant is a coverage failure even if the unmodified scheduler passes.

## Supplementary robustness evidence

After the load-bearing layers pass, run stateful property testing over generated DAGs:

- 1,000 examples;
- 75 steps maximum;
- 2–8 workers and 4–25 nodes;
- logical clock and deterministic confirmatory seed;
- biased generation around expiry, invalidation, response loss, and shared descendants;
- deadline disabled; and
- persisted minimized counterexamples.

Report transition and transition-pair coverage. Do not call generated serial API sequences real concurrency interleavings. This layer broadens robustness evidence but does not carry the core claim.

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

> Scheduler version X preserved the declared safety invariants over Y completely explored bounded states, Z frozen race schedules, C pre-commit crash points, and all M declared mutants under a trusted checker, scheduler process, SQLite engine, operating system, clock, and storage root.

Even after a pass, do not claim that hypothesis graphs are generally safe, Byzantine-fault tolerant, semantically correct, durable under storage rollback, or automatically confer these guarantees on arbitrary applications.

## Execution order

1. Implement observability, deterministic dependencies, arbitrary fixtures, and semantics test-first.
2. Freeze the transition table, projection, invariants, exhaustive bounds, races, failpoints, and exact mutant patches.
3. Commit and push the preregistration before confirmatory outcomes.
4. Run deterministic and bounded-exploration layers.
5. Run races, crashes, and mutants.
6. Run supplementary property and separate liveness suites.
7. Publish every trace, state count, mutation result, and work-log decision.
