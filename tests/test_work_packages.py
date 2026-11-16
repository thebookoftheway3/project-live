"""Include dependency-free WP experiments in the existing root test command."""

import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def load_tests(loader, tests, pattern):
    source = ROOT / "wp2-bayesian-voi-engine/src"
    sys.path.insert(0, str(source))
    suite = unittest.TestSuite()
    suite.addTests(unittest.TestLoader().discover(str(ROOT / "wp2-bayesian-voi-engine/tests")))
    for directory in ("topdown-quantifier", "topological-room-graph"):
        sys.path.insert(0, str(ROOT / "wp3-edge-vision-pipelines" / directory))
    suite.addTests(unittest.TestLoader().discover(str(ROOT / "wp3-edge-vision-pipelines/tests")))
    return suite
