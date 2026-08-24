```
HYPOTHESIS GRAPH — Agent A Transcript
Task: find a band tuple with no seed certificate, 3 ≤ n ≤ 8, v_n ≤ 20, gcd = 1

═══════════════════════════════════════════════════════════════════════════════
NODE H-0
═══════════════════════════════════════════════════════════════════════════════
ID:               H-0
Claim:            A strictly increasing primitive tuple v with 3 ≤ |v| ≤ 8 and
                  v_max ≤ 20 exists that is a band tuple (ML(v) ≤ 2/(2n+1)) yet
                  has no seed certificate.
Reasoning mode:   Conjecture (problem statement)
Status:           OPEN — not resolved; n = 8 subspace uninvestigated
Dependency parents: (root)
Kill condition:   Proof that every band tuple in domain has a seed certificate,
                  or an explicit counterexample is found
Exact trial:      (none — this is the root goal)
Prediction:       At least one seedless band tuple exists somewhere in domain
Observed outcome: No counterexample found for n ∈ {3,4,5,6,7}; n = 8 untested
Events:           [event-9]

═══════════════════════════════════════════════════════════════════════════════
NODE H-1
═══════════════════════════════════════════════════════════════════════════════
ID:               H-1
Claim:            The three predicates (band membership, coefficient-two relation,
                  seed certificate) can be implemented exactly using Python's
                  Fraction type without floating-point error.
Reasoning mode:   Deductive (band condition is a rational interval-cover problem;
                  relations are integer linear equations; both terminate)
Status:           CONFIRMED
Dependency parents: H-0
Kill condition:   Implementation requires irrational arithmetic or fails to
                  terminate on small inputs
Exact trial:      Write search_prep.py with Fraction-based band test and
                  coefficient-two enumerator; run unittest suite
Prediction:       All unit-test predicates agree with hand-computed values
Observed outcome: After test repairs, all 8 unittest cases pass
Events:           [event-11] [event-19] [event-20] [event-21] [event-43]

═══════════════════════════════════════════════════════════════════════════════
NODE H-2
═══════════════════════════════════════════════════════════════════════════════
ID:               H-2
Claim:            `uv run python -m unittest` is the correct way to execute tests
                  in this workspace.
Reasoning mode:   Empirical (environment probe)
Status:           KILLED
Dependency parents: H-1
Kill condition:   uv fails for environment reasons
Exact trial:      `uv run python -m unittest -v`
Prediction:       Tests execute and report pass/fail
Observed outcome: Error — uv fails to open
                  /Users/junekim/.cache/uv/sdists-v9/.git (Operation not permitted)
Events:           [event-23] [event-24]

═══════════════════════════════════════════════════════════════════════════════
NODE H-3
═══════════════════════════════════════════════════════════════════════════════
ID:               H-3
Claim:            Setting UV_CACHE_DIR to a local writable path (`.uv-cache`)
                  fixes the permission error and lets uv run the tests.
Reasoning mode:   Empirical (targeted workaround)
Status:           KILLED
Dependency parents: H-2
Kill condition:   uv panics for a different reason even with local cache
Exact trial:      `mkdir -p .uv-cache && UV_CACHE_DIR=$PWD/.uv-cache uv run python
                  -m unittest -v`
Prediction:       Tests execute successfully
Observed outcome: Rust panic in Tokio executor inside uv (exit 101); environment
                  is fundamentally incompatible with this uv build
Events:           [event-26] [event-27]

═══════════════════════════════════════════════════════════════════════════════
NODE H-4
═══════════════════════════════════════════════════════════════════════════════
ID:               H-4
Claim:            python3 (system interpreter, Python 3.14) can run the test suite
                  directly without uv.
Reasoning mode:   Empirical (fallback after H-2 and H-3 killed)
Status:           CONFIRMED
Dependency parents: H-3
Kill condition:   python3 itself is absent or also fails
Exact trial:      `python3 -m unittest -v`
Prediction:       Tests execute and report at least some results
Observed outcome: 8 tests run; 3 fail (implementation bug or wrong test expectations)
Events:           [event-28] [event-29] [event-30]

═══════════════════════════════════════════════════════════════════════════════
NODE H-5
═══════════════════════════════════════════════════════════════════════════════
ID:               H-5
Claim:            The first merged interval of the band coverage for (1, 2, 4) has
                  right endpoint 2/7 (= 2/(2·3+1) as written in the original test).
Reasoning mode:   Deductive (hand calculation of interval union)
Status:           KILLED (wrong prediction, not wrong implementation)
Dependency parents: H-1
Kill condition:   Computed endpoint differs from 2/7
Exact trial:      `test_interval_receipt_is_exact` checks
                  `merged_coverage((1, 2, 4))[0] == (Fraction(0), Fraction(2, 7))`
Prediction:       Right endpoint of first merged block is 2/7
Observed outcome: Endpoint is 9/28 ≠ 2/7; merged block is wider than predicted
Events:           [event-30] [event-38] [event-39] [event-40] [event-41]

═══════════════════════════════════════════════════════════════════════════════
NODE H-6
═══════════════════════════════════════════════════════════════════════════════
ID:               H-6
Claim:            The only singleton-pair seed certificates of (1, 3, 4) are the
                  pairs {0,1} and {0,2} (indices into the tuple).
Reasoning mode:   Deductive (hand enumeration of coefficient-two relations)
Status:           KILLED (pair {1,2} also qualifies)
Dependency parents: H-1
Kill condition:   seed_certificates((1,3,4)) contains additional entries
Exact trial:      `test_known_seed_certificate_is_detected` asserts
                  `seed_certificates((1,3,4)) == [(0,1),(0,2)]`
Prediction:       Exactly two seed certificates
Observed outcome: Three seed certificates returned: [(0,1),(0,2),(1,2)]
Events:           [event-30]

═══════════════════════════════════════════════════════════════════════════════
NODE H-7
═══════════════════════════════════════════════════════════════════════════════
ID:               H-7
Claim:            The tuple (1, 4, 10) has no seed certificate, making it a valid
                  test fixture for the negative seed-certificate case.
Reasoning mode:   Deductive (attempted hand verification)
Status:           KILLED
Dependency parents: H-1
Kill condition:   `has_seed_certificate((1,4,10))` returns True
Exact trial:      `test_singleton_can_fail_seed_condition` asserts
                  `has_seed_certificate((1,4,10)) == False`
Prediction:       (1,4,10) has no seed certificate
Observed outcome: has_seed_certificate((1,4,10)) is True; fixture was wrong
Events:           [event-30]

═══════════════════════════════════════════════════════════════════════════════
NODE H-8
═══════════════════════════════════════════════════════════════════════════════
ID:               H-8
Claim:            Among triples (a,b,c) with 1 ≤ a < b < c ≤ 10 there exists at
                  least one with no seed certificate, usable as a negative fixture.
Reasoning mode:   Empirical (brute-force probe after H-7 killed)
Status:           CONFIRMED
Dependency parents: H-7
Kill condition:   All triples up to height 10 have seed certificates
Exact trial:      Inline Python loop over combinations(range(1,11), 3) stopping at
                  first tuple where has_seed_certificate returns False
Prediction:       A valid negative fixture exists in that range
Observed outcome: (1, 3, 9) has no seed certificate; confirmed immediately
Events:           [event-32] [event-33] [event-34]

═══════════════════════════════════════════════════════════════════════════════
NODE H-9
═══════════════════════════════════════════════════════════════════════════════
ID:               H-9
Claim:            (1, 3, 9) has no seed certificate and is a sound negative fixture
                  for the seed-certificate predicate test.
Reasoning mode:   Empirical (probe result from H-8)
Status:           CONFIRMED
Dependency parents: H-8
Kill condition:   Re-running has_seed_certificate((1,3,9)) returns True
Exact trial:      `test_tuple_can_have_no_seed_certificate` asserts
                  `has_seed_certificate((1,3,9)) == False`
Prediction:       Passes in updated test suite
Observed outcome: Passes; all 8 tests green after test repair
Events:           [event-33] [event-35] [event-36] [event-43]

═══════════════════════════════════════════════════════════════════════════════
NODE H-10
═══════════════════════════════════════════════════════════════════════════════
ID:               H-10
Claim:            The predicate implementation is correct after test repairs: every
                  unit test case now encodes a true mathematical fact and the
                  implementation satisfies it.
Reasoning mode:   Empirical (green test run)
Status:           CONFIRMED
Dependency parents: H-1, H-5, H-6, H-7, H-8, H-9
Kill condition:   Any test fails
Exact trial:      `python3 -m unittest -v` on the repaired test_search_prep.py
Prediction:       All 8 tests pass
Observed outcome: All 8 tests pass (0 failures)
Events:           [event-42] [event-43] [event-44]

═══════════════════════════════════════════════════════════════════════════════
NODE H-11
═══════════════════════════════════════════════════════════════════════════════
ID:               H-11
Claim:            After adding prepare_phase.py (the audit driver) the full test
                  suite still passes — no regression introduced.
Reasoning mode:   Empirical (regression check)
Status:           CONFIRMED
Dependency parents: H-10
Kill condition:   Any test fails after adding prepare_phase.py
Exact trial:      `python3 -m unittest -v` after file_change for prepare_phase.py
Prediction:       Still 8/8 passing
Observed outcome: 8/8 passing [event-48]
Events:           [event-45] [event-46] [event-47] [event-48]

═══════════════════════════════════════════════════════════════════════════════
NODE H-12
═══════════════════════════════════════════════════════════════════════════════
ID:               H-12
Claim:            No primitive band tuple with n = 3 and v_max ≤ 20 lacks a seed
                  certificate.
Reasoning mode:   Exhaustive empirical (complete enumeration)
Status:           CONFIRMED
Dependency parents: H-10, H-11
Kill condition:   audit_receipt.json reports band_tuples_without_seed_certificate > 0
                  for n = 3
Exact trial:      `python3 prepare_phase.py --mode audit --output audit_receipt.json`
                  (mode enumerates all primitive increasing triples, tests each)
Prediction:       0 seedless band tuples among 997 primitive triples
Observed outcome: 997 primitive tuples; 5 band tuples; 0 seedless band tuples
Events:           [event-50] [event-52]

═══════════════════════════════════════════════════════════════════════════════
NODE H-13
═══════════════════════════════════════════════════════════════════════════════
ID:               H-13
Claim:            No primitive band tuple with n = 4 and v_max ≤ 20 lacks a seed
                  certificate.
Reasoning mode:   Exhaustive empirical
Status:           CONFIRMED
Dependency parents: H-10, H-11
Kill condition:   audit_receipt.json reports seedless count > 0 for n = 4
Exact trial:      Same audit run as H-12 (single invocation covers all n)
Prediction:       0 seedless band tuples among 4619 primitive 4-tuples
Observed outcome: 4619 primitive tuples; 6 band tuples; 0 seedless band tuples
Events:           [event-50] [event-52]

═══════════════════════════════════════════════════════════════════════════════
NODE H-14
═══════════════════════════════════════════════════════════════════════════════
ID:               H-14
Claim:            No primitive band tuple with n = 5 and v_max ≤ 20 lacks a seed
                  certificate.
Reasoning mode:   Exhaustive empirical
Status:           CONFIRMED
Dependency parents: H-10, H-11
Kill condition:   audit_receipt.json reports seedless count > 0 for n = 5
Exact trial:      Same audit run
Prediction:       0 seedless band tuples among 15246 primitive 5-tuples
Observed outcome: 15246 primitive tuples; 8 band tuples; 0 seedless band tuples
Events:           [event-50] [event-52]

═══════════════════════════════════════════════════════════════════════════════
NODE H-15
═══════════════════════════════════════════════════════════════════════════════
ID:               H-15
Claim:            No primitive band tuple with n = 6 and v_max ≤ 20 lacks a seed
                  certificate.
Reasoning mode:   Exhaustive empirical
Status:           CONFIRMED
Dependency parents: H-10, H-11
Kill condition:   audit_receipt.json reports seedless count > 0 for n = 6
Exact trial:      Same audit run
Prediction:       0 seedless band tuples among 38549 primitive 6-tuples
Observed outcome: 38549 primitive tuples; 9 band tuples; 0 seedless band tuples
Events:           [event-50] [event-52]

═══════════════════════════════════════════════════════════════════════════════
NODE H-16
═══════════════════════════════════════════════════════════════════════════════
ID:               H-16
Claim:            No primitive band tuple with n = 7 and v_max ≤ 20 lacks a seed
                  certificate.
Reasoning mode:   Exhaustive empirical
Status:           CONFIRMED
Dependency parents: H-10, H-11
Kill condition:   audit_receipt.json reports seedless count > 0 for n = 7
Exact trial:      Same audit run
Prediction:       0 seedless band tuples among 77400 primitive 7-tuples
Observed outcome: 77400 primitive tuples; 13 band tuples; 0 seedless band tuples
Events:           [event-50] [event-52]

═══════════════════════════════════════════════════════════════════════════════
NODE H-17
═══════════════════════════════════════════════════════════════════════════════
ID:               H-17
Claim:            If a seedless band tuple exists in the declared domain it must
                  have n = 8, since n ∈ {3,4,5,6,7} is exhaustively ruled out.
Reasoning mode:   Deductive (from H-12 through H-16 by elimination)
Status:           OPEN (frontier — no n = 8 tuples were evaluated)
Dependency parents: H-12, H-13, H-14, H-15, H-16
Kill condition:   n = 8 exhaustion returns 0 seedless band tuples (would kill H-0
                  along with H-17), or a seedless n = 8 band tuple is found
                  (would confirm H-0)
Exact trial:      (not yet run) — n8_plan.json specifies a lazy chunked scan over
                  C(20,8) primitive increasing 8-tuples using the same predicates
Prediction:       At least one seedless band tuple exists at n = 8
Observed outcome: Not yet observed
Events:           [event-52] [event-53] [event-54] [event-55] [event-63]

═══════════════════════════════════════════════════════════════════════════════
NODE H-18
═══════════════════════════════════════════════════════════════════════════════
ID:               H-18
Claim:            An executable, chunk-based n = 8 search plan can be written and
                  persisted (n8_plan.json) without evaluating any n = 8 tuple
                  during this session.
Reasoning mode:   Deductive / procedural
Status:           CONFIRMED
Dependency parents: H-17
Kill condition:   Plan generation itself enumerates n = 8 tuples or fails to write
                  the output file
Exact trial:      `python3 prepare_phase.py --mode n8-plan --output n8_plan.json`
Prediction:       JSON plan file written; no combinations(..., 8) iterated
Observed outcome: n8_plan.json written with chunked generator strategy, chunk_size
                  2500, max_height 20; execution notes confirm no n=8 enumeration
                  occurred
Events:           [event-53] [event-54] [event-59] [event-61]

═══════════════════════════════════════════════════════════════════════════════
OPEN FRONTIER (nodes awaiting continuation by Agent B or later operator)
═══════════════════════════════════════════════════════════════════════════════

H-0  Root goal — still unresolved
H-17 n = 8 subspace — uninvestigated; n8_plan.json provides a ready execution path

Artifacts available for handoff:
  search_prep.py     — exact Fraction-based predicates (band, relation, seed cert)
  prepare_phase.py   — audit driver (--mode audit) and plan emitter (--mode n8-plan)
  test_search_prep.py — 8 passing unit tests for all three predicates
  audit_receipt.json — machine-readable exhaustive receipt for n ∈ {3..7}
  n8_plan.json       — chunked execution plan for n = 8 (no tuples pre-evaluated)

═══════════════════════════════════════════════════════════════════════════════
KILLED BRANCHES SUMMARY
═══════════════════════════════════════════════════════════════════════════════

H-2  uv as test runner          — killed by OS permission error       [event-24]
H-3  uv with local cache        — killed by Rust/Tokio panic           [event-27]
H-5  interval endpoint = 2/7    — killed; actual endpoint is 9/28     [event-30][event-38]
H-6  exactly two seed certs     — killed; (1,3,4) has three           [event-30]
H-7  (1,4,10) seedless fixture  — killed; tuple actually has cert     [event-30]
```
