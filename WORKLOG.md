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

## 2026-08-24 — Agent A outcome and primary protocol freeze

- The first Agent A launch failed before receiving a prompt because a shell substitution expanded to empty. Preserved as `agent-a-session.jsonl`; it performed no task work.
- The direct-stdin relaunch completed all three discrete logs with baby-step giant-step and independently replayed every modular-exponentiation receipt.
- Agent A reported residues `112107027`, `819310576`, and `873153835`. Its run cost USD 0.650285 and used six turns; raw trace and working files are preserved under `runs/2x2/agent-a/`.
- Discovery was unexpectedly cheap in local Python (0.00–0.01 seconds per instance), weakening the discovery-versus-replay cost contrast. We retained the task rather than replacing it after outcome observation.
- Froze the 2×2 preregistration, Agent B prompt, downstream tasks, and four task-aware memory projections before any Agent B or control result.
- The Joint and Independent rows contain the same three checkpoints. Notes and Graph state the same downstream dependencies; only chronological prose versus explicit node/edge organization changes.

Receipt: `2x2-preregistration.md`, `artifacts/2x2/`, `prompts/2x2-agent-b.md`, and the next commit.

## 2026-08-24 — 2x2 primary runs, controls, and diagnostics

- Ran controls first: Oracle Joint passed without DLog search; No-handoff Joint passed after three BSGS searches.
- Ran the four primary cells in preregistered order: Independent–Graph, Joint–Notes, Independent–Notes, Joint–Graph.
- Applied the hidden exact grader only after all four primary runs finished. All four passed.
- Every primary cell inherited all three residues, replayed all three cheap receipts, and ran zero discrete-log searches. The predicted difference in unnecessary rederivation was therefore null.
- Graph minus Notes duration was -0.374 seconds for Independent and +10.599 seconds for Joint, yielding an unfavorable +10.973-second descriptive interaction. The corresponding cost interaction was +$0.061178 against Graph.
- Ran the preregistered post-primary probes. A corrupted R2 receipt failed replay; the agent retracted and rediscovered only R2, preserved R1/R3, and passed. Deleting R2 likewise caused exactly one DLog search before passing.
- Interpretation fixed as a protocol-transfer success but a null/contrary result for the graph-format interaction in this construction pilot. No run was replaced.

Receipt: `2x2-results.md`, `2x2-result-hypothesis-graph.md`, `runs/2x2/`, and the next commit.

## 2026-08-24 — Prospective expensive-checkpoint recovery design

- Reframed the next study as a mechanism demonstration rather than an underpowered population comparison. One frozen adversarial case may support an existence claim; it cannot estimate frequency or average benefit.
- Consulted Claude on a tunably expensive proof-of-work construction. Accepted its six-node branching DAG and correction that corruption must target a source with descendants, not a leaf.
- Fixed the prospective corruption target `N1`, exact retraction set `{N1, D12, E}`, and preservation set `{N2, N3, D23}`.
- Separated the primary verifiability claim from the conditional Graph-versus-Notes claim. A Notes success will be reported as a representation null, not followed by retrospective task hardening.
- No instance, artifact, or recovery outcome has been generated.

Receipt: `pow-recovery-design.md` and the next commit.

## 2026-08-24 — Prospective PoW construction freeze

- Wrote failing tests before implementation for the six-node DAG, exact transitive invalidation, deterministic receipts, fail-closed checks, and selective-recovery grading.
- Implemented the harness after the expected missing-module failure; all 25 repository tests pass.
- Calibration at 18–20 bits was performed before instance freeze. Exact 21–22-bit challenges showed an excessive deterministic heavy tail; stopped only those calibration processes and retained every observation.
- Froze difficulty at 20 bits. The old bundle requires 6,292,014 sequential candidate hashes; the authoritative repaired subtree requires 1,781,267 across `N1`, `D12`, and `E`. Verification remains one hash per receipt.
- Defined corruption as a stale authoritative root: `N1` salt changes from `n1-authoritative-v1` to `n1-authoritative-v2`. This genuinely changes exactly `N1`, `D12`, and `E`; it is not a forged receipt that resolves to the old subtree after one repair.
- Froze Agent A's task and prompt before its run. No recovery-agent outcome has been observed.

## 2026-08-24 — PoW Agent A outcome and recovery freeze

- Agent A independently implemented the frozen construction and produced receipts exactly matching the hidden deterministic bundle.
- It performed 6,292,520 candidate hashes in 16.46 seconds across six nodes. Raw trace, program, receipts, measurements, and report are preserved under `runs/pow-recovery/agent-a/`.
- Agent A also rescanned earlier nonces to verify the lowest-nonce convention. We clarified prospectively that receiver entitlement requires only PoW validity under current roots (one hash); lowest nonce remains a deterministic generation/grading convention, not a cheaply verified claim.
- Froze the stale-N1 task, identical recovery prompt, Notes and Graph artifacts, and preregistration before any recovery-agent result.
- Notes are 178 words and Graph 133 words; length was recorded rather than equalized.

Receipt: `pow-recovery-preregistration.md`, `artifacts/pow-recovery/`, `prompts/pow-agent-b.md`, Agent A files, and the next commit.

## 2026-08-24 — Expensive-checkpoint recovery outcomes

- Ran recovery in preregistered order: Notes, then Graph. Applied the exact hidden grader only after both completed.
- Both passed with exact retraction `{N1,D12,E}`, preservation `{N2,N3,D23}`, recomputation `{N1,D12,E}`, and fully valid current bundles.
- Each performed exactly 1,781,267 candidate hashes. A deterministic full rebuild would require 5,455,691, so selective recovery avoided 3,674,424 hashes (67.35%).
- Notes finished in 64.542 seconds for $0.796555; Graph in 86.126 seconds for $0.848847. The representation comparison was null on correctness/work and unfavorable to Graph on observed time/cost.
- No-corruption control passed: all six nodes preserved and zero rebuilt.
- The unverifiable-attestation ablation failed before task work with organization-level HTTP 403. Preserved the failure and did not replace it; its outcome remains unobserved.
- Interpretation: primary existence claim for selective recovery supported; Graph-over-Notes claim not supported.

Receipt: `pow-recovery-results.md`, `pow-recovery-result-hypothesis-graph.md`, `runs/pow-recovery/`, and the next commit.

## 2026-08-24 — Prospective concurrent-handoff round designed

- Identified concurrency and clean entry points as a distinct untested motivation for the hypothesis graph.
- Attempted a Claude design consultation; Claude Code returned the same organization-level HTTP 403 before producing advice. No Claude recommendation was available.
- Designed three comparisons: serial versus concurrent Graph execution; Shared Notes versus manually Curated Packets versus mechanically generated Graph Packets; and a concurrent stale-root invalidation probe.
- Added Curated Packets as the strongest baseline. This prevents attributing the general benefit of bounded context to graph structure.
- Defined graph-native addressability, dependency-closure queries, atomic node claiming, automatic unlocking, and invalidation as the actual treatment—not graph-shaped prose.
- No task instance, prompt, or outcome has been generated.

Receipt: `concurrent-handoff-experiment-design.md` and the next commit.

## 2026-08-24 — Independent review improves concurrency design

- At the user's request, delegated an independent review to a fresh Codex subagent before implementation.
- The reviewer identified that only three child workers can run concurrently because the root occupies one of four collaboration slots. Replaced the four-branch DAG with `R0→{A,B,C}`, `{A,B}→JAB`, and `{JAB,C}→F`.
- Removed the heterogeneous task mixture because unmatched costs and verifiers would obscure coordination. Selected calibrated deterministic PoW.
- Replaced the three-condition end-to-end comparison with a canonical packet-equivalence and byte-transfer audit. Curated packets remain the strong baseline without treating noisy coordinator-writing time as a primary outcome.
- Specified a versioned scheduler with atomic claims, leases, parent-version vectors, exact publication checks, stale rejection, transitive invalidation, idempotency, and an immutable log.
- Fixed invalidation after JAB claims the old A version and records a progress marker.
- Narrowed claims to safe concurrency, automatic bounded entry packets, and localized versioned recovery on one frozen DAG.
- No implementation or outcome has been generated.

Receipt: revised `concurrent-handoff-experiment-design.md` and the next commit.

## 2026-08-24 — Economy of search added prospectively

- Clarified the user's intended term: Peircean uberty is expected fertility, or how much new knowledge a move may produce.
- Identified a construct-validity problem before implementation: deterministic PoW has controllable cost but nearly zero epistemic uberty because its successful result is guaranteed.
- Kept PoW for the concurrency workload and added a separate five-gate discriminating frontier for the economy-of-search mechanism.
- Fixed scheduler priority as preregistered expected decisive yield divided by expected total cost, applied only among currently open nodes with stable ties.
- Required scores and priors to be frozen without hidden answers or realized nonce counts; required exact logging of avoided work and regret against a frozen fixed order.
- Added a hidden failing gate whose cheap verdict must prevent an expensive successor subtree from ever being claimed.
- No gate instance, score, or outcome has been generated.

Receipt: revised `concurrent-handoff-experiment-design.md` and the next commit.
