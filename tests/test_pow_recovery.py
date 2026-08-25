from dataclasses import replace

from pow_recovery import (
    DAG,
    build_bundle,
    changed_descendants,
    grade_recovery,
    verify_bundle,
    verify_receipt,
)


def test_frozen_dag_has_required_branching_shape() -> None:
    assert DAG == {
        "N1": (),
        "N2": (),
        "N3": (),
        "D12": ("N1", "N2"),
        "D23": ("N2", "N3"),
        "E": ("D12",),
    }
    assert changed_descendants({"N1"}) == {"N1", "D12", "E"}
    assert changed_descendants({"N3"}) == {"N3", "D23"}


def test_bundle_is_deterministic_and_every_receipt_verifies() -> None:
    first = build_bundle(difficulty_bits=12)
    second = build_bundle(difficulty_bits=12)

    assert first == second
    assert verify_bundle(first) == []
    assert all(verify_receipt(receipt) for receipt in first.receipts.values())


def test_changed_n1_root_invalidates_exactly_its_subgraph() -> None:
    old = build_bundle(difficulty_bits=12)
    new = build_bundle(difficulty_bits=12, n1_salt="n1-authoritative-v2")

    changed = {
        node for node in DAG if old.receipts[node] != new.receipts[node]
    }
    preserved = set(DAG) - changed

    assert changed == {"N1", "D12", "E"}
    assert preserved == {"N2", "N3", "D23"}


def test_receipt_fails_closed_when_nonce_or_challenge_changes() -> None:
    bundle = build_bundle(difficulty_bits=12)
    receipt = bundle.receipts["N1"]

    assert not verify_receipt(replace(receipt, nonce=receipt.nonce + 1))
    assert not verify_receipt(replace(receipt, challenge=receipt.challenge + "x"))


def test_exact_recovery_grader_requires_selective_repair() -> None:
    expected = build_bundle(difficulty_bits=12, n1_salt="n1-authoritative-v2")
    correct = {
        "retracted": ["D12", "E", "N1"],
        "preserved": ["D23", "N2", "N3"],
        "recomputed": ["D12", "E", "N1"],
        "receipts": {
            node: receipt.to_dict() for node, receipt in expected.receipts.items()
        },
    }

    assert grade_recovery(expected, correct) == {"passed": True, "errors": []}

    over_retracted = dict(correct)
    over_retracted["retracted"] = ["D12", "D23", "E", "N1"]
    assert not grade_recovery(expected, over_retracted)["passed"]
