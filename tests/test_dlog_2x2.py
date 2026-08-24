from dataclasses import replace

import pytest

from dlog_2x2 import (
    DLogReceipt,
    checksum,
    crt,
    generate_bundle,
    independent_outputs,
    joint_output,
    validate_bundle,
    verify_receipt,
)


def test_generated_bundle_is_deterministic_and_valid() -> None:
    first = generate_bundle(seed=8242026)
    second = generate_bundle(seed=8242026)

    assert first == second
    assert validate_bundle(first) == []
    assert len(first.instances) == 3
    assert len({instance.order for instance in first.instances}) == 3


def test_receipts_are_executable_and_fail_closed() -> None:
    bundle = generate_bundle(seed=8242026)

    for instance, receipt in zip(bundle.instances, bundle.receipts, strict=True):
        assert verify_receipt(instance, receipt)
        assert not verify_receipt(
            instance,
            replace(receipt, residue=(receipt.residue + 1) % instance.order),
        )
        assert not verify_receipt(instance, DLogReceipt(residue=-1))


def test_crt_recovers_unique_joint_secret() -> None:
    bundle = generate_bundle(seed=8242026)
    residues = [receipt.residue for receipt in bundle.receipts]
    orders = [instance.order for instance in bundle.instances]

    recovered, modulus = crt(residues, orders)

    assert modulus == bundle.joint_bound
    assert recovered == bundle.joint_secret
    assert joint_output(bundle.receipts, bundle.instances) == checksum(
        "joint", bundle.joint_secret
    )


@pytest.mark.parametrize("missing", [0, 1, 2])
def test_every_joint_checkpoint_is_necessary(missing: int) -> None:
    bundle = generate_bundle(seed=8242026)
    retained_orders = [
        instance.order
        for index, instance in enumerate(bundle.instances)
        if index != missing
    ]
    retained_residues = [
        receipt.residue
        for index, receipt in enumerate(bundle.receipts)
        if index != missing
    ]
    partial, partial_modulus = crt(retained_residues, retained_orders)
    candidates = range(partial, bundle.joint_bound, partial_modulus)

    assert len(candidates) == bundle.instances[missing].order
    assert bundle.joint_secret in candidates
    assert len(candidates) > bundle.max_missing_residue_enumeration


def test_independent_outputs_use_one_checkpoint_each() -> None:
    bundle = generate_bundle(seed=8242026)
    outputs = independent_outputs(bundle.receipts)

    assert outputs == tuple(
        checksum(f"independent-{index}", receipt.residue)
        for index, receipt in enumerate(bundle.receipts, start=1)
    )

    for missing in range(3):
        retained = tuple(
            output for index, output in enumerate(outputs) if index != missing
        )
        assert len(retained) == 2
        assert all(output in outputs for output in retained)


def test_joint_output_rejects_missing_or_invalid_receipts() -> None:
    bundle = generate_bundle(seed=8242026)

    with pytest.raises(ValueError, match="three receipts"):
        joint_output(bundle.receipts[:2], bundle.instances)

    corrupted = list(bundle.receipts)
    corrupted[1] = replace(
        corrupted[1], residue=(corrupted[1].residue + 1) % bundle.instances[1].order
    )
    with pytest.raises(ValueError, match="invalid receipt"):
        joint_output(tuple(corrupted), bundle.instances)
