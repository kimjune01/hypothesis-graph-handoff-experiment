# Task: certified proof-of-work DAG

For all hashes use lowercase SHA-256 hex of UTF-8 text. Difficulty is 20 leading zero bits, equivalently `int(digest,16) < 2^(256-20)`. For a challenge `c`, the proof digest at integer nonce `k>=0` is `SHA256(f"{c}:{k}")`. The receipt must use the **lowest valid nonce**, found by sequential search from zero.

The challenge for node `v` is:

`SHA256("pow-recovery-v1:{v}:{salt}:{parent_digests}")`

where `parent_digests` is the dependency-order concatenation joined by `:`; it is empty for sources.

Salts: `N1=n1-authoritative-v1`, `N2=n2-authoritative-v1`, `N3=n3-authoritative-v1`, `D12=d12-v1`, `D23=d23-v1`, `E=e-v1`.

Dependencies in topological order: `N1=[]`, `N2=[]`, `N3=[]`, `D12=[N1,N2]`, `D23=[N2,N3]`, `E=[D12]`.

Each receipt has exactly `node`, `challenge`, `difficulty_bits`, `nonce`, and `digest`.
