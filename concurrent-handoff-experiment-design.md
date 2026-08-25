# Concurrent graph handoff experiment

Status: revised prospectively after independent subagent review; no instance or outcome has been generated.

## Claim under test

> A versioned hypothesis graph can expose bounded, independently claimable entry points; support correct concurrent execution; and localize cancellation and recovery when an upstream root changes.

This is a mechanism demonstration, not a population comparison. Previous rounds showed that concise Notes can equal Graph for single-agent reuse and recovery. This round tests graph-native querying, claiming, unlocking, version checking, and invalidation—not graph-shaped prose.

## Feasible frozen DAG

The environment permits three concurrent child workers because the root coordinator occupies the fourth slot:

```text
                  R0
               /  |  \
              A   B   C
               \ /
               JAB
                 \ /
                  F
```

Edges: `R0→A`, `R0→B`, `R0→C`, `A→JAB`, `B→JAB`, `JAB→F`, `C→F`.

Use calibrated deterministic proof-of-work certificates. Frontier discovery should take approximately 15–30 seconds single-core; joins 5–10 seconds. Verification is one hash. Freeze challenges, lowest-valid nonces, process/thread count, and calibration before agent runs. Workers invoke provided `discover` and `check` commands; they do not edit scheduler or verifier code.

PoW gives controlled work and exact receipts, but it has almost no epistemic uberty: every nonce is known to exist and no hypothesis is genuinely at risk. It therefore tests concurrency and coordination only. Economy of search is tested through a separate set of cheap discriminating gates described below; do not infer search fertility from PoW completion.

## Executable scheduler semantics

Node states are `BLOCKED`, `OPEN`, `CLAIMED`, `VERIFIED`, and `STALE`.

1. `BLOCKED→OPEN` exactly when all parents are `VERIFIED` at recorded versions.
2. Claim is an atomic compare-and-swap `OPEN→CLAIMED` carrying worker ID, run ID, lease, claim token, and parent-version vector.
3. Publish is accepted only with a live token and lease, unchanged verified parent versions, and an exact valid receipt.
4. Otherwise publication is rejected as stale or invalid and cannot unlock children.
5. Root rotation increments its version, marks it stale, transitively marks descendants stale/blocked, and cancels only affected live claims.
6. Retry and publication are idempotent. Every transition enters an immutable event log.

Before agents run, tests must cover double-claim races, expired claims, duplicate publications, stale parent-version publications, exact transitive invalidation, unaffected-branch preservation, and deterministic reopening.

The root may start workers and observe events, but must not manually assign substantive node context or relay dependency results. Workers claim and publish through the scheduler.

## Economy-of-search scheduling

Scheduling among simultaneously `OPEN` nodes follows Peirce's economy of research: buy the greatest expected decisive yield per unit cost first.

For node `v`, freeze before outcomes:

```text
priority(v) = expected_decisive_yield(v) / expected_cost(v)
```

`expected_decisive_yield` is the preregistered expected amount of downstream work that the node's possible verdicts will either validly unlock or prune. It is not confidence, downstream node count alone, or a reward assigned after seeing the result. `expected_cost` includes predicted tool time, model tokens, and scarce worker occupancy. Scores, priors, estimates, and stable tie-breaking order are committed before runs; realized nonce counts or hidden answers may not influence priority.

Add five cheap, exactly checked gate nodes `GA`–`GE`, all initially open and competing for three workers. Each gate tests a bounded proposition whose pass/fail verdict controls a substantially more expensive successor branch. At least one frozen gate fails and legitimately kills its branch; others unlock work with unequal downstream costs. Their outcomes remain hidden from workers but are fixed before scheduling.

The scheduler must:

1. claim the highest-priority open gates first;
2. publish and propagate each verdict before assigning newly avoidable expensive work;
3. never start a killed successor;
4. recompute priorities only from changed public graph state, using the frozen scoring rule; and
5. record the counterfactual cost of a fixed-order schedule from the same frozen node costs.

Primary economy-of-search receipt:

- every claimed node was maximal under the frozen priority rule at claim time;
- all cheap discriminating gates completed before any lower-yield expensive node that they could prune;
- the failed gate prevented its entire expensive branch from being claimed; and
- exact avoided candidate hashes/tokens and scheduler regret versus the frozen fixed order are reported.

This gate demonstration supports only that the scheduler executed a cost-and-uberty ordering and avoided known unnecessary work in this instance. It does not validate the prior yield estimates or establish that the scoring rule is generally optimal.

## Experiment A: safe concurrent entry

Start three fresh Codex subagents with the same minimal wrapper and access only to the scheduler client. Each calls `claim`, receives a mechanically generated entry packet, discovers and checks its node, and calls `publish`. Idle workers may subsequently claim `JAB` and `F` as they open.

Run the identical frozen nodes through the same scheduler with one worker and no overlap as a serial oracle.

Existence criteria:

- both runs produce an exact final certificate;
- `A`, `B`, and `C` have overlapping claimed intervals;
- no node starts before prerequisites verify;
- each node is accepted exactly once;
- no packet contains the answer to its open node; and
- concurrent frontier wall time is below serial frontier wall time, with contention reported.

Failure of the timing criterion does not erase a passing safety result.

## Experiment B: bounded entry-packet audit

This is an artifact audit, not three noisy end-to-end trials. For each open node construct prospectively:

1. the complete chronological Notes artifact;
2. an oracle-curated minimum-sufficient note packet; and
3. the mechanically emitted Graph packet.

Oracle and Graph packets must be field-for-field equivalent on objective, verified prerequisite claims, roots, receipts, checks, kill conditions, output contract, and publication target. Neither may contain the open-node answer.

Measure canonical UTF-8 bytes, full delivered prompt bytes separately, observable model input tokens, dependency-closure completeness, extraneous-node count, and mechanical packet-generation time. Report graph/scheduler authoring as setup cost or explicitly exclude it from the runtime claim.

Success shows that a graph query can automatically emit a sufficient bounded handoff. It does not show that a human could not curate an equivalent packet.

## Experiment C: versioned invalidation during concurrency

Give `A` its own versioned root; do not rotate shared `R0`. Trigger the update only after:

1. `A` and `B` verify;
2. `JAB` is claimed with its parent-version vector;
3. its worker records a frozen progress marker after a specified chunk; and
4. JAB has not published.

Then rotate A's root. Expected behavior:

- invalidate `A`, `JAB`, and `F`;
- preserve `B`, `C`, and their receipts;
- cancel the active JAB claim;
- reject any later JAB publication carrying old A version;
- reopen and recompute A, then JAB, then F; and
- accept one exact final certificate.

Measure propagation and cancellation latency, stale publication rejection, wasted hashes after the trigger, over/under-invalidation, coordinator interventions, and recovery time. A no-update control uses the same marker but causes no cancellation or recomputation.

## Measurements

- exact per-node and final grading;
- claim, first-tool-call, progress, publish, accept/reject, cancel, and reopen timestamps;
- condition payload bytes, full prompt bytes, and observable input tokens;
- hashes per node;
- duplicate accepted work and double-claim attempts;
- scheduler messages and transitions;
- stale publications accepted/rejected;
- over/under-invalidation; and
- wall time, critical path, model cost, CPU/process count, and setup cost.
- frozen expected cost, expected decisive yield, priority score, realized decisive yield, avoided work, and scheduling regret.

Use claim-to-first-tool-call and claim-to-valid-publication timestamps rather than subjective “first useful action” judgments.

## Controls and integrity

- TDD for scheduler, lock, version, packet, and exact-grader semantics.
- Same Codex model family, wrapper, tools, budgets, and scheduler in serial and concurrent runs.
- Fresh subagents with `fork_turns="none"` and node-local packets only.
- Behavioral filesystem isolation disclosed; all agents technically share the workspace.
- Hashes of tasks, packets, code, roots, and graders frozen before outcomes.
- No failed run replaced; infrastructure/model-routing changes remain logged.
- Publish raw worker traces, scheduler events, packets, grades, and work log.

## Claim boundary

A passing round may show that safe concurrent execution occurred, graph queries emitted sufficient bounded packets, and versioned coordination rejected a stale publication and selectively recovered one subtree.

It may not show general superiority over curated Notes, persistent speedup, asymptotic scalability, or better reasoning from graph syntax. The treatment is explicitly a systems bundle—executable graph scheduler versus static artifacts—not a representation-only comparison.

## Execution order

1. Implement scheduler, client, generator, packet audit, and graders test-first.
2. Calibrate work; freeze gate propositions, hidden outcomes, cost/yield estimates, priority scores, and the instance.
3. Pass race and invalidation tests.
4. Freeze serial, concurrent, packet, and invalidation protocols.
5. Run serial oracle, then concurrent entry demonstration.
6. Run no-update control, then versioned invalidation demonstration.
7. Grade, record a result graph and work log, commit, and push.
