"""Value-snapshot regressions for synthetic observations."""
import copy
import json
import tempfile
import unittest
from dataclasses import FrozenInstanceError, asdict, fields, replace
from datetime import datetime, timezone
from pathlib import Path

from project_live.events import Observation
from project_live.replay import load_events


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

    def test_json_values_order_and_serialization_are_preserved(self):
        payload = {"z": [None, True, False, 42, -7, 1.5, -0.0, "café", {}, []],
                   "a": {"second": [1, {"first": "value"}]}}
        for direct in (False, True):
            with self.subTest(direct=direct):
                event = observation(payload, direct=direct)
                self.assertEqual(event.payload, payload)
                self.assertEqual(json.dumps(event.payload), json.dumps(payload))
                self.assertEqual(list(event.payload), ["z", "a"])
                self.assertEqual(
                    [type(v) for v in event.payload["z"]],
                    [type(v) for v in payload["z"]],
                )
                exported = asdict(event)
                self.assertEqual(exported["payload"], payload)
                exported["payload"]["z"].clear()
                self.assertEqual(event.payload, payload)

    def test_equality_remains_value_based_not_serialization_based(self):
        first = observation({"z": [1, True], "a": {"b": 2}})
        reordered = observation({"a": {"b": 2.0}, "z": [1.0, True]}, direct=True)
        self.assertEqual(first, reordered)
        self.assertNotEqual(first, observation({"z": [True, 2], "a": {"b": 2}}))
        self.assertEqual(first, replace(first))
        self.assertEqual(first, copy.copy(first))
        self.assertEqual(first, copy.deepcopy(first))
        self.assertEqual([f.name for f in fields(first)],
                         ["id", "at", "kind", "source", "payload", "synthetic"])
        with self.assertRaises(FrozenInstanceError):
            first.payload = {}
        with self.assertRaises(TypeError):
            Observation(id="sample", at=NOW, kind="vision_feature",
                        source="synthetic", synthetic=True)

    def test_shared_nested_containers_are_values_not_live_aliases(self):
        shared = [{"value": 1}]
        event = observation({"left": shared, "right": shared})
        shared[0]["value"] = 2
        returned = event.payload
        returned["left"][0]["value"] = 3
        self.assertEqual(returned["right"], [{"value": 1}])
        self.assertEqual(event.payload, {"left": [{"value": 1}],
                                        "right": [{"value": 1}]})

    def test_unsupported_values_and_keys_are_rejected_at_both_entry_points(self):
        class CustomDict(dict):
            pass

        class CustomList(list):
            pass

        class CustomInt(int):
            pass

        class CustomString(str):
            pass

        invalid = [
            {"nested": [set([1])]}, {"nested": [bytearray(b"a")]},
            {"nested": [b"a"]}, {"nested": [(1, 2)]},
            {"nested": [object()]}, {"nested": [{1: "coercion forbidden"}]},
            {"nested": [CustomDict()]}, {"nested": [CustomList()]},
            {"nested": [CustomInt(1)]}, {"nested": [CustomString("value")]},
            CustomDict(), [], None,
            *({"nested": [number]} for number in (float("nan"), float("inf"), -float("inf"))),
        ]
        for direct in (False, True):
            for i, payload in enumerate(invalid):
                with self.subTest(direct=direct, case=i):
                    with self.assertRaises(ValueError):
                        observation(payload, direct=direct)

    def test_cycles_are_rejected(self):
        cyclic_dict = {}
        cyclic_dict["self"] = cyclic_dict
        cyclic_list = []
        cyclic_list.append(cyclic_list)
        for direct in (False, True):
            for payload in (cyclic_dict, {"nested": cyclic_list}):
                with self.subTest(direct=direct):
                    with self.assertRaisesRegex(ValueError, "cycles"):
                        observation(payload, direct=direct)

    def test_jsonl_round_trip_preserves_equality_and_isolation(self):
        original = observation({"samples": [{"value": 1}, [2, None]]})
        record = asdict(original)
        record["at"] = original.at.isoformat()
        record["schema_version"] = 1
        encoded = json.dumps(record, sort_keys=True, separators=(",", ":"))
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "synthetic.jsonl"
            path.write_text(encoded + "\n", encoding="utf-8")
            loaded = load_events(path)[0]
        self.assertEqual(original, loaded)
        loaded.payload["samples"][0]["value"] = 99
        self.assertEqual(original, loaded)
        again = asdict(loaded)
        again["at"] = loaded.at.isoformat()
        again["schema_version"] = 1
        self.assertEqual(encoded, json.dumps(again, sort_keys=True, separators=(",", ":")))


if __name__ == "__main__":
    unittest.main()
