"""Command-line entry point for synthetic replay."""
import argparse
import json
from .replay import replay

def main() -> None:
    parser = argparse.ArgumentParser(description="Project LIVE shadow-mode synthetic replay")
    sub = parser.add_subparsers(dest="operation", required=True)
    r = sub.add_parser("replay", help="Replay synthetic events from JSONL")
    r.add_argument("path")
    args = parser.parse_args()
    for item in replay(args.path):
        print(json.dumps(item, sort_keys=True))

if __name__ == "__main__":
    main()
