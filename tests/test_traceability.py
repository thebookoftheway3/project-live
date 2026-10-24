"""ADR 0002 referential checks of existing Markdown, not an assurance scoring system."""

import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class TraceabilityTests(unittest.TestCase):
    def test_direct_ci_tool_pins_match_resolved_lock(self):
        def pins(path):
            return {
                name.lower().replace("_", "-").replace(".", "-"): version
                for name, version in re.findall(
                    r"^([\w.-]+)==([^\s\\]+)", path.read_text(), re.MULTILINE
                )
            }

        inputs = pins(ROOT / "requirements/ci.in")
        locked = pins(ROOT / "requirements/ci.txt")
        self.assertTrue(inputs)
        self.assertTrue(inputs.items() <= locked.items(), "regenerate CI dependency lock")

    def test_claims_have_hazards_safeguards_plans_and_resolvable_evidence(self):
        matrix = (ROOT / "docs/assurance/CLAIMS_MATRIX.md").read_text()
        claims = re.findall(r"^\| \*\*C-(\d{2}):\*\*.*$", matrix, re.MULTILINE)
        rows = re.findall(r"^\| \*\*C-\d{2}:\*\*.*$", matrix, re.MULTILINE)
        evidence_rows = re.findall(r"^\| \*\*E\d{2}\*\*.*$", matrix, re.MULTILINE)
        evidence_ids = [re.search(r"E\d{2}", row)[0] for row in evidence_rows]
        self.assertEqual(len(claims), len(set(claims)), "duplicate claim ID")
        self.assertEqual(len(evidence_ids), len(set(evidence_ids)), "duplicate evidence ID")
        self.assertTrue(
            set(f"{n:02}" for n in range(1, 10)) <= set(claims),
            "do not silently remove the adopted claims",
        )
        ledger = (ROOT / "docs/requirements/LEDGER.md").read_text()
        requirements = set(re.findall(r"^\| (R\d{2}) \|", ledger, re.MULTILINE))
        evidence = dict(zip(evidence_ids, evidence_rows))
        for number, row in zip(claims, rows):
            with self.subTest(claim=f"C-{number}"):
                self.assertEqual(len(row.split("|")), 7, "expected five populated columns")
                self.assertTrue(all(cell.strip() for cell in row.split("|")[1:-1]))
                for prefix in ("H", "S", "V"):
                    self.assertIn(f"**{prefix}-{number}:**", row)
                self.assertRegex(row, r"R\d{2}", "claim must name its source requirement")
                self.assertFalse(set(re.findall(r"R\d{2}", row)) - requirements)
                for evidence_id in re.findall(r"\bE\d{2}\b", row):
                    self.assertIn(evidence_id, evidence, "undefined evidence")
                    self.assertIn(f"C-{number}", evidence[evidence_id], "missing reverse link")
        for row in evidence_rows:
            self.assertFalse(set(re.findall(r"C-(\d{2})", row)) - set(claims))
        self.assertIn("No independent human reviewer", matrix)

    def test_accepted_adr_register_matches_decision_files(self):
        register = (ROOT / "docs/decisions/README.md").read_text()
        entries = re.findall(r"\| \[(\d{4})\]\(([^)]+)\) \| ([^|]+) \|", register)
        self.assertTrue(entries)
        self.assertEqual(len(entries), len({number for number, _, _ in entries}))
        for number, filename, status in entries:
            with self.subTest(adr=number):
                self.assertTrue(filename.startswith(number + "-"))
                text = (ROOT / "docs/decisions" / filename).read_text()
                state = status.strip().split()[0]
                self.assertRegex(text, rf"- Status: (?:\*\*)?{state}\b")
