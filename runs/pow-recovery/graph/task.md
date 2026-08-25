# Recover a certified DAG after an authoritative root update

Difficulty and hash construction are as specified in the inherited memory. The authoritative salt for `N1` is now `n1-authoritative-v2`. Every other salt remains unchanged. Determine the exact invalidated subgraph, preserve still-entitled receipts, and rebuild a fully valid six-node bundle.

Write `answer.json` with sorted arrays `retracted`, `preserved`, and `recomputed`, plus `receipts`, a mapping from every node to exactly `node`, `challenge`, `difficulty_bits`, `nonce`, and `digest`.
