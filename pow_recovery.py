"""Deterministic proof-of-work DAG for selective recovery experiments."""

from __future__ import annotations

from dataclasses import asdict, dataclass
from hashlib import sha256
from typing import Any, Mapping


DAG: dict[str, tuple[str, ...]] = {
    "N1": (),
    "N2": (),
    "N3": (),
    "D12": ("N1", "N2"),
    "D23": ("N2", "N3"),
    "E": ("D12",),
}

BASE_SALTS = {
    "N1": "n1-authoritative-v1",
    "N2": "n2-authoritative-v1",
    "N3": "n3-authoritative-v1",
    "D12": "d12-v1",
    "D23": "d23-v1",
    "E": "e-v1",
}


@dataclass(frozen=True)
class PowReceipt:
    node: str
    challenge: str
    difficulty_bits: int
    nonce: int
    digest: str

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class PowBundle:
    difficulty_bits: int
    salts: tuple[tuple[str, str], ...]
    receipts: dict[str, PowReceipt]


def _hash(text: str) -> str:
    return sha256(text.encode()).hexdigest()


def _challenge(
    node: str, salt: str, parents: tuple[str, ...], receipts: Mapping[str, PowReceipt]
) -> str:
    parent_roots = ":".join(receipts[parent].digest for parent in parents)
    return _hash(f"pow-recovery-v1:{node}:{salt}:{parent_roots}")


def _digest(challenge: str, nonce: int) -> str:
    return _hash(f"{challenge}:{nonce}")


def _valid_digest(digest: str, difficulty_bits: int) -> bool:
    return int(digest, 16) < (1 << (256 - difficulty_bits))


def discover_receipt(node: str, challenge: str, difficulty_bits: int) -> PowReceipt:
    nonce = 0
    while True:
        digest = _digest(challenge, nonce)
        if _valid_digest(digest, difficulty_bits):
            return PowReceipt(node, challenge, difficulty_bits, nonce, digest)
        nonce += 1


def verify_receipt(receipt: PowReceipt) -> bool:
    return (
        receipt.nonce >= 0
        and receipt.digest == _digest(receipt.challenge, receipt.nonce)
        and _valid_digest(receipt.digest, receipt.difficulty_bits)
    )


def build_bundle(
    difficulty_bits: int = 22, n1_salt: str = BASE_SALTS["N1"]
) -> PowBundle:
    salts = dict(BASE_SALTS)
    salts["N1"] = n1_salt
    receipts: dict[str, PowReceipt] = {}
    for node, parents in DAG.items():
        challenge = _challenge(node, salts[node], parents, receipts)
        receipts[node] = discover_receipt(node, challenge, difficulty_bits)
    return PowBundle(difficulty_bits, tuple(salts.items()), receipts)


def verify_bundle(bundle: PowBundle) -> list[str]:
    errors: list[str] = []
    salts = dict(bundle.salts)
    for node, parents in DAG.items():
        receipt = bundle.receipts.get(node)
        if receipt is None:
            errors.append(f"missing receipt {node}")
            continue
        expected_challenge = _challenge(node, salts[node], parents, bundle.receipts)
        if receipt.challenge != expected_challenge:
            errors.append(f"wrong challenge {node}")
        if receipt.difficulty_bits != bundle.difficulty_bits or not verify_receipt(receipt):
            errors.append(f"invalid proof {node}")
    return errors


def changed_descendants(changed: set[str]) -> set[str]:
    affected = set(changed)
    progress = True
    while progress:
        progress = False
        for node, parents in DAG.items():
            if node not in affected and any(parent in affected for parent in parents):
                affected.add(node)
                progress = True
    return affected


def grade_recovery(bundle: PowBundle, submission: Mapping[str, Any]) -> dict[str, Any]:
    errors: list[str] = []
    expected_retracted = ["D12", "E", "N1"]
    expected_preserved = ["D23", "N2", "N3"]
    if sorted(submission.get("retracted", [])) != expected_retracted:
        errors.append("incorrect retraction set")
    if sorted(submission.get("preserved", [])) != expected_preserved:
        errors.append("incorrect preservation set")
    if sorted(submission.get("recomputed", [])) != expected_retracted:
        errors.append("incorrect recomputation set")
    supplied = submission.get("receipts", {})
    for node, expected in bundle.receipts.items():
        if supplied.get(node) != expected.to_dict():
            errors.append(f"incorrect receipt {node}")
    return {"passed": not errors, "errors": errors}
