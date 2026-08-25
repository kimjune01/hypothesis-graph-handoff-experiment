import json
import threading
import time
from pathlib import Path

import pytest

from concurrency_scheduler import Scheduler, StalePublication
from concurrency_work import check_receipt, discover
from concurrency_worker import run


def scheduler(tmp_path: Path) -> Scheduler:
    s = Scheduler(tmp_path / "scheduler.db", lease_seconds=30)
    s.install_frozen_dag(difficulty=2)
    s.verify_root("R0", {"value": "frozen-root"})
    return s


class LogicalClock:
    def __init__(self, now=100.0):
        self.now = now

    def __call__(self):
        return self.now


def solve_and_publish(s: Scheduler, worker: str, expected: str | None = None):
    claim = s.claim(worker)
    assert claim
    if expected:
        assert claim["node_id"] == expected
    receipt = discover(claim["work"])
    return claim, s.publish(claim["claim_token"], receipt)


def test_priority_and_gate_pruning(tmp_path):
    s = scheduler(tmp_path)
    claimed = []
    for gate in ("GD", "GA", "GB", "GC", "GE"):
        claim, result = solve_and_publish(s, "w", gate)
        claimed.append(claim["node_id"])
        assert result["status"] == "VERIFIED"
    assert claimed == ["GD", "GA", "GB", "GC", "GE"]
    assert s.node("D")["state"] == "KILLED"
    assert all(e["node_id"] != "D" for e in s.events("claim"))


def test_double_claim_is_atomic(tmp_path):
    s = scheduler(tmp_path)
    barrier = threading.Barrier(2)
    claims = []

    def race(name):
        barrier.wait()
        claims.append(s.claim(name))

    threads = [threading.Thread(target=race, args=(f"w{i}",)) for i in range(2)]
    [t.start() for t in threads]
    [t.join() for t in threads]
    assert len([c for c in claims if c and c["node_id"] == "GD"]) == 1
    assert len({c["node_id"] for c in claims if c}) == 2


def test_publish_is_exact_and_idempotent(tmp_path):
    s = scheduler(tmp_path)
    claim = s.claim("w")
    with pytest.raises(ValueError):
        s.publish(claim["claim_token"], {"kind": "gate", "verdict": True})
    receipt = discover(claim["work"])
    first = s.publish(claim["claim_token"], receipt)
    second = s.publish(claim["claim_token"], receipt)
    assert first == second
    assert len([e for e in s.events("accept") if e["node_id"] == claim["node_id"]]) == 1


def test_expired_and_stale_publications_rejected(tmp_path):
    s = Scheduler(tmp_path / "s.db", lease_seconds=-1)
    s.install_frozen_dag(difficulty=1)
    s.verify_root("R0", {"value": "root"})
    claim = s.claim("w")
    with pytest.raises(StalePublication):
        s.publish(claim["claim_token"], discover(claim["work"]))
    assert s.reap_expired() == [claim["node_id"]]
    replacement = s.claim("w2")
    assert replacement["node_id"] == claim["node_id"]
    assert replacement["claim_token"] != claim["claim_token"]


def test_invalidation_is_transitive_and_preserves_branches(tmp_path):
    s = scheduler(tmp_path)
    for gate in ("GD", "GA", "GB", "GC", "GE"):
        solve_and_publish(s, "w", gate)
    for node in ("A", "B", "C", "X"):
        solve_and_publish(s, "w", node)
    claim, _ = solve_and_publish(s, "w", "JAB")
    solve_and_publish(s, "w", "F")
    before = {n: s.node(n)["version"] for n in ("B", "C", "X")}
    changed = s.invalidate("A", {"challenge": "rotated-a"})
    assert set(changed) == {"A", "JAB", "F"}
    assert s.node("A")["state"] == "OPEN"
    assert s.node("JAB")["state"] == s.node("F")["state"] == "BLOCKED"
    assert {n: s.node(n)["version"] for n in before} == before


def test_active_join_progress_cancel_and_stale_rejection(tmp_path):
    s = scheduler(tmp_path)
    for node in ("GD", "GA", "GB", "GC", "GE", "A", "B", "C", "X"):
        solve_and_publish(s, "w", node)
    claim = s.claim("joiner")
    assert claim["node_id"] == "JAB"
    s.progress(claim["claim_token"], 100)
    s.invalidate("A", {"challenge": "new"})
    assert s.cancelled(claim["claim_token"])
    with pytest.raises(StalePublication):
        s.publish(claim["claim_token"], discover(claim["work"]))


def test_packet_is_dependency_bounded_and_has_no_answer(tmp_path):
    s = scheduler(tmp_path)
    for node in ("GD", "GA", "GB", "GC", "GE", "A", "B", "C", "X"):
        solve_and_publish(s, "w", node)
    packet = s.claim("w")
    assert packet["node_id"] == "JAB"
    assert set(packet["prerequisites"]) == {"A", "B"}
    assert "nonce" not in json.dumps(packet["work"])
    assert "C" not in packet["prerequisites"]


def test_work_receipts_are_exact():
    work = {"kind": "pow", "node_id": "T", "challenge": "x", "difficulty": 2}
    receipt = discover(work)
    assert check_receipt(work, receipt)
    assert not check_receipt(work, {**receipt, "nonce": receipt["nonce"] + 1})


def finish_gates(s):
    for gate in ("GD", "GA", "GB", "GC", "GE"):
        solve_and_publish(s, "gate-worker", gate)


def test_readiness_barrier_blocks_until_three_distinct_workers(tmp_path):
    s = Scheduler(tmp_path / "barrier.db")
    s.install_frozen_dag(difficulty=1, barrier_target=3)
    s.verify_root("R0", {"value": "root"})
    finish_gates(s)
    s.register("w1")
    assert s.claim("w1") is None
    s.register("w2")
    assert s.claim("w2") is None
    s.register("w3")
    assert s.claim("w3")["node_id"] == "A"


def test_three_workers_receive_distinct_frontier_claims(tmp_path):
    s = Scheduler(tmp_path / "frontier.db")
    s.install_frozen_dag(difficulty=1, barrier_target=3)
    s.verify_root("R0", {"value": "root"})
    finish_gates(s)
    for worker in ("w1", "w2", "w3"):
        s.register(worker)
    barrier = threading.Barrier(3)
    claims = {}

    def race(worker):
        barrier.wait()
        claims[worker] = s.claim(worker)

    threads = [threading.Thread(target=race, args=(w,)) for w in ("w1", "w2", "w3")]
    [t.start() for t in threads]
    [t.join() for t in threads]
    assert {c["node_id"] for c in claims.values()} == {"A", "B", "C"}
    assert len({c["worker"] for c in claims.values()}) == 3


def test_semantic_packet_is_canonical_immutable_and_bounded(tmp_path):
    s = scheduler(tmp_path)
    finish_gates(s)
    for node in ("A", "B", "C", "X"):
        solve_and_publish(s, "w", node)
    claim = s.claim("joiner")
    captured = s.packet(claim["claim_token"])
    semantic = captured["packet"]
    assert captured["byte_count"] == len(captured["canonical_json"].encode())
    assert captured["byte_count"] < 2_048
    assert captured["canonical_json"] == json.dumps(semantic, sort_keys=True, separators=(",", ":"))
    assert set(semantic["prerequisites"]) == {"A", "B"}
    assert {"objective", "work", "prerequisites", "checks", "kill_condition", "output_contract"} <= set(semantic)
    assert "claim_token" not in captured["canonical_json"] and "lease" not in captured["canonical_json"]
    assert "answer" not in captured["canonical_json"].lower()
    with s._db() as db:
        with pytest.raises(Exception):
            db.execute("UPDATE packets SET canonical_json='{}' WHERE claim_token=?", (claim["claim_token"],))


def test_worker_polls_pending_barrier_and_exits_at_terminal(tmp_path):
    s = Scheduler(tmp_path / "poll.db")
    s.install_frozen_dag(difficulty=1, barrier_target=3)
    s.verify_root("R0", {"value": "root"})
    finish_gates(s)
    finished = []
    thread = threading.Thread(target=lambda: finished.extend(run(s.path, "w1", poll_seconds=.01)))
    thread.start()
    time.sleep(.05)
    assert thread.is_alive()
    s.register("w2"); s.register("w3")
    thread.join(5)
    assert not thread.is_alive()
    # Other workers may finish the now-released graph; terminal means F verified.
    assert s.node("F")["state"] == "VERIFIED"


def test_claim_freezes_node_version_parent_versions_and_work(tmp_path):
    s = scheduler(tmp_path)
    claim = s.claim("w")
    with s._db() as db:
        row = db.execute("SELECT * FROM claims WHERE token=?", (claim["claim_token"],)).fetchone()
    assert row["node_version"] == s.node(claim["node_id"])["version"]
    assert json.loads(row["parent_versions"]) == claim["parent_versions"]
    assert json.loads(row["claimed_work"]) == claim["work"]


def test_publication_is_immutable_and_records_entitlement(tmp_path):
    s = scheduler(tmp_path)
    claim = s.claim("w")
    receipt = discover(claim["work"])
    result = s.publish(claim["claim_token"], receipt)
    with s._db() as db:
        publication = db.execute("SELECT * FROM publications WHERE claim_token=?", (claim["claim_token"],)).fetchone()
        assert publication["node_version"] == claim["node_version"]
        assert json.loads(publication["parent_versions"]) == claim["parent_versions"]
        assert json.loads(publication["result"]) == result
        with pytest.raises(Exception):
            db.execute("DELETE FROM publications WHERE claim_token=?", (claim["claim_token"],))
        with pytest.raises(Exception):
            db.execute("UPDATE events SET kind='tampered'")


def test_accepted_replay_after_invalidation_is_historical_only(tmp_path):
    s = scheduler(tmp_path)
    claim, accepted = solve_and_publish(s, "w")
    s.invalidate(claim["node_id"], {"n": 99})
    replay = s.publish(claim["claim_token"], discover(claim["work"]))
    assert accepted["superseded"] is False
    assert replay == {**accepted, "superseded": True}
    assert s.node(claim["node_id"])["state"] != "VERIFIED"


def test_progress_rejects_expired_lease_with_logical_clock(tmp_path):
    clock = LogicalClock()
    s = Scheduler(tmp_path / "clock.db", lease_seconds=5, clock=clock, token_source=iter(["token-1"]).__next__)
    s.install_frozen_dag(difficulty=1)
    s.verify_root("R0", {"value": "root"})
    claim = s.claim("w")
    assert claim["claim_token"] == "token-1"
    clock.now += 6
    with pytest.raises(StalePublication):
        s.progress(claim["claim_token"], 1)


def test_root_admission_rejects_non_root_and_arbitrary_dag_is_supported(tmp_path):
    s = Scheduler(tmp_path / "dag.db", token_source=iter(["t"]).__next__)
    nodes = [
        {"id": "R", "state": "STALE", "work": {"kind": "root", "node_id": "R"}},
        {"id": "A", "state": "BLOCKED", "work": {"kind": "gate", "node_id": "A", "n": 3}},
    ]
    s.install_dag(nodes, [("R", "A")])
    with pytest.raises(ValueError):
        s.verify_root("A", {"value": "not-authoritative"})
    s.verify_root("R", {"value": "root"})
    assert s.claim("w")["node_id"] == "A"


def test_authoritative_root_update_invalidates_only_reachable_nodes(tmp_path):
    s = Scheduler(tmp_path / "roots.db")
    nodes = [
        {"id": "R1", "state": "STALE", "work": {"kind": "root", "node_id": "R1"}},
        {"id": "A", "state": "BLOCKED", "work": {"kind": "gate", "node_id": "A", "n": 3}},
        {"id": "R2", "state": "STALE", "work": {"kind": "root", "node_id": "R2"}},
        {"id": "B", "state": "BLOCKED", "work": {"kind": "gate", "node_id": "B", "n": 3}},
    ]
    s.install_dag(nodes, [("R1", "A"), ("R2", "B")])
    s.verify_root("R1", {"value": "one"})
    s.verify_root("R2", {"value": "two"})
    with pytest.raises(ValueError):
        s.verify_root("R1", {"value": "silent-replacement"})
    before = s.node("B")
    changed = s.update_root("R1", {"value": "one-v2"})
    assert changed == ["R1", "A"]
    assert s.node("R1")["state"] == "VERIFIED"
    assert s.node("A")["state"] == "OPEN"
    assert s.node("B")["state"] == before["state"]
    assert s.node("B")["version"] == before["version"]
    with pytest.raises(ValueError):
        s.update_root("A", {"value": "forbidden"})
