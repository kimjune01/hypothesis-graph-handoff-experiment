# Ecological semantic-memory ablation results

Date: 2026-08-24

## Outcome

Both agents were explicitly instructed to use `MEMORY.md` as untrusted semantic memory. Both returned `(1,4,5,6,7,11,13,16)`, and the hidden verifier accepted both submissions with exact `ML(v)=2/17` and no seed certificate.

## Metrics

| Condition | Memory size | First `n=8` trial | Pre-trial tool calls | Replays | Duplicates | Total wall time | Cost | Turns | Output tokens |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Graph | 1,618 words | 25.718 s | 7 | 0 | 0 | 143.939 s | $0.38694 | 11 | 3,673 |
| Notes | 374 words | 30.756 s | 8 | 0 | 0 | 140.787 s | $0.23991 | 12 | 3,068 |

Time to first trial is measured from the first recorded tool event. The trial itself is not included in the pre-trial tool-call count.

Both sessions attempted to read Claude's project-level memory path before reading the experimental `MEMORY.md`; the path did not exist, so it leaked no prior result. Notes made one additional directory check for that missing path. These calls remain in the ecological timing rather than being removed post hoc.

## Claim ledger

- **Ecological use:** confirmed operationally. Both agents read the explicitly supplied memory and proceeded directly to `n=8`; neither duplicated the completed `n<=7` audit.
- **Faster orientation:** graph reached the first novel trial 5.038 seconds and one tool call earlier than notes in this single comparison.
- **Faster completion:** not supported. Notes finished 3.152 seconds sooner.
- **Lower cost:** contradicted. Graph cost $0.14703 more, about 61% above notes.
- **Less duplication or replay:** no separation; both recorded zero.
- **Better task success:** no separation; both passed.

## Interpretation

The ecologically accurate conclusion is a tradeoff:

> When both artifacts were explicitly used as semantic memory, the graph localized the continuation frontier slightly faster, while concise chronological notes achieved the same verified result with lower cost and slightly lower total wall time.

This does not establish incremental overall usefulness for the graph. Its five-second orientation advantage did not repay the additional reading and processing cost of an artifact more than four times as long.

## Limitations

- One post-outcome task and one run per arm.
- Artifact length was intentionally not equalized: 1,618 versus 374 words.
- The notes were manually written from the frozen trajectory, while the graph was model-generated.
- The graph included more detailed failed branches than the notes, so this compares deployed artifacts rather than structure under matched information density.
- The same model family had already solved the task in Pilot 4, though each run used a fresh session and no project memory file existed.
