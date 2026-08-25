# Dependency-structured semantic memory

Challenge formula for every node: `SHA256("pow-recovery-v1:{node}:{salt}:{parent_digests}")`, parent digests joined by `:` in edge order; empty for sources. A receipt is true when `digest == SHA256("{challenge}:{nonce}")` with 20 leading zero bits. Kill on failed check or changed challenge root. Verification is one hash; discovery scans sequential nonces. Exact checked receipts are in `receipts.json`.

- `N1` [true]: salt `n1-authoritative-v1`; parents `[]`.
- `N2` [true]: salt `n2-authoritative-v1`; parents `[]`.
- `N3` [true]: salt `n3-authoritative-v1`; parents `[]`.
- `D12` [true]: salt `d12-v1`; parents `[N1,N2]`; retract if either parent loses entitlement.
- `D23` [true]: salt `d23-v1`; parents `[N2,N3]`; retract if either parent loses entitlement.
- `E` [true]: salt `e-v1`; parents `[D12]`; retract if D12 loses entitlement.

Edges: `N1→D12`, `N2→D12`, `N2→D23`, `N3→D23`, `D12→E`. D12 and D23 share N2 but do not otherwise support each other.
