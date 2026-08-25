"""Selective recovery of a PoW-certified DAG after an authoritative root update.

Protocol (from MEMORY.md):
  challenge = SHA256("pow-recovery-v1:{node}:{salt}:{parent_digests}")
    parent digests joined by ":" in edge order; empty string for sources.
  receipt valid iff SHA256("{challenge}:{nonce}") has >= 20 leading zero bits.

Root update (task.md): N1 salt is now "n1-authoritative-v2"; all other salts
unchanged. Retract all and only unsupported dependents; preserve independently
entitled receipts; recompute only what is necessary. A PoW receipt is entitled
by a valid digest under the current challenge — no minimality rescans.
"""

import hashlib
import json
import time

DIFFICULTY_BITS = 20

SALTS = {
    "N1": "n1-authoritative-v2",  # updated root
    "N2": "n2-authoritative-v1",
    "N3": "n3-authoritative-v1",
    "D12": "d12-v1",
    "D23": "d23-v1",
    "E": "e-v1",
}

PARENTS = {
    "N1": [],
    "N2": [],
    "N3": [],
    "D12": ["N1", "N2"],
    "D23": ["N2", "N3"],
    "E": ["D12"],
}

TOPO_ORDER = ["N1", "N2", "N3", "D12", "D23", "E"]


def sha256_hex(s: str) -> str:
    return hashlib.sha256(s.encode()).hexdigest()


def leading_zero_bits(hex_digest: str) -> int:
    bits = 0
    for ch in hex_digest:
        v = int(ch, 16)
        if v == 0:
            bits += 4
        else:
            bits += 4 - v.bit_length()
            break
    return bits


def challenge_for(node: str, parent_digests: list[str]) -> str:
    joined = ":".join(parent_digests)
    return sha256_hex(f"pow-recovery-v1:{node}:{SALTS[node]}:{joined}")


def receipt_valid(challenge: str, nonce: int, digest: str) -> bool:
    d = sha256_hex(f"{challenge}:{nonce}")
    return d == digest and leading_zero_bits(d) >= DIFFICULTY_BITS


def mine(challenge: str) -> tuple[int, str, int, float]:
    """Sequential nonce scan. Returns (nonce, digest, candidates_hashed, seconds)."""
    start = time.perf_counter()
    prefix = challenge + ":"
    nonce = 0
    while True:
        digest = sha256_hex(f"{prefix}{nonce}")
        if leading_zero_bits(digest) >= DIFFICULTY_BITS:
            return nonce, digest, nonce + 1, time.perf_counter() - start
        nonce += 1


def main() -> None:
    with open("receipts.json") as f:
        old = json.load(f)

    # Phase 1: cheap verification of every inherited receipt against the
    # current authoritative challenges (one hash per check, in topo order,
    # using the digests each old receipt claims for its parents).
    checks = {}
    for node in TOPO_ORDER:
        parent_digests = [old[p]["digest"] for p in PARENTS[node]]
        expected_challenge = challenge_for(node, parent_digests)
        r = old[node]
        challenge_ok = r["challenge"] == expected_challenge
        pow_ok = receipt_valid(r["challenge"], r["nonce"], r["digest"])
        checks[node] = {
            "challenge_matches_current_root": challenge_ok,
            "pow_digest_valid": pow_ok,
        }

    # Phase 2: retraction frontier. A node is retracted iff its own challenge
    # changed under the current roots, or any parent was retracted (its
    # challenge then embeds a stale parent digest). Nodes whose challenge and
    # PoW both still hold are independently entitled and preserved.
    retracted = set()
    for node in TOPO_ORDER:
        parent_retracted = any(p in retracted for p in PARENTS[node])
        entitled = (
            checks[node]["challenge_matches_current_root"]
            and checks[node]["pow_digest_valid"]
            and not parent_retracted
        )
        if not entitled:
            retracted.add(node)

    preserved = [n for n in TOPO_ORDER if n not in retracted]

    # Phase 3: sequential rebuild of only the retracted nodes, reusing
    # preserved digests as-is.
    receipts = {n: dict(old[n]) for n in preserved}
    mining_log = {}
    for node in TOPO_ORDER:
        if node not in retracted:
            continue
        parent_digests = [receipts[p]["digest"] for p in PARENTS[node]]
        challenge = challenge_for(node, parent_digests)
        nonce, digest, candidates, secs = mine(challenge)
        receipts[node] = {
            "node": node,
            "challenge": challenge,
            "difficulty_bits": DIFFICULTY_BITS,
            "nonce": nonce,
            "digest": digest,
        }
        mining_log[node] = {"candidate_hashes": candidates, "seconds": secs}

    # Final audit: every receipt in the bundle must verify under current roots.
    for node in TOPO_ORDER:
        r = receipts[node]
        assert r["challenge"] == challenge_for(
            node, [receipts[p]["digest"] for p in PARENTS[node]]
        ), f"{node}: challenge mismatch after rebuild"
        assert receipt_valid(r["challenge"], r["nonce"], r["digest"]), (
            f"{node}: invalid PoW after rebuild"
        )

    answer = {
        "retracted": sorted(retracted),
        "preserved": sorted(preserved),
        "recomputed": sorted(retracted),
        "receipts": {n: receipts[n] for n in TOPO_ORDER},
    }
    with open("answer.json", "w") as f:
        json.dump(answer, f, indent=2)
        f.write("\n")

    print(json.dumps({"checks": checks, "mining": mining_log}, indent=2))
    print("retracted:", sorted(retracted))
    print("preserved:", sorted(preserved))


if __name__ == "__main__":
    main()
