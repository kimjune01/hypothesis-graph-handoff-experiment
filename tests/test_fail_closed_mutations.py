from pathlib import Path

from fail_closed_mutations import run_declared_mutants


def test_every_declared_mutant_is_killed(tmp_path):
    results = run_declared_mutants(Path(__file__).parents[1], tmp_path)

    assert len(results) == 7
    assert all(result.killed for result in results), results
