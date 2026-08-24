from fractions import Fraction

from grader.verifier import (
    coefficient_two_seed_sets,
    is_bounded_claim_counterexample,
    maximum_loneliness,
)


def test_outside_band_fixture_is_rejected_by_exact_margin() -> None:
    speeds = (1, 2, 18)
    threshold = Fraction(2, 7)
    assert maximum_loneliness(speeds) == Fraction(6, 19)
    assert maximum_loneliness(speeds) - threshold == Fraction(4, 133)
    assert not is_bounded_claim_counterexample(speeds)


def test_band_fixture_has_a_two_seed_certificate() -> None:
    speeds = (1, 3, 4, 5, 9)
    assert maximum_loneliness(speeds) < Fraction(2, 11)
    assert any(len(seeds) <= 2 for seeds in coefficient_two_seed_sets(speeds))
    assert not is_bounded_claim_counterexample(speeds)
