#!/bin/sh
# Offline one-command baseline: requires Python >=3.11 and a C++17 compiler.
set -eu
cd "$(dirname "$0")/.."
"${PYTHON:-python3}" -c 'import sys; assert sys.version_info >= (3, 11), "Python 3.11+ required"'
"${PYTHON:-python3}" -m unittest discover -s tests -v
"${PYTHON:-python3}" -m project_live.cli replay data/synthetic_example.jsonl
sh tools/check_mmu.sh
