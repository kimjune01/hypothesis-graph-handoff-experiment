"""Complete, depth-bounded exploration of the tiny diamond reference model."""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum

from fail_closed_model import Action, Model, initial_diamond, invariant_violations, project, step


class ExplorationStatus(Enum):
    COMPLETE = "complete"
    INCONCLUSIVE = "inconclusive"
    FAILED = "failed"


@dataclass(frozen=True)
class ExplorationReport:
    status: ExplorationStatus
    states: int
    transitions: int
    equivalent_pruned: int
    max_depth_reached: int
    cap_hit: bool
    violations: tuple[str, ...]


def _actions(state: Model) -> tuple[Action, ...]:
    actions: list[Action] = [Action("tick"), Action("update_root")]
    actions += [Action("claim", worker=w, node=n) for w in ("w1", "w2") for n in ("A", "B", "J")]
    # Existing tokens only: unknown-token rejection is covered by deterministic tests and
    # adds no reachable state to exhaustive exploration.
    for token in sorted(state.claims):
        actions.extend((Action("publish", token=token, receipt="valid"),
                        Action("publish", token=token, receipt="invalid")))
    return tuple(actions)


def explore_diamond(max_depth: int, state_cap: int) -> ExplorationReport:
    initial = initial_diamond()
    seen = {project(initial)}
    frontier = [(initial, 0)]
    transitions = pruned = deepest = 0
    violations: list[str] = []
    while frontier:
        state, depth = frontier.pop(0)
        deepest = max(deepest, depth)
        found = invariant_violations(state)
        if found:
            violations.extend(found)
            return ExplorationReport(ExplorationStatus.FAILED, len(seen), transitions, pruned,
                                     deepest, False, tuple(sorted(set(violations))))
        if depth == max_depth:
            continue
        for action in _actions(state):
            successor, _ = step(state, action)
            transitions += 1
            key = project(successor)
            if key in seen:
                pruned += 1
                continue
            if len(seen) >= state_cap:
                return ExplorationReport(ExplorationStatus.INCONCLUSIVE, len(seen), transitions,
                                         pruned, deepest, True, ())
            seen.add(key)
            frontier.append((successor, depth + 1))
    return ExplorationReport(ExplorationStatus.COMPLETE, len(seen), transitions, pruned,
                             deepest, False, ())

