# Verifiable-memory 2×2 preregistration

Status: frozen after Agent A and before any Agent B or control outcome.

## Question and design

Does dependency-structured semantic memory reduce unnecessary rediscovery specifically when three verified facts must be used jointly, relative to when the same three facts support independent outputs?

The 2×2 crosses task structure (joint CRT versus independent outputs) with memory format (chronological Notes versus dependency Graph). All cells inherit the same three Agent A residues, public roots, executable checks, receipts, and replay-cost statements. Task-aware projections may express the downstream dependency, but Notes and Graph must contain informationally equivalent statements.

## Frozen checkpoints

Agent A used baby-step giant-step and recorded:

1. `x1 = 112107027 mod 1018699967`
2. `x2 = 819310576 mod 1032750773`
3. `x3 = 873153835 mod 1084101493`

Each receipt is checked by `pow(g, r, p) == h`. Agent A did not see either downstream task.

## Tasks

- **Joint:** recover the unique `x` in `0 <= x < n1*n2*n3` by CRT and compute SHA-256 of `dlog-2x2-v1:joint:{x}`.
- **Independent:** compute SHA-256 of `dlog-2x2-v1:independent-{i}:{ri}` for each of the same three residues.

Every joint residue is necessary: deletion leaves `ni` candidates, over one billion in each case. Independent deletion affects only its paired output.

## Outcomes

Primary descriptive outcomes per cell: exact grader pass; whether any BSGS/discrete-log search was run; number of cheap receipt replays; number of inherited checkpoints used; tool calls, wall time, tokens, and cost. The planned contrast is whether `Graph - Notes` in unnecessary rediscovery/replay is more favorable in Joint than Independent.

End-to-end success is secondary because Joint includes CRT. With one run per cell, report cases and measurements only; do not claim a rate or statistical interaction.

## Controls and order

Run oracle Joint first to test CRT ceiling, then no-handoff to measure independent rediscovery, then the four cells in deterministic randomized order from seed `8242026`. A corrupted-receipt probe and one-checkpoint deletion probe follow the primary cells and cannot replace them.

No failed or null run is replaced. Infrastructure failures remain recorded. The hidden deterministic grader is invoked only after all four primary runs finish.

## Fixed environment

Claude Code 2.1.227, the available default model reported by each trace, identical Agent B prompt, local Read/Write/Edit/Bash tools, 20-minute ceiling. Each run is isolated by instruction and contains only its task, memory, and created files. This is behavioral rather than security isolation.

## Claim boundary

This is a construction pilot with one shared instance bundle. It can show that the predicted mechanism occurs in these runs, or that it does not. Fast BSGS discovery creates a weak cost separation and limits claims about expensive proof inheritance.
