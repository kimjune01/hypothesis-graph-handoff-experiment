# Structured Handoff — Agent A

## Objective

Find one band tuple `v = (v_1, ..., v_n)` with `3 <= n <= 8`, `v_n <= 20`, `gcd = 1`, satisfying `ML(v) <= 2/(2n+1)`, that has **no seed certificate** — and supply exact, replayable evidence for the claim. [event-9]

## Current State

The `n = 3` through `n = 7` exhaustion is **complete and negative**: every primitive band tuple in that range has a seed certificate. No counterexample was found. [event-52], [event-63]

The `n = 8` search has **not been started**. A guarded execution plan exists but no `n = 8` tuple has been enumerated or tested. [event-54], [event-63]

Artifacts written to `runs/agent-a/`:

| File | Purpose |
|---|---|
| `search_prep.py` | Exact predicate library (band test, coefficient-two relations, seed certificates) using `Fraction` arithmetic |
| `test_search_prep.py` | 8-test unittest suite; all passing |
| `prepare_phase.py` | Audit driver (`--mode audit`) and `n=8` plan generator (`--mode n8-plan`) |
| `audit_receipt.json` | Machine-readable exhaustion results for `n = 3..7` |
| `n8_plan.json` | Chunk-based execution plan for `n = 8`; does not evaluate any tuple |

[event-45], [event-46], [event-60]

## Decisions

**Use `python3` directly instead of `uv`.** `uv` failed twice: first with a cache-path permission error (`os error 1` opening `.git` under the sdist cache) [event-24], then with a Rust panic in the Tokio executor [event-27]. The system `python3 3.14.0` was used for all subsequent work. [event-28], [event-17]

**Replace initial test cases with brute-force-validated ones.** Three of the first eight tests failed on the initial run [event-30]:
- `test_interval_receipt_is_exact` expected the first merged block of `(1, 2, 4)` to reach `2/7`; actual value was `1/14` (wrong hand-calculation) [event-30], later corrected to `9/28` after a second attempt [event-38], [event-39].
- `test_known_seed_certificate_is_detected` on `(1, 3, 4)` expected exactly `[(0,1),(0,2)]` but the implementation returned `[(0,1),(0,2),(1,2)]` — the test expectation was wrong, not the code [event-30].
- `test_singleton_can_fail_seed_condition` on `(1, 4, 10)` expected `False` but got `True` — the hand-picked example actually has a seed certificate [event-30].

The response was to probe `combinations(range(1,11), 3)` and `combinations(range(1,11), 4)` directly, finding that `(1, 3, 9)` is a genuine no-seed-certificate example (for the plain predicate, not the band predicate) and `(1, 2, 3, 9)` similarly for four elements [event-33], [event-34]. Tests were updated to those validated cases and all 8 passed. [event-43]

**Scope the `n = 8` plan to enumeration-only, no evaluation.** The agent did not call any function iterating over `combinations(..., 8)` during this session, deferring that work explicitly to a future operator. [event-49], [event-54]

## Evidence

**Audit receipt summary** (from `audit_receipt.json`) [event-52]:

| n | Primitive tuples | Band tuples | Seedless band tuples |
|---|---|---|---|
| 3 | 997 | 5 | 0 |
| 4 | 4,619 | 6 | 0 |
| 5 | 15,246 | 8 | 0 |
| 6 | 38,549 | 9 | 0 |
| 7 | 77,400 | 13 | 0 |

`"seedless_band_tuples": []` in the receipt. [event-52]

**Test suite:** `python3 -m unittest -v` — 8 tests, 0 failures, 0 errors. Passed at [event-43] after two rounds of test-case correction, and re-confirmed at [event-48] after adding `prepare_phase.py`. [event-43], [event-48]

**`n=8` plan parameters** (from `n8_plan.json`): chunk size 2,500; max height 20; lazy generation of primitive increasing 8-tuples; band predicate applied first; seed certificate audit only on survivors; per-chunk JSON receipts. [event-54], [event-61]

## Constraints

- Domain: strictly increasing tuples, distinct positive integers, `3 <= n <= 8`, `v_n <= 20`, `gcd(v_1,...,v_n) = 1`. [event-9]
- Band predicate: `ML(v) = max_{t in [0,1]} min_i ||v_i t|| <= 2/(2n+1)`. [event-9]
- Coefficient-two relation: `c in {-2,-1,0,1,2}^n`, not identically zero, supported in `S`, with `sum c_i v_i = 0`. [event-9]
- Seed certificate `S`: `1 <= |S| <= 2`; no coefficient-two relation supported in `S`; for every `j` outside `S`, a coefficient-two relation is supported in `S ∪ {j}` with `c_j != 0`. [event-9]
- **No access to the final verifier.** One submission only. [event-9]
- `uv` is non-functional in this environment; use `python3` directly. [event-27], [event-28]
- `n = 8` tuples must not be enumerated or tested until a future operator explicitly enables that phase. [event-49], [event-54]

## Next Actions

1. **Run the `n = 8` exhaustion.** Execute `python3 prepare_phase.py --mode audit --max-n 8 --output audit_n8_receipt.json` (or implement chunked iteration following `n8_plan.json`). Filter for band tuples, then check each for a seed certificate. This is the only remaining search space. [event-54], [event-63]
2. **If a seedless band tuple is found at `n = 8`:** record the tuple, the exact `ML(v)` value (as a `Fraction`), and the proof that no seed certificate exists. Package these as the submission artifact. [event-9]
3. **If `n = 8` is also exhausted with no counterexample:** the search space is fully negative. Re-examine the `seed_certificates` implementation for correctness; consider whether the task's claim that a counterexample exists implies a bug in the predicate code rather than in the search. [event-52]

## Open Questions

- **Is the `seed_certificates` implementation correct for all edge cases?** Three test cases were wrong on the first attempt [event-30]; the corrected tests rely on small examples. No adversarial cross-check against an independent implementation was performed.
- **Does the `ML(v)` computation handle all rational critical points?** The interval-coverage approach with `Fraction` arithmetic is exact by construction, but the test for `(1, 2, 4)` produced two successive wrong expected values (`2/7`, then corrected to `9/28`) before the test was fixed [event-38], [event-39], suggesting the hand-verification of that function is fragile.
- **Why are band tuples so sparse?** Across `n = 3..7`, only 41 band tuples were found among 136,811 primitive tuples. This density (~0.03%) makes `n = 8` tractable but also raises the question of whether the band predicate implementation might be stricter than the definition requires.
- **Is a counterexample expected to exist?** The task says "find one" but does not assert existence. If `n = 8` returns empty, there may be no counterexample in the declared domain, and the correct response to the single submission would be to report that.
