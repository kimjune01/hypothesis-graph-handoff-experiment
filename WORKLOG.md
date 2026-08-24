# Work log

Purpose: preserve the experiment's decision history, including failed protocols, post-outcome changes, and negative results. This file is append-only after its initial reconstruction. Corrections must be new dated entries; do not silently rewrite earlier entries.

Commit history and raw artifacts remain the authoritative receipts. This log is a navigational record, not a replacement for them.

## 2026-08-24 — Initial protocol

- Defined the target claim as usefulness at an agent handoff rather than standalone truth or improvement to Agent A's reasoning.
- Chose same-run projection as the central control: all memory artifacts must derive from one Agent A trajectory.
- Initially considered GitHub debugging tasks and audited `sharkdp/bat#3724`, `sharkdp/bat#3710`, `flux-rs/flux#1532`, and `antonmedv/fx#415` under Claim, Spec, Oracle, Frame, Gold, Score, and Decay.
- Rejected the GitHub tasks for public-solution leakage, ceiling effects, incomplete grading, or missing raw trajectories.
- After discussion with Claude, selected a bounded mathematical counterexample search derived from the Lonely Runner case study.
- This task choice occurred before Agent A or Agent B outcome runs.

Receipts: commits `441757a` and `8395c93`; `candidate-audit.md`; `preregistration.md`.

## 2026-08-24 — Agent A checkpoint

- Agent A was restricted to `3 <= n <= 7` and forbidden to evaluate an `n=8` tuple.
- Agent A built exact predicates, corrected three mistaken test expectations, exhausted the permitted domain, and found no seedless band tuple through `n=7`.
- Agent A left executable code, receipts, and an `n=8` plan.
- No canary match or `n=8` evaluation occurred.

Receipt: commit `5d39b68`; `runs/agent-a/`.

## 2026-08-24 — Pilots 1–3 stopped before outcomes

- Pilot 1 required claim-level transcript citations. Initial and one allowed regenerated artifacts used block-level citations, triggering the preregistered stop.
- Pilot 2 banned tables and tightened inline citations. It again failed the one-shot citation rule.
- Pilot 3 used JSON schemas requiring an event list for every atomic field. Both artifacts passed schema and event-existence validation, but semantic audit found unsupported or inaccurately compressed claims.
- No Agent B outcome was run in Pilots 1–3.
- These failures were retained rather than repaired silently.

Receipts: commits `5b88db2`, `4a7eb04`, `51df25e`, `f6ef2ed`, and `6800dbe`; `artifacts/pilot*/pre-run-audit.md`.

## 2026-08-24 — Pilot 4 outcome run

- Started a new, explicitly disclosed protocol after the three instrumentation stops.
- Selected already-public version-2 Structured and Graph artifacts before any Agent B outcome.
- Ran conditions in preregistered order: Structured, Graph, Transcript, Restart.
- All four conditions returned the same verifier-accepted tuple.
- Graph reached the first novel trial and final answer fastest, but Transcript was slightly cheaper and all conditions had zero duplicate `n<=7` trials.
- Restart also solved the task, revealing a ceiling effect. The result does not show that the graph enabled completion.
- Restart stated an incorrect exact `ML` value in its explanation; the hidden verifier recomputed the correct value and still accepted the tuple.

Receipt: commit `8ae5794`; `results.md`; `result-hypothesis-graph.md`; `runs/pilot4/`.

## 2026-08-24 — Ecological-ablation motivation

- After seeing Pilot 4, we questioned whether identifying the graph and telling the agent to use semantic memory was a bias.
- We decided that explicit semantic-memory instructions are part of the intended deployment, not a nuisance variable.
- Proposed a more ecologically accurate comparison: ordinary chronological notes versus a structured hypothesis graph, with identical instructions to use `MEMORY.md` as untrusted semantic memory.
- This was a post-outcome design change. It was preregistered as an ablation, not represented as an untouched confirmation.

Receipt: commit `406d8ee`; `ecological-ablation-preregistration.md`.

## 2026-08-24 — Ecological ablation outcome

- Graph and Notes both found the same verifier-accepted tuple and neither repeated the completed `n<=7` audit.
- Graph reached the first `n=8` trial 5.038 seconds and one tool call earlier.
- Notes finished 3.152 seconds sooner and cost about 61% less.
- Artifact lengths were not matched: Graph was 1,618 words; Notes was 374 words.
- Both Claude sessions attempted to read a project-level memory path. The file did not exist and leaked no result. Notes made one additional directory check; these calls remained in the metrics.
- Interpretation: graph structure may help frontier localization, but the tested graph's extra processing cost outweighed that small advantage.

Receipt: commit `747b41a`; `ecological-ablation-results.md`; `ecological-result-hypothesis-graph.md`; `runs/ecological/`.

## 2026-08-24 — Prospective next experiment

- We observed that the current task is a direct frontier search. Neither memory contained the final proof, so both agents necessarily derived and verified it.
- Proposed a two-regime experiment:
  1. chained-verification tasks, where a downstream result depends on composing several already verified checkpoints; and
  2. neutral tasks, where continuation depends on at most one inherited result.
- Prospective mechanism prediction: the Graph–Notes difference in unnecessary re-derivation should be larger for chained-verification tasks than for neutral tasks.
- The current task may serve as a neutral control, but this designation is post hoc and must be treated as such. A new neutral task should be sampled prospectively for confirmatory use.
- No chained-verification task has been selected and no result for this interaction hypothesis has been observed.
- To avoid prompting the desired behavior, future Agent B instructions should say only to use the semantic memory; they should not explicitly say “do not re-derive proofs.”

## Rules for future entries

- Add an entry before each task selection, protocol freeze, exclusion, run, grader invocation, and analysis change.
- Label decisions as prospective or post-outcome.
- Record exclusions and infrastructure failures, even when inconvenient.
- Never replace a failed or null run; record any follow-up as a new pilot.
- Link each entry to immutable commits and raw artifacts.
- Distinguish exploratory observations from claims that were preregistered.

## 2026-08-24 — Prospective protocol correction: verifiable knowledge

- Before selecting a chained-verification task, we noticed that earlier graph-generation prompts mostly requested graph fields and did not fully run the *Verifiable Knowledge* protocol.
- Added a shared operational contract requiring an exact claim, three-state verdict, executable check, kill condition, pinned provenance roots, terminal witness, replay cost, and downstream retraction semantics.
- Added an author prompt that distinguishes proof discovery from proof verification and preserves completed proofs or certificates as reusable interfaces.
- Added a parallel chronological-notes author prompt carrying the same entitlement fields without explicit node or dependency-edge syntax.
- Added a receiver prompt instructing the continuation agent not to re-derive established proofs by default, but to replay attached checks when receipts are stale, inconsistent, challenged, or rooted in changed inputs.
- This change is prospective. No chained-verification task has been selected and no outcome under these prompts has been observed.
- Future Notes and Graph artifacts must contain the same verification primitives; their difference should be chronological versus dependency-structured organization, not bare assertions versus executable receipts.

## 2026-08-24 — Prospective 2x2 task-selection consultation begins

- Began a Claude consultation before selecting either task for the planned 2x2.
- Required one chained-verification task and one neutral-continuation task, each crossed with Notes and Graph memory.
- Selection criteria were fixed before recommendations: exact mechanical grading; fresh Agent A trajectories; completed proof or certificate checkpoints for the chained task; downstream work that uses rather than merely re-proves those checkpoints; comparable surface difficulty; no answer leakage; and checks cheaper than original discovery.
- No task has been selected and no 2x2 outcome has been run.

## 2026-08-24 — Prospective 2x2 task family selected provisionally

- Claude's first suggestions included a linear-system handoff whose downstream task used only the final null-space basis. We rejected it because the earlier checkpoints were decorative rather than necessary.
- A bounded null-space replacement was rejected because it hid provenance roots from Agent B and its independent step bounds did not safely characterize their combined feasible region.
- We proposed three discrete-log residues composed by CRT for the chained task and one matched-cost discrete log for the neutral task.
- Claude identified a fatal one-versus-three item-count confound: memory load, payload size, and retrieval surface would vary with task structure.
- We corrected the neutral task to three independent discrete logs with three independent downstream outputs. The joint task uses the same three kinds of residues but requires their composition through CRT.
- Provisionally selected this `CRT versus independent outputs` family, conditional on a construction audit, oracle-CRT ceiling test, per-residue deletion ablations, no-handoff baseline, corrupted-receipt test, and matched artifact construction.
- No instances have been generated and no outcome has been observed.

Receipt: `2x2-task-selection.md` and the commit containing this entry.

## 2026-08-24 — Prospective 2x2 construction begins

- Fixed generator seed `8242026` before Agent A or Agent B outcomes.
- Wrote failing tests first for deterministic generation, exact subgroup and receipt checks, CRT recovery, necessity of every joint checkpoint, independent-output separability, answer non-leakage, and exact graders.
- Implemented the construction only after observing the expected missing-module and missing-function failures. All 20 repository tests pass.
- Chose one shared set of three discrete-log instances for both task regimes. Agent A's discoveries can therefore be held fixed; only Agent B's downstream obligation changes.
- Froze Agent A's public task and protocol prompt. The task withholds downstream use so Agent A cannot tailor checkpoint discovery to either experimental row.
- No Agent A or Agent B outcome has yet been observed.
