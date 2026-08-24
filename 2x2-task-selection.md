# Prospective 2×2 Task Selection

Status: provisional design recommendation; no instances generated and no outcomes observed.

## Factors

1. Task structure: **joint dependency** versus **independent outputs**.
2. Memory format: **chronological Notes** versus **dependency-structured Graph**.

Every cell uses the same Verifiable Knowledge fields, evidence, task instructions, and continuation policy. The format manipulation changes organization, not informational content.

## Recommended task family

Use fresh discrete-log instances in cyclic subgroups. Agent A discovers three residues and emits a checkable receipt for each. A receipt must pin the group parameters and demonstrate the claimed residue with modular exponentiation; verification must be materially cheaper than discovery.

### Joint-dependency task

Agent A establishes:

- `x ≡ r1 (mod n1)`
- `x ≡ r2 (mod n2)`
- `x ≡ r3 (mod n3)`

The subgroup orders are pairwise coprime. Agent B must use all three verified residues with CRT, under `0 <= x < n1*n2*n3`, to recover the unique `x` and return a deterministic checksum.

Deleting any one residue must leave multiple admissible values of `x` within the bound. This makes all three checkpoints necessary rather than decorative.

### Independent-output task

Agent A solves three discrete-log instances of the same sizes and supplies the same kind of receipts. Agent B returns three independent deterministic outputs, one derived from each residue. There is no operation that combines the residues.

This replaces the initially proposed one-log neutral task. A one-versus-three comparison would confound dependency structure with item count, payload size, and retrieval load.

## Matching requirements

- Use the same number and sizes of groups, residues, receipts, roots, and checks in both task regimes.
- Pad or canonicalize encodings so payload length does not reveal the condition.
- Put the statement of which inputs the final computation requires in both formats. The Graph may encode it as edges, but Notes must state the same dependency in prose.
- Generate one Agent A trajectory per task instance, then mechanically project the same substantive content into Notes and Graph.
- Use the same checksum family and comparable B-side arithmetic.
- Fix model, tools, token budget, timeout, and semantic-memory instructions across all four cells.

## Primary estimand

The confirmatory quantity is the interaction:

`(Graph - Notes under joint dependency) - (Graph - Notes under independent outputs)`

Measure checkpoint use and unnecessary replay per checkpoint. Treat end-to-end exact success as secondary because joint success compounds per-item failure and includes CRT execution.

## Required controls

1. **Oracle handoff:** give B the three residues directly. This estimates the ceiling and isolates CRT/computation failures from handoff failures.
2. **Deletion ablation:** remove each residue in turn. Joint-task uniqueness must fail; the independent task should lose only the corresponding output.
3. **No-handoff baseline:** confirm that B cannot cheaply redo discovery within its budget.
4. **Corrupted receipt:** verify that B rejects or replays a checkpoint whose executable check fails.
5. **Interruption at one, two, and three completed checkpoints:** measure correct frontier localization and resumption. This is a preregistered secondary test, not a replacement outcome.

## Instance constraints to freeze before generation

- `n1`, `n2`, and `n3` are pairwise coprime and each generator has the claimed exact order.
- The discrete-log solver and cost model are fixed in advance; empirical Agent A cost is checked for balance across regimes.
- Each missing joint-task residue leaves too many candidates to enumerate under B's fixed compute budget.
- Checksums are deterministic and sufficiently collision-resistant for exact grading.
- Instances, expected answers, and graders are generated and committed before any B run.

## Rejected candidates

- **Linear-system/null-space inheritance:** the proposed downstream task depended only on the final basis, so earlier checkpoints were ornamental.
- **Bounded null-space optimization:** proposed hidden roots made receipts unreplayable, and independently computed coefficient bounds did not safely compose.
- **One chained task versus one no-handoff task:** removed the memory manipulation from the neutral row.
- **Three-log CRT versus one matched-cost log:** confounded dependency with the number of inherited facts.

## Selection verdict

Proceed with the three-residue **CRT versus independent outputs** pair, subject to a construction audit and frozen instance generator. It isolates joint use of verified knowledge more cleanly than the alternatives considered. Do not run the 2×2 until the oracle, deletion, and difficulty-matching checks pass.
