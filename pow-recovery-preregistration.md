# Expensive-checkpoint selective-recovery preregistration

Status: frozen after Agent A and before any recovery run.

Agent A built the six-node DAG at 20-bit difficulty under the v1 roots. The perturbation changes only authoritative `N1` salt to `n1-authoritative-v2`. The exact target is retraction and recomputation of `{N1,D12,E}`, preservation of `{N2,N3,D23}`, and a fully verified final bundle.

Primary existence criterion: at least one recovery condition produces the exact sets and bundle while verifying preserved receipts cheaply and searching only the three affected nodes. One frozen case supports only “can,” not a frequency or average-effect claim.

Secondary comparison: Graph versus information-matched chronological Notes on exact recovery, unnecessary searches, candidate hashes, time, turns, and cost. If both succeed similarly, representation is null. No significance test is planned.

Both conditions receive identical `receipts.json`, task, protocol prompt, model invocation, and tools. Only `MEMORY.md` changes. Notes and Graph state the same formula, roots, receipts, dependencies, kill semantics, and cost asymmetry. Artifact lengths are reported, not silently equalized.

Run order from seed `8242026` is Notes then Graph. Grade only after both finish. Do not replace either run. A no-corruption control and unverifiable-attestation ablation are secondary and cannot alter the primary result.
