from fail_closed_conformance import REQUIRED_DISPOSITIONS, run_conformance_basis


def test_economical_basis_matches_after_every_action(tmp_path):
    report = run_conformance_basis(tmp_path)

    assert report.mismatches == ()
    assert report.dispositions == REQUIRED_DISPOSITIONS
    assert report.traces == 2
    assert report.actions == 18
    assert report.comparisons == 20
