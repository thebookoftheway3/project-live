# SPDX-License-Identifier: AGPL-3.0-only
"""Exact EVSI oracle, candidate budgets and synthetic detector boundary cases."""

import unittest

from detector_health import Health, assess_health
from voi_attention_gate import AttentionGate, attention_cost, expected_value_of_sample_information


class VOITests(unittest.TestCase):
    def test_perfect_and_uninformative_sample_against_hand_oracle(self):
        # Best action without information succeeds 3/4; with perfect info succeeds 1.
        self.assertEqual(
            expected_value_of_sample_information([0.75, 0.25], [[1, 0], [0, 1]], [[1, 0], [0, 1]]),
            0.25,
        )
        self.assertEqual(
            expected_value_of_sample_information(
                [0.75, 0.25], [[0.5, 0.5], [0.5, 0.5]], [[1, 0], [0, 1]]
            ),
            0,
        )

    def test_invalid_probabilities_and_utilities_fail(self):
        for prior in ([0.2, 0.2], [True, 0], [float("nan"), 0], [-1, 2]):
            with self.assertRaises(ValueError):
                expected_value_of_sample_information(prior, [[1, 0], [0, 1]], [[1, 0]])
        for likelihood in ([[1]], [[1, 0], [0.5, 0.2]], [[1, 0], [float("nan"), 0]]):
            with self.assertRaises(ValueError):
                expected_value_of_sample_information([0.5, 0.5], likelihood, [[1, 0]])

    def test_cooldown_exact_boundary_budget_rolling_window_and_duplicates(self):
        gate = AttentionGate(cooldown_seconds=900, daily_limit=2)

        def ask(t, key):
            return gate.consider(now=t, evidence_id=key, evsi=1, cost=0.1, consent=True)

        self.assertTrue(ask(0, "first").dispatch)
        self.assertEqual(ask(899, "second").reason, "cooldown")
        self.assertTrue(ask(900, "second").dispatch)
        self.assertEqual(ask(1800, "second").reason, "duplicate_evidence")
        self.assertEqual(ask(1800, "third").reason, "daily_budget")
        self.assertEqual(ask(86399, "third").reason, "daily_budget")
        self.assertTrue(ask(86400, "third").dispatch)
        with self.assertRaises(ValueError):
            ask(100, "regressed")

    def test_denial_cost_and_unanswered_candidates_consume_no_extra_dispatch(self):
        gate = AttentionGate()
        self.assertFalse(
            gate.consider(now=0, evidence_id="a", evsi=1, cost=0, consent=False).dispatch
        )
        self.assertFalse(
            gate.consider(now=1, evidence_id="a", evsi=1, cost=1, consent=True).dispatch
        )
        self.assertTrue(
            gate.consider(now=2, evidence_id="a", evsi=1, cost=0, consent=True).dispatch
        )
        self.assertEqual(attention_cost(0.2, 2, 3), 1.6)
        with self.assertRaises(ValueError):
            gate.consider(now=float("nan"), evidence_id="x", evsi=1, cost=0, consent=True)
        with self.assertRaises(ValueError):
            AttentionGate(cooldown_seconds=0)

    def test_synthetic_interruptions_are_bounded_not_a_field_benefit_claim(self):
        gate = AttentionGate(daily_limit=3)
        dispatched = sum(
            gate.consider(now=i * 1000, evidence_id=str(i), evsi=1, cost=0.1, consent=True).dispatch
            for i in range(20)
        )
        self.assertEqual(dispatched, 3)
        # 85% fewer candidates for this fixture; no evidence of clinical alarm reduction.


class DetectorTests(unittest.TestCase):
    def assess(self, age, **kwargs):
        values = dict(fresh=True, nocturnal=False, low_candidate=False, bed_motion=False)
        values.update(kwargs)
        return assess_health(sensor_age_hours=age, **values)

    def test_warmup_boundary_and_artifact_never_excludes_true_low(self):
        self.assertEqual(self.assess(11.999).state, Health.WARMUP_DEGRADED)
        self.assertEqual(self.assess(12).state, Health.NOMINAL)
        result = self.assess(1, nocturnal=True, low_candidate=True, bed_motion=True)
        self.assertEqual(result.state, Health.ARTIFACT_SUSPECT)
        self.assertIsNone(result.variance_multiplier)
        self.assertEqual(len(result.reasons), 2)

    def test_missing_stale_and_invalid(self):
        self.assertEqual(self.assess(None).state, Health.UNKNOWN)
        self.assertEqual(self.assess(15, fresh=False).state, Health.UNKNOWN)
        self.assertEqual(
            self.assess(15, nocturnal=True, low_candidate=True, bed_motion=None).state,
            Health.UNKNOWN,
        )
        for age in (-1, float("nan"), float("inf"), True):
            with self.assertRaises(ValueError):
                self.assess(age)
