# Agent A report: certified PoW DAG (pow-recovery-v1)

Built 2026-08-24 with `pow_dag.py` (Python 3, hashlib), single-threaded sequential search. Receipts in `receipts.json`, per-node search measurements in `measurements.json`.

## Shared definitions

- Hash: lowercase SHA-256 hex of UTF-8 text.
- Difficulty: 20 leading zero bits — `int(digest, 16) < 2**236`.
- Proof digest at nonce `k`: `SHA256(f"{challenge}:{k}")`.
- Challenge for node `v`: `SHA256("pow-recovery-v1:{v}:{salt}:{parent_digests}")`, where `parent_digests` is the parents' receipt digests in dependency order joined by `:` (empty for sources, leaving a trailing colon in the preimage).
- Every receipt uses the **lowest** valid nonce, found by sequential search from 0.

## Nodes

### N1

- **Claim / state:** Certified source node. Lowest valid nonce for challenge `61aca0207ddbaf49027ff8ba25638dcbef2fd8b0653b23a170b8091b4e26b2d1` is **1884136**, with proof digest `00000b3b32378af750a60ba22a964295c90526936e37fc3ac00c7d41129d8421`.
- **Pinned roots:** salt `n1-authoritative-v1`; challenge preimage `pow-recovery-v1:N1:n1-authoritative-v1:` (trailing colon, empty parent list); difficulty 20 bits.
- **Executable check:** `python3 -c "import hashlib; c=hashlib.sha256('pow-recovery-v1:N1:n1-authoritative-v1:'.encode()).hexdigest(); d=hashlib.sha256(f'{c}:1884136'.encode()).hexdigest(); assert int(d,16) < 2**236 and d=='00000b3b32378af750a60ba22a964295c90526936e37fc3ac00c7d41129d8421'"` — plus the lowest-nonce scan in `pow_dag.py:verify` (all `k < 1884136` fail the threshold).
- **Kill condition:** any recomputed challenge or digest mismatch; digest ≥ 2^236; or any nonce below 1884136 satisfying the threshold.
- **Dependencies:** none (source).
- **Observed receipt:** nonce 1884136, digest `00000b3b...129d8421` (full value in `receipts.json`).
- **Verification vs discovery cost:** discovery 1,884,137 hashes, 4.704 s. Validity check: 2 hashes. Lowest-nonce certification: same 1,884,137 hashes — no shortcut exists.

### N2

- **Claim / state:** Certified source node. Lowest valid nonce for challenge `1b57582ba064cdd58cda11ecd9f5e13e9c4d1673adeff98f00cea0d31c99f523` is **678483**, digest `00000f55eede454d6c6259182b3004f7d6afd4637d4732d217c22e8a8966dd40`.
- **Pinned roots:** salt `n2-authoritative-v1`; preimage `pow-recovery-v1:N2:n2-authoritative-v1:`; difficulty 20 bits.
- **Executable check:** same pattern as N1 with N2's challenge and nonce; lowest-nonce scan in `pow_dag.py:verify`.
- **Kill condition:** challenge/digest mismatch, threshold failure, or a valid nonce below 678483.
- **Dependencies:** none (source).
- **Observed receipt:** nonce 678483, digest `00000f55...8966dd40`.
- **Verification vs discovery cost:** discovery 678,484 hashes, 1.690 s. Validity: 2 hashes. Lowest-nonce certification: full 678,484-hash rescan.

### N3

- **Claim / state:** Certified source node. Lowest valid nonce for challenge `21be343cdaa4f7c93a1eaa8bdb6c944bb9d1f52e132ecdd8bcc85df063e50cb2` is **2876980**, digest `00000037aeabc6a5142ed81cfbf19f428588ad352600a030870c99960e8987cc`.
- **Pinned roots:** salt `n3-authoritative-v1`; preimage `pow-recovery-v1:N3:n3-authoritative-v1:`; difficulty 20 bits.
- **Executable check:** same pattern as N1 with N3's values; lowest-nonce scan in `pow_dag.py:verify`.
- **Kill condition:** challenge/digest mismatch, threshold failure, or a valid nonce below 2876980.
- **Dependencies:** none (source).
- **Observed receipt:** nonce 2876980, digest `00000037...0e8987cc`.
- **Verification vs discovery cost:** discovery 2,876,981 hashes, 7.484 s (the most expensive node). Validity: 2 hashes. Lowest-nonce certification: full rescan.

### D12

- **Claim / state:** Certified derived node over [N1, N2]. Challenge `36ea6ec46f0dbe9f126f8b7e5cf1b361715bec42d8fbdbb99c11fca9556d33e0` (preimage embeds N1's then N2's receipt digests); lowest valid nonce **385518**, digest `00000ec2c86cc7fc312b9a1112b4063765ac17729a6f9bf2dd496dca8edacd04`.
- **Pinned roots:** salt `d12-v1`; parent digests pinned to N1 = `00000b3b...8421` and N2 = `00000f55...dd40` in that order.
- **Executable check:** recompute challenge from the two parent receipt digests, hash at nonce 385518, compare; lowest-nonce scan in `pow_dag.py:verify`.
- **Kill condition:** either parent receipt is killed (its digest changes, invalidating this challenge); challenge/digest mismatch; threshold failure; or a valid nonce below 385518.
- **Dependencies:** N1, N2 — their receipt digests are baked into this challenge, so this receipt certifies them transitively.
- **Observed receipt:** nonce 385518, digest `00000ec2...8edacd04`.
- **Verification vs discovery cost:** discovery 385,519 hashes, 1.305 s. Validity: 3 hashes (challenge + digest). Lowest-nonce certification: full rescan.

### D23

- **Claim / state:** Certified derived node over [N2, N3]. Challenge `26f52b9563cef539b1f571081ceafdb882bcbdba61b4e3e1c96966796e77461a`; lowest valid nonce **118958**, digest `00000269d55068d329270b73cec561f9d7ad101b42b9d5c73376071df18244e9`.
- **Pinned roots:** salt `d23-v1`; parent digests pinned to N2 = `00000f55...dd40` and N3 = `00000037...87cc` in that order.
- **Executable check:** recompute challenge from N2 and N3 receipt digests, verify nonce 118958; lowest-nonce scan in `pow_dag.py:verify`.
- **Kill condition:** N2 or N3 receipt killed; challenge/digest mismatch; threshold failure; or a valid nonce below 118958.
- **Dependencies:** N2, N3.
- **Observed receipt:** nonce 118958, digest `00000269...f18244e9`.
- **Verification vs discovery cost:** discovery 118,959 hashes, 0.329 s (cheapest node). Validity: 3 hashes. Lowest-nonce certification: full rescan.

### E

- **Claim / state:** Certified sink node over [D12]. Challenge `de1e232b7f2a486ef88a2f21ecbcd60fa5eefc85166b8b9f3f665c6b8ca8b91f`; lowest valid nonce **348439**, digest `00000f8bf9c1c7342760358b13b9d4f5dccf4ebbf1a42e2dbe9db61e46abf2f7`.
- **Pinned roots:** salt `e-v1`; parent digest pinned to D12 = `00000ec2...cd04` (which itself pins N1 and N2).
- **Executable check:** recompute challenge from D12's receipt digest, verify nonce 348439; lowest-nonce scan in `pow_dag.py:verify`.
- **Kill condition:** D12 receipt killed (transitively: N1 or N2 killed); challenge/digest mismatch; threshold failure; or a valid nonce below 348439.
- **Dependencies:** D12 (transitively N1, N2). E does **not** depend on N3 or D23.
- **Observed receipt:** nonce 348439, digest `00000f8b...46abf2f7`.
- **Verification vs discovery cost:** discovery 348,440 hashes, 0.949 s. Validity: 3 hashes. Lowest-nonce certification: full rescan.

## Whole-DAG summary

| Node | Nonce | Hashes tried | Search time (s) |
|---|---|---|---|
| N1 | 1884136 | 1,884,137 | 4.704 |
| N2 | 678483 | 678,484 | 1.690 |
| N3 | 2876980 | 2,876,981 | 7.484 |
| D12 | 385518 | 385,519 | 1.305 |
| D23 | 118958 | 118,959 | 0.329 |
| E | 348439 | 348,440 | 0.949 |
| **Total** | | **6,292,520** | **16.461** |

- **Discovery cost:** 6,292,520 SHA-256 evaluations, 16.461 s total, single-threaded.
- **Verification cost, validity only:** 16 hashes (~microseconds) — recompute each challenge and one proof digest per node. This is the certificate's asymmetry: ~400,000× cheaper than discovery.
- **Verification cost, lowest-nonce certification:** the "lowest" claim has no succinct witness; certifying it requires rescanning every nonce below each receipt's, which is essentially full rediscovery (measured 16.965 s via `pow_dag.py:verify`, exit OK).
- **Structural note:** each derived challenge pins its parents' exact receipt digests, so any change to a root receipt invalidates every downstream receipt on its dependency path. N3 is the most expensive root (2.88 M hashes) but only D23 depends on it; N1's 1.88 M-hash receipt is load-bearing for D12 and E.
