"""Exact verifier for the bounded two-seed claim.

This implementation follows the mathematical specification directly. It does
not import code or fixtures from the source case study.
"""

from __future__ import annotations

from fractions import Fraction
from itertools import combinations, product
from math import gcd
from typing import Iterable


def fractional_distance(value: Fraction) -> Fraction:
    residue = value % 1
    return min(residue, 1 - residue)


def _critical_times(speeds: tuple[int, ...]) -> set[Fraction]:
    denominators = {2 * speed for speed in speeds}
    for left, right in combinations(speeds, 2):
        denominators.add(left + right)
        denominators.add(abs(left - right))
    return {
        Fraction(numerator, denominator)
        for denominator in denominators
        if denominator
        for numerator in range(denominator + 1)
    }


def maximum_loneliness(speeds: Iterable[int]) -> Fraction:
    values = tuple(speeds)
    if not values:
        raise ValueError("at least one speed is required")
    return max(
        min(fractional_distance(time * speed) for speed in values)
        for time in _critical_times(values)
    )


def _has_relation(
    speeds: tuple[int, ...], support: tuple[int, ...], target: int | None = None
) -> bool:
    for coefficients in product(range(-2, 3), repeat=len(support)):
        if not any(coefficients):
            continue
        if target is not None and coefficients[support.index(target)] == 0:
            continue
        if sum(coefficient * speeds[index] for index, coefficient in zip(support, coefficients)) == 0:
            return True
    return False


def coefficient_two_seed_sets(speeds: Iterable[int]) -> tuple[tuple[int, ...], ...]:
    values = tuple(speeds)
    indices = tuple(range(len(values)))
    certificates: list[tuple[int, ...]] = []
    for size in range(3):
        for seeds in combinations(indices, size):
            if _has_relation(values, seeds):
                continue
            if all(
                _has_relation(values, tuple((*seeds, target)), target=target)
                for target in indices
                if target not in seeds
            ):
                certificates.append(seeds)
    return tuple(certificates)


def _in_frame(speeds: tuple[int, ...]) -> bool:
    return (
        3 <= len(speeds) <= 8
        and len(set(speeds)) == len(speeds)
        and all(left < right for left, right in zip(speeds, speeds[1:]))
        and speeds[0] > 0
        and speeds[-1] <= 20
        and gcd(*speeds) == 1
    )


def is_bounded_claim_counterexample(speeds: Iterable[int]) -> bool:
    values = tuple(speeds)
    if not _in_frame(values):
        return False
    threshold = Fraction(2, 2 * len(values) + 1)
    return maximum_loneliness(values) <= threshold and not coefficient_two_seed_sets(values)
