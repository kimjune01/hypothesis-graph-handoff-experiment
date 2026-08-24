from fractions import Fraction

from grader.verifier import (
    coefficient_two_seed_sets,
    is_bounded_claim_counterexample,
    maximum_loneliness,
)


def test_maximum_loneliness_is_exact_on_small_fixtures() -> None:
    assert maximum_loneliness((1,)) == Fraction(1, 2)
    assert maximum_loneliness((1, 2)) == Fraction(1, 3)
    assert maximum_loneliness((1, 2, 3)) == Fraction(1, 4)


def test_known_boundary_fixture_has_exact_value() -> None:
    assert maximum_loneliness((1, 4, 5, 6, 7, 11, 13, 16)) == Fraction(2, 17)


def test_seed_certificate_exists_for_negative_fixture() -> None:
    assert coefficient_two_seed_sets((1, 2, 3))
    assert not is_bounded_claim_counterexample((1, 2, 3))


def test_verifier_rejects_out_of_frame_tuple() -> None:
    assert not is_bounded_claim_counterexample((2, 4, 6))
    assert not is_bounded_claim_counterexample((1, 2))
    assert not is_bounded_claim_counterexample(tuple(range(1, 22, 3)))


def test_verifier_accepts_known_counterexample() -> None:
    assert is_bounded_claim_counterexample((1, 4, 5, 6, 7, 11, 13, 16))


def test_additional_first_band_fixtures_are_not_counterexamples() -> None:
    for speeds in ((1, 3, 4, 7), (1, 3, 4, 5, 9), (1, 5, 6, 11, 16, 17)):
        assert not is_bounded_claim_counterexample(speeds)
