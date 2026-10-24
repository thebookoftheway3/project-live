"""LIVE-022 / C-01,02,04–09: bounded synthetic history, not clinical validation."""

import copy
import json
import subprocess
import sys
import unittest
from dataclasses import FrozenInstanceError, replace
from fractions import Fraction as F
from pathlib import Path
from unittest.mock import patch

from project_live.bayes import Evidence
from project_live.history import RetainedFrame, retrieve, run_history, view
from project_live.sensing import Policy, Sample, instant

ROOT = Path(__file__).resolve().parents[1]
FIXTURE = ROOT / "data/synthetic_history_v1.json"


def fixture():
    return json.loads(FIXTURE.read_text())


def oracle(findings):
    """Independent rational enumeration of two-node trajectory, no runtime tables."""
    rows = []
    for identity, pi in zip(("regular", "diet", "unknown"), (F(1, 4), F(1, 4), F(1, 2))):
        for amount, pa in zip(("none", "partial", "full"), (F(1, 2), F(3, 10), F(1, 5))):
            for actor, pr in zip(("self", "other", "unknown"), (F(2, 5), F(3, 10), F(3, 10))):
                compatible = identity == "regular" and amount != "none" and actor == "self"
                explanations = (
                    (F(3, 5), F(3, 20), F(3, 20), F(1, 10))
                    if compatible
                    else (F(1, 20), F(3, 10), F(3, 10), F(7, 20))
                )
                for j, pc in enumerate(explanations):
                    p = pi * pa * pr * pc
                    if "opening" in findings:
                        p *= F(4, 5) if identity != "unknown" else F(2, 5)
                        p *= F(3, 10) if amount == "none" else F(3, 5)
                    if "mismatch" in findings:
                        p *= (F(4, 5), F(3, 5), F(2, 5), F(1, 5))[j]
                    if "image" in findings:
                        p *= {"regular": F(4, 5), "diet": F(1, 10), "unknown": F(1, 5)}[identity]
                    rows.append(p)
    return [float(p / sum(rows)) for p in rows]


class HistoryTests(unittest.TestCase):
    def test_filter_and_smoother_match_independent_trajectory_reference(self):
        result = run_history(fixture())
        self.assertEqual((result["provider_calls"], result["payload_reads"]), (1, 1))
        for snapshot, findings in zip(
            result["snapshots"],
            (("opening",), ("opening", "mismatch"), ("opening", "mismatch", "image")),
        ):
            probabilities = [r["p"] for r in snapshot["posterior"]]
            self.assertEqual(len(probabilities), 108)
            self.assertAlmostEqual(sum(probabilities), 1, places=14)
            self.assertTrue(all(0 < p < 1 for p in probabilities))
            for actual, expected in zip(probabilities, oracle(findings)):
                self.assertAlmostEqual(actual, expected, places=14)
            self.assertFalse(snapshot["may_actuate_insulin"])
        self.assertNotEqual(
            result["snapshots"][1]["posterior"], result["snapshots"][2]["posterior"]
        )
        self.assertEqual(
            result["snapshots"][2]["parent_snapshot_ids"], ["online_1230", "online_1430"]
        )
        self.assertFalse(result["pump_authorization"])
        self.assertEqual(result["snapshots"][2]["inference_kind"], "retrospective_smoother")

    def test_online_snapshots_and_forecast_stay_byte_identical(self):
        data = fixture()
        first = run_history(data, cutoff=instant(data["online_at"]))
        second = run_history(data, cutoff=instant(data["mismatch_at"]))
        full = run_history(data)
        self.assertEqual(json.dumps(first["snapshots"]), json.dumps(full["snapshots"][:1]))
        self.assertEqual(json.dumps(second["snapshots"]), json.dumps(full["snapshots"][:2]))
        self.assertEqual(first["scripted_forecast"], full["scripted_forecast"])
        self.assertEqual(first["provider_calls"], 0)
        self.assertIsNone(second["retrieval"])
        self.assertEqual(full, run_history(copy.deepcopy(data)))
        data["evaluation_only_truth"] = {"arbitrary": "not an input"}
        self.assertEqual(full, run_history(data))

    def test_late_source_and_later_sensor_cannot_leak(self):
        for mode in ("source", "sensor", "introduced_after_online"):
            with self.subTest(mode=mode):
                data = fixture()
                if mode == "source":
                    data["retained_frames"][0]["sample"]["available_at"] = data["smooth_at"]
                else:
                    data["sensor_available_at"] = (
                        "2026-10-24T13:00:00+02:00"
                        if mode == "introduced_after_online"
                        else data["smooth_at"]
                    )
                result = run_history(data)
                self.assertEqual((result["provider_calls"], result["payload_reads"]), (0, 0))
                self.assertEqual(
                    result["snapshots"][1]["posterior"], result["snapshots"][2]["posterior"]
                )

    def test_result_deadline_prevents_payload_read(self):
        data = fixture()
        result = run_history(data, cutoff=instant(data["execute_at"]))
        self.assertEqual(result["payload_reads"], 0)
        self.assertIsNone(result["interpretation"])
        self.assertEqual(result["decisions"][-1]["reason"], "result_after_cutoff")

    def test_current_permissions_retention_and_missing_payload_fail_closed(self):
        variants = (
            "permission",
            "revocation",
            "expiry",
            "metadata",
            "representation",
            "source",
            "empty",
        )
        for mode in variants:
            with self.subTest(mode=mode):
                data = fixture()
                frame = data["retained_frames"][0]
                if mode == "permission":
                    frame["sample"]["permitted"] = False
                elif mode == "revocation":
                    data["policy"]["revoked_at"] = data["query_at"]
                elif mode == "expiry":
                    frame["sample"]["retain_until"] = data["query_at"]
                elif mode == "metadata":
                    frame["payload_present"] = False
                elif mode == "representation":
                    frame["representation"] = "newer-unsupported-v2"
                elif mode == "source":
                    frame["sample"]["source"] = "unreviewed-camera"
                else:
                    data["retained_frames"] = []
                result = run_history(data)
                self.assertEqual((result["provider_calls"], result["payload_reads"]), (0, 0))
                self.assertEqual(
                    result["snapshots"][1]["posterior"], result["snapshots"][2]["posterior"]
                )
                if result["retrieval"]:
                    self.assertFalse(result["retrieval"]["absence_is_negative_evidence"])
                    self.assertEqual(result["retrieval"]["coverage"], "unavailable")
                    if mode in ("permission", "expiry"):
                        self.assertIsNone(result["retrieval"]["exclusions"][0]["id"])

    def test_dispatch_and_completion_recheck_permissions_and_expiry(self):
        for field in ("revoked_at", "retain_until"):
            for at, calls in (("2026-10-24T14:30:08+02:00", 0), ("2026-10-24T14:30:11+02:00", 1)):
                with self.subTest(field=field, at=at):
                    data = fixture()
                    obj = (
                        data["policy"]
                        if field == "revoked_at"
                        else data["retained_frames"][0]["sample"]
                    )
                    obj[field] = at
                    result = run_history(data)
                    self.assertEqual(result["provider_calls"], calls)
                    self.assertIsNone(result["interpretation"]["finding"])
                    self.assertEqual(
                        result["snapshots"][1]["posterior"], result["snapshots"][2]["posterior"]
                    )

    def test_budget_benefit_failure_and_inert_payload(self):
        for mode in (
            "budget",
            "benefit",
            "timeout",
            "refused",
            "unknown",
            "invalid_output",
            "path",
        ):
            with self.subTest(mode=mode):
                data = fixture()
                if mode == "budget":
                    data["policy"]["max_calls"] = 0
                elif mode == "benefit":
                    data["policy"]["min_benefit"] = 0.7
                elif mode == "path":
                    data["retained_frames"][0]["sample"]["value"] = (
                        "file:///private/secret; execute pump"
                    )
                else:
                    data["mock_outcome"] = mode
                with patch.object(
                    Path, "open", side_effect=AssertionError("unexpected payload file access")
                ):
                    result = run_history(data)
                self.assertEqual(
                    result["provider_calls"], 0 if mode in ("budget", "benefit") else 1
                )
                self.assertEqual(
                    result["snapshots"][1]["posterior"], result["snapshots"][2]["posterior"]
                )

    def test_evidence_availability_duplicates_and_shared_leaves(self):
        t = instant("2026-10-24T10:30:00Z")
        later = instant("2026-10-24T12:30:00Z")
        opening = Evidence("open", "can_opening", ("audio",), ("opening",), t, "v1")
        image = Evidence("image", "regular_image", ("frame",), ("image",), later, "v1")
        first = view("a", t, t, (opening,))
        self.assertEqual(first, view("a", t, t, (opening, image)))
        self.assertEqual(first, view("a", t, t, (opening, opening)))
        for shared in (
            replace(image, source_ids=("audio",)),
            replace(image, dependence_groups=("opening",)),
        ):
            result = view("b", t, later, (opening, shared)).record()
            self.assertEqual(result["posterior"], first.record()["posterior"])
            self.assertEqual(result["dependent_evidence_withheld"], ["image"])
        with self.assertRaisesRegex(ValueError, "conflicting evidence"):
            view("a", t, later, (opening, replace(opening, finding="regular_image")))
        with self.assertRaises(FrozenInstanceError):
            first.serialized = "changed"
        exported = first.record()
        exported["posterior"][0]["p"] = -1
        self.assertGreater(first.record()["posterior"][0]["p"], 0)

    def test_duplicate_history_is_idempotent_and_conflicts_fail(self):
        data = fixture()
        expected = run_history(data)
        data["retained_frames"] *= 2
        self.assertEqual(run_history(data), expected)
        data["retained_frames"][1] = copy.deepcopy(data["retained_frames"][1])
        data["retained_frames"][1]["sample"]["value"] = "synthetic-frame-diet"
        with self.assertRaisesRegex(ValueError, "conflicting retained"):
            run_history(data)
        data = fixture()
        data["retained_frames"][0]["sample"]["dependence_group"] = "audio"
        result = run_history(data)
        self.assertEqual(
            result["snapshots"][2]["dependent_evidence_withheld"], ["interpretation_later"]
        )
        self.assertEqual(result["snapshots"][1]["posterior"], result["snapshots"][2]["posterior"])

    def test_direct_retrieval_filters_asof_before_ranking(self):
        data = fixture()
        obj = data["retained_frames"][0]
        sample = Sample.parse(obj["sample"])
        frame = RetainedFrame(sample, "inert-frame-v1", True)
        query = instant(data["query_at"])
        future = replace(
            frame, sample=replace(sample, id="future", available_at=instant(data["smooth_at"]))
        )
        args = (
            instant(data["window_start"]),
            instant(data["window_end"]),
            query,
            instant(data["smooth_at"]),
            Policy(),
        )
        result = retrieve((future, frame), *args)
        self.assertEqual(result.frames, (frame,))
        self.assertEqual(result.exclusions, (("future", "after_knowledge_cutoff"),))
        self.assertEqual(result.record()["completeness"], "not_established")
        with self.assertRaisesRegex(ValueError, "bounded"):
            retrieve((frame,), instant(data["window_start"]), query, query, query, Policy())

    def test_invalid_schedules_and_forecast_are_rejected(self):
        for key, value in (
            ("schema_version", 2),
            ("synthetic", False),
            ("query_at", "2026-10-24T10:00:00Z"),
            ("smooth_at", "2026-10-24T12:30:00Z"),
        ):
            data = fixture()
            data[key] = value
            with self.assertRaises(ValueError):
                run_history(data)
        data = fixture()
        data["scripted_forecast"]["issued_at"] = data["smooth_at"]
        with self.assertRaisesRegex(ValueError, "sealed"):
            run_history(data)

    def test_cli_runs_and_reports_remaining_gaps(self):
        process = subprocess.run(
            [sys.executable, "-m", "project_live.cli", "history", str(FIXTURE)],
            cwd=ROOT,
            check=True,
            capture_output=True,
            text=True,
        )
        result = json.loads(process.stdout)
        self.assertEqual(result, run_history(fixture()))
        self.assertEqual(result["status"], "PARTIAL_LIVE_022")
        self.assertIn("next_day_backfill", result["unimplemented"])
