# Fail-closed shared memory results

## Outcome

Confirmatory follow-up 2 passed every frozen layer. Confirmatory run 1 remains failed because one malformed mutant did not execute; it was not counted as evidence.

The result supports a bounded mechanism claim: a versioned, receipt-checked hypothesis graph can make unsupported or stale worker publications fail closed under the declared fault boundary. It does not establish general scheduler correctness or model capability.

## Exact evidence

| Layer | Frozen scope | Outcome |
|---|---:|---:|
| Relevant deterministic tests | 37 tests | passed |
| Full repository regression | 62 tests | passed in 1.65 s |
| Protocol exploration | depth 6, cap 20,000 | complete |
| Explored states | 14,967 | zero violations |
| Explored transitions | 39,288 | zero counterexamples |
| Equivalent states pruned | 24,322 | cap not hit |
| Model–SQLite conformance | 2 traces, 18 actions, 20 comparisons | zero mismatches |
| Forced race/boundary schedules | 6 exact schedules | all permitted outcomes |
| Pre-commit process deaths | 2 exact failpoints | complete rollback |
| Source mutants | 7 exact transformations | all killed by executed assertions |

No randomized trials, effect estimates, confidence intervals, or significance tests were used. Counts describe the frozen finite evidence surface; they are not population estimates.

## What was exercised

The conformance basis covered claimed, not-claimable, unknown-token, invalid-receipt, accepted, current replay, expired, cancelled, root-updated, and superseded-replay dispositions. SQLite matched the independent declarative model after every action and at both initial states.

The forced schedules covered one same-node double claim, both orders of publication versus root update, and publication immediately before, exactly at, and immediately after lease expiry. The exact deadline rule is `now >= lease_until` means expired.

The crash probes killed a subprocess after the node write in publication and after the first affected-node write in invalidation, both before commit. Reopening SQLite yielded the complete pre-transition state in both cases.

The mutation suite bypassed receipt checking, version entitlement, lease expiry, and claim exclusivity; under- and over-invalidated; and split the publication transaction. Every selected test executed and failed with `pytest` exit code 1.

## Integrity history

Confirmatory run 1 otherwise completed, but the version-entitlement source transform produced invalid Python and exited during collection. The old runner incorrectly treated every nonzero exit as a killed mutant. The run was failed and retained.

Follow-up 2 changed only that transform and the kill criterion: only an executed assertion failure counts. Scheduler, model, bounds, traces, races, and crash points were unchanged and frozen before rerun.

An unchanged exact replication was run afterward at the user's request. It again passed 62 tests, explored the same 14,967 states and 39,288 transitions with zero violations, produced zero mismatches across 20 conformance comparisons, and killed all seven mutants by executed assertion failures. This replication is reported separately and is not treated as a statistical sample or pooled estimate.

## Supported claim

> The declarative graph protocol preserved its fail-closed invariants over 14,967 completely explored bounded states. Scheduler commit `f88647b` matched a frozen ten-disposition conformance basis and preserved the declared invariants across six forced schedules, two pre-commit process deaths, and seven killed source mutants under the stated trusted boundary.

This is evidence that the hypothesis graph is effective as shared semantic memory when knowledge is carried as versioned claims with checkable receipts: stale or unsupported results are rejected rather than silently becoming current shared knowledge.

Unsupported: general Byzantine tolerance, semantic correctness of a trusted checker, durability under database rollback or disk loss, exhaustive SQLite behavior, arbitrary-application safety, or better underlying model reasoning.
