"""Export immutable scheduler state and exact descriptive grades."""

from __future__ import annotations

import json
import sqlite3
import sys
from pathlib import Path

from concurrency_scheduler import Scheduler
from concurrency_work import check_receipt


def export(run_dir: Path) -> None:
    scheduler = Scheduler(run_dir / "state.db")
    events = scheduler.events()
    with sqlite3.connect(run_dir / "state.db") as db:
        db.row_factory = sqlite3.Row
        nodes = {row["id"]: dict(row) for row in db.execute("SELECT * FROM nodes")}
        claims = [dict(row) for row in db.execute("SELECT * FROM claims ORDER BY rowid")]
        packets = [dict(row) for row in db.execute("SELECT * FROM packets ORDER BY rowid")]

    bad_receipts = []
    for node_id, node in nodes.items():
        if node["state"] == "VERIFIED" and node_id != "R0":
            if not check_receipt(json.loads(node["work"]), json.loads(node["receipt"])):
                bad_receipts.append(node_id)
    claim_events = [event for event in events if event["kind"] == "claim"]
    accept_events = [event for event in events if event["kind"] == "accept"]
    first_claim = claim_events[0]["at"] if claim_events else None
    final_accept = next(
        (event["at"] for event in reversed(accept_events) if event["node_id"] == "F"),
        None,
    )
    intervals = {}
    for node_id in ("A", "B", "C"):
        claimed = next(
            (event["at"] for event in claim_events if event["node_id"] == node_id), None
        )
        accepted = next(
            (event["at"] for event in accept_events if event["node_id"] == node_id), None
        )
        intervals[node_id] = [claimed, accepted]
    overlap_start = max(value[0] for value in intervals.values() if value[0] is not None)
    overlap_end = min(value[1] for value in intervals.values() if value[1] is not None)

    grade = {
        "final_verified": nodes["F"]["state"] == "VERIFIED",
        "bad_receipts": bad_receipts,
        "claim_order": [event["node_id"] for event in claim_events],
        "gate_order_correct": [event["node_id"] for event in claim_events[:5]]
        == ["GD", "GA", "GB", "GC", "GE"],
        "d_killed_and_unclaimed": nodes["D"]["state"] == "KILLED"
        and "D" not in [event["node_id"] for event in claim_events],
        "abc_intervals": intervals,
        "abc_all_overlap": overlap_start < overlap_end,
        "elapsed_first_claim_to_f_seconds": (
            final_accept - first_claim if first_claim and final_accept else None
        ),
        "invalidated": [
            event["node_id"] for event in events if event["kind"] == "invalidate"
        ],
        "cancelled_claims": [
            claim["node_id"] for claim in claims if claim["status"] == "CANCELLED"
        ],
        "duplicate_node_version_accepts": sorted(
            key
            for key in {
                f'{claim["node_id"]}@{json.loads(claim["result"])["version"]}'
                for claim in claims
                if claim["status"] == "ACCEPTED"
            }
            if sum(
                claim["status"] == "ACCEPTED"
                and f'{claim["node_id"]}@{json.loads(claim["result"])["version"]}'
                == key
                for claim in claims
            )
            > 1
        ),
    }
    (run_dir / "events.json").write_text(json.dumps(events, indent=2) + "\n")
    (run_dir / "nodes.json").write_text(json.dumps(nodes, indent=2) + "\n")
    (run_dir / "claims.json").write_text(json.dumps(claims, indent=2) + "\n")
    (run_dir / "packets.json").write_text(json.dumps(packets, indent=2) + "\n")
    (run_dir / "grade.json").write_text(json.dumps(grade, indent=2) + "\n")


if __name__ == "__main__":
    export(Path(sys.argv[1]))
