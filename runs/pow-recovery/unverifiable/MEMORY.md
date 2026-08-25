# Dependency-structured but unverifiable memory

The remembered claims say six PoW nodes once existed, but their executable receipts are unavailable. Current formula and difficulty remain `SHA256("pow-recovery-v1:{node}:{salt}:{parent_digests}")` and 20 leading zero bits.

- `N1`: old salt was `n1-authoritative-v1`; parents `[]`.
- `N2`: salt `n2-authoritative-v1`; parents `[]`.
- `N3`: salt `n3-authoritative-v1`; parents `[]`.
- `D12`: salt `d12-v1`; parents `[N1,N2]`.
- `D23`: salt `d23-v1`; parents `[N2,N3]`.
- `E`: salt `e-v1`; parents `[D12]`.

Edges: `N1→D12`, `N2→D12`, `N2→D23`, `N3→D23`, `D12→E`. Because `receipts.json` contains no executable receipts, none of these attestations is currently entitled.
