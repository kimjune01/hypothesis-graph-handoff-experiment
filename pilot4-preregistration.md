# Pilot 4 preregistration: outcome run

Status: frozen before any Agent B outcome.

## Disclosure

Pilots 1–3 stopped during artifact validation; no Agent B condition has run. Their failures show that sentence-level citation conformance is a separate artifact-generation problem. Pilot 4 tests the original handoff outcome and reports provenance quality as a limitation rather than a stopping gate.

Pilot 4 selects two already-public version-2 artifacts from commit `5b88db2`; they were generated before any Agent B outcome and cannot be changed. Selection after inspecting artifact form is disclosed. Block-level event citations are allowed. Unsupported or inaccurate inherited claims are not repaired: Agent B's response to them is part of the handoff test.

## Frozen conditions

Task, Agent A working tree, Agent B model and budget, isolation settings, outcome definitions, one-shot grading, and analysis remain those of `preregistration.md`.

- Restart: task plus identical Agent A working files.
- Transcript: Restart plus `runs/agent-a/agent-a-transcript.events.jsonl`.
- Structured: Restart plus `artifacts/structured-handoff.md`.
- Graph: Restart plus `artifacts/hypothesis-graph.md`.

Each condition runs once. No artifact regeneration, run replacement, or prompt change is permitted. Condition order is generated once from a recorded random seed before runs. The hidden verifier is applied only after all four conditions finish.

## Frozen hashes

```text
835b88c8fdc356e03164c1dddd0f974ce96727dacac102b3e30d0ee36bac14d8  artifacts/structured-handoff.md
63752beb0585074e3fbe0365b2da38f9b08b5d970f246032367fc9577cc43ff8  artifacts/hypothesis-graph.md
c5d7d0b0882628886210f8eb8c046d7472b87ea2a2c73c69fb5ae9e716b5841a  runs/agent-a/agent-a-transcript.events.jsonl
```
