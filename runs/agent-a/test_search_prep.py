import unittest
from fractions import Fraction

from search_prep import (
    coverage_intervals,
    first_uncovered_point,
    has_coefficient_two_relation,
    has_seed_certificate,
    is_band_tuple,
    merged_coverage,
    seed_certificates,
)


class RelationTests(unittest.TestCase):
    def test_pair_can_have_coefficient_two_relation(self) -> None:
        self.assertTrue(has_coefficient_two_relation((1, 2), (0, 1)))

    def test_pair_can_lack_coefficient_two_relation(self) -> None:
        self.assertFalse(has_coefficient_two_relation((1, 3), (0, 1)))

    def test_triple_relation_can_require_third_index(self) -> None:
        self.assertTrue(
            has_coefficient_two_relation((1, 3, 4), (0, 1, 2), required_index=2)
        )


class SeedCertificateTests(unittest.TestCase):
    def test_known_seed_certificate_is_detected(self) -> None:
        self.assertEqual(seed_certificates((1, 3, 4)), [(0, 1), (0, 2), (1, 2)])
        self.assertTrue(has_seed_certificate((1, 3, 4)))

    def test_tuple_can_have_no_seed_certificate(self) -> None:
        self.assertEqual(seed_certificates((1, 3, 9)), [])
        self.assertFalse(has_seed_certificate((1, 3, 9)))


class BandTests(unittest.TestCase):
    def test_known_band_tuple(self) -> None:
        self.assertTrue(is_band_tuple((1, 2, 3)))

    def test_known_non_band_tuple(self) -> None:
        self.assertFalse(is_band_tuple((1, 2, 4)))
        self.assertEqual(first_uncovered_point((1, 2, 4)), Fraction(19, 56))

    def test_interval_receipt_is_exact(self) -> None:
        intervals = coverage_intervals((1, 2, 4))
        self.assertEqual(intervals[0], (Fraction(0), Fraction(1, 14)))
        self.assertIn((Fraction(5, 14), Fraction(9, 14)), intervals)
        self.assertEqual(merged_coverage((1, 2, 4))[0], (Fraction(0), Fraction(9, 28)))


if __name__ == "__main__":
    unittest.main()
