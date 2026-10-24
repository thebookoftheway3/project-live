"""Command-line entry point for synthetic replay."""

import argparse
import json

from .history import run_history_fixture
from .pipeline import run_fixture
from .replay import replay


def main() -> None:
    parser = argparse.ArgumentParser(description="Project LIVE shadow-mode synthetic replay")
    sub = parser.add_subparsers(dest="operation", required=True)
    r = sub.add_parser("replay", help="Replay synthetic events from JSONL")
    r.add_argument("path")
    b = sub.add_parser("beverage", help="Run the synthetic LIVE-022 beverage increment")
    b.add_argument("path")
    b.add_argument("--cutoff", help="Online availability cutoff (timezone-aware ISO timestamp)")
    h = sub.add_parser("history", help="Replay bounded synthetic historical investigation")
    h.add_argument("path")
    h.add_argument("--cutoff", help="Knowledge cutoff (timezone-aware ISO timestamp)")
    args = parser.parse_args()
    if args.operation == "history":
        print(
            json.dumps(
                run_history_fixture(args.path, cutoff=args.cutoff), sort_keys=True, allow_nan=False
            )
        )
        return
    if args.operation == "beverage":
        print(
            json.dumps(run_fixture(args.path, cutoff=args.cutoff), sort_keys=True, allow_nan=False)
        )
        return
    for item in replay(args.path):
        print(json.dumps(item, sort_keys=True))


if __name__ == "__main__":
    main()
