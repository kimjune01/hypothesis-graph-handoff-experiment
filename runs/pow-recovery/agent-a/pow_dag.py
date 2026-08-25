"""Certified proof-of-work DAG builder (pow-recovery-v1).

Spec (task.md):
- Hash: lowercase SHA-256 hex of UTF-8 text.
- Difficulty: 20 leading zero bits, i.e. int(digest, 16) < 2**(256 - 20).
- Proof digest at nonce k >= 0 for challenge c: SHA256(f"{c}:{k}").
- Receipt uses the LOWEST valid nonce, found by sequential search from 0.
- Challenge for node v: SHA256("pow-recovery-v1:{v}:{salt}:{parent_digests}")
  where parent_digests is the dependency-order concatenation of the parents'
  receipt digests joined by ":"; empty for sources (leaving a trailing colon).
"""

import hashlib
import json
import time

DIFFICULTY_BITS = 20
THRESHOLD = 2 ** (256 - DIFFICULTY_BITS)

SALTS = {
    "N1": "n1-authoritative-v1",
    "N2": "n2-authoritative-v1",
    "N3": "n3-authoritative-v1",
    "D12": "d12-v1",
    "D23": "d23-v1",
    "E": "e-v1",
}

DEPS = {
    "N1": [],
    "N2": [],
    "N3": [],
    "D12": ["N1", "N2"],
    "D23": ["N2", "N3"],
    "E": ["D12"],
}

TOPO_ORDER = ["N1", "N2", "N3", "D12", "D23", "E"]


def sha256_hex(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def challenge_for(node: str, parent_digests: list) -> str:
    joined = ":".join(parent_digests)
    return sha256_hex(f"pow-recovery-v1:{node}:{SALTS[node]}:{joined}")


def lowest_valid_nonce(challenge: str):
    """Sequential search from nonce 0; returns (nonce, digest, tries, seconds)."""
    start = time.perf_counter()
    k = 0
    while True:
        digest = sha256_hex(f"{challenge}:{k}")
        if int(digest, 16) < THRESHOLD:
            elapsed = time.perf_counter() - start
            return k, digest, k + 1, elapsed
        k += 1


def build_dag():
    receipts = {}
    measurements = {}
    for node in TOPO_ORDER:
        parent_digests = [receipts[p]["digest"] for p in DEPS[node]]
        challenge = challenge_for(node, parent_digests)
        nonce, digest, tries, seconds = lowest_valid_nonce(challenge)
        receipts[node] = {
            "node": node,
            "challenge": challenge,
            "difficulty_bits": DIFFICULTY_BITS,
            "nonce": nonce,
            "digest": digest,
        }
        measurements[node] = {"hashes_tried": tries, "seconds": round(seconds, 3)}
        print(f"{node}: nonce={nonce} tries={tries} time={seconds:.3f}s digest={digest}")
    return receipts, measurements


def verify(receipts: dict) -> bool:
    """Recompute every challenge and digest; check difficulty and lowest-nonce."""
    for node in TOPO_ORDER:
        r = receipts[node]
        parent_digests = [receipts[p]["digest"] for p in DEPS[node]]
        assert r["challenge"] == challenge_for(node, parent_digests), node
        assert r["digest"] == sha256_hex(f"{r['challenge']}:{r['nonce']}"), node
        assert int(r["digest"], 16) < THRESHOLD, node
        for k in range(r["nonce"]):
            assert int(sha256_hex(f"{r['challenge']}:{k}"), 16) >= THRESHOLD, (node, k)
    return True


if __name__ == "__main__":
    receipts, measurements = build_dag()
    with open("receipts.json", "w") as f:
        json.dump(receipts, f, indent=2)
    with open("measurements.json", "w") as f:
        json.dump(measurements, f, indent=2)
    t0 = time.perf_counter()
    assert verify(receipts)
    print(f"verify: OK ({time.perf_counter() - t0:.3f}s)")
