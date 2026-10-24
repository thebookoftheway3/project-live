import json
import tempfile
import unittest
from datetime import datetime, timedelta, timezone
from pathlib import Path

from project_live.context import MealContextEstimator
from project_live.environment import EnvironmentTracker
from project_live.events import Observation
from project_live.replay import load_events, replay
from project_live.safety_boundary import NoPumpAccess

NOW = datetime(2026, 10, 24, 10, tzinfo=timezone.utc)


def sample(kind, at=NOW, payload=None, id="s1", synthetic=True):
    return Observation.parse(
        {
            "schema_version": 1,
            "id": id,
            "at": at.isoformat(),
            "kind": kind,
            "source": "test",
            "payload": payload or {},
            "synthetic": synthetic,
        }
    )


class ShadowTests(unittest.TestCase):
    def test_no_pump_action_can_be_authorized_even_at_home(self):
        b = NoPumpAccess()
        for env in ("home", "office", "car", "mobile"):
            for action in ("bolus", "increase_basal", "suspend", "resume"):
                self.assertFalse(b.authorize(action, env).permitted)
                with self.assertRaises(PermissionError):
                    b.execute(action)

    def test_real_observations_are_rejected_by_early_prototype(self):
        with self.assertRaises(ValueError):
            sample("glucose", synthetic=False)

    def test_unknown_or_expired_environment_never_grants_privileges(self):
        tracker = EnvironmentTracker(ttl_seconds=30)
        tracker.observe(sample("environment", payload={"name": "home", "confidence": 0.99}))
        self.assertEqual(tracker.state(NOW).name, "home")
        self.assertFalse(tracker.state(NOW + timedelta(seconds=31)).verified)

    def test_correlated_audio_features_not_double_counted(self):
        model = MealContextEstimator()
        model.observe(sample("audio_feature", payload={"feature": "audio_eating_sounds"}, id="1"))
        p1 = model.estimate(NOW).probability
        model.observe(sample("audio_feature", payload={"feature": "audio_meal_speech"}, id="2"))
        self.assertEqual(model.estimate(NOW).probability, p1)

    def test_evidence_expires(self):
        m = MealContextEstimator(evidence_ttl_seconds=10)
        m.observe(sample("vision_feature", payload={"feature": "vision_table_eating"}))
        self.assertGreater(
            m.estimate(NOW).probability, m.estimate(NOW + timedelta(seconds=11)).probability
        )

    def test_deterministic_replay_and_denied_pump(self):
        path = Path(__file__).resolve().parents[1] / "data/synthetic_example.jsonl"
        first = replay(path)
        self.assertEqual(first, replay(path))
        self.assertTrue(all(not step["pump_authorization"] for step in first))
        self.assertTrue(any(step["support_action"] == "review_possible_meal" for step in first))

    def test_reject_duplicate_ids(self):
        e = {
            "schema_version": 1,
            "id": "x",
            "at": "2026-10-24T10:00:00Z",
            "kind": "glucose",
            "source": "fake",
            "payload": {},
            "synthetic": True,
        }
        with tempfile.TemporaryDirectory() as d:
            path = Path(d) / "events.jsonl"
            path.write_text(json.dumps(e) + "\n" + json.dumps(e) + "\n")
            with self.assertRaises(ValueError):
                load_events(path)


if __name__ == "__main__":
    unittest.main()
