# Chronological semantic-memory notes

We began with three independent 20-bit SHA-256 searches. N1 used salt `n1-authoritative-v1`; N2 used `n2-authoritative-v1`; N3 used `n3-authoritative-v1`. Their checked receipts are in `receipts.json`. A receipt is true when its digest equals `SHA256("{challenge}:{nonce}")` and has 20 leading zero bits. Kill it if that check fails or its challenge roots change; checking costs one hash, while discovery scans sequential nonces.

Later D12 was built using salt `d12-v1` and the ordered receipt digests of N1 and N2. Its roots therefore include both. We next built D23 from N2 and N3 using `d23-v1`; it is unrelated to N1. Both receipts checked true.

After that, E was built using `e-v1` from D12's digest alone, so changes reaching D12 also reach E. Its receipt checked true. The challenge formula throughout was `SHA256("pow-recovery-v1:{node}:{salt}:{parent_digests}")`, with parent digests joined by `:` in the order just stated and empty for sources.

The shared N2 root supports both D12 and D23, but those two derived branches do not otherwise support each other. The six receipts were valid under the roots recorded at the time.
