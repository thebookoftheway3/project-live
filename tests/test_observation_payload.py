"""Value-snapshot regressions for synthetic observations."""
import copy
import unittest
from datetime import datetime, timezone

from project_live.events import Observation


NOW = datetime(2026, 10, 24, 10, tzinfo=timezone.utc)


def observation(payload, *, direct=False):
    if direct:
        return Observation("sample", NOW, "vision_feature", "synthetic", payload, True)
    return Observation.parse({
        "schema_version": 1, "id": "sample", "at": NOW.isoformat(),
        "kind": "vision_feature", "source": "synthetic",
        "payload": payload, "synthetic": True,
    })


class ObservationPayloadTests(unittest.TestCase):
    def test_external_references_cannot_change_observation(self):
        for direct in (False, True):
            with self.subTest(direct=direct):
                payload = {"feature": "vision_table_eating",
                           "details": {"samples": [{"value": 1}, [2, 3]]}}
                expected = copy.deepcopy(payload)
                event = observation(payload, direct=direct)
                payload["feature"] = "vision_food_preparation"
                payload["details"]["samples"][0]["value"] = 99
                payload["details"]["samples"][1].append(4)
                self.assertEqual(event.payload, expected)

    def test_returned_references_cannot_change_stored_observation(self):
        for direct in (False, True):
            with self.subTest(direct=direct):
                payload = {"details": {"samples": [{"value": 1}, [2, 3]]}}
                expected = copy.deepcopy(payload)
                event = observation(payload, direct=direct)
                returned = event.payload
                returned["details"]["samples"][0]["value"] = 99
                returned["details"]["samples"][1].clear()
                returned["extra"] = True
                self.assertEqual(event.payload, expected)


if __name__ == "__main__":
    unittest.main()
