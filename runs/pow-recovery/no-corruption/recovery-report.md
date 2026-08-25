# Recovery report — no-corruption audit

## Outcome

All six nodes verified against the unchanged authoritative salts. Nothing was retracted, nothing recomputed; the full inherited bundle is preserved as-is.

- **Retracted:** none
- **Preserved:** D12, D23, E, N1, N2, N3
- **Recomputed:** none
- **Discovery time:** 0.000 s (no nonce scans were needed)

## Checks performed (6 checks, one hash each plus one challenge recomputation)

Processed in topological order (N1, N2, N3, D12, D23, E). For each node:

1. Recomputed the challenge from the authoritative salt in `MEMORY.md` and the entitled parent digests, joined `:` in edge order: `SHA256("pow-recovery-v1:{node}:{salt}:{parent_digests}")`.
2. Confirmed the recomputed challenge equals the challenge recorded in `receipts.json` (root unchanged).
3. Confirmed `digest == SHA256("{challenge}:{nonce}")` and that the digest has 20 leading zero bits.

| Node | Challenge match | PoW valid | Verdict |
|------|-----------------|-----------|---------|
| N1 | yes | yes (nonce 1884136) | preserved |
| N2 | yes | yes (nonce 678483) | preserved |
| N3 | yes | yes (nonce 2876980) | preserved |
| D12 | yes | yes (nonce 385518) | preserved |
| D23 | yes | yes (nonce 118958) | preserved |
| E | yes | yes (nonce 348439) | preserved |

## Retraction / preservation reasoning

No root changed and no receipt failed, so no retraction propagated along `N1→D12`, `N2→D12`, `N2→D23`, `N3→D23`, or `D12→E`. Every node is independently entitled by a valid digest under its current challenge; under the protocol that entitlement stands without rescanning earlier nonces to establish minimality.

## Candidate hashes

Zero candidate hashes were spent on discovery. Total hashing: 6 verification hashes (one per receipt) plus 6 challenge recomputations.

## Artifacts

- `recover.py` — recovery program (verifies, and would selectively retract/rediscover on failure).
- `answer.json` — sorted `retracted`/`preserved`/`recomputed` arrays and the full six-node receipts mapping.
