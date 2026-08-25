# Hypothesis Graph Handoff Experiment

## Research question

Can a second agent resume, verify, or challenge a first agent's unfinished inquiry more cheaply and reliably from a replayable hypothesis graph than from no memory, a raw transcript, or a strong structured handoff?

The experiment measures the value of the **persisted representation at an agent boundary**. It does not test whether a hypothesis graph makes the first agent reason better.

## Scope

### In scope

- One bounded mathematical inquiry begun by Agent A and continued by Agent B.
- A finite decision problem whose counterexamples and certificates are mechanically gradeable.
- Inquiries long enough to contain a genuine diagnosis, at least one plausible wrong turn, and useful unfinished work at the handoff point.
- The information Agent B can recover, check, reject, and reuse from different projections of the same Agent A run.
- Task outcome, resumption cost, duplicated work, false-claim inheritance, premise localization, retraction, and review cost.

### Out of scope

- Whether external verification can raise a model's capability. The Verus experiment tests that claim by varying the verdict source; this experiment holds the verdict-producing inquiry fixed.
- Whether graph-shaped prompting improves Agent A's reasoning.
- General long-term memory, personal memory, conversational recall, preference retention, or retrieval at scale.
- Cross-task learning from one issue to a related issue.
- Training, fine-tuning, or changing model weights.
- Claims about all tasks or mathematics in general. The pilot regime is bounded conjecture testing with exact verification.

## Claims this experiment can support

The experiment exists to supply evidence for the hypothesis graph **as a persistent handoff representation**. Every permitted claim must name the comparison, measured outcome, task regime, and sample.

### Primary claims

1. **Resumption:** Agent B resumes an unfinished coding inquiry from a hypothesis graph at lower measured cost than from the comparison artifacts, without reducing task completion.
   - Evidence: task completion plus tokens, dollars, commands, and time to first useful novel action.
2. **Reduced duplication:** Agent B repeats less of Agent A's completed investigation when handed the graph.
   - Evidence: mechanically derived duplicate-action and replay counts.
3. **Safer inheritance:** Agent B is less likely to act on a false inherited claim when the handoff carries replayable trials.
   - Evidence: natural and seeded false-premise outcomes.
4. **Cheaper verification:** An independent Agent C accepts or rejects the completed work at lower measured cost when given the graph.
   - Evidence: reviewer commands, tokens, time, and correct verdict.

These claims are comparative. The strongest non-graph condition that matches the graph on available evidence is the relevant baseline, not merely restart or a weak summary.

### Secondary claims

5. **Premise localization:** The graph lowers the cost of finding the earliest failed premise behind a wrong branch.
6. **Targeted retraction:** When a recorded root fails, Agent B retracts more dependent claims and preserves more independent claims than under the comparison artifacts.
7. **Representation efficiency:** The graph carries more reusable, checkable inquiry per handoff token or production dollar.

These claims are secondary because premise and dependency structure are native to the graph. They strengthen a result only if the graph also competes on representation-neutral primary outcomes.

### Claim strength by result

- **One successful case:** existence claim only: a graph *can* improve a handoff in the demonstrated regime.
- **Small preregistered pilot:** evidence about the sampled tasks, reported case by case; no population rate.
- **Larger sampled study:** paired average effects with uncertainty, limited to the declared task-selection population.
- **Null:** evidence that the graph did not separate from the strongest baseline under the tested conditions.

### Claims this experiment cannot support

- The hypothesis graph improves Agent A's reasoning.
- The graph independently produces the external-comparator capability lift demonstrated by Verus.
- The method works across arbitrary tasks, domains, models, or harnesses.
- Knowledge compounds across unrelated tasks or repositories.
- Kill-generated successor edges generally discover better hypotheses.
- The graph guarantees truth, soundness, or complete diagnosis.
- The graph is cheaper in absolute terms without including artifact-production and replay costs.

The paper must not turn a handoff result into any of these broader claims.

## Unit of comparison

The unit is one fixed Agent A trajectory projected into six handoff formats. Agent B receives the same repository state, task, remaining budget, model configuration, and Agent A evidence in every arm. Only the handoff artifact changes.

This same-run projection is the central control. If Agent A runs separately for each condition, the experiment confounds representation with differences in the original inquiry.

## Conditions

1. **Restart:** task statement and repository state only.
2. **Transcript:** Agent A's complete chronological trajectory, including commands and outputs.
3. **Summary:** a prose handoff produced from the trajectory by a strong model under a declared, generous budget.
4. **Provenance:** a mechanical log of actions, inputs, outputs, timestamps, and dependencies, without hypothesis or kill semantics.
5. **Structured handoff:** objective, current state, decisions, evidence, constraints, next action, and open questions, following the Handover design.
6. **Hypothesis graph:** claims, exact trials, predictions, observed outcomes, verdicts, kill conditions, dependency edges, killed branches, and open frontier.

All derived artifacts must come from the same source trajectory. Artifact sizes and production costs are reported rather than silently equalized. A secondary analysis may impose a common token budget.

## What is measured

### Primary outcomes

1. **Task completion:** whether Agent B produces a proof certificate or counterexample that passes the independent verifier.
2. **Resumption cost:** tokens, dollars, commands, and wall time until Agent B performs its first useful action not already completed by Agent A.
3. **Duplicated work:** Agent B commands or trials semantically equivalent to completed Agent A work, reported as a count and share of Agent B's pre-solution actions.
4. **False-claim inheritance:** whether Agent B acts on an Agent A claim whose recorded or seeded trial fails.

These are representation-neutral outcomes and carry the headline comparison.

### Secondary outcomes

5. **Failed-premise localization:** cost until Agent B identifies the earliest invalid premise supporting a wrong branch.
6. **Dependency-directed retraction:** after one root is invalidated, whether Agent B retracts all and only the conclusions that depend on it.
7. **Review cost:** commands, time, and tokens required by an independent Agent C to accept or reject Agent B's final result.
8. **Information efficiency:** useful inherited facts and trials per handoff token and per dollar spent producing the artifact.

Retraction and premise localization are native to the graph. They are secondary so the graph must first compete on outcomes every representation can achieve.

## Operational definitions

### First useful novel action

The first command or edit that advances the inquiry and is not equivalent to an action Agent A already completed. The classification rule must be written before inspecting condition outcomes. Exact command normalization is mechanical; ambiguous equivalence is adjudicated blind to condition.

### Duplicate

An action that tests the same predicate over materially the same state as an Agent A action and produces no new discriminating evidence. Re-running a recorded trial expressly to verify it is classified as **replay**, not duplication. Replay cost is reported separately.

### False-claim inheritance

Agent B inherits a false claim when it uses that claim to choose an edit, skip a relevant branch, or justify a conclusion before running the claim's available falsifying trial.

### Successful retraction

After a declared root fails, Agent B marks every dependent conclusion unsupported and preserves unrelated claims. Over-retraction and under-retraction are scored separately.

## Task selection

The pilot uses a freshly generated inquiry into a bounded mathematical claim. Later studies should sample tasks through a declared procedure rather than selecting only cases where the graph succeeds.

Each task must satisfy all of the following:

- A clean task environment and independent verifier can be pinned.
- The visible problem permits plausible but incomplete approaches.
- Agent A requires enough investigation for a handoff to contain useful state.
- The final outcome and decisive intermediate trials can be replayed exactly.

Run a recall probe for each task. Report exclusions and failed setup attempts. Do not replace hard nulls after observing condition results.

## Handoff points

Choose handoff points by a rule fixed before running Agent B, for example:

- a fixed token or cost budget;
- the first killed plausible hypothesis;
- immediately after a plausible but false hypothesis becomes the leading branch;
- immediately before a known discriminating trial.

The primary experiment should use one uniform budget-based rule. Event-based points can form preregistered diagnostic strata.

## Perturbations

Two forms of false premise are needed:

1. **Natural:** a wrong claim Agent A actually adopted during inquiry.
2. **Seeded:** a forged or stale claim inserted into every representational condition with equivalent surface content.

Every seeded claim must have a cheap deterministic trial that refutes it. In the graph arm, the forged node must look structurally valid except that replay kills it. This tests replay rather than malformed-record detection.

A separate root-pull perturbation invalidates one previously accepted premise after handoff. This measures retraction rather than initial skepticism.

## Procedure

1. Freeze the task, environment, verifier, model versions, prompts, and budgets.
2. Run Agent A once under the inquiry harness and retain its full artifacts.
3. Stop at the preregistered handoff point.
4. Generate all six handoff conditions from that same trajectory.
5. Randomize condition order and run fresh Agent B instances in isolated environments.
6. Apply the natural, seeded, and root-pull probes according to the preregistration.
7. Grade final certificates with the independent verifier.
8. Derive mechanical metrics from command logs and recorded trials.
9. Have blind adjudicators resolve only the equivalence judgments that cannot be computed.
10. Give Agent C the final result and its condition-specific record, then measure review cost.

Agent B should come from a different model family than Agent A in the main analysis. A same-family replication separates cross-model handoff from general session resumption.

## Sources to reuse

- **SWE-ContextBench:** coding-task execution, resolution, time, and cost metrics. Reuse the measurement machinery, not its pre-cutoff task pool.
- **Handover:** transcript, compressed-memory, and structured-handoff comparison design; deterministic field scoring.
- **STALE:** false-premise resistance and downstream adaptation probes.
- **Scientific-RAM:** obligation preservation across role handoffs, especially evaluator-facing details that are easy to omit.
- **MemoryArena and MemoryAgentBench:** related-work baselines for multi-session action and memory competence, not experimental substrates.

## Analysis

Report every task-condition result and denominator. With a small task set, emphasize paired differences, confidence intervals, and existence or null evidence rather than a population resolve rate.

Primary paired comparisons:

- hypothesis graph versus transcript;
- hypothesis graph versus summary;
- hypothesis graph versus structured handoff;
- hypothesis graph versus provenance.

The restart condition estimates how much any inherited artifact helps. Transcript is the lossless but costly baseline. Structured handoff is the strongest practical non-graph baseline.

## Success and falsification

The graph is useful if it reduces resumption or review cost without reducing task completion, and if it reduces false-claim inheritance relative to the strongest non-graph handoff.

The preferred reporting form is concrete:

> On [N] preregistered bounded mathematical inquiries, Agent B receiving a hypothesis graph achieved [completion result] while using [cost difference] to resume, repeating [duplication difference] fewer completed trials, and inheriting [false-claim difference] fewer refuted claims than [strongest baseline].

Omit any clause whose outcome was not measured or did not separate. Report the paired cases and denominators next to the aggregate.

The strong claim fails if a transcript, summary, provenance log, or structured handoff matches the graph on completion, resumption cost, false-claim inheritance, and review cost. If the graph wins only on retraction fields defined in its own vocabulary, the experiment does not establish general usefulness.

A null on tasks Agent B solves immediately from scratch does not distinguish the formats. It diagnoses bad task selection for this question and must still be reported.

## Main threats to validity

- **Contamination:** Agent B may know the fix and ignore every artifact.
- **Ceiling effects:** easy tasks hide the value of handoff.
- **Selection on success:** choosing only long inquiries where the graph already looks useful inflates the result.
- **Format versus process:** separately generated Agent A runs confound the treatment.
- **Weak competing artifacts:** low-effort summaries or handoffs create a straw baseline.
- **Unequal information:** conditions may omit different evidence rather than encode the same evidence differently.
- **Graph-native scoring:** retraction metrics may reward the treatment by definition.
- **Judge leakage:** LLM scoring can import the same unsupported judgment the graph is meant to replace.
- **Model-family effects:** Agent B may understand artifacts written by its own family better.
- **Infrastructure failures:** setup and grader failures can be mistaken for task or memory failures.

## Relationship to the Verus result

This experiment does not replace Verus.

Verus varies the source of the verdict and tests a capability mechanism: an external comparator carries a model to a fix it does not reach through self-grading. The handoff experiment holds Agent A's inquiry fixed and varies its persisted representation. It tests whether the hypothesis graph makes verified work cheaper and safer to inherit.

The two experiments support separable claims:

- **External comparator:** capability through surprise from outside the model.
- **Hypothesis graph:** accountable, reusable inquiry across agent boundaries.

## Fail-closed mechanism result

A separate bounded experiment now supports the narrower shared-memory claim without relying on model-performance effects:

> When graph claims carry frozen work, dependency versions, and checkable receipts, the tested protocol rejects stale or unsupported worker publications instead of admitting them as current shared knowledge.

The declarative protocol passed complete depth-6 exploration of 14,967 states. Scheduler commit `f88647b` matched the independent model on a frozen ten-disposition basis, passed six forced race/boundary schedules and two pre-commit crash probes, and killed seven exact source mutants. This is exact bounded evidence, not a significance study or a claim about arbitrary schedulers.

This result makes **safer inheritance** the load-bearing experimentally supported extension of verifiable knowledge. Resumption cost, concurrency, and bounded packets remain useful demonstrations, but they do not carry the reliability claim.

## Minimum viable pilot

- One bounded counterexample-search task for the instrumentation pilot.
- One fixed Agent A trajectory per task.
- Four initial conditions: restart, transcript, strong structured handoff, hypothesis graph.
- One Agent B family, with a second family only after the harness is validated.
- A natural false premise if one occurs; no seeded premise in the first run.
- Mechanical grading of completion, cost, duplicate trials, replay, and inheritance.

The pilot tests whether the instrumentation works. It does not support a rate claim. Expand only after the scoring rules and task-selection procedure survive the pilot without retrospective repair.
