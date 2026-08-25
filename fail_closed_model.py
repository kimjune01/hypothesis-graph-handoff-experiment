"""Small declarative reference model for the fail-closed experiment.

This model intentionally describes protocol rules, not SQLite implementation steps.
"""

from __future__ import annotations

from dataclasses import dataclass
from hashlib import sha256
from typing import NamedTuple


class Node(NamedTuple):
    state: str
    version: int
    receipt: str | None
    work_root: str
    accepted_parent_versions: tuple[tuple[str, int], ...] = ()


class Claim(NamedTuple):
    token: str
    node: str
    worker: str
    node_version: int
    parent_versions: tuple[tuple[str, int], ...]
    work_root: str
    expires_at: int
    status: str


class Publication(NamedTuple):
    token: str
    node: str
    node_version: int
    parent_versions: tuple[tuple[str, int], ...]
    work_root: str
    receipt_digest: str
    sequence: int


class Model(NamedTuple):
    nodes: dict[str, Node]
    edges: tuple[tuple[str, str], ...]
    claims: dict[str, Claim]
    publications: tuple[Publication, ...]
    clock: int
    lease_ticks: int
    next_token: int
    events: tuple[str, ...]


@dataclass(frozen=True)
class Action:
    kind: str
    worker: str | None = None
    node: str | None = None
    token: str | None = None
    receipt: str | None = None


@dataclass(frozen=True)
class Result:
    accepted: bool
    disposition: str
    token: str | None = None


# The table is the model's specification surface. Handlers implement each rule below.
TRANSITION_TABLE = {
    "claim": "open node + exclusive worker/node lease -> live versioned claim",
    "publish": "live current claim + valid receipt + current parents -> atomic acceptance",
    "tick": "advance logical time; expire leases and reopen their current nodes",
    "update_root": "trusted root version update; invalidate exactly reachable descendants",
}


def _digest(value: str) -> str:
    return sha256(value.encode()).hexdigest()


def initial_diamond(lease_ticks: int = 2, work_roots: dict[str, str] | None = None) -> Model:
    roots = work_roots or {node: _digest(f"work:{node}:1") for node in ("R", "A", "B", "J")}
    nodes = {
        "R": Node("VERIFIED", 1, "root:1", roots["R"]),
        "A": Node("OPEN", 1, None, roots["A"]),
        "B": Node("OPEN", 1, None, roots["B"]),
        "J": Node("BLOCKED", 1, None, roots["J"]),
    }
    return Model(nodes, (("R", "A"), ("R", "B"), ("A", "J"), ("B", "J")), {}, (), 0, lease_ticks, 1, ())


def _parents(state: Model, node: str) -> tuple[str, ...]:
    return tuple(sorted(parent for parent, child in state.edges if child == node))


def _descendants(state: Model, root: str) -> set[str]:
    found, frontier = set(), [root]
    while frontier:
        parent = frontier.pop()
        for edge_parent, child in state.edges:
            if edge_parent == parent and child not in found:
                found.add(child)
                frontier.append(child)
    return found


def _refresh(nodes: dict[str, Node], edges: tuple[tuple[str, str], ...]) -> None:
    changed = True
    while changed:
        changed = False
        for node_id, node in tuple(nodes.items()):
            if node.state != "BLOCKED":
                continue
            parents = [nodes[p] for p, c in edges if c == node_id]
            if parents and all(parent.state == "VERIFIED" for parent in parents):
                nodes[node_id] = node._replace(state="OPEN")
                changed = True


def step(state: Model, action: Action) -> tuple[Model, Result]:
    if action.kind not in TRANSITION_TABLE:
        return state, Result(False, "unknown-action")
    return globals()[f"_{action.kind}"](state, action)


def _claim(state: Model, action: Action) -> tuple[Model, Result]:
    if action.node not in state.nodes or not action.worker:
        return state, Result(False, "unknown-target")
    node = state.nodes[action.node]
    live = [c for c in state.claims.values() if c.status == "LIVE" and c.expires_at > state.clock]
    if node.state != "OPEN" or any(c.node == action.node or c.worker == action.worker for c in live):
        return state, Result(False, "not-claimable")
    token = f"t{state.next_token}"
    pv = tuple((p, state.nodes[p].version) for p in _parents(state, action.node))
    claim = Claim(token, action.node, action.worker, node.version, pv, node.work_root,
                  state.clock + state.lease_ticks, "LIVE")
    claims = dict(state.claims); claims[token] = claim
    nodes = dict(state.nodes); nodes[action.node] = node._replace(state="CLAIMED")
    new = state._replace(nodes=nodes, claims=claims, next_token=state.next_token + 1,
                         events=state.events + ("claim",))
    return new, Result(True, "claimed", token)


def _publish(state: Model, action: Action) -> tuple[Model, Result]:
    claim = state.claims.get(action.token or "")
    if claim is None:
        return state, Result(False, "unknown-token")
    if claim.status == "ACCEPTED":
        current = state.nodes[claim.node].version == claim.node_version and state.nodes[claim.node].state == "VERIFIED"
        return state, Result(True, "current-replay" if current else "superseded-replay", claim.token)
    if claim.status != "LIVE":
        return state, Result(False, claim.status.lower())
    if claim.expires_at <= state.clock:
        return state, Result(False, "expired")
    node = state.nodes[claim.node]
    current_pv = tuple((p, state.nodes[p].version) for p in _parents(state, claim.node))
    if node.version != claim.node_version or node.work_root != claim.work_root or current_pv != claim.parent_versions:
        return state, Result(False, "stale")
    if any(state.nodes[p].state != "VERIFIED" for p, _ in claim.parent_versions):
        return state, Result(False, "stale-parent")
    if action.receipt in (None, "invalid"):
        return state, Result(False, "invalid-receipt")
    claims = dict(state.claims); claims[claim.token] = claim._replace(status="ACCEPTED")
    nodes = dict(state.nodes)
    nodes[claim.node] = node._replace(state="VERIFIED", receipt=action.receipt,
                                      accepted_parent_versions=claim.parent_versions)
    _refresh(nodes, state.edges)
    pub = Publication(claim.token, claim.node, claim.node_version, claim.parent_versions,
                      claim.work_root, _digest(action.receipt), len(state.publications) + 1)
    new = state._replace(nodes=nodes, claims=claims, publications=state.publications + (pub,),
                         events=state.events + ("publish",))
    return new, Result(True, "accepted", claim.token)


def _tick(state: Model, action: Action) -> tuple[Model, Result]:
    clock = state.clock + 1
    claims, nodes = dict(state.claims), dict(state.nodes)
    expired = False
    for token, claim in tuple(claims.items()):
        if claim.status == "LIVE" and claim.expires_at <= clock:
            claims[token] = claim._replace(status="EXPIRED")
            node = nodes[claim.node]
            if node.version == claim.node_version and node.state == "CLAIMED":
                nodes[claim.node] = node._replace(state="OPEN")
            expired = True
    return state._replace(clock=clock, claims=claims, nodes=nodes,
                          events=state.events + (("expire",) if expired else ("tick",))), Result(True, "ticked")


def _update_root(state: Model, action: Action) -> tuple[Model, Result]:
    nodes, claims = dict(state.nodes), dict(state.claims)
    root = nodes["R"]
    root_version = root.version + 1
    nodes["R"] = root._replace(version=root_version,
                                receipt=action.receipt or f"root:{root_version}")
    descendants = _descendants(state, "R")
    for node_id in descendants:
        node = nodes[node_id]
        nodes[node_id] = node._replace(state="BLOCKED", version=node.version + 1, receipt=None,
                                       accepted_parent_versions=())
    for token, claim in tuple(claims.items()):
        if claim.status == "LIVE" and claim.node in descendants:
            claims[token] = claim._replace(status="CANCELLED")
    _refresh(nodes, state.edges)
    return state._replace(nodes=nodes, claims=claims,
                          events=state.events + ("root-update",)), Result(True, "root-updated")


def project(state: Model) -> tuple:
    """Canonical observable state; excludes clock-independent token generator details."""
    return (
        tuple((key, *state.nodes[key]) for key in sorted(state.nodes)),
        state.edges,
        tuple((key, *state.claims[key]) for key in sorted(state.claims)),
        state.publications,
        state.clock,
        state.events,
    )


def invariant_violations(state: Model) -> tuple[str, ...]:
    """Checks are separate from transition handlers by design."""
    violations: list[str] = []
    pubs = {(p.node, p.node_version): p for p in state.publications}
    if len(pubs) != len(state.publications):
        violations.append("unique-acceptance")
    for node_id, node in state.nodes.items():
        if node.state == "VERIFIED" and node_id != "R":
            pub = pubs.get((node_id, node.version))
            if pub is None or pub.receipt_digest != _digest(node.receipt or "") or pub.work_root != node.work_root:
                violations.append(f"receipt-entitlement:{node_id}")
                continue
            if pub.parent_versions != node.accepted_parent_versions:
                violations.append(f"version-entitlement:{node_id}")
            for parent, version in pub.parent_versions:
                if state.nodes[parent].state != "VERIFIED" or state.nodes[parent].version != version:
                    violations.append(f"dependency-closure:{node_id}")
    live = [c for c in state.claims.values() if c.status == "LIVE" and c.expires_at > state.clock]
    if len({(c.node, c.node_version) for c in live}) != len(live):
        violations.append("node-claim-exclusivity")
    if len({c.worker for c in live}) != len(live):
        violations.append("worker-claim-exclusivity")
    return tuple(violations)
