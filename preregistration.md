# Preregistration: bounded mathematical handoff pilot

Status: ready to freeze. The verifier has eight passing tests, the recall probe returned `NO RECALL`, and the frozen inputs are hash-pinned below. No experimental agent run may begin before the freeze commit.

## Question and claim boundary

Does a hypothesis graph let Agent B continue one bounded conjecture search with less duplicated work or lower resumption cost than restart, a lossless transcript, or a strong structured handoff, without reducing task success?

This is an instrumentation pilot with one run per condition. It can support only a case-level existence or null statement, not an average effect, a rate, or a claim about mathematical reasoning generally.

## Formal task

For a strictly increasing tuple of distinct positive integers

```text
v = (v_1, ..., v_n),  3 <= n <= 8,  v_n <= 20,  gcd(v_1,...,v_n) = 1,
```

let `||x|| = min_{m in Z} |x-m|` and

```text
ML(v) = max_{t in [0,1]} min_i ||v_i t||.
```

The maximum exists because the objective is continuous. Call `v` a band tuple when `ML(v) <= 2/(2n+1)`.

For `S subseteq {1,...,n}`, a coefficient-two relation supported in `S` is a vector `c in {-2,-1,0,1,2}^n`, not identically zero, such that `c_i=0` for `i notin S` and `sum_i c_i v_i=0`. Elements of `S` may also have zero coefficients; “supported in” does not mean support exactly equal to `S`.

A seed certificate is a set `S` with `1 <= |S| <= 2` satisfying:

1. no coefficient-two relation is supported in `S`; and
2. for every `j notin S`, there exists a coefficient-two relation supported in `S union {j}` with `c_j != 0`.

The experimental task is to find one band tuple in the declared domain that has no seed certificate. A final answer succeeds only if it supplies a tuple accepted by the one-shot hidden verifier. “No counterexample exists” is a failed submission; no exhaustive-proof branch is scored.

## Exact oracle and frame

The verifier recomputes, rather than matches against a stored answer:

1. arity, ordering, distinctness, positivity, height, and gcd;
2. exact `ML(v)` using rational critical times from the cusps and pairwise intersections of the sawtooth functions `||v_i t||`; and
3. failure of every one- or two-element `S`, by exhaustive coefficient enumeration.

The experimenter wrote the verifier from this formal specification while aware of a known counterexample. “Independent” therefore means implementation-independent from the Lonely Runner repository and answer-independent at grading time; it does not mean blind verifier authorship. This limitation is reported.

Before Agent A runs, tests must include the quarantined known counterexample, a bad-gcd frame failure, a tuple outside the band by a checked exact margin, and at least one band tuple with a valid two-seed certificate. All verifier repairs occur before the freeze commit and remain in Git history.

Agent A and B cannot query the verifier. Each Agent B gets one final submission, graded after its run ends.

## Agents, budgets, and isolation

- Agent A: Codex CLI 0.149.0, model `gpt-5.4`.
- Agent B and both artifact generators: Claude Code 2.1.227, model `claude-sonnet-4-6`.
- One Agent B run per condition.
- Each Agent B run has a USD 5 model budget and a 20-minute wall-time cap. A timeout is a retained failure.
- Agent A has a 20-minute wall-time cap and the phase-restricted task below.
- No run is replaced or restarted. A ceiling-effect solution in Restart remains a result.

Runs occur in separate directories. Every condition receives an identical frozen working-tree snapshot plus its condition artifact. Claude's `WebSearch` and `WebFetch` tools are disabled. Settings deny reads of the source repository, grader, other conditions, and answer-bearing experiment files. Shell commands are constrained to the run directory. The exact settings file is hash-pinned before freeze.

Because model API access must remain available, this is tool-level rather than network-level isolation. A no-tools recall probe is mandatory. It asks the Agent B model to state any known counterexample to the formal bounded claim. A correct hidden tuple, a source H-number, or recognition of the exact public artifact fails the contamination gate and stops the experiment before condition runs.

A frozen canary list contains the hidden tuple and source-specific terms. Appearance before a logged derivation is flagged for blinded review. The canary is diagnostic; the recall probe is the predeclared stop rule.

## Agent A phase and handoff point

Agent A receives the formal definitions but is assigned only this phase:

1. implement exact predicates needed for the search;
2. test or exhaust the domain for `3 <= n <= 7`, height at most 20;
3. prepare an executable plan for `n=8`; and
4. stop without evaluating any `n=8` tuple.

The handoff occurs at the first tool-call boundary after Agent A reports the `n<=7` audit complete, or at the 20-minute cap if incomplete. Any evaluation of an `n=8` tuple by Agent A is a protocol deviation; the run is retained and the experiment stops rather than being rerun.

## Conditions and matched information

All four conditions start from the identical Agent A working-tree snapshot. Files are included in every arm because executable inquiry state is part of the shared task environment.

1. **Restart:** formal Agent B task plus the working tree; no account of Agent A's actions.
2. **Transcript:** Restart contents plus the complete chronological Agent A interaction, commands, and outputs.
3. **Structured handoff:** Restart contents plus a structured artifact generated from the transcript.
4. **Hypothesis graph:** Restart contents plus a graph artifact generated from the transcript.

The structured handoff and graph are produced by the same model, with the same USD 2 budget and matched prompts stored in `prompts/`. Neither may add evidence absent from the transcript. Every factual claim must cite a transcript event identifier. A pre-run audit rejects either artifact if a citation is missing or does not support the claim; both artifacts are regenerated once under their frozen prompts if either fails, and both versions are retained. A second failure stops the experiment.

Artifact lengths and production costs are reported, not equalized.

## Outcomes

Primary outcomes are verifier-confirmed task completion; tokens, tool calls, and wall time to the first useful novel trial; duplicate trials before completion; and false-claim inheritance if a natural false claim exists in Agent A's frozen trajectory.

A useful novel trial is the first executed computation that evaluates an `n=8` tuple, tests an untried pruning predicate on the `n=8` domain, or implements machinery necessary for either, excluding environment inspection and rereading. Its timestamp and command are derived from the tool log.

A duplicate is a command that reevaluates the same mathematical predicate over an `n<=7` tuple set already exhaustively evaluated by Agent A, without changing the implementation or checking a newly stated concern. Re-running an Agent A fixture or range expressly to validate inherited code is a replay, recorded separately. Ambiguous classifications are made from redacted logs by an adjudicator who does not see the condition label.

False-claim inheritance is scored only if Agent A states a claim contradicted by the verifier or a retained exact trial. Agent B inherits it if the claim causes a skipped branch, edit, or final conclusion before running an available exact refutation. If no natural false claim exists, the outcome is `undefined`, not zero.

Secondary outcomes are replay count, time and tokens to a verifier-accepted tuple, final verifier verdict, and total run cost.

## Analysis, success, and falsification

Report all four runs individually. There is no significance test and no “strongest baseline” selected after the fact.

The graph earns a case-level usefulness result only if it completes the task, and compared separately with Transcript and Structured handoff it has fewer duplicates or lower resumption cost without worse false-claim inheritance when that outcome is defined. A baseline that is cheaper because it fails is not evidence against the graph, but its failure remains visible.

If Restart solves immediately, or Transcript or Structured handoff matches the graph on completion, resumption cost, duplicates, and inheritance, the pilot supplies no evidence of incremental graph usefulness. All infrastructure failures, protocol deviations, and ceiling effects remain in the report.

## Frozen hashes

SHA-256:

```text
3413c256d3d028b0be49de739cc4bdcbe18e60cebb25786013755ab619aadf82  grader/verifier.py
2d5fe2de1b5b2666da8f10f2a32ba4dc4aa214b5a12caa6f2c61e1a9261700e0  task.md
09005a3baea23944f64c2cbfb22238f55c887bfa5d2ae2debd77c8dfa6ceb01d  prompts/agent-a.md
359c69a7fb80353d89cdd461fafc3767cd60e3a8181c37f5567a3924e1db7334  prompts/agent-b.md
f73dc5b1fca8a0fad55321bc4f1fda81019ed6a2bfc4b2ee92a86d41c299b310  prompts/hypothesis-graph.md
aba9e85599a9c5b8f4a9eb97c5271c19cec7b06147b87147df2ae95578b54fcc  prompts/recall-probe.md
6f6ef284371adc6d020f29a2d785dd391a279e2ac40f9182bb4f225b28b199dd  prompts/structured-handoff.md
ff70bf1dfd698163ea68462e6ee5fc03017c4f2d0c4349b1bb681d2823465731  isolation-settings.json
5c8535a3ff9f2ede36a87c3c94679613889a986dacd5d33bdd47c301fa90431c  canaries.txt
8ed5a9331897f56db7cc5eb462c9d0ae3248b7d2342a0943f9d99f8751632ff5  manifest.json
```
