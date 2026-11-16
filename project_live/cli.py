"""Command-line entry point for synthetic replay."""

import argparse
import json

from .history import run_history_fixture
from .loop_observations import replay_file
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
    g = sub.add_parser(
        "loop-replay", help="Analyse the Loop research v1 observation interface locally"
    )
    g.add_argument("path")
    g.add_argument("--output", required=True, help="New private report path outside Git")
    g.add_argument("--cutoff", help="Phone-reception cutoff, timezone-aware ISO timestamp")
    mode = g.add_mutually_exclusive_group(required=True)
    mode.add_argument("--synthetic", action="store_true")
    mode.add_argument("--consent-local-health-data", action="store_true")
    args = parser.parse_args()
    if args.operation == "loop-replay":
        try:
            replay_file(
                args.path,
                args.output,
                consent=args.consent_local_health_data,
                synthetic_only=args.synthetic,
                cutoff=args.cutoff,
            )
        except ValueError as error:
            parser.exit(2, str(error) + "\n")
        except OSError:
            parser.exit(
                2,
                "Local input/output failed; choose a readable file and a new private output path.\n",
            )
        print("Research report written locally; no observations transmitted.")
        return
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
