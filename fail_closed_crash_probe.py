"""Subprocess entry point for exact pre-commit crash probes."""

from __future__ import annotations

import json
import os
import sys

from concurrency_scheduler import Scheduler


def main() -> None:
    path, operation, *args = sys.argv[1:]
    expected = "publication_after_node_write" if operation == "publish" else "invalidation_after_first_node_write"
    exit_code = 77 if operation == "publish" else 78

    def crash(name: str) -> None:
        if name == expected:
            os._exit(exit_code)

    scheduler = Scheduler(path, failpoint=crash)
    if operation == "publish":
        scheduler.publish(args[0], json.loads(args[1]))
    elif operation == "update-root":
        scheduler.update_root(args[0], json.loads(args[1]))
    else:
        raise ValueError(operation)


if __name__ == "__main__":
    main()
