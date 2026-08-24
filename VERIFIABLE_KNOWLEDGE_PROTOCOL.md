# Verifiable-knowledge protocol for memory experiments

This is the operational contract future Notes and Hypothesis Graph conditions must share. It is distilled from *Verifiable Knowledge*; it is not an experimental result.

## Verification primitive

Every consequential claim travels with:

1. the exact claim and its bounded scope;
2. its state: `untrue` (no completed check), `true` (the check ran and stood), or `false` (the check ran and broke);
3. a check another agent can execute;
4. the condition and observable witness that would refute it;
5. provenance edges to the claims, inputs, code, environment, and terminal witnesses it depends on;
6. the last observed verdict and its receipt; and
7. declared replay cost and remaining trust roots.

An attestation such as “I ran it” is not entitlement. Entitlement comes from a receiver being able to replay the pinned check to the same verdict. Where direct replay cannot reach an empirical root, record the independent cross-check that can disagree.

## Inheritance rule

Re-checkable does not mean always re-checked. A receiver may use a standing verified claim as an interface without re-deriving its proof. It should replay a check when the claim is load-bearing and its receipt is absent, stale, inconsistent, challenged, or rooted in something that changed.

Replay the check, not the original search. Proof discovery and verification are different costs. If a proof or certificate already checks, do not search for it again merely to establish entitlement.

## Retraction rule

If replay fails, mark the claim false or unsupported, retract every downstream claim whose only surviving entitlement depends on it, and preserve claims with independent surviving support. A canonical label never overrides a failed replay.

## Canon rule

A passing claim may enter semantic memory only with its check attached. It remains provisional and revocable. The memory is a cache over a verifiable substrate: later agents normally read the verdict and build on it, while retaining the live option to replay at any depth.

## Experimental consequence

Both Notes and Graph arms must carry the same verification primitives. The ablation changes organization—chronological notes versus explicit nodes and dependency edges—not whether one arm receives executable entitlement while the other receives bare assertions.
