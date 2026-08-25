# Recovery agent

Work only from `task.md`, `MEMORY.md`, and `receipts.json` in this directory. Do not inspect parent directories, Git history, experiment code, or other runs.

Treat memory claims as reusable interfaces under the Verifiable Knowledge protocol. Check receipts cheaply against current authoritative roots. When a root or receipt fails, retract all and only unsupported dependents, preserve independently entitled work, and sequentially rebuild only what is necessary.

Write the exact requested `answer.json`, a working recovery program, and `recovery-report.md` accounting for checks, retractions, preservations, recomputed nodes, candidate hashes, and elapsed discovery time. A PoW receipt is entitled by a valid digest under the current challenge; do not rescan earlier nonces merely to establish minimality.
