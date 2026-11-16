# SPDX-License-Identifier: AGPL-3.0-only
import unittest
from dataclasses import replace

from surfer_session import SemanticEvent, SurferSession


class SurferTests(unittest.TestCase):
    def setUp(self):
        self.session = SurferSession()
        self.event = SemanticEvent(
            "event", "leaf", "home_poe", "meal_candidate", "self", 0, 0, True
        )

    def consider(self, event=None, now=0, **kwargs):
        return self.session.consider(
            event or self.event, now=now, **{"evsi": 1, "base_cost": 0.1, "consent": True, **kwargs}
        )

    def test_home_nomadic_same_evidence_does_not_duplicate_question(self):
        _, prompt = self.consider()
        self.assertEqual(prompt.expires_at, 180)
        self.assertEqual(self.consider()[0], "duplicate")
        mobile = replace(self.event, event_id="mobile", source="brilliant_frame")
        self.assertEqual(self.consider(mobile, now=1)[0], "question_pending")
        self.session.reply(now=2, question_id="event", answer=True)
        mobile = replace(mobile, event_id="mobile-again")
        self.assertEqual(self.consider(mobile, now=1500)[0], "duplicate_evidence")

    def test_timeout_exactly_180_seconds_and_cost_increase(self):
        self.consider()
        self.session.advance(179)
        self.assertIsNotNone(self.session.pending)
        self.session.advance(180)
        self.assertIsNone(self.session.pending)
        self.assertEqual(self.session.unanswered_streak, 1)
        with self.assertRaises(ValueError):
            self.session.reply(now=181, question_id="event", answer=True)
        event = replace(self.event, event_id="next", evidence_id="next")
        self.assertEqual(self.consider(event, now=1500, evsi=0.12)[0], "insufficient_value")

    def test_clearance_is_attention_only_and_is_not_interlock_lockout(self):
        self.session.preempt(now=0, clearance_minutes=90)
        self.assertEqual(self.consider(now=100)[0], "manual_attention_clearance")
        with self.assertRaises(ValueError):
            self.session.preempt(now=100, clearance_minutes=90)
        event = replace(self.event, event_id="later", evidence_id="later")
        self.assertIsNotNone(self.consider(event, now=5400)[1])

    def test_unknown_identity_future_availability_and_conflict(self):
        self.assertEqual(self.consider(replace(self.event, available_at=1))[0], "not_available")
        self.assertEqual(
            self.consider(replace(self.event, subject="unknown"))[0], "subject_unconfirmed"
        )
        with self.assertRaises(ValueError):
            self.consider()
        with self.assertRaises(ValueError):
            replace(self.event, synthetic=False)
