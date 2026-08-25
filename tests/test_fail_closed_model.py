from fail_closed_explorer import ExplorationStatus, explore_diamond
from fail_closed_model import Action, initial_diamond, invariant_violations, project, step


def test_claim_publish_and_idempotent_replay():
    state = initial_diamond()
    state, claim = step(state, Action("claim", worker="w1", node="A"))
    assert claim.accepted and claim.token == "t1"

    state, published = step(state, Action("publish", token="t1", receipt="valid"))
    assert published.accepted
    assert state.nodes["A"].state == "VERIFIED"
    assert len(state.publications) == 1

    replayed, replay = step(state, Action("publish", token="t1", receipt="valid"))
    assert replay.accepted and replay.disposition == "current-replay"
    assert project(replayed) == project(state)
    assert not invariant_violations(replayed)


def test_root_update_cancels_claims_and_makes_replay_superseded():
    state = initial_diamond()
    old_work_roots = {node: record.work_root for node, record in state.nodes.items()}
    state, claim = step(state, Action("claim", worker="w1", node="A"))
    state, _ = step(state, Action("publish", token=claim.token, receipt="valid"))
    state, _ = step(state, Action("update_root"))

    assert state.nodes["A"].state == "OPEN"
    assert {node: record.work_root for node, record in state.nodes.items()} == old_work_roots
    replayed, replay = step(state, Action("publish", token=claim.token, receipt="valid"))
    assert replay.accepted and replay.disposition == "superseded-replay"
    assert replayed.nodes["A"].state == "OPEN"
    assert not invariant_violations(replayed)


def test_expired_and_invalid_publications_fail_closed():
    state = initial_diamond(lease_ticks=1)
    state, claim = step(state, Action("claim", worker="w1", node="A"))
    state, _ = step(state, Action("tick"))
    after, result = step(state, Action("publish", token=claim.token, receipt="valid"))
    assert not result.accepted and result.disposition == "expired"
    assert after.nodes["A"].state == "OPEN"

    after, claim2 = step(after, Action("claim", worker="w1", node="A"))
    rejected, result = step(after, Action("publish", token=claim2.token, receipt="invalid"))
    assert not result.accepted and result.disposition == "invalid-receipt"
    assert rejected.nodes["A"].state == "CLAIMED"
    assert not invariant_violations(rejected)


def test_projection_omits_incidental_next_token_counter():
    state = initial_diamond()
    altered = state._replace(next_token=99)
    assert project(state) == project(altered)


def test_bounded_exploration_completes_and_checks_every_state():
    report = explore_diamond(max_depth=6, state_cap=20_000)
    assert report.status is ExplorationStatus.COMPLETE
    assert report.states > 1
    assert report.transitions > report.states
    assert report.max_depth_reached == 6
    assert report.violations == ()


def test_state_cap_is_inconclusive_not_pass():
    report = explore_diamond(max_depth=8, state_cap=5)
    assert report.status is ExplorationStatus.INCONCLUSIVE
    assert report.cap_hit
