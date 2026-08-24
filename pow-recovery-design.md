# Expensive-checkpoint recovery demonstration

Status: prospective design; no task instance or outcome has been generated.

## Claim boundary

This is a mechanism demonstration, not a frequency estimate.

- **Primary existence claim:** verifiable memory can detect a corrupted expensive checkpoint, retract exactly its dependent work, preserve an unaffected branch, and rebuild only the necessary subgraph.
- **Conditional representation claim:** if equally informative Notes mislocalize the repair or cost more while Graph succeeds, this instance demonstrates a representation-induced difference. If both succeed equally, this claim is null.

No significance test is planned. One frozen adversarial instance can support the primary existence claim; it cannot support typicality, expected savings, or a population effect.

## Candidate mechanism

Use deterministic proof-of-work checkpoints: discovery is sequential SHA-256 nonce search at a frozen difficulty; verification is one hash. Deterministic lowest-valid-nonce search makes rebuild cost reproducible rather than dependent on luck.

## Minimal dependency DAG

- `N1`, `N2`, `N3`: independent source PoW checkpoints.
- `D12`: PoW rooted in verified outputs of `N1` and `N2` plus a pinned salt.
- `D23`: PoW rooted in verified outputs of `N2` and `N3` plus a pinned salt.
- `E`: PoW rooted in `D12` plus a pinned salt.

Corrupt `N1` after handoff. The exact required retraction set is `{N1, D12, E}`. The exact preservation set is `{N2, N3, D23}`. Rebuilding the certified bundle requires precisely three discovery searches.

This topology exercises a join, a shared ancestor, an independent surviving branch, and transitive propagation.

## Required controls

1. Information- and approximately token-matched chronological Notes and dependency Graph.
2. Same claims, checks, roots, receipts, salts, and dependency statements in both.
3. No-corruption false-positive-retraction control.
4. Symmetric `N3` corruption probe frozen in advance.
5. Verifiability ablation using unsupported attestations, to isolate cheap checking from graph organization.
6. Exact grader for retraction set, preservation set, rebuilt receipts, number of searches, and final certified bundle.

## Construction hazards

- Keep salts and dependencies in both memory artifacts so receipts alone do not reveal topology.
- Do not put recovery instructions in Graph fields that Notes lacks.
- Freeze chronological placement before runs; do not make Notes artificially confusing after seeing Graph succeed.
- Calibrate difficulty before freezing the instance, targeting meaningful seconds per discovery without exceeding the run budget.
- Report the mechanism as verifiable computational memory unless a later task adds genuinely semantic claims.
