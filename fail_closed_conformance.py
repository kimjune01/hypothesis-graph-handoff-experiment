"""Economical correspondence checks between the pure model and SQLite scheduler.

This is intentionally a transition/disposition basis, not a replay of exploration
edges. The model remains the semantic oracle; this module only adapts API shapes.
"""

from __future__ import annotations

import json
from dataclasses import dataclass
from hashlib import sha256
from pathlib import Path

from concurrency_scheduler import Scheduler, StalePublication
from concurrency_work import discover
from fail_closed_model import Action, Model, initial_diamond, step


REQUIRED_DISPOSITIONS = frozenset({
    "claimed", "not-claimable", "unknown-token", "invalid-receipt", "accepted",
    "current-replay", "expired", "cancelled", "root-updated", "superseded-replay",
})


class LogicalClock:
    def __init__(self):
        self.value = 0.0

    def __call__(self):
        return self.value

    def advance(self, amount: float):
        self.value += amount


@dataclass(frozen=True)
class ConformanceReport:
    traces: int
    actions: int
    dispositions: frozenset[str]
    comparisons: int
    mismatches: tuple[str, ...]


def _canonical(value) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"))


def _digest_json(value) -> str:
    return sha256(_canonical(value).encode()).hexdigest()


def _works() -> dict[str, dict]:
    return {
        "R": {"kind": "root", "node_id": "R"},
        "A": {"kind": "gate", "node_id": "A", "n": 2},
        "B": {"kind": "gate", "node_id": "B", "n": 3},
        "J": {"kind": "gate", "node_id": "J", "n": 5},
    }


def _new_pair(path: Path):
    clock = LogicalClock()
    tokens = iter(f"t{i}" for i in range(1, 100))
    scheduler = Scheduler(path, lease_seconds=1, clock=clock, token_source=lambda: next(tokens))
    works = _works()
    scheduler.install_dag(
        [{"id": node, "state": "STALE" if node == "R" else "BLOCKED",
          "work": work, "tie_order": index}
         for index, (node, work) in enumerate(works.items())],
        (("R", "A"), ("R", "B"), ("A", "J"), ("B", "J")),
    )
    root_receipt = {"authority": "fixture", "version": 1}
    scheduler.verify_root("R", root_receipt)
    roots = {node: _digest_json(work) for node, work in works.items()}
    model = initial_diamond(lease_ticks=1, work_roots=roots)
    nodes = dict(model.nodes)
    nodes["R"] = nodes["R"]._replace(receipt=_canonical(root_receipt))
    return scheduler, model._replace(nodes=nodes), clock, works


def _model_projection(model: Model) -> tuple:
    nodes = tuple(
        (node_id, node.state, node.version,
         sha256((node.receipt or "").encode()).hexdigest() if node.receipt else None,
         node.work_root)
        for node_id, node in sorted(model.nodes.items())
    )
    claims = tuple(
        (token, claim.node, claim.worker, claim.node_version, claim.parent_versions,
         claim.work_root, claim.status)
        for token, claim in sorted(model.claims.items())
    )
    publications = tuple(
        (pub.token, pub.node, pub.node_version, pub.parent_versions, pub.work_root,
         pub.receipt_digest, pub.sequence)
        for pub in model.publications
    )
    return nodes, claims, publications


def _sqlite_projection(scheduler: Scheduler) -> tuple:
    with scheduler._db() as db:
        node_rows = db.execute("SELECT * FROM nodes ORDER BY id").fetchall()
        nodes = tuple(
            (row["id"], row["state"], row["version"],
             _digest_json(json.loads(row["receipt"])) if row["receipt"] else None,
             _digest_json(json.loads(row["work"])))
            for row in node_rows
        )
        claim_rows = db.execute("SELECT * FROM claims ORDER BY token").fetchall()
        claims = tuple(
            (row["token"], row["node_id"], row["worker"], row["node_version"],
             tuple(sorted(json.loads(row["parent_versions"]).items())),
             _digest_json(json.loads(row["claimed_work"])), row["status"])
            for row in claim_rows
        )
        pub_rows = db.execute("SELECT * FROM publications ORDER BY acceptance_seq").fetchall()
        claim_work = {row["token"]: _digest_json(json.loads(row["claimed_work"])) for row in claim_rows}
        publications = tuple(
            (row["claim_token"], row["node_id"], row["node_version"],
             tuple(sorted(json.loads(row["parent_versions"]).items())),
             claim_work[row["claim_token"]], row["receipt_digest"], index)
            for index, row in enumerate(pub_rows, 1)
        )
    return nodes, claims, publications


def run_conformance_basis(directory: Path) -> ConformanceReport:
    dispositions: set[str] = set()
    mismatches: list[str] = []
    comparisons = actions = 0

    def compare(label: str, scheduler: Scheduler, model: Model):
        nonlocal comparisons
        comparisons += 1
        expected, actual = _model_projection(model), _sqlite_projection(scheduler)
        if expected != actual:
            mismatches.append(f"{label}: model={expected!r} sqlite={actual!r}")

    # Trace 1 covers valid/invalid acceptance, join unlocking, both replay modes,
    # and exact root invalidation. Scheduler priority determines A, then B, then J.
    scheduler, model, _, works = _new_pair(directory / "basis-main.sqlite")
    compare("main:initial", scheduler, model)
    accepted_tokens: list[str] = []
    for expected_node in ("A", "B", "J"):
        packet = scheduler.claim(f"w-{expected_node}")
        assert packet and packet["node_id"] == expected_node
        model, result = step(model, Action("claim", worker=f"w-{expected_node}", node=expected_node))
        actions += 1; dispositions.add(result.disposition); compare(f"main:claim-{expected_node}", scheduler, model)
        token = packet["claim_token"]
        if expected_node == "A":
            assert scheduler.claim("w-A") is None
            unchanged, result = step(model, Action("claim", worker="w-A", node="B"))
            assert unchanged == model
            actions += 1; dispositions.add(result.disposition); compare("main:not-claimable", scheduler, model)
            try:
                scheduler.publish(token, {"bad": True})
            except ValueError:
                pass
            model, result = step(model, Action("publish", token=token, receipt="invalid"))
            actions += 1; dispositions.add(result.disposition); compare("main:invalid", scheduler, model)
        receipt = discover(works[expected_node])
        scheduler.publish(token, receipt)
        model, result = step(model, Action("publish", token=token, receipt=_canonical(receipt)))
        actions += 1; dispositions.add(result.disposition); compare(f"main:accept-{expected_node}", scheduler, model)
        accepted_tokens.append(token)
        if expected_node == "A":
            scheduler.publish(token, receipt)
            model, result = step(model, Action("publish", token=token, receipt=_canonical(receipt)))
            actions += 1; dispositions.add(result.disposition); compare("main:current-replay", scheduler, model)
    new_root = {"authority": "fixture", "version": 2}
    scheduler.update_root("R", new_root)
    model, result = step(model, Action("update_root", receipt=_canonical(new_root)))
    actions += 1; dispositions.add(result.disposition); compare("main:root-update", scheduler, model)
    scheduler.publish(accepted_tokens[-1], discover(works["J"]))
    model, result = step(model, Action("publish", token=accepted_tokens[-1], receipt=_canonical(discover(works["J"]))))
    actions += 1; dispositions.add(result.disposition); compare("main:superseded-replay", scheduler, model)
    try:
        scheduler.publish("missing", {})
    except StalePublication:
        pass
    unchanged, result = step(model, Action("publish", token="missing", receipt="invalid"))
    assert unchanged == model
    actions += 1; dispositions.add(result.disposition); compare("main:unknown-token", scheduler, model)
    packet = scheduler.claim("w-cancel")
    model, result = step(model, Action("claim", worker="w-cancel", node="A"))
    actions += 1; dispositions.add(result.disposition); compare("main:claim-before-cancel", scheduler, model)
    newer_root = {"authority": "fixture", "version": 3}
    scheduler.update_root("R", newer_root)
    model, result = step(model, Action("update_root", receipt=_canonical(newer_root)))
    actions += 1; dispositions.add(result.disposition); compare("main:cancel-root-update", scheduler, model)
    try:
        scheduler.publish(packet["claim_token"], discover(works["A"]))
    except StalePublication:
        pass
    unchanged, result = step(model, Action("publish", token=packet["claim_token"], receipt=_canonical(discover(works["A"]))))
    assert unchanged == model
    actions += 1; dispositions.add(result.disposition); compare("main:cancelled-publish", scheduler, model)

    # Trace 2 isolates expiry; advancing past (rather than exactly to) the lease
    # avoids relying on an implementation-specific boundary convention.
    scheduler, model, clock, _ = _new_pair(directory / "basis-expiry.sqlite")
    compare("expiry:initial", scheduler, model)
    packet = scheduler.claim("w-expiry")
    model, result = step(model, Action("claim", worker="w-expiry", node="A"))
    actions += 1; dispositions.add(result.disposition); compare("expiry:claim", scheduler, model)
    clock.advance(2)
    scheduler.reap_expired()
    model, _ = step(model, Action("tick")); model, result = step(model, Action("tick"))
    actions += 1; dispositions.add("expired"); compare("expiry:expire", scheduler, model)
    try:
        scheduler.publish(packet["claim_token"], discover(_works()["A"]))
    except StalePublication:
        pass
    unchanged, rejected = step(model, Action("publish", token=packet["claim_token"], receipt=_canonical(discover(_works()["A"]))))
    assert unchanged == model and rejected.disposition == "expired"
    actions += 1; compare("expiry:rejected-publish", scheduler, model)

    return ConformanceReport(2, actions, frozenset(dispositions), comparisons, tuple(mismatches))
