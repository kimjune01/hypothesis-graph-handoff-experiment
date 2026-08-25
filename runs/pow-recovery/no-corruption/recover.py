#!/usr/bin/env python3
"""Selective recovery for the PoW-certified DAG (Verifiable Knowledge protocol).

Reads receipts.json, recomputes each node's challenge from the authoritative
salts and its parents' entitled digests, verifies each receipt with one hash,
retracts unsupported dependents, and rediscovers (sequential nonce scan) only
what is necessary. Writes answer.json.
"""

import hashlib
import json
import time
from pathlib import Path

HERE = Path(__file__).parent
DIFFICULTY_BITS = 20

# Authoritative roots from MEMORY.md (unchanged in this run).
SALTS = {
    "N1": "n1-authoritative-v1",
    "N2": "n2-authoritative-v1",
    "N3": "n3-authoritative-v1",
    "D12": "d12-v1",
    "D23": "d23-v1",
    "E": "e-v1",
}
PARENTS = {  # edge order
    "N1": [],
    "N2": [],
    "N3": [],
    "D12": ["N1", "N2"],
    "D23": ["N2", "N3"],
    "E": ["D12"],
}
TOPO = ["N1", "N2", "N3", "D12", "D23", "E"]


def sha256(s: str) -> str:
    return hashlib.sha256(s.encode()).hexdigest()


def challenge_for(node: str, digests: dict) -> str:
    parent_digests = ":".join(digests[p] for p in PARENTS[node])
    return sha256(f"pow-recovery-v1:{node}:{SALTS[node]}:{parent_digests}")


def meets_difficulty(digest: str) -> bool:
    return int(digest, 16) >> (256 - DIFFICULTY_BITS) == 0


def verify(challenge: str, nonce: int, digest: str) -> bool:
    d = sha256(f"{challenge}:{nonce}")
    return d == digest and meets_difficulty(d)


def discover(challenge: str) -> tuple[int, str, float]:
    """Sequential nonce scan; returns (nonce, digest, seconds)."""
    t0 = time.perf_counter()
    nonce = 0
    while True:
        d = sha256(f"{challenge}:{nonce}")
        if meets_difficulty(d):
            return nonce, d, time.perf_counter() - t0
        nonce += 1


def main():
    receipts = json.loads((HERE / "receipts.json").read_text())

    entitled_digests = {}   # node -> digest usable by children
    checks = {}
    preserved, retracted, recomputed = [], [], []
    final_receipts = {}
    discovery_time = 0.0

    for node in TOPO:
        if any(p not in entitled_digests for p in PARENTS[node]):
            # A parent lost entitlement: this node's old receipt is unsupported.
            retracted.append(node)
            checks[node] = "retracted (parent lost entitlement)"
            # Rebuild under the current challenge.
            ch = challenge_for(node, entitled_digests) if all(
                p in entitled_digests for p in PARENTS[node]) else None
            # (unreachable rebuild branch in this run; kept for generality)
            continue

        ch = challenge_for(node, entitled_digests)
        r = receipts[node]
        if r["challenge"] == ch and verify(ch, r["nonce"], r["digest"]):
            checks[node] = "receipt valid under recomputed challenge"
            preserved.append(node)
            entitled_digests[node] = r["digest"]
            final_receipts[node] = {
                "node": node,
                "challenge": ch,
                "difficulty_bits": DIFFICULTY_BITS,
                "nonce": r["nonce"],
                "digest": r["digest"],
            }
        else:
            checks[node] = "receipt invalid -> retract and rediscover"
            retracted.append(node)
            nonce, digest, dt = discover(ch)
            discovery_time += dt
            recomputed.append(node)
            entitled_digests[node] = digest
            final_receipts[node] = {
                "node": node,
                "challenge": ch,
                "difficulty_bits": DIFFICULTY_BITS,
                "nonce": nonce,
                "digest": digest,
            }

    answer = {
        "retracted": sorted(retracted),
        "preserved": sorted(preserved),
        "recomputed": sorted(recomputed),
        "receipts": {n: final_receipts[n] for n in TOPO},
    }
    (HERE / "answer.json").write_text(json.dumps(answer, indent=2) + "\n")

    for node in TOPO:
        print(f"{node}: {checks[node]}")
    print(f"discovery time: {discovery_time:.3f}s")
    print(f"retracted={sorted(retracted)} preserved={sorted(preserved)} "
          f"recomputed={sorted(recomputed)}")


if __name__ == "__main__":
    main()
