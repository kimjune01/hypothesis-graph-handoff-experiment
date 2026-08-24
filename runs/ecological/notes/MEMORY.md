# Previous agent's notes

Started by reading the bounded-counterexample task. The search needs three exact checks: band membership, coefficient-two relations, and whether a one- or two-element seed certificate exists. I decided to use exact `Fraction` arithmetic. Band membership can be tested as interval coverage; the relation checks only need coefficient enumeration on supports of at most three indices.

I wrote `search_prep.py` and `test_search_prep.py`. `uv run python -m unittest -v` failed because the global uv cache was not writable. Redirecting `UV_CACHE_DIR` locally then caused a Rust/Tokio panic, so I switched to system `python3` 3.14.0.

The first test run had three failures caused by bad hand-written expectations. For `(1,2,4)`, my expected merged-interval endpoint `2/7` was wrong; the corrected endpoint is `9/28`. I expected only two seed pairs for `(1,3,4)`, but all three pairs qualify. I also chose `(1,4,10)` as a seedless fixture, but it actually has a certificate. A small brute-force probe found `(1,3,9)` as a genuine seedless triple and `(1,2,3,9)` as a seedless four-tuple. After correcting the fixtures, all eight tests passed.

I added `prepare_phase.py`, reran the eight tests, and they still passed. Then I exhaustively audited primitive increasing tuples of height at most 20 for `n=3..7`. Results in `audit_receipt.json`:

- n=3: 997 primitive, 5 band, 0 seedless band tuples.
- n=4: 4,619 primitive, 6 band, 0 seedless band tuples.
- n=5: 15,246 primitive, 8 band, 0 seedless band tuples.
- n=6: 38,549 primitive, 9 band, 0 seedless band tuples.
- n=7: 77,400 primitive, 13 band, 0 seedless band tuples.

So the bounded search is unresolved only at `n=8`. I deliberately did not evaluate an eight-tuple. `n8_plan.json` proposes lazy lexicographic generation of primitive eight-tuples from `1..20`, applying the exact band predicate first and the seed-certificate check only to survivors, with chunk size 2,500 and receipts.

Useful files are `search_prep.py` for the predicates, `prepare_phase.py` for the audit driver, `test_search_prep.py` for the eight tests, `audit_receipt.json` for the completed lower-dimensional scan, and `n8_plan.json` for the remaining search.

Things I would verify before trusting a final answer: rerun the unit tests; inspect `search_prep.py` because the early hand-calculated fixtures were wrong; and obtain exact replayable evidence for both full interval coverage and failure of every possible seed set. The immediate next action is the `n=8` scan, not another `n<=7` audit.
