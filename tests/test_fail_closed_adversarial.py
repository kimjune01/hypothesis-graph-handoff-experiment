"""Frozen, economical adversarial checks for the fail-closed claim.

These are exact boundary/interleaving tests, not repeated statistical trials.
"""

import json
import subprocess
import sys
import threading

import pytest

from concurrency_scheduler import Scheduler, StalePublication
from concurrency_work import discover


class Clock:
    def __init__(self, now=100.0):
        self.now = now

    def __call__(self):
        return self.now


def one_edge_scheduler(tmp_path, name="case", *, clock=None, lease_seconds=5):
    tokens = iter(f"{name}-token-{i}" for i in range(4))
    scheduler = Scheduler(
        tmp_path / f"{name}.db",
        lease_seconds=lease_seconds,
        clock=clock,
        token_source=tokens.__next__,
    )
    scheduler.install_dag(
        [
            {"id": "R", "state": "STALE", "work": {"kind": "root", "node_id": "R"}},
            {
                "id": "A",
                "state": "BLOCKED",
                "work": {"kind": "gate", "node_id": "A", "n": 3},
            },
        ],
        [("R", "A")],
    )
    scheduler.verify_root("R", {"value": "root-v1"})
    return scheduler


def test_forced_double_claim_has_one_winner_for_the_only_open_node(tmp_path):
    scheduler = one_edge_scheduler(tmp_path, "double-claim")
    barrier = threading.Barrier(2)
    outcomes = []

    def claim(worker):
        barrier.wait()
        outcomes.append(scheduler.claim(worker))

    threads = [threading.Thread(target=claim, args=(worker,)) for worker in ("w1", "w2")]
    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join()

    winners = [outcome for outcome in outcomes if outcome is not None]
    assert len(winners) == 1
    assert winners[0]["node_id"] == "A"


def test_publish_then_root_update_makes_acceptance_historical(tmp_path):
    scheduler = one_edge_scheduler(tmp_path, "publish-first")
    claim = scheduler.claim("worker")
    accepted = scheduler.publish(claim["claim_token"], discover(claim["work"]))

    assert accepted["superseded"] is False
    assert scheduler.update_root("R", {"value": "root-v2"}) == ["R", "A"]
    replay = scheduler.publish(claim["claim_token"], discover(claim["work"]))
    assert replay["superseded"] is True
    assert scheduler.node("A")["state"] == "OPEN"


def test_root_update_then_publish_rejects_old_entitlement(tmp_path):
    scheduler = one_edge_scheduler(tmp_path, "update-first")
    claim = scheduler.claim("worker")
    scheduler.update_root("R", {"value": "root-v2"})

    with pytest.raises(StalePublication):
        scheduler.publish(claim["claim_token"], discover(claim["work"]))
    assert scheduler.node("A")["state"] == "OPEN"
    assert not scheduler.events("accept")


@pytest.mark.parametrize(
    ("offset", "accepted"),
    [(-1e-9, True), (0.0, False), (1e-9, False)],
    ids=("immediately-before", "exactly-at", "immediately-after"),
)
def test_publication_at_exact_lease_boundary(tmp_path, offset, accepted):
    clock = Clock()
    scheduler = one_edge_scheduler(tmp_path, f"expiry-{accepted}-{offset}", clock=clock)
    claim = scheduler.claim("worker")
    clock.now = claim["lease_until"] + offset

    if accepted:
        assert scheduler.publish(claim["claim_token"], discover(claim["work"]))["status"] == "VERIFIED"
    else:
        with pytest.raises(StalePublication):
            scheduler.publish(claim["claim_token"], discover(claim["work"]))


def test_invariant_sensitivity_receipt_and_version_bypasses(tmp_path):
    scheduler = one_edge_scheduler(tmp_path, "bypasses")
    claim = scheduler.claim("worker")
    with pytest.raises(ValueError):
        scheduler.publish(claim["claim_token"], {"kind": "gate", "node_id": "A", "verdict": True})

    # A changed prerequisite version must invalidate the old entitlement even if
    # a caller presents the originally valid receipt.
    scheduler.update_root("R", {"value": "root-v2"})
    with pytest.raises(StalePublication):
        scheduler.publish(claim["claim_token"], discover(claim["work"]))


def test_invariant_sensitivity_exact_invalidation_and_atomic_publication(tmp_path):
    scheduler = Scheduler(tmp_path / "diamond.db", token_source=iter(f"t{i}" for i in range(8)).__next__)
    scheduler.install_dag(
        [
            {"id": "R", "state": "STALE", "work": {"kind": "root", "node_id": "R"}},
            {"id": "A", "state": "BLOCKED", "work": {"kind": "gate", "node_id": "A", "n": 3}},
            {"id": "B", "state": "BLOCKED", "work": {"kind": "gate", "node_id": "B", "n": 3}},
            {"id": "J", "state": "BLOCKED", "work": {"kind": "gate", "node_id": "J", "n": 3}},
        ],
        [("R", "A"), ("R", "B"), ("A", "J")],
    )
    scheduler.verify_root("R", {"value": "root"})
    claim = scheduler.claim("worker")
    scheduler.publish(claim["claim_token"], discover(claim["work"]))

    with scheduler._db() as db:
        publication = db.execute(
            "SELECT acceptance_seq FROM publications WHERE claim_token=?", (claim["claim_token"],)
        ).fetchone()
        event = db.execute("SELECT kind FROM events WHERE seq=?", (publication["acceptance_seq"],)).fetchone()
    assert event["kind"] == "accept"

    before_b = scheduler.node("B")["version"]
    assert scheduler.invalidate("A") == ["A", "J"]
    assert scheduler.node("B")["version"] == before_b


def _semantic_snapshot(scheduler):
    with scheduler._db() as db:
        return {
            "nodes": [tuple(row) for row in db.execute(
                "SELECT id,state,version,work,receipt FROM nodes ORDER BY id"
            )],
            "claims": [tuple(row) for row in db.execute(
                "SELECT token,status,result FROM claims ORDER BY token"
            )],
            "publications": [tuple(row) for row in db.execute(
                "SELECT * FROM publications ORDER BY acceptance_seq"
            )],
            "events": [tuple(row) for row in db.execute(
                "SELECT kind,node_id,detail FROM events ORDER BY seq"
            )],
        }


def _crash_probe(db_path, operation, *args):
    probe = __import__("pathlib").Path(__file__).parents[1] / "fail_closed_crash_probe.py"
    return subprocess.run(
        [sys.executable, str(probe), str(db_path), operation, *map(str, args)],
        check=False,
    )


def test_crash_before_publication_commit_is_all_or_nothing(tmp_path):
    scheduler = one_edge_scheduler(tmp_path, "crash-publish")
    claim = scheduler.claim("worker")
    before = _semantic_snapshot(scheduler)
    receipt = json.dumps(discover(claim["work"]), sort_keys=True)

    result = _crash_probe(scheduler.path, "publish", claim["claim_token"], receipt)

    assert result.returncode == 77
    assert _semantic_snapshot(scheduler) == before


def test_crash_before_invalidation_commit_is_all_or_nothing(tmp_path):
    scheduler = one_edge_scheduler(tmp_path, "crash-invalidate")
    claim = scheduler.claim("worker")
    scheduler.publish(claim["claim_token"], discover(claim["work"]))
    before = _semantic_snapshot(scheduler)

    result = _crash_probe(scheduler.path, "update-root", "R", json.dumps({"value": "v2"}))

    assert result.returncode == 78
    assert _semantic_snapshot(scheduler) == before
