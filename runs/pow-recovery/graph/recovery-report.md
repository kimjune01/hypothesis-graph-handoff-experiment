# Recovery report: N1 salt rotation (`n1-authoritative-v1` → `n1-authoritative-v2`)

Run by `recover.py` on 2026-08-24. Result: 3 retracted, 3 preserved, 3 recomputed; full six-node bundle re-verified in `answer.json`.

## Checks (cheap verification, one hash each)

Every inherited receipt in `receipts.json` was checked two ways against the current authoritative roots, in topological order:

1. **Challenge check** — recompute `SHA256("pow-recovery-v1:{node}:{salt}:{parent_digests}")` under the current salts and the parent digests the old receipt chain claims, compare to the stored challenge.
2. **PoW check** — recompute `SHA256("{challenge}:{nonce}")`, compare to the stored digest, confirm ≥ 20 leading zero bits.

| Node | Challenge matches current root | PoW digest valid |
|------|-------------------------------|------------------|
| N1   | **no** (salt rotated)          | yes (but under stale challenge) |
| N2   | yes                            | yes |
| N3   | yes                            | yes |
| D12  | yes, relative to old N1 digest | yes |
| D23  | yes                            | yes |
| E    | yes, relative to old D12 digest | yes |

Total verification cost: 12 hashes (2 per node). No mining was needed to determine the frontier.

## Retractions (all and only unsupported dependents)

- **N1** — its stored challenge was built from the retired `n1-authoritative-v1` salt; under `n1-authoritative-v2` the challenge is different, so the old receipt certifies work on a dead root.
- **D12** — its challenge embeds N1's digest as first parent digest. N1's retraction forces a new N1 digest, which changes D12's challenge, voiding its receipt. (Its stored PoW was internally valid, but only against the stale parent.)
- **E** — sole parent is D12; D12's new digest changes E's challenge the same way.

## Preservations (independently entitled work)

- **N2, N3** — source nodes on unchanged salts; challenges and digests re-verify exactly.
- **D23** — parents are N2 and N3 only. Both parents kept their digests, so D23's challenge is unchanged and its receipt re-verifies. Sharing N2 with D12 creates no support edge from N1's subtree, so D23 is untouched by the rotation.

Preserved receipts are carried into the new bundle byte-for-byte; none were re-mined.

## Recomputations (sequential rebuild, topological order)

Discovery is a sequential nonce scan from 0; a receipt is entitled by the first valid digest found under the current challenge (no minimality rescan of earlier nonces beyond the natural sequential order).

| Node | New challenge (prefix) | Nonce | Candidate hashes tried | Discovery time |
|------|------------------------|-------|------------------------|----------------|
| N1   | `a5430d5fc2c1…` | 1,205,509 | 1,205,510 | 0.508 s |
| D12  | `25267e1736d0…` | 309,229 | 309,230 | 0.132 s |
| E    | `5f4c76806c19…` | 266,526 | 266,527 | 0.112 s |

Totals: 1,781,267 candidate hashes, 0.752 s of discovery time. Expected cost per node at 20 bits is ~2²⁰ ≈ 1,048,576 candidates; the observed total (~0.57× of 3·2²⁰) is within normal variance.

## Final audit

After rebuild, all six receipts were re-verified end-to-end: each challenge recomputed from current salts and current parent digests, each digest recomputed from `{challenge}:{nonce}`, difficulty confirmed at 20 bits. All pass. `answer.json` contains the sorted `retracted` / `preserved` / `recomputed` arrays and the full receipt bundle.
