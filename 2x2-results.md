# Verifiable-memory 2×2 results

Status: complete construction pilot; one run per cell.

## Primary cells

| Task | Format | Exact pass | DLog searches | Receipt replays | Duration | Turns | Cost |
|---|---|---:|---:|---:|---:|---:|---:|
| Independent | Graph | yes | 0 | 3 | 37.674 s | 5 | $0.463044 |
| Joint | Notes | yes | 0 | 3 | 28.636 s | 5 | $0.476204 |
| Independent | Notes | yes | 0 | 3 | 38.048 s | 5 | $0.467314 |
| Joint | Graph | yes | 0 | 3 | 39.235 s | 6 | $0.533112 |

Every cell inherited and used all three verified residues, replayed each cheap modular-exponentiation check, ran no BSGS, and produced an exactly correct answer. Thus Notes and Graph tied on completion, checkpoint reuse, replay count, and avoided rediscovery.

Graph minus Notes was -0.374 seconds in Independent and +10.599 seconds in Joint. The descriptive difference-in-differences was therefore +10.973 seconds against Graph. For cost it was -$0.004270 in Independent and +$0.056908 in Joint, an interaction of +$0.061178 against Graph. With one run per cell these are observations, not effect estimates.

## Controls and probes

- **Oracle Joint:** passed in 26.855 seconds, five turns, $0.443279, without DLog search.
- **No-handoff Joint:** passed in 41.694 seconds, six turns, $0.659259, after three BSGS searches. Its trace was routed across multiple reported Claude models, so its cost is not a clean paired baseline.
- **Corrupted R2:** replay killed the off-by-one residue, preserved R1 and R3, ran one BSGS for R2, then passed. This is successful targeted retraction and repair in the tested Graph case.
- **Deleted R2:** correctly treated the joint result as unsupported, ran one BSGS for the missing checkpoint, then passed.

## Interpretation

The pilot supports the more basic claim that both representations can transmit checked results as reusable interfaces under the Verifiable Knowledge protocol. It also supplies one Graph case of correct dependency-directed retraction.

It does not support the predicted format-by-task interaction. Explicit dependency edges did not reduce replay or rediscovery relative to informationally equivalent prose. The joint Graph run was instead slower and costlier than Joint Notes.

The task was too computationally cheap for a strong efficiency test: Agent A's BSGS searches took only 0.00–0.01 seconds each. All primary agents also chose to replay all three receipts, making the primary mechanism insensitive to organization. Artifact lengths were not matched: Joint Notes 154 words versus Graph 115; Independent Notes 127 versus Graph 106.

## Claim boundary

This is a one-bundle, one-run-per-cell construction pilot. It establishes neither a population effect nor a general null. The honest result is: in this instance, the protocol transferred verified knowledge successfully, while graph structure added no observed reuse benefit over concise notes.
