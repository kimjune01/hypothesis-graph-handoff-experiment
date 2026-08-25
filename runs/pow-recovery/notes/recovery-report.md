# Recovery report: N1 salt rotation `n1-authoritative-v1` → `n1-authoritative-v2`

## What happened

The authoritative salt for source node `N1` rotated to `n1-authoritative-v2`; all
other salts are unchanged. Under the challenge formula
`SHA256("pow-recovery-v1:{node}:{salt}:{parent_digests}")` this changes N1's
challenge, hence its digest, hence the challenge of every node whose parent-digest
chain reaches N1: `D12` (parents N1, N2) and `E` (parent D12). `D23` (parents N2,
N3) does not depend on N1 and is untouched.

## Checks performed (cheap, one hash each per receipt)

`recovery.py` walks the DAG in topological order (`N1, N2, N3, D12, D23, E`),
recomputes each node's authoritative challenge from the current salts and the
current parent digests, and checks the inherited receipt against it: challenge
must match, `SHA256("{challenge}:{nonce}")` must equal the recorded digest, and
the digest must carry 20 leading zero bits.

| Node | Check result | Reason |
|------|--------------|--------|
| N1   | FAIL | challenge changed under the v2 salt |
| N2   | PASS | root unchanged, digest re-derives, difficulty holds |
| N3   | PASS | root unchanged, digest re-derives, difficulty holds |
| D12  | FAIL | parent digest N1 changed → challenge changed |
| D23  | PASS | parents N2, N3 unchanged; independently entitled |
| E    | FAIL | parent digest D12 changed → challenge changed |

The N2/N3/D23 passes also confirm the challenge-formula reconstruction (sources
use an empty parent-digest field, leaving a trailing `:`), since their recorded
challenges reproduce exactly.

## Retractions (all and only unsupported dependents)

Retracted: **N1, D12, E** — N1 because its root changed; D12 and E because their
entitlement chains pass through N1. Nothing else was retracted.

## Preservations

Preserved as-is: **N2, N3, D23**. Their receipts remain valid under the current
roots, so their original nonces and digests carry over unchanged into the new
bundle. D23 shares the N2 root with D12 but does not depend on the retracted
branch, so it keeps its entitlement.

## Recomputations (sequential nonce scan from 0, 20-bit difficulty)

| Node | New nonce | Candidate hashes tried | Discovery time (s) |
|------|-----------|------------------------|--------------------|
| N1   | 1,205,509 | 1,205,510 | 0.634 |
| D12  | 309,229   | 309,230   | 0.161 |
| E    | 266,526   | 266,527   | 0.139 |
| **Total** | | **1,781,267** | **0.934** |

Each recomputed receipt is entitled by its valid digest under the current
challenge; per protocol, earlier nonces were not rescanned to establish
minimality of the preserved receipts.

## Final state

`answer.json` holds the sorted `retracted` / `preserved` / `recomputed` arrays
and the rebuilt six-node receipt bundle. `recovery.py` ends with a full-bundle
validation pass: all six receipts check true under the current authoritative
roots (6 verification hashes, plus 6 challenge derivations).
