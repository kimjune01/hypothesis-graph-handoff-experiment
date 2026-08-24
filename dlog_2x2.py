"""Deterministic construction and exact graders for the 2x2 task family."""

from __future__ import annotations

from dataclasses import dataclass
from hashlib import sha256
from math import gcd, prod
from random import Random
from typing import Any, Iterable, Mapping, Sequence


@dataclass(frozen=True)
class DLogInstance:
    modulus: int
    order: int
    generator: int
    target: int


@dataclass(frozen=True)
class DLogReceipt:
    residue: int


@dataclass(frozen=True)
class DLogBundle:
    instances: tuple[DLogInstance, ...]
    receipts: tuple[DLogReceipt, ...]
    joint_secret: int
    joint_bound: int
    max_missing_residue_enumeration: int = 100_000


def _is_prime(value: int) -> bool:
    if value < 2:
        return False
    small_primes = (2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37)
    for prime in small_primes:
        if value % prime == 0:
            return value == prime
    exponent = value - 1
    shifts = 0
    while exponent % 2 == 0:
        shifts += 1
        exponent //= 2
    # Deterministic for unsigned 64-bit integers.
    for base in (2, 325, 9375, 28178, 450775, 9780504, 1795265022):
        if base % value == 0:
            continue
        witness = pow(base, exponent, value)
        if witness in (1, value - 1):
            continue
        for _ in range(shifts - 1):
            witness = pow(witness, 2, value)
            if witness == value - 1:
                break
        else:
            return False
    return True


def _next_prime(start: int) -> int:
    candidate = max(3, start | 1)
    while not _is_prime(candidate):
        candidate += 2
    return candidate


def _group_for_order(order: int) -> tuple[int, int]:
    multiplier = 2
    while True:
        modulus = multiplier * order + 1
        if _is_prime(modulus):
            for base in range(2, 100):
                generator = pow(base, multiplier, modulus)
                if generator != 1:
                    return modulus, generator
        multiplier += 2


def generate_bundle(seed: int) -> DLogBundle:
    rng = Random(seed)
    starts = sorted(rng.sample(range(1_000_000_000, 1_100_000_000), 3))
    orders: list[int] = []
    for start in starts:
        order = _next_prime(start)
        while order in orders:
            order = _next_prime(order + 2)
        orders.append(order)

    bound = prod(orders)
    secret = rng.randrange(bound)
    instances: list[DLogInstance] = []
    receipts: list[DLogReceipt] = []
    for order in orders:
        modulus, generator = _group_for_order(order)
        residue = secret % order
        instances.append(
            DLogInstance(
                modulus=modulus,
                order=order,
                generator=generator,
                target=pow(generator, residue, modulus),
            )
        )
        receipts.append(DLogReceipt(residue=residue))
    return DLogBundle(
        instances=tuple(instances),
        receipts=tuple(receipts),
        joint_secret=secret,
        joint_bound=bound,
    )


def verify_receipt(instance: DLogInstance, receipt: DLogReceipt) -> bool:
    return (
        0 <= receipt.residue < instance.order
        and pow(instance.generator, receipt.residue, instance.modulus)
        == instance.target
    )


def crt(residues: Iterable[int], moduli: Iterable[int]) -> tuple[int, int]:
    residue_values = tuple(residues)
    modulus_values = tuple(moduli)
    if not residue_values or len(residue_values) != len(modulus_values):
        raise ValueError("residues and moduli must have equal nonzero length")
    combined = residue_values[0] % modulus_values[0]
    combined_modulus = modulus_values[0]
    for residue, modulus in zip(
        residue_values[1:], modulus_values[1:], strict=True
    ):
        if gcd(combined_modulus, modulus) != 1:
            raise ValueError("moduli must be pairwise coprime")
        step = (
            (residue - combined) * pow(combined_modulus, -1, modulus)
        ) % modulus
        combined += step * combined_modulus
        combined_modulus *= modulus
        combined %= combined_modulus
    return combined, combined_modulus


def checksum(domain: str, value: int) -> str:
    return sha256(f"dlog-2x2-v1:{domain}:{value}".encode()).hexdigest()


def joint_output(
    receipts: Sequence[DLogReceipt], instances: Sequence[DLogInstance]
) -> str:
    if len(receipts) != 3 or len(instances) != 3:
        raise ValueError("joint output requires three receipts and instances")
    if not all(
        verify_receipt(instance, receipt)
        for instance, receipt in zip(instances, receipts, strict=True)
    ):
        raise ValueError("invalid receipt")
    secret, _ = crt(
        (receipt.residue for receipt in receipts),
        (instance.order for instance in instances),
    )
    return checksum("joint", secret)


def independent_outputs(receipts: Sequence[DLogReceipt]) -> tuple[str, ...]:
    return tuple(
        checksum(f"independent-{index}", receipt.residue)
        for index, receipt in enumerate(receipts, start=1)
    )


def public_instances(bundle: DLogBundle) -> tuple[dict[str, int], ...]:
    return tuple(
        {
            "modulus": instance.modulus,
            "order": instance.order,
            "generator": instance.generator,
            "target": instance.target,
        }
        for instance in bundle.instances
    )


def grade_joint_submission(
    bundle: DLogBundle, submission: Mapping[str, Any]
) -> dict[str, Any]:
    errors: list[str] = []
    if submission.get("secret") != bundle.joint_secret:
        errors.append("secret is incorrect")
    expected_checksum = checksum("joint", bundle.joint_secret)
    if submission.get("checksum") != expected_checksum:
        errors.append("checksum is incorrect")
    return {"passed": not errors, "errors": errors}


def grade_independent_submission(
    bundle: DLogBundle, submission: Mapping[str, Any]
) -> dict[str, Any]:
    errors: list[str] = []
    expected_residues = [receipt.residue for receipt in bundle.receipts]
    expected_checksums = list(independent_outputs(bundle.receipts))
    if submission.get("residues") != expected_residues:
        errors.append("residues are incorrect")
    if submission.get("checksums") != expected_checksums:
        errors.append("checksums are incorrect")
    return {"passed": not errors, "errors": errors}


def validate_bundle(bundle: DLogBundle) -> list[str]:
    errors: list[str] = []
    if len(bundle.instances) != 3 or len(bundle.receipts) != 3:
        errors.append("bundle must contain exactly three instances and receipts")
        return errors
    orders = tuple(instance.order for instance in bundle.instances)
    if prod(orders) != bundle.joint_bound:
        errors.append("joint bound must equal the product of orders")
    if not 0 <= bundle.joint_secret < bundle.joint_bound:
        errors.append("joint secret is outside the declared bound")
    for left_index, left in enumerate(orders):
        if not _is_prime(left):
            errors.append(f"order {left_index} is not prime")
        for right in orders[left_index + 1 :]:
            if gcd(left, right) != 1:
                errors.append("orders are not pairwise coprime")
    for index, (instance, receipt) in enumerate(
        zip(bundle.instances, bundle.receipts, strict=True)
    ):
        if not _is_prime(instance.modulus):
            errors.append(f"modulus {index} is not prime")
        if pow(instance.generator, instance.order, instance.modulus) != 1:
            errors.append(f"generator {index} does not have the declared order")
        if instance.generator == 1:
            errors.append(f"generator {index} is trivial")
        if not verify_receipt(instance, receipt):
            errors.append(f"receipt {index} does not verify")
        if receipt.residue != bundle.joint_secret % instance.order:
            errors.append(f"receipt {index} is inconsistent with the joint secret")
    return errors
