"""Deterministic, exactly checked work used by the concurrency demonstration."""

from __future__ import annotations

import hashlib
import json


def _digest(payload: dict) -> str:
    return hashlib.sha256(json.dumps(payload, sort_keys=True, separators=(",", ":")).encode()).hexdigest()


def _prime(n: int) -> bool:
    if n < 2:
        return False
    d = 2
    while d * d <= n:
        if n % d == 0:
            return False
        d += 1
    return True


def discover(work: dict, progress=None) -> dict:
    if work["kind"] == "gate":
        core = {"kind": "gate", "node_id": work["node_id"], "verdict": _prime(work["n"])}
        return {**core, "digest": _digest(core)}
    prefix = "0" * int(work["difficulty"])
    nonce = 0
    while True:
        digest = hashlib.sha256(f'{work["challenge"]}:{nonce}'.encode()).hexdigest()
        if progress and nonce and nonce % 10_000 == 0:
            progress(nonce)
        if digest.startswith(prefix):
            return {"kind": "pow", "node_id": work["node_id"], "nonce": nonce, "digest": digest}
        nonce += 1


def check_receipt(work: dict, receipt: dict) -> bool:
    if work["kind"] == "gate":
        expected = discover(work)
        return receipt == expected
    if set(receipt) != {"kind", "node_id", "nonce", "digest"}:
        return False
    if receipt["kind"] != "pow" or receipt["node_id"] != work["node_id"]:
        return False
    digest = hashlib.sha256(f'{work["challenge"]}:{receipt["nonce"]}'.encode()).hexdigest()
    return receipt["digest"] == digest and digest.startswith("0" * int(work["difficulty"]))
