# Expensive-checkpoint selective-recovery results

## Outcome

The primary mechanism demonstration passed in both representations.

| Format | Exact recovery | Retracted | Preserved | Recomputed | Candidate hashes | Agent duration | Turns | Cost |
|---|---:|---|---|---|---:|---:|---:|---:|
| Notes | yes | N1, D12, E | N2, N3, D23 | N1, D12, E | 1,781,267 | 64.542 s | 8 | $0.796555 |
| Graph | yes | N1, D12, E | N2, N3, D23 | N1, D12, E | 1,781,267 | 86.126 s | 8 | $0.848847 |

Both agents cheaply checked inherited receipts against current authoritative roots, localized the stale N1 subtree, preserved the independent D23 branch despite its shared N2 ancestor, rebuilt only the three affected nodes in topological order, and produced a fully valid six-node bundle.

Selective recovery required 1,781,267 candidate hashes. Rebuilding the entire current bundle deterministically would require 5,455,691. The protocol therefore avoided 3,674,424 candidate hashes, or 67.35% of full rediscovery, in this frozen instance. Entitlement checks required constant hashes per receipt rather than nonce rescans.

## Representation comparison

Graph supplied no correctness or work advantage over information-matched Notes. Candidate hashes and recovery sets were identical. Graph took 21.584 seconds longer and cost $0.052292 more. This is a second representation null/contrary case, not evidence that Graph is generally slower.

Artifact lengths differed: Notes 178 words, Graph 133 words. One run per format supports no average-effect claim.

## Controls

- **No corruption:** exact pass; all six nodes preserved, none retracted or recomputed. Duration 54.056 seconds, seven turns, $0.671146.
- **Unverifiable attestations:** infrastructure failure before task work. Claude Code returned organization-level HTTP 403 in 0.489 seconds. The run is preserved and was not replaced. Therefore the planned empirical contrast between selective recovery and full rebuild without receipts remains unobserved.

## Supported claim

> In one preregistered branching PoW DAG, a receiving agent using verifiable memory detected a stale expensive checkpoint, retracted exactly its transitive dependents, preserved all independent verified work, and reduced deterministic rediscovery by 67.35% relative to rebuilding the full bundle.

This is an existence demonstration of selective recovery. It does not establish frequency, expected savings, semantic-memory performance, or a Graph advantage over good notes.
