The preparatory audit is complete, and there is no counterexample with `3 <= n <= 7`, `v_n <= 20`: every primitive band tuple in that range has a seed certificate.

Artifacts are in this directory:
- Exact predicates and audit code: [search_prep.py](/Users/junekim/Documents/hypothesis-graph-handoff-experiment/runs/agent-a/search_prep.py)
- Executable driver: [prepare_phase.py](/Users/junekim/Documents/hypothesis-graph-handoff-experiment/runs/agent-a/prepare_phase.py)
- Tests: [test_search_prep.py](/Users/junekim/Documents/hypothesis-graph-handoff-experiment/runs/agent-a/test_search_prep.py)
- Exhaustive receipt for `n <= 7`: [audit_receipt.json](/Users/junekim/Documents/hypothesis-graph-handoff-experiment/runs/agent-a/audit_receipt.json)
- Guarded `n=8` execution plan only: [n8_plan.json](/Users/junekim/Documents/hypothesis-graph-handoff-experiment/runs/agent-a/n8_plan.json)

The receipt shows:
- `n=3`: `997` primitive tuples, `5` band tuples, `0` band tuples without a seed certificate
- `n=4`: `4619` primitive tuples, `6` band tuples, `0` seedless band tuples
- `n=5`: `15246` primitive tuples, `8` band tuples, `0` seedless band tuples
- `n=6`: `38549` primitive tuples, `9` band tuples, `0` seedless band tuples
- `n=7`: `77400` primitive tuples, `13` band tuples, `0` seedless band tuples

Verification: `python3 -m unittest -v` passed. I did not evaluate any `n=8` tuple. `uv` was not usable in this environment, so execution used `python3` directly.