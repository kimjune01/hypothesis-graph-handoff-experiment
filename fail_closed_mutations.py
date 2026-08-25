"""Exact, isolated mutations used to demonstrate safety-suite sensitivity."""

from __future__ import annotations

import shutil
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class MutationResult:
    name: str
    test: str
    killed: bool
    returncode: int


MUTANTS = (
    ("receipt-bypass", "tests/test_fail_closed_adversarial.py::test_invariant_sensitivity_receipt_and_version_bypasses"),
    ("version-entitlement-bypass", "tests/test_fail_closed_adversarial.py::test_root_update_then_publish_rejects_old_entitlement"),
    ("expired-token-acceptance", "tests/test_fail_closed_adversarial.py::test_publication_at_exact_lease_boundary"),
    ("claim-exclusivity-loss", "tests/test_fail_closed_adversarial.py::test_forced_double_claim_has_one_winner_for_the_only_open_node"),
    ("under-invalidation", "tests/test_concurrency_scheduler.py::test_authoritative_root_update_invalidates_only_reachable_nodes"),
    ("over-invalidation", "tests/test_concurrency_scheduler.py::test_authoritative_root_update_invalidates_only_reachable_nodes"),
    ("split-publication-transaction", "tests/test_fail_closed_adversarial.py::test_crash_before_publication_commit_is_all_or_nothing"),
)


def _replace_once(source: str, old: str, new: str) -> str:
    if source.count(old) < 1:
        raise AssertionError(f"mutation anchor missing: {old!r}")
    return source.replace(old, new, 1)


def _in_update_root(source: str, old: str, new: str) -> str:
    start = source.index("    def update_root(")
    end = source.index("    def invalidate(", start)
    block = _replace_once(source[start:end], old, new)
    return source[:start] + block + source[end:]


def _mutate(source: str, name: str) -> str:
    if name == "receipt-bypass":
        return _replace_once(source, "if not check_receipt(work, receipt):", "if False and not check_receipt(work, receipt):")
    if name == "version-entitlement-bypass":
        source = _replace_once(source, "or node[\"state\"] != \"CLAIMED\" or node[\"version\"] != claim[\"node_version\"]\n                    or current != json.loads(claim[\"parent_versions\"])", "or False")
        return _in_update_root(source, "db.execute(\"UPDATE claims SET status='CANCELLED' WHERE node_id=? AND status='LIVE'\", (nid,))", "pass  # mutant: leave stale claim live")
    if name == "expired-token-acceptance":
        return _replace_once(source, "claim[\"lease_until\"] <= self._clock()", "False and claim[\"lease_until\"] <= self._clock()")
    if name == "claim-exclusivity-loss":
        source = _replace_once(source, "SELECT * FROM nodes WHERE state='OPEN' ORDER BY", "SELECT * FROM nodes WHERE state IN ('OPEN','CLAIMED') ORDER BY")
        return _replace_once(source, "UPDATE nodes SET state='CLAIMED' WHERE id=? AND state='OPEN'", "UPDATE nodes SET state='CLAIMED' WHERE id=?")
    if name == "under-invalidation":
        return _in_update_root(source, "todo += [r[\"child\"] for r in db.execute(\n                    \"SELECT child FROM edges WHERE parent=? ORDER BY child\", (nid,)\n                )]", "pass  # mutant: omit descendants")
    if name == "over-invalidation":
        anchor = "            if work_patch:\n"
        addition = "            affected = [r[\"id\"] for r in db.execute(\"SELECT id FROM nodes ORDER BY id\")]\n"
        start = source.index("    def update_root(")
        end = source.index("    def invalidate(", start)
        block = _replace_once(source[start:end], anchor, addition + anchor)
        return source[:start] + block + source[end:]
    if name == "split-publication-transaction":
        return _replace_once(source, "            self._failpoint(\"publication_after_node_write\")", "            db.commit()\n            db.execute(\"BEGIN IMMEDIATE\")\n            self._failpoint(\"publication_after_node_write\")")
    raise ValueError(name)


def run_declared_mutants(repo: Path, scratch: Path) -> tuple[MutationResult, ...]:
    results = []
    for name, test in MUTANTS:
        target = scratch / name
        target.mkdir()
        for module in repo.glob("*.py"):
            shutil.copy2(module, target / module.name)
        (target / "tests").mkdir()
        for test_file in (repo / "tests").glob("*.py"):
            shutil.copy2(test_file, target / "tests" / test_file.name)
        scheduler_path = target / "concurrency_scheduler.py"
        scheduler_path.write_text(_mutate(scheduler_path.read_text(), name))
        completed = subprocess.run(
            [sys.executable, "-m", "pytest", "-q", test], cwd=target,
            stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=False,
        )
        # Pytest code 1 means the selected test executed and failed. Collection,
        # usage, interruption, and infrastructure errors do not kill a mutant.
        results.append(MutationResult(name, test, completed.returncode == 1, completed.returncode))
    return tuple(results)
