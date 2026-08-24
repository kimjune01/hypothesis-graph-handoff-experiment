**Objective**

Find a band tuple v = (v_1, ..., v_n) with 3 ≤ n ≤ 8, v_n ≤ 20, gcd(v) = 1, ML(v) ≤ 2/(2n+1) that has no seed certificate, then return it with exact, replayable evidence. [event-9]

---

**Current State**

The preparatory audit for all n ∈ {3, 4, 5, 6, 7} is exhaustively complete. No counterexample was found in that range. The n = 8 search has not been started; no n = 8 tuple has been evaluated. [event-52, event-63]

All predicate code is verified by a passing eight-test suite (python3 -m unittest). [event-43, event-48, event-63]

Artifacts present in runs/agent-a/:
- search_prep.py — exact predicates (band, coefficient-two relation, seed certificate) using Fraction arithmetic [event-21, event-46]
- prepare_phase.py — audit driver with --mode audit and --mode n8-plan flags [event-45, event-46]
- test_search_prep.py — eight passing unit tests [event-21, event-36, event-41, event-43]
- audit_receipt.json — machine-readable exhaustive receipt for n ∈ {3..7} [event-52]
- n8_plan.json — guarded execution plan for n = 8 that enumerates no tuple [event-54]

---

**Decisions**

- Use exact rational arithmetic (Python Fraction) throughout rather than floating-point, to guarantee correctness of both the band predicate and the relation search. [event-19, event-44]
- Run the band predicate first on every candidate; invoke the seed-certificate check only on surviving band tuples, to keep the search tractable. [event-49]
- Use python3 directly instead of uv after uv failed with a Rust-level panic in this environment. [event-27, event-28]
- Defer all n = 8 enumeration to a future run; Agent A's scope ends after the n ≤ 7 audit. [event-49, event-54, event-63]

---

**Evidence**

Exhaustive audit results from audit_receipt.json (bounds: max_height = 20, min_n = 3, max_n = 7): [event-52]

- n = 3: 997 primitive tuples checked, 5 band tuples found, 0 seedless band tuples. [event-52]
- n = 4: 4,619 primitive tuples checked, 6 band tuples found, 0 seedless band tuples. [event-52]
- n = 5: 15,246 primitive tuples checked, 8 band tuples found, 0 seedless band tuples. [event-52]
- n = 6: 38,549 primitive tuples checked, 9 band tuples found, 0 seedless band tuples. [event-52]
- n = 7: 77,400 primitive tuples checked, 13 band tuples found, 0 seedless band tuples. [event-52]

Probe confirming that seed-certificate-free tuples exist in the search space (not band tuples): (1, 3, 9) has no seed certificate for n = 3, and (1, 2, 3, 9) for n = 4. These were used to fix erroneous test cases and are not counterexamples to the task. [event-33, event-34]

Three initial tests failed and were corrected before the audit ran: [event-30]
- test_interval_receipt_is_exact: expected boundary was wrong; corrected to 9/28. [event-38, event-41, event-43]
- test_known_seed_certificate_is_detected: (1, 3, 4) has three seed certificates, not two. [event-30, event-36]
- test_singleton_can_fail_seed_condition: (1, 4, 10) does have a seed certificate, contrary to the initial test. [event-30, event-33]

All eight tests pass as of event-43 and remained passing through all subsequent file edits. [event-43, event-48, event-63]

uv 0.9.13 failed with a NULL-object Rust panic, unrelated to the code. [event-27]

---

**Constraints**

- v must be a strictly increasing tuple of distinct positive integers. [event-9]
- 3 ≤ n ≤ 8, v_n ≤ 20, gcd(v_1, ..., v_n) = 1. [event-9]
- ML(v) = max_{t ∈ [0,1]} min_i ||v_i t|| ≤ 2/(2n+1). [event-9]
- A seed certificate S has |S| ∈ {1, 2}; condition 1: no coefficient-two relation supported in S; condition 2: for every j outside S, a coefficient-two relation is supported in S ∪ {j} with c_j ≠ 0. [event-9]
- Coefficients are in {-2, -1, 0, 1, 2}; sum c_i v_i = 0. [event-9]
- Agent A was prohibited from evaluating any n = 8 tuple during its run. [event-49, event-54]
- No final verifier access; one submission allowed. [event-9]

---

**Next Actions**

- Execute the n = 8 search using the plan in n8_plan.json and the predicates in search_prep.py. [event-54, event-63]
- Run: python3 prepare_phase.py --mode audit --output audit_receipt_n8.json after extending the driver to cover n = 8 (the current --mode audit caps at max_n = 7). [event-52, event-54]
- If a seedless band tuple is found at n = 8, collect its exact ML witness (the argmax t and per-component ||v_i t|| values) and the proof that every size-1 and size-2 subset S fails at least one seed-certificate condition, then format both as the submission evidence. [event-9, event-63]
- If n = 8 is also exhausted with no counterexample, the task has no solution in the declared domain and the situation must be escalated. [event-52]

---

**Open Questions**

- Whether any n = 8 primitive band tuple with v_8 ≤ 20 exists at all: the n ≤ 7 audit found at most 13 band tuples at n = 7 across roughly 77,000 primitive tuples, suggesting band tuples are rare and n = 8 may have zero or very few. [event-52]
- Whether the n8_plan.json chunk size of 2,500 is appropriate for runtime; the number of primitive 8-tuples with max entry ≤ 20 is not computed in the plan. [event-54]
- Whether the current seed-certificate implementation correctly handles the case where S is a singleton with a zero-coefficient element allowed by the task definition ("Elements of S may have zero coefficients"). This edge case was not explicitly tested. [event-9, event-43]
- uv is non-functional in this environment; any Agent B run should use python3 directly. [event-27, event-28]
