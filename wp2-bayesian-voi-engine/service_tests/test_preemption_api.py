# SPDX-License-Identifier: AGPL-3.0-only
import unittest

from fastapi.testclient import TestClient
from preemption_api import create_app


class APITests(unittest.TestCase):
    def setUp(self):
        self.tick = 0
        self.client = TestClient(create_app(token="x" * 32, clock=lambda: self.tick))
        self.headers = {"Authorization": "Bearer " + "x" * 32}
        self.body = {"request_id": "one", "clearance_minutes": 15, "synthetic": True}

    def post(self, body):
        return self.client.post("/v1/preemptions", json=body, headers=self.headers)

    def test_authentication_and_synthetic_strictness(self):
        self.assertEqual(self.client.post("/v1/preemptions", json=self.body).status_code, 401)
        for change in (
            {"synthetic": False},
            {"synthetic": 1},
            {"clearance_minutes": 181},
            {"clearance_minutes": True},
            {"pump": "command"},
        ):
            self.assertEqual(self.post({**self.body, **change}).status_code, 422)
        with self.assertRaises(ValueError):
            create_app(token="short")

    def test_idempotency_no_renewal_expiry_and_clock_regression(self):
        self.assertFalse(self.post(self.body).json()["may_actuate_insulin"])
        self.tick = 100
        self.assertEqual(self.post(self.body).status_code, 200)
        status = self.client.get("/v1/status", headers=self.headers).json()
        self.assertEqual(status["clearance_seconds_remaining"], 800)
        self.assertEqual(self.post({**self.body, "request_id": "two"}).status_code, 409)
        self.assertEqual(self.post({**self.body, "clearance_minutes": 1}).status_code, 409)
        self.tick = 900
        self.assertEqual(self.post({**self.body, "request_id": "two"}).status_code, 200)
        self.tick = 1
        self.assertEqual(self.client.get("/v1/status", headers=self.headers).status_code, 503)

    def test_unanswered_is_unknown_and_does_not_make_outbound_call(self):
        body = {
            "request_id": "prompt",
            "answer": "unanswered",
            "escalation_level": 1,
            "synthetic": True,
        }
        response = self.client.post("/v1/voice/callbacks", json=body, headers=self.headers)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["answer"], "unanswered")
        self.assertEqual(response.json()["next_escalation_level"], 2)
        self.assertFalse(response.json()["callback_dispatched"])

    def test_home_mobile_contract_question_and_feedback(self):
        event = {
            "event_id": "home",
            "evidence_id": "meal",
            "source": "home_poe",
            "action": "meal_candidate",
            "subject": "self",
            "observed_at": 0.0,
            "available_at": 0.0,
            "synthetic": True,
            "consent": True,
            "evsi": 1.0,
            "attention_cost": 0.1,
        }
        response = self.client.post("/v1/events/context", json=event, headers=self.headers)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["prompt"]["expires_at"], 180)
        reply = {"question_id": "home", "answer": None, "synthetic": True}
        response = self.client.post("/v1/feedback/1bit", json=reply, headers=self.headers)
        self.assertEqual(response.json()["status"], "unknown")
        self.tick = 1500
        event.update(event_id="mobile", evidence_id="new_meal", source="brilliant_halo")
        response = self.client.post("/v1/events/context", json=event, headers=self.headers)
        self.assertEqual(response.json()["status"], "synthetic_question_candidate")
