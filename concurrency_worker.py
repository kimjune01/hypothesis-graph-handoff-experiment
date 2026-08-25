"""Minimal worker CLI: atomically claim, execute, and publish node-local work."""

import argparse
import json
import time

from concurrency_scheduler import Scheduler, StalePublication
from concurrency_work import discover


def run(db, worker, once=False, poll_seconds=0.05):
    scheduler = Scheduler(db)
    completed = []
    scheduler.register(worker)
    while True:
        claim = scheduler.claim(worker)
        if not claim:
            if once or scheduler.run_state() in ("COMPLETE", "TERMINAL"):
                break
            time.sleep(poll_seconds)
            continue
        def progress(units):
            scheduler.progress(claim["claim_token"], units)
        receipt = discover(claim["work"], progress)
        try:
            completed.append(scheduler.publish(claim["claim_token"], receipt))
        except StalePublication:
            pass
        if once: break
    return completed


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("db"); parser.add_argument("--worker", required=True); parser.add_argument("--once", action="store_true")
    args = parser.parse_args()
    print(json.dumps(run(args.db, args.worker, args.once), sort_keys=True))
