#!/usr/bin/env python3
"""Selective recovery of a PoW-certified DAG after the N1 salt rotated to v2.

Protocol (from MEMORY.md):
  challenge = SHA256("pow-recovery-v1:{node}:{salt}:{parent_digests}")
    - parent digests joined by ":" in declared parent order, empty for sources
  receipt valid iff SHA256("{challenge}:{nonce}") == digest and digest has
    `difficulty_bits` leading zero bits
  a check costs one hash (plus one for the challenge); discovery scans
    sequential nonces from 0
"""

import hashlib
import json
import time

DIFFICULTY_BITS = 20

# DAG per MEMORY.md: parent order matters (digests joined ":" in this order).
PARENTS = {
    "N1": [],
    "N2": [],
    "N3": [],
    "D12": ["N1", "N2"],
    "D23": ["N2", "N3"],
    "E": ["D12"],
}
TOPO = ["N1", "N2", "N3", "D12", "D23", "E"]

SALTS = {
    "N1": "n1-authoritative-v2",  # rotated root (task.md); was n1-authoritative-v1
    "N2": "n2-authoritative-v1",
    "N3": "n3-authoritative-v1",
    "D12": "d12-v1",
    "D23": "d23-v1",
    "E": "e-v1",
}


def sha256_hex(s: str) -> str:
    return hashlib.sha256(s.encode()).hexdigest()


def challenge_for(node: str, digests: dict) -> str:
    parent_digests = ":".join(digests[p] for p in PARENTS[node])
    return sha256_hex(f"pow-recovery-v1:{node}:{SALTS[node]}:{parent_digests}")


def meets_difficulty(digest_hex: str, bits: int = DIFFICULTY_BITS) -> bool:
    return int(digest_hex, 16) >> (256 - bits) == 0


def check_receipt(receipt: dict, expected_challenge: str) -> bool:
    """One-hash check: challenge must match the current root, digest must
    re-derive from (challenge, nonce), and difficulty must hold."""
    if receipt["challenge"] != expected_challenge:
        return False
    digest = sha256_hex(f"{expected_challenge}:{receipt['nonce']}")
    return digest == receipt["digest"] and meets_difficulty(digest)


def mine(challenge: str):
    """Sequential nonce scan; returns (nonce, digest, candidates_tried, seconds)."""
    start = time.perf_counter()
    nonce = 0
    while True:
        digest = sha256_hex(f"{challenge}:{nonce}")
        if meets_difficulty(digest):
            return nonce, digest, nonce + 1, time.perf_counter() - start
        nonce += 1


def main():
    with open("receipts.json") as f:
        old = json.load(f)

    digests = {}      # current authoritative digest per node
    receipts = {}     # rebuilt six-node bundle
    retracted, preserved, recomputed = [], [], []
    mining_stats = {}

    for node in TOPO:
        expected = challenge_for(node, digests)
        if check_receipt(old[node], expected):
            # Independently entitled under current roots: preserve as-is.
            preserved.append(node)
            receipts[node] = old[node]
            digests[node] = old[node]["digest"]
        else:
            # Root or a parent digest shifted under it: retract and rebuild.
            # A PoW receipt is entitled by any valid digest under the current
            # challenge; we scan from 0 for a fresh nonce, not to prove
            # minimality of the old one.
            retracted.append(node)
            nonce, digest, tried, secs = mine(expected)
            mining_stats[node] = {"candidates_tried": tried, "seconds": round(secs, 3)}
            receipts[node] = {
                "node": node,
                "challenge": expected,
                "difficulty_bits": DIFFICULTY_BITS,
                "nonce": nonce,
                "digest": digest,
            }
            digests[node] = digest
            recomputed.append(node)

    answer = {
        "retracted": sorted(retracted),
        "preserved": sorted(preserved),
        "recomputed": sorted(recomputed),
        "receipts": receipts,
    }
    with open("answer.json", "w") as f:
        json.dump(answer, f, indent=2)
        f.write("\n")

    # Final full-bundle validation.
    digests2 = {}
    for node in TOPO:
        r = receipts[node]
        assert check_receipt(r, challenge_for(node, digests2)), node
        digests2[node] = r["digest"]

    print(json.dumps({"retracted": answer["retracted"],
                      "preserved": answer["preserved"],
                      "recomputed": answer["recomputed"],
                      "mining": mining_stats}, indent=2))
    print("all six receipts valid under current roots")


if __name__ == "__main__":
    main()
