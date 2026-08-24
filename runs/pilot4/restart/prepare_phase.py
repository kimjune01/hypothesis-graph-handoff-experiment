from __future__ import annotations

import argparse
import json
from pathlib import Path

from search_prep import build_n8_execution_plan, write_audit_receipts


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--mode",
        choices=("audit", "n8-plan"),
        required=True,
        help="Run the bounded audit or write the guarded n=8 execution plan.",
    )
    parser.add_argument(
        "--output",
        default=None,
        help="Optional output path. Defaults to audit_receipt.json or n8_plan.json.",
    )
    args = parser.parse_args()

    if args.mode == "audit":
        output = args.output or "audit_receipt.json"
        summary = write_audit_receipts(output_path=output)
    else:
        output = args.output or "n8_plan.json"
        summary = build_n8_execution_plan()
        Path(output).write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n")

    print(json.dumps(summary, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
