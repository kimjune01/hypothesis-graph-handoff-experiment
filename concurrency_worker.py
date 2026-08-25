"""Minimal worker CLI: atomically claim, execute, and publish node-local work."""

import argparse
import json

from concurrency_scheduler import Scheduler, StalePublication
from concurrency_work import discover


def run(db, worker, once=False):
    scheduler = Scheduler(db)
    completed = []
    while claim := scheduler.claim(worker):
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
