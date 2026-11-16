"""G6 bridge: synthetic protocol, privacy, temporal and non-actuation evidence."""

import copy
import json
import os
import stat
import subprocess
import sys
import tempfile
import unittest
from dataclasses import FrozenInstanceError, replace
from fractions import Fraction
from pathlib import Path
from unittest.mock import patch

from project_live.loop_observations import (
    LoopGlucose,
    analyse_observations,
    decode_observations,
    replay_file,
)
from project_live.sensing import instant

ROOT = Path(__file__).resolve().parents[1]
FIXTURE = ROOT / "data/synthetic_loop_g6_v1.jsonl"
NOW = instant("2026-01-01T11:00:00Z")


def records():
    return [json.loads(line) for line in FIXTURE.read_text().splitlines()]


def encode(rows):
    return "\n".join(json.dumps(r) for r in rows).encode()


class LoopObservationTests(unittest.TestCase):
    def test_schema_preserves_source_times_quality_and_immutable_values(self):
        row = records()[0]
        item = LoopGlucose.parse(row)
        row["glucose"] = 999
        self.assertEqual(item.value, 100)
        self.assertEqual((item.received_at - item.event_at).total_seconds(), 3)
        with self.assertRaises(FrozenInstanceError):
            item.value = 200
        result = analyse_observations(
            decode_observations(FIXTURE.read_bytes()), as_of=NOW, generated_at=NOW
        )
        self.assertEqual(len(result["history"]), 5)
        self.assertEqual(len(result["snapshots"]), 3)
        self.assertFalse(result["may_actuate_insulin"])
        reasons = {r["reason"] for r in result["quality"]}
        self.assertEqual(
            reasons, {"gap", "delayed_sample_history_only", "quality_excluded_from_model"}
        )

    def test_independent_gaussian_reference_and_prediction_precedes_observation(self):
        items = decode_observations(FIXTURE.read_bytes())[:2]
        result = analyse_observations(items, as_of=NOW, generated_at=NOW)
        prior_variance = Fraction(25) + Fraction(4) * 5
        gain = prior_variance / (prior_variance + 25)
        self.assertAlmostEqual(result["snapshots"][1]["mean_mg_dl"], float(100 + gain * 10))
        self.assertAlmostEqual(
            result["snapshots"][1]["variance_mg_dl2"], float((1 - gain) * prior_variance)
        )
        prediction = result["comparisons"][0]
        self.assertEqual(prediction["mean_mg_dl"], 100)
        self.assertEqual(prediction["error_mg_dl"], 10)
        self.assertNotEqual(prediction["input_snapshot_id"], result["snapshots"][1]["snapshot_id"])
        self.assertLess(instant(prediction["issued_at"]), instant(prediction["target_at"]))

    def test_asof_excludes_late_arrivals_without_rewriting_earlier_snapshots(self):
        items = decode_observations(FIXTURE.read_bytes())
        early = analyse_observations(items, as_of=items[1].received_at, generated_at=NOW)
        full = analyse_observations(items, as_of=NOW, generated_at=NOW)
        self.assertEqual(early["snapshots"], full["snapshots"][:2])
        self.assertEqual(early["unavailable_records"], 3)
        mutated = list(items)
        mutated[-1] = replace(mutated[-1], value=600)
        self.assertEqual(
            early,
            analyse_observations(tuple(mutated), as_of=items[1].received_at, generated_at=NOW),
        )
        self.assertEqual(
            full, analyse_observations(tuple(reversed(items)), as_of=NOW, generated_at=NOW)
        )

    def test_backfill_is_not_scored_as_if_received_before_measurement(self):
        items = decode_observations(FIXTURE.read_bytes())[:2]
        batch = tuple(replace(i, received_at=NOW) for i in items)
        result = analyse_observations(batch, as_of=NOW, generated_at=NOW)
        self.assertEqual(result["comparisons"], [])
        self.assertEqual(len(result["snapshots"]), 2)
        self.assertEqual(result["snapshots"][0]["evidence_cutoff"], NOW.isoformat())

    def test_duplicates_idempotent_conflicts_rejected(self):
        rows = records()
        expected = decode_observations(encode(rows))
        self.assertEqual(expected, decode_observations(encode(rows + rows)))
        later = copy.deepcopy(rows[0])
        later["received_at"] = "2026-01-01T10:00:05Z"
        self.assertEqual(expected, decode_observations(encode(rows + [later])))
        earlier = copy.deepcopy(rows[0])
        earlier["received_at"] = "2026-01-01T10:00:01Z"
        self.assertEqual(
            decode_observations(encode([later, earlier]))[0].received_at,
            instant(earlier["received_at"]),
        )
        later["glucose"] = 120
        with self.assertRaisesRegex(ValueError, "conflicting observation ID"):
            decode_observations(encode(rows + [later]))

    def test_same_time_conflicts_and_different_id_duplicates_do_not_add_certainty(self):
        items = decode_observations(FIXTURE.read_bytes())[:1]
        duplicate = replace(items[0], id="f" * 64)
        result = analyse_observations(items + (duplicate,), as_of=NOW, generated_at=NOW)
        self.assertEqual(len(result["snapshots"]), 1)
        self.assertEqual(result["quality"][0]["reason"], "duplicate_event")
        conflict = replace(duplicate, value=200)
        result = analyse_observations(items + (conflict,), as_of=NOW, generated_at=NOW)
        self.assertFalse(result["snapshots"])
        later = replace(conflict, received_at=instant("2026-01-01T10:01:00Z"))
        result = analyse_observations(items + (later,), as_of=NOW, generated_at=NOW)
        self.assertEqual(len(result["snapshots"]), 1)
        self.assertEqual(result["quality"][0]["reason"], "later_conflicting_revision")

    def test_quality_markers_are_not_treated_as_exact_measurements(self):
        item = decode_observations(FIXTURE.read_bytes())[0]
        for variant in (
            replace(item, display_only=True),
            replace(item, user_entered=True),
            replace(item, condition="belowRange"),
        ):
            result = analyse_observations((variant,), as_of=NOW, generated_at=NOW)
            self.assertFalse(result["snapshots"])
            self.assertEqual(len(result["history"]), 1)
            self.assertIsNone(result["latest_usable_age_minutes"])

    def test_bad_schema_authority_units_and_numeric_values_fail_closed(self):
        for field, value in (
            ("schema", "pump-command"),
            ("schema_version", True),
            ("schema_version", 2),
            ("id", "transmitter-serial"),
            ("source", "arbitrary-device"),
            ("source_version", "unknown"),
            ("unit", "mmol/L"),
            ("shadow_only", False),
            ("may_actuate_insulin", True),
            ("glucose", True),
            ("glucose", -1),
            ("glucose", float("nan")),
            ("glucose", float("inf")),
            ("event_at", "private-invalid-time"),
            ("event_at", "2026-01-02T12:00:00Z"),
        ):
            with self.subTest(field=field, value=value):
                row = records()[0]
                row[field] = value
                with self.assertRaisesRegex(ValueError, "raw content withheld"):
                    decode_observations(encode([row]))
        row = records()[0]
        row["command"] = "bolus"
        with self.assertRaises(ValueError):
            LoopGlucose.parse(row)

    def test_missing_quality_and_malformed_input_are_rejected_privately(self):
        for quality in (
            {},
            {"is_display_only": True},
            {
                "is_display_only": "false",
                "was_user_entered": False,
                "condition": None,
                "trend": None,
            },
        ):
            row = records()[0]
            row["quality"] = quality
            with self.assertRaises(ValueError):
                decode_observations(encode([row]))
        for raw in (b"private secret\n", b"\xff", b"{}\n"):
            with self.assertRaises(ValueError) as error:
                decode_observations(raw)
            self.assertNotIn("private secret", str(error.exception))

    def test_real_data_requires_consent_and_is_refused_in_ci(self):
        rows = records()
        for row in rows:
            row["synthetic"] = False
        with patch.dict(os.environ, {}, clear=True):
            with self.assertRaisesRegex(ValueError, "local consent"):
                decode_observations(encode(rows))
            self.assertEqual(len(decode_observations(encode(rows), consent=True)), 5)
        with patch.dict(os.environ, {"GITHUB_ACTIONS": "true"}):
            with self.assertRaisesRegex(ValueError, "forbidden"):
                decode_observations(encode(rows), consent=True)
        rows[0]["synthetic"] = True
        with patch.dict(os.environ, {}, clear=True), self.assertRaisesRegex(ValueError, "mix"):
            decode_observations(encode(rows), consent=True)

    def test_file_consent_precedes_reads_and_output_is_private_exclusive(self):
        with patch.object(Path, "read_bytes", side_effect=AssertionError("unauthorized read")):
            with self.assertRaisesRegex(ValueError, "consent"):
                replay_file("missing", "missing-output", consent=False)
        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory).resolve() / "report.json"
            original = FIXTURE.read_bytes()
            replay_file(str(FIXTURE), str(output), consent=False, synthetic_only=True)
            self.assertEqual(stat.S_IMODE(output.stat().st_mode), 0o600)
            self.assertEqual(original, FIXTURE.read_bytes())
            result = json.loads(output.read_text())
            self.assertEqual(len(result["history"]), 5)
            with self.assertRaises(FileExistsError):
                replay_file(str(FIXTURE), str(output), consent=False, synthetic_only=True)

    def test_git_and_symlink_destinations_are_rejected(self):
        with self.assertRaisesRegex(ValueError, "outside Git"):
            replay_file(
                str(FIXTURE), str(ROOT / "private-report.json"), consent=False, synthetic_only=True
            )
        with tempfile.TemporaryDirectory() as directory:
            base = Path(directory).resolve()
            (base / "link").symlink_to(ROOT, target_is_directory=True)
            with self.assertRaisesRegex(ValueError, "symlink"):
                replay_file(
                    str(FIXTURE),
                    str(base / "link/private-report.json"),
                    consent=False,
                    synthetic_only=True,
                )

    def test_cloud_paths_and_nonregular_input_are_refused(self):
        with tempfile.TemporaryDirectory() as directory:
            base = Path(directory).resolve()
            for source, target in (
                (base / "CloudStorage/input.jsonl", base / "report.json"),
                (FIXTURE, base / "Mobile Documents/report.json"),
            ):
                with self.assertRaisesRegex(ValueError, "cloud-sync"):
                    replay_file(str(source), str(target), consent=False, synthetic_only=True)
            fifo = base / "input.fifo"
            os.mkfifo(fifo)
            process = subprocess.run(
                [
                    sys.executable,
                    "-m",
                    "project_live.cli",
                    "loop-replay",
                    str(fifo),
                    "--synthetic",
                    "--output",
                    str(base / "report.json"),
                ],
                cwd=ROOT,
                capture_output=True,
                text=True,
                timeout=2,
            )
            self.assertEqual(process.returncode, 2)
            self.assertIn("regular local file", process.stderr)

    def test_cli_synthetic_round_trip_no_observations_in_stdout(self):
        with tempfile.TemporaryDirectory() as directory:
            process = subprocess.run(
                [
                    sys.executable,
                    "-m",
                    "project_live.cli",
                    "loop-replay",
                    str(FIXTURE),
                    "--synthetic",
                    "--output",
                    str(Path(directory).resolve() / "report.json"),
                ],
                cwd=ROOT,
                capture_output=True,
                text=True,
                check=True,
            )
            self.assertNotIn("mg_dl", process.stdout)
            self.assertIn("written locally", process.stdout)
