"""LIVE-022 increment: independent toy oracle and forbidden-path observations."""

import io
import json
import tempfile
import unittest
from contextlib import redirect_stdout
from dataclasses import FrozenInstanceError, replace
from fractions import Fraction
from pathlib import Path
from unittest.mock import patch

from project_live.bayes import PRIOR, STATES, Evidence, JointBelief, condition
from project_live.cli import main
from project_live.pipeline import run_fixture, run_samples
from project_live.safety_boundary import NoPumpAccess
from project_live.sensing import MockImageProvider, Policy, Sample, instant

FIXTURE = Path(__file__).resolve().parents[1] / "data/synthetic_beverage_v1.json"


class BayesianPipelineTests(unittest.TestCase):
    def setUp(self):
        self.raw = json.loads(FIXTURE.read_text())
        self.samples = [Sample.parse(s) for s in self.raw["samples"]]
        self.at = instant("2026-01-01T10:00:04Z")

    def run_samples(self, samples=None, policy=None, outcome="ok", cutoff=None):
        return run_samples(
            self.samples if samples is None else samples,
            policy or Policy(),
            MockImageProvider(outcome),
            cutoff=cutoff,
        )

    def test_complete_joint_table_against_independent_rational_oracle(self):
        result = run_fixture(FIXTURE)
        posterior = result["snapshots"][-1]["posterior"]
        weights = []
        # Independent rational enumeration; no production likelihood/conditioning call.
        for row in posterior:
            identity, quantity, actor = row["identity"], row["quantity"], row["actor"]
            prior = (
                {"regular": Fraction(1, 4), "diet": Fraction(1, 4), "unknown": Fraction(1, 2)}[
                    identity
                ]
                * {"none": Fraction(1, 2), "partial": Fraction(3, 10), "full": Fraction(1, 5)}[
                    quantity
                ]
                * {"self": Fraction(2, 5), "other": Fraction(3, 10), "unknown": Fraction(3, 10)}[
                    actor
                ]
            )
            opening = (Fraction(2, 5) if identity == "unknown" else Fraction(4, 5)) * (
                Fraction(3, 10) if quantity == "none" else Fraction(3, 5)
            )
            image = {"regular": Fraction(4, 5), "diet": Fraction(1, 10), "unknown": Fraction(1, 5)}[
                identity
            ]
            weight = {"none": Fraction(1, 5), "partial": Fraction(7, 10), "full": Fraction(1, 2)}[
                quantity
            ]
            weights.append(prior * opening * image * weight)
        self.assertEqual(len(posterior), 27)
        for row, weight in zip(posterior, weights):
            self.assertAlmostEqual(row["p"], float(weight / sum(weights)), places=14)
            self.assertGreater(row["p"], 0)
        self.assertAlmostEqual(sum(r["p"] for r in posterior), 1)
        self.assertAlmostEqual(sum(r["p"] for r in posterior if r["actor"] == "self"), 0.4)
        self.assertEqual([e["status"] for e in result["evidence"]], ["admitted"] * 3)
        self.assertEqual(result["provider_calls"], 1)
        self.assertFalse(result["pump_authorization"])

    def test_deterministic_replay_duplicates_and_truth_are_not_inputs(self):
        original = run_fixture(FIXTURE)
        self.assertEqual(original, run_fixture(FIXTURE))
        baseline = self.run_samples()
        self.assertEqual(baseline, self.run_samples(list(reversed(self.samples)) + self.samples))
        self.raw["evaluation_only_truth"] = {
            "identity": "diet",
            "quantity": "none",
            "actor": "other",
        }
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "fixture.json"
            path.write_text(json.dumps(self.raw))
            self.assertEqual(original, run_fixture(path))

    def test_cli_emits_executable_partial_result(self):
        out = io.StringIO()
        with patch("sys.argv", ["live", "beverage", str(FIXTURE)]), redirect_stdout(out):
            main()
        result = json.loads(out.getvalue())
        self.assertEqual(result["status"], "PARTIAL_LIVE_022_SYNTHETIC_ONLY")
        self.assertIn("retrospective_smoothing", result["unimplemented"])

    def test_missing_trigger_stops_without_acquisition_or_weight_inference(self):
        for samples in (self.samples[1:], [s for s in self.samples if s.kind != "audio"]):
            result = self.run_samples(samples)
            self.assertEqual(result["provider_calls"], 0)
            self.assertEqual(result["evidence"], [])
            self.assertEqual(result["decisions"][-1]["reason"], "no_trigger")

    def test_late_arrival_and_result_cannot_leak_into_earlier_cutoff(self):
        cutoff = instant("2026-01-01T10:00:02Z")
        before = self.run_samples(cutoff=cutoff)
        self.assertEqual(before["provider_calls"], 0)
        self.assertEqual(before["decisions"][0]["reason"], "cutoff_deadline")
        self.assertTrue(all(instant(s["evidence_cutoff"]) <= cutoff for s in before["snapshots"]))
        late = replace(self.samples[2], available_at=instant("2026-01-01T10:30:00Z"))
        result = self.run_samples(self.samples[:2] + [late], cutoff=cutoff)
        self.assertEqual(result, self.run_samples(self.samples[:2], cutoff=cutoff))
        self.assertEqual(before, self.run_samples(cutoff=cutoff))

    def test_snapshots_are_detached_and_cannot_be_backdated(self):
        belief = JointBelief()
        first = belief.snapshot("initial", self.at)
        e = Evidence("e", "regular_image", ("leaf",), ("group",), self.at, "v1")
        self.assertEqual(belief.admit(e, self.at), "admitted")
        self.assertEqual(first.probabilities, PRIOR)
        record = belief.snapshot("later", self.at).record()
        record["evidence_manifest"][0]["source_ids"].append("mutated")
        record["posterior"][0]["p"] = 100
        self.assertEqual(belief.evidence[0].source_ids, ("leaf",))
        self.assertLess(belief.probabilities[0], 1)
        with self.assertRaises(FrozenInstanceError):
            e.finding = "diet_image"
        with self.assertRaises(ValueError):
            belief.snapshot("backdated", instant("2026-01-01T09:00:00Z"))
        with self.assertRaises(ValueError):
            replace(e, source_ids=["mutable"])

    def test_duplicate_leaf_and_shared_error_group_are_withheld(self):
        belief = JointBelief()
        first = Evidence("first", "can_opening", ("audio",), ("shared",), self.at, "v1")
        self.assertEqual(belief.admit(first, self.at), "admitted")
        initial = belief.probabilities
        self.assertEqual(belief.admit(first, self.at), "duplicate")
        for evidence in (
            replace(first, id="child", dependence_groups=("different",)),
            replace(first, id="correlated", source_ids=("another",)),
        ):
            self.assertEqual(belief.admit(evidence, self.at), "dependent_evidence_withheld")
        self.assertEqual(belief.probabilities, initial)
        with self.assertRaises(ValueError):
            belief.admit(replace(first, finding="diet_image"), self.at)
        future = replace(first, id="future", available_at=instant("2026-01-01T11:00:00Z"))
        self.assertEqual(belief.admit(future, self.at), "future_evidence_withheld")

    def test_permission_budget_and_no_value_prevent_dispatch(self):
        # Positive control proves both counters can detect the mock operation.
        allowed = self.run_samples()
        self.assertEqual((allowed["provider_calls"], allowed["provider_payload_reads"]), (1, 1))
        for policy in (
            Policy(allow_image=False),
            Policy(max_calls=0),
            Policy(min_benefit=1),
            Policy(revoked_at=instant("2026-01-01T10:00:02Z")),
        ):
            with self.subTest(policy=policy):
                denied = self.run_samples(policy=policy)
                self.assertEqual(
                    (denied["provider_calls"], denied["provider_payload_reads"]), (0, 0)
                )
        for frame in (
            replace(self.samples[2], permitted=False),
            replace(self.samples[2], retain_until=self.samples[2].available_at),
        ):
            denied = self.run_samples(self.samples[:2] + [frame])
            self.assertEqual(denied["provider_payload_reads"], 0)

    def test_provider_entry_point_checks_permissions_and_budget(self):
        frame = self.samples[2]
        for changed, at, policy in (
            (replace(frame, permitted=False), self.at, Policy()),
            (frame, instant("2026-01-01T09:00:00Z"), Policy()),
            (frame, instant("2026-01-01T11:00:00Z"), Policy()),
            (frame, self.at, Policy(max_calls=0)),
            (frame, self.at, Policy(allow_image=False)),
        ):
            mock = MockImageProvider()
            self.assertIsNone(mock.infer(changed, at, policy).finding)
            self.assertEqual(mock.payload_reads, 0)
        mock = MockImageProvider()
        self.assertEqual(mock.infer(frame, self.at, Policy()).status, "ok")
        self.assertEqual(mock.infer(frame, self.at, Policy()).status, "budget_exhausted")
        self.assertEqual(mock.payload_reads, 1)
        with self.assertRaises(ValueError):
            run_samples(self.samples, Policy(), mock)

    def test_midflight_revocation_and_expiry_withhold_results(self):
        at = instant("2026-01-01T10:00:03Z")
        for samples, policy in (
            (self.samples, Policy(revoked_at=at)),
            (
                self.samples[:2] + [replace(self.samples[2], retain_until=at)] + self.samples[3:],
                Policy(),
            ),
        ):
            result = self.run_samples(samples, policy)
            image = next(e for e in result["evidence"] if e["id"].startswith("image:"))
            self.assertEqual(image["status"], "permission_or_retention_changed")
            self.assertIsNone(image["finding"])
            self.assertEqual(result["provider_calls"], 1)
            self.assertFalse(
                any(
                    e["id"].startswith("image:")
                    for e in result["snapshots"][-1]["evidence_manifest"]
                )
            )

    def test_failed_and_malicious_provider_results_are_inert(self):
        without_image = self.run_samples(policy=Policy(max_calls=0))["snapshots"][-1]["posterior"]
        for outcome in ("unknown", "timeout", "refused", "invalid_output"):
            result = self.run_samples(outcome=outcome)
            self.assertEqual(result["snapshots"][-1]["posterior"], without_image)
            self.assertIn(outcome, [e["status"] for e in result["evidence"]])
        malicious = replace(
            self.samples[2], value="file:///private/secret; __import__('os').system('pump')"
        )
        with patch("pathlib.Path.open", side_effect=AssertionError("unexpected file read")):
            result = self.run_samples(self.samples[:2] + [malicious] + self.samples[3:])
        self.assertEqual(result["snapshots"][-1]["posterior"], without_image)
        self.assertFalse(result["pump_authorization"])
        with self.assertRaises(PermissionError):
            NoPumpAccess().execute("bolus")

    def test_numerical_and_fixture_validation_fail_closed(self):
        self.assertIsNone(condition(PRIOR, (0.0,) * len(STATES)))
        for likelihood in ((1.0,), (float("nan"),) * 27, (-0.1,) * 27, (1.1,) * 27):
            with self.assertRaises(ValueError):
                condition(PRIOR, likelihood)
        for changes in (
            {"synthetic": False},
            {"permitted": "true"},
            {"event_at": "2026-01-01"},
            {"available_at": "2025-01-01T00:00:00Z"},
            {"sequence": True},
            {"kind": "pump"},
            {"value": []},
        ):
            with self.subTest(changes=changes), self.assertRaises(ValueError):
                Sample.parse(self.raw["samples"][0] | changes)
        for value in (float("nan"), float("inf"), -1, True, "250"):
            with self.assertRaises(ValueError):
                Sample.parse(self.raw["samples"][3] | {"value": value})
        for obj in ({"max_calls": 2}, {"allow_image": "true"}, {"min_benefit": float("nan")}):
            with self.assertRaises(ValueError):
                Policy.parse(obj)
        with self.assertRaises(ValueError):
            self.run_samples(self.samples + [replace(self.samples[0], value="closed")])
        with self.assertRaises(ValueError):
            self.run_samples(
                [
                    self.samples[0],
                    replace(
                        self.samples[1],
                        event_at=self.samples[0].event_at,
                        available_at=self.samples[0].available_at,
                        sequence=0,
                    ),
                ]
            )
