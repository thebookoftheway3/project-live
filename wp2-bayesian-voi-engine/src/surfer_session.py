# SPDX-License-Identifier: AGPL-3.0-only
"""Surfer OS synthetic home/nomadic session; no physiology, delivery or network."""

from dataclasses import dataclass

from voi_attention_gate import AttentionGate, attention_cost, nonnegative

SOURCES = {"home_poe", "home_matstation_2d", "brilliant_halo", "brilliant_frame"}
ACTIONS = {"meal_candidate", "chewing_candidate", "kitchen_activity"}


@dataclass(frozen=True)
class SemanticEvent:
    event_id: str
    evidence_id: str
    source: str
    action: str
    subject: str
    observed_at: float
    available_at: float
    synthetic: bool

    def __post_init__(self):
        for identifier in (self.event_id, self.evidence_id):
            if type(identifier) is not str or not 1 <= len(identifier) <= 64:
                raise ValueError("bounded event/evidence identifiers required")
        if self.source not in SOURCES or self.action not in ACTIONS:
            raise ValueError("unsupported semantic source/action")
        if self.subject not in {"self", "bystander", "unknown"} or self.synthetic is not True:
            raise ValueError("explicit subject and synthetic input required")
        if not all(nonnegative(v) for v in (self.observed_at, self.available_at)):
            raise ValueError("finite synthetic timeline required")
        if self.observed_at > self.available_at:
            raise ValueError("observation cannot follow availability")


@dataclass(frozen=True)
class Prompt:
    question_id: str
    issued_at: float
    expires_at: float
    text: str = "Is this a meal?"
    answers: tuple[str, str] = ("Yes", "No")


class SurferSession:
    """One synthetic session. Identity uncertainty never defaults to SELF.

    EVSI is supplied by a declared decision model, never inferred from a VLM's
    confidence alone. Missing replies suggest burden but do not diagnose it.
    """

    def __init__(self):
        self.gate = AttentionGate(cooldown_seconds=1500, daily_limit=3)
        self.pending = None
        self.unanswered_streak = 0
        self.clearance_until = 0
        self._clock = 0
        self._events = {}
        self._closed = {}

    def advance(self, now):
        if not nonnegative(now) or now < self._clock:
            raise ValueError("invalid or regressed session clock")
        self._clock = now
        if self.pending and now >= self.pending.expires_at:
            self._closed[self.pending.question_id] = None
            self.pending = None
            self.unanswered_streak += 1

    def preempt(self, *, now, clearance_minutes):
        self.advance(now)
        if type(clearance_minutes) is not int or not 1 <= clearance_minutes <= 180:
            raise ValueError("synthetic attention clearance must be 1..180 minutes")
        if now < self.clearance_until:
            raise ValueError("clearance already active")
        self.clearance_until = now + clearance_minutes * 60
        if self.pending:
            self._closed[self.pending.question_id] = None
            self.pending = None  # intentional preemption does not imply cognitive overload

    def consider(self, event, *, now, evsi, base_cost, consent):
        self.advance(now)
        if type(event) is not SemanticEvent:
            raise ValueError("validated semantic event required")
        if not all(nonnegative(v) for v in (evsi, base_cost)) or type(consent) is not bool:
            raise ValueError("finite utility/cost and explicit consent required")
        if event.event_id in self._events:
            if self._events[event.event_id] != event:
                raise ValueError("conflicting event ID")
            return "duplicate", None
        if event.available_at > now:
            return "not_available", None
        if len(self._events) >= 1000:
            raise ValueError("synthetic session capacity exhausted")
        self._events[event.event_id] = event
        if event.subject != "self":
            return "subject_unconfirmed", None
        if now < self.clearance_until:
            return "manual_attention_clearance", None
        if self.pending:
            return "question_pending", None
        cost = attention_cost(base_cost, 1 + 0.25 * self.unanswered_streak, 0)
        decision = self.gate.consider(
            now=now, evidence_id=event.evidence_id, evsi=evsi, cost=cost, consent=consent
        )
        if not decision.dispatch:
            return decision.reason, None
        self.pending = Prompt(event.event_id, now, now + 180)
        return "synthetic_question_candidate", self.pending

    def reply(self, *, now, question_id, answer):
        self.advance(now)
        if answer is not None and type(answer) is not bool:
            raise ValueError("reply is Yes, No or unknown")
        if question_id in self._closed:
            if self._closed[question_id] != answer:
                raise ValueError("late or conflicting reply")
            return "duplicate"
        if self.pending is None or self.pending.question_id != question_id:
            raise ValueError("no matching current question")
        self._closed[question_id] = answer
        self.pending = None
        self.unanswered_streak = self.unanswered_streak + 1 if answer is None else 0
        return "unknown" if answer is None else "human_annotation"
