# SPDX-License-Identifier: AGPL-3.0-only
import unittest

from quantifier import bite_cadence_per_minute, calibrate_homography, project, volume_cm3
from room_graph import PortalToken, cascade, export_event, pass_portal


class GeometryTests(unittest.TestCase):
    def test_calibration_box_volume_and_candidate_cadence(self):
        h = calibrate_homography(
            [(0, 0), (100, 0), (100, 100), (0, 100)], [(0, 0), (10, 0), (10, 10), (0, 10)]
        )
        self.assertEqual(project(h, 50, 50), (5, 5))
        self.assertEqual(
            volume_cm3([[True, True]], [[2, 2]], cell_area_cm2=25, metric_calibrated=True), 100
        )
        self.assertEqual(bite_cadence_per_minute([0, 10, 20]), 6)
        self.assertIsNone(bite_cadence_per_minute([0]))

    def test_unknown_scale_degenerate_points_and_invalid_depth_refused(self):
        with self.assertRaises(ValueError):
            volume_cm3([[True]], [[2]], cell_area_cm2=1)
        with self.assertRaises(ValueError):
            calibrate_homography([(0, 0)] * 4, [(0, 0)] * 4)
        for value in (-1, float("nan")):
            with self.assertRaises(ValueError):
                volume_cm3([[True]], [[value]], cell_area_cm2=1, metric_calibrated=True)


class PrivacyTests(unittest.TestCase):
    def test_cascade_stops_on_resolution_denial_and_budget(self):
        self.assertEqual(cascade("zone", unresolved=True, consent=True, remaining_calls=1), "pose")
        for values in ({"unresolved": False}, {"consent": False}, {"remaining_calls": 0}):
            args = {"unresolved": True, "consent": True, "remaining_calls": 1, **values}
            self.assertIsNone(cascade("zone", **args))

    def test_portal_expiry_and_media_rejection(self):
        token = PortalToken("kitchen", "hall", 0, 30)
        args = {"allowed_edges": {("kitchen", "hall")}, "consent": True}
        self.assertEqual(pass_portal(token, now=29, **args), "hall")
        self.assertIsNone(pass_portal(token, now=30, **args))
        self.assertIsNone(pass_portal(token, now=1, **{**args, "consent": False}))
        event = {"schema_version": 1, "kind": "meal_candidate", "synthetic": True}
        self.assertEqual(export_event(event), event)
        for field in ("video", "audio", "face_embedding", "identity"):
            with self.assertRaises(ValueError):
                export_event({**event, field: "synthetic-placeholder"})
