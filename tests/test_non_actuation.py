"""C-01/H-01/S-01/V-01 negative paths; no real transport or device is used."""

import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from project_live.replay import replay
from project_live.safety_boundary import NoPumpAccess


class NonActuationTests(unittest.TestCase):
    def test_unknown_commands_and_environments_cannot_bypass_denial(self):
        boundary = NoPumpAccess()
        for action in (
            "",
            "bolus",
            "set_basal",
            "pair",
            "set_parameters",
            "emergency_override",
            "resume",
            "suspend",
            "deliver;override",
            "any_pump_action",
        ):
            for environment in ("home", "office", "car", "mobile", "", "unknown", "admin"):
                with self.subTest(action=action, environment=environment):
                    self.assertIs(boundary.authorize(action, environment).permitted, False)
                    with self.assertRaises(PermissionError):
                        boundary.execute(action)

    def test_command_like_payloads_are_inert_even_with_verified_home_and_meal(self):
        records = []
        for index, (kind, payload) in enumerate(
            [
                ("environment", {"name": "home", "confidence": 1.0}),
                ("audio_feature", {"feature": "audio_eating_sounds"}),
                ("vision_feature", {"feature": "vision_table_eating"}),
                ("motion_feature", {"feature": "motion_phone_on_table"}),
                ("pump_telemetry", {"command": "bolus", "authorized": True}),
                ("bolus_observed", {"command": "set_basal", "pump_authorization": True}),
            ]
        ):
            records.append(
                {
                    "schema_version": 1,
                    "id": str(index),
                    "at": f"2026-10-24T10:00:0{index}Z",
                    "kind": kind,
                    "source": "synthetic-negative-control",
                    "synthetic": True,
                    "payload": payload | {"execute": "bolus", "override": True},
                }
            )
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "synthetic.jsonl"
            path.write_text("\n".join(json.dumps(record) for record in records))
            # Positive control proves the observer can register a harmless mock call.
            with patch.object(NoPumpAccess, "execute") as execute:
                NoPumpAccess().execute("synthetic-observer-control")
                execute.assert_called_once_with("synthetic-observer-control")
                execute.reset_mock()
                result = replay(path)
                execute.assert_not_called()
        self.assertEqual(len(result), len(records))
        self.assertTrue(all(item["environment_verified"] for item in result))
        self.assertTrue(any(item["support_action"] == "review_possible_meal" for item in result))
        self.assertTrue(all(item["pump_authorization"] is False for item in result))

    def test_command_event_kinds_are_rejected_at_replay_ingress(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "synthetic.jsonl"
            for kind in ("bolus", "pump_command", "set_basal", "treatment_parameters"):
                with self.subTest(kind=kind):
                    path.write_text(
                        json.dumps(
                            {
                                "schema_version": 1,
                                "id": "forbidden",
                                "at": "2026-10-24T10:00:00Z",
                                "kind": kind,
                                "source": "synthetic",
                                "synthetic": True,
                                "payload": {},
                            }
                        )
                    )
                    with self.assertRaisesRegex(ValueError, "Unknown observation kind"):
                        replay(path)
