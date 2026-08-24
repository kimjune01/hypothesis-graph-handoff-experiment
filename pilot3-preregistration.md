# Pilot 3 preregistration: schema-constrained artifacts

Status: frozen. This is a new preregistration, not an amendment.

## Prior failures

Pilot 1 and Pilot 2 both stopped before any Agent B run. Free-form Markdown generators repeatedly attached citations to blocks rather than individual factual claims. Their prompts, outputs, and audits remain in Git history through commit `51df25e`. No Agent B outcome has been observed.

## Frozen inputs and sole change

Pilot 3 reuses Agent A's trajectory and working tree unchanged from commit `5d39b68`. The task, verifier, agents, isolation, four conditions, budgets, outcome definitions, and analysis remain those of `preregistration.md`.

Only artifact serialization changes. Claude Code must return JSON conforming to frozen schemas. Every structured-handoff claim and every hypothesis-graph field is an object with atomic `text` and a nonempty list of `event-N` sources. This makes citation presence mechanically checkable.

## One-shot gate

Each artifact gets one generation attempt. A validator must confirm schema conformance and that every cited event exists in the frozen transcript. The experimenter then checks whether each event supports its atomic claim. Any unsupported claim or missing event stops Pilot 3 before Agent B. There is no repair or regeneration.

The JSON is the condition artifact; it is not converted to prose before Agent B receives it.

## Frozen hashes

SHA-256:

```text
203e115c3d5a61996f1dd5ec7500e38dbed54b7567c155501cabb220115684fe  schemas/hypothesis-graph.schema.json
e1b47079c77690f73927525e9c041add55a70b1283133e12ca0e3cf50275c2f8  schemas/structured-handoff.schema.json
8cfb92ed0be967d8c80245d73adeb06eac881584e4f8873a96fc22e50b0d27c5  prompts/pilot3-hypothesis-graph.md
a74a03d370e4232dfae56c4ee7cfe21ae688c0c42d56387319c1585a86a11c78  prompts/pilot3-structured-handoff.md
9d48be8f46b0483a4edd11c52152da83bb5cd40d706aebecbd4b2ea3f91dd58b  artifact_validation.py
c5d7d0b0882628886210f8eb8c046d7472b87ea2a2c73c69fb5ae9e716b5841a  runs/agent-a/agent-a-transcript.events.jsonl
```
