from __future__ import annotations

from fractions import Fraction
import json
from itertools import combinations, product
from math import gcd
from pathlib import Path
from typing import Iterable


def band_radius(n: int) -> Fraction:
    return Fraction(2, 2 * n + 1)


def coverage_intervals(v: tuple[int, ...]) -> list[tuple[Fraction, Fraction]]:
    n = len(v)
    delta = band_radius(n)
    intervals: list[tuple[Fraction, Fraction]] = []
    for value in v:
        radius = delta / value
        for multiple in range(value + 1):
            center = Fraction(multiple, value)
            left = max(Fraction(0), center - radius)
            right = min(Fraction(1), center + radius)
            intervals.append((left, right))
    intervals.sort()
    return intervals


def merged_coverage(v: tuple[int, ...]) -> list[tuple[Fraction, Fraction]]:
    merged: list[list[Fraction]] = []
    for left, right in coverage_intervals(v):
        if not merged or left > merged[-1][1]:
            merged.append([left, right])
            continue
        if right > merged[-1][1]:
            merged[-1][1] = right
    return [(left, right) for left, right in merged]


def is_band_tuple(v: tuple[int, ...]) -> bool:
    merged = merged_coverage(v)
    return bool(merged) and merged[0][0] == 0 and merged[-1][1] == 1 and all(
        merged[i][1] >= merged[i + 1][0] for i in range(len(merged) - 1)
    )


def first_uncovered_point(v: tuple[int, ...]) -> Fraction | None:
    merged = merged_coverage(v)
    if not merged:
        return Fraction(0)
    if merged[0][0] > 0:
        return merged[0][0] / 2
    current_right = merged[0][1]
    for left, right in merged[1:]:
        if left > current_right:
            return (current_right + left) / 2
        if right > current_right:
            current_right = right
    if current_right < 1:
        return (current_right + 1) / 2
    return None


def has_coefficient_two_relation(
    v: tuple[int, ...], support: tuple[int, ...], required_index: int | None = None
) -> bool:
    support_values = [v[index] for index in support]
    required_position = None
    if required_index is not None:
        required_position = support.index(required_index)
    for coeffs in product(range(-2, 3), repeat=len(support)):
        if all(coeff == 0 for coeff in coeffs):
            continue
        if required_position is not None and coeffs[required_position] == 0:
            continue
        total = sum(coeff * value for coeff, value in zip(coeffs, support_values))
        if total == 0:
            return True
    return False


def seed_certificates(v: tuple[int, ...]) -> list[tuple[int, ...]]:
    certificates: list[tuple[int, ...]] = []
    indices = tuple(range(len(v)))
    for size in (1, 2):
        for support in combinations(indices, size):
            if has_coefficient_two_relation(v, support):
                continue
            if all(
                has_coefficient_two_relation(
                    v, tuple(sorted((*support, outsider))), required_index=outsider
                )
                for outsider in indices
                if outsider not in support
            ):
                certificates.append(support)
    return certificates


def has_seed_certificate(v: tuple[int, ...]) -> bool:
    return bool(seed_certificates(v))


def primitive(v: Iterable[int]) -> bool:
    g = 0
    for value in v:
        g = gcd(g, value)
    return g == 1


def audit_range(
    min_n: int = 3, max_n: int = 7, max_height: int = 20
) -> dict[str, object]:
    summary: dict[str, object] = {
        "bounds": {
            "min_n": min_n,
            "max_n": max_n,
            "max_height": max_height,
        },
        "per_n": {},
        "seedless_band_tuples": [],
    }
    for n in range(min_n, max_n + 1):
        total = 0
        primitive_count = 0
        band_count = 0
        band_with_seed_count = 0
        seedless_band_count = 0
        first_band: tuple[int, ...] | None = None
        first_seedless_band: tuple[int, ...] | None = None
        for v in combinations(range(1, max_height + 1), n):
            total += 1
            if not primitive(v):
                continue
            primitive_count += 1
            if not is_band_tuple(v):
                continue
            band_count += 1
            if first_band is None:
                first_band = v
            certs = seed_certificates(v)
            if certs:
                band_with_seed_count += 1
                continue
            seedless_band_count += 1
            if first_seedless_band is None:
                first_seedless_band = v
            summary["seedless_band_tuples"].append(list(v))
        summary["per_n"][str(n)] = {
            "total_increasing_tuples": total,
            "primitive_tuples": primitive_count,
            "band_tuples": band_count,
            "band_tuples_with_seed_certificate": band_with_seed_count,
            "band_tuples_without_seed_certificate": seedless_band_count,
            "first_band_tuple": list(first_band) if first_band else None,
            "first_seedless_band_tuple": (
                list(first_seedless_band) if first_seedless_band else None
            ),
        }
    return summary


def write_audit_receipts(
    output_path: str = "audit_receipt.json", min_n: int = 3, max_n: int = 7, max_height: int = 20
) -> dict[str, object]:
    summary = audit_range(min_n=min_n, max_n=max_n, max_height=max_height)
    Path(output_path).write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n")
    return summary


def build_n8_execution_plan(max_height: int = 20, chunk_size: int = 2500) -> dict[str, object]:
    return {
        "purpose": "Executable plan for a future n=8 search. This function does not enumerate or evaluate any n=8 tuple.",
        "parameters": {
            "n": 8,
            "max_height": max_height,
            "chunk_size": chunk_size,
        },
        "phases": [
            "Generate the primitive increasing 8-tuples lazily in lexicographic order.",
            "Assign tuples to chunks of at most chunk_size candidates without precomputing the full list.",
            "For each chunk, run the exact band predicate first.",
            "Only on surviving band tuples, run the seed-certificate audit.",
            "Persist per-chunk JSON receipts and a final merged report.",
        ],
        "execution_notes": [
            "The exact predicate implementation is already in search_prep.py.",
            "To respect the current instruction set, do not call any function that iterates over combinations(..., 8) during this preparatory phase.",
            "A future operator can implement chunk execution by adding a generator over combinations(range(1, max_height + 1), 8).",
        ],
    }


def write_n8_plan(output_path: str = "n8_plan.json") -> dict[str, object]:
    plan = build_n8_execution_plan()
    Path(output_path).write_text(json.dumps(plan, indent=2, sort_keys=True) + "\n")
    return plan


if __name__ == "__main__":
    write_audit_receipts()
    write_n8_plan()
