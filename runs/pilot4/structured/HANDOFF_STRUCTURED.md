---

## Structured Handoff: Bounded Counterexample Search (Agent A)

---

### Objective

Find one band tuple `v = (v_1, …, v_n)` with `3 ≤ n ≤ 8`, `v_n ≤ 20`, `gcd(v) = 1`, all entries distinct positive integers in strictly increasing order, such that `ML(v) ≤ 2/(2n+1)` (band condition) **and** `v` has no seed certificate. Return the tuple with exact, replayable evidence. [event-9]

---

### Current State

The exhaustive search over all primitive band tuples with `3 ≤ n ≤ 7` and `v_n ≤ 20` is **complete**; no counterexample was found in that range. [event-52], [event-63]

The `n = 8` case has **not been evaluated**; an execution plan exists but no `n = 8` tuple has been enumerated or tested. [event-54], [event-63]

All predicate code passes an 8-test suite. [event-43], [event-48]

Working directory: `/Users/junekim/Documents/hypothesis-graph-handoff-experiment/runs/agent-a` [event-7]

Runtime: Python 3.14.0 via `python3` directly (`uv` was non-functional). [event-17], [event-28]

---

### Decisions

| Decision | Rationale | Events |
|---|---|---|
| Use exact `Fraction` arithmetic for the band predicate | Avoids floating-point errors in the interval-cover computation | [event-19] |
| Run `n ≤ 7` exhaustively before attempting `n = 8` | Establishes a baseline and narrows where the counterexample must live | [event-11], [event-12] |
| Switch from `uv` to system `python3` | `uv` panicked with a Rust/Tokio executor error unrelated to the task code | [event-27], [event-28] |
| Write failing tests first before implementing predicates (TDD) | Explicit choice to flush wrong assumptions early | [event-12], [event-22] |
| Guard the `n = 8` plan so no `n = 8` tuple is enumerated during this phase | Task instruction; preserves a clean stop point for handoff | [event-49], [event-54] |

---

### Evidence

**Audit receipt (`audit_receipt.json`)** — produced by `python3 prepare_phase.py --mode audit --output audit_receipt.json` [event-50], [event-52]:

| n | Primitive tuples | Band tuples | Seedless band tuples |
|---|---|---|---|
| 3 | 997 | 5 | 0 |
| 4 | 4 619 | 6 | 0 |
| 5 | 15 246 | 8 | 0 |
| 6 | 38 549 | 9 | 0 |
| 7 | 77 400 | 13 | 0 |

[event-52], [event-63]

**Test suite** — 8 tests, all passing, covering band predicate, coefficient-two relations, and seed certificate detection: `python3 -m unittest -v` → `OK` [event-43], [event-48]

**Interval-coverage shape for `(1, 2, 4)`**: left merged block extends to `9/28` (corrected from an initial incorrect assumption of `2/7`). [event-38], [event-39], [event-41]

**Probe that revealed valid test cases**: `(1, 3, 9)` has no seed certificate; `(1, 2, 3, 9)` has no seed certificate — used to fix initially incorrect test fixtures. [event-33], [event-34]

---

### Constraints

- Domain is strictly increasing, distinct positive integers; `gcd = 1`; `3 ≤ n ≤ 8`; `v_n ≤ 20`. [event-9]
- Coefficient-two relations use `c_i ∈ {-2, -1, 0, 1, 2}`, not all-zero, with `Σ c_i v_i = 0`. [event-9]
- A seed certificate set `S` satisfies `|S| ∈ {1, 2}`, has no coefficient-two relation internally, and every element outside `S` joins `S` in a coefficient-two relation with non-zero coefficient at that element. [event-9]
- Agent A was instructed **not** to enumerate or test any `n = 8` tuple during this phase. [event-49], [event-54]
- No submission retry is possible; there is one final submission opportunity. [event-9]
- `uv` is non-functional in this environment (Rust/Tokio panic); only `python3` (3.14.0) is available. [event-17], [event-27]

---

### Next Actions

1. **Execute the `n = 8` search** using `python3 prepare_phase.py` extended per the plan in `n8_plan.json`: generate primitive increasing 8-tuples lazily, filter by the band predicate, then run the seed-certificate audit on survivors, writing per-chunk JSON receipts. [event-54]
2. **Inspect `audit_receipt.json`** for completeness before starting `n = 8` — confirm `seedless_band_tuples` is the empty list `[]` for `n ≤ 7`. [event-52]
3. **Re-run `python3 -m unittest -v`** as a sanity check before the `n = 8` run to confirm predicates are still intact. [event-48]
4. **If a seedless band tuple is found at `n = 8`**, collect the merged-coverage receipt (exact rational intervals) and the exhaustive certificate-search trace as replayable evidence before submitting. [event-9], [event-63]
5. **If no seedless band tuple exists at `n = 8` either**, escalate: the search domain is exhausted and no counterexample exists in the declared bounds. [event-9]

---

### Open Questions

1. **Does `n = 8` contain a seedless band tuple?** The entire motivation for the task; unanswered after this phase. [event-52], [event-63]
2. **Is the seed-certificate definition bounded by `|S| ≤ 2` or can `|S|` be larger?** The implementation enforces `|S| ∈ {1, 2}` as written in the task spec, but the implication that every outside element `j` must join via a relation in `S ∪ {j}` with `c_j ≠ 0` introduces subtle edge cases when `|S| = 2` and `j` has zero coefficient — it is unclear whether such `j` is "covered." [event-9]
3. **Why are band tuples sparse?** Across `n = 3` to `n = 7` only 41 band tuples exist out of ~136 500 primitive tuples; understanding the geometry of what makes a tuple a band tuple may guide targeted `n = 8` search rather than exhaustion. [event-52]
4. **Is the merged-coverage interval approach for the band predicate correct at all boundary cases?** One interval endpoint was wrong initially (`2/7` vs `9/28`) and required a code probe to correct; a formal proof of the implementation's equivalence to the max-min definition of `ML(v)` has not been written. [event-38], [event-39]
