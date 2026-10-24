"""Environment recognition for support features only.

The environment is NOT used to grant authority to dose insulin.
"""
from __future__ import annotations
from dataclasses import dataclass
from datetime import datetime, timedelta
from .events import Observation

ENVIRONMENTS = frozenset({"home", "office", "car", "mobile"})

@dataclass(frozen=True)
class EnvironmentState:
    name: str
    confidence: float
    verified: bool
    reason: str

class EnvironmentTracker:
    def __init__(self, ttl_seconds: int = 300, min_confidence: float = 0.80):
        self.ttl = timedelta(seconds=ttl_seconds)
        self.min_confidence = min_confidence
        self._last: Observation | None = None

    def observe(self, event: Observation) -> None:
        if event.kind == "environment":
            self._last = event

    def state(self, now: datetime) -> EnvironmentState:
        e = self._last
        if e is None:
            return EnvironmentState("mobile", 0.0, False, "no_environment_evidence")
        name = e.payload.get("name")
        conf = e.payload.get("confidence", 0.0)
        if name not in ENVIRONMENTS or not isinstance(conf, (int, float)):
            return EnvironmentState("mobile", 0.0, False, "invalid_environment_evidence")
        age = now - e.at
        if not timedelta(0) <= age <= self.ttl or not self.min_confidence <= conf <= 1.0:
            return EnvironmentState("mobile", 0.0, False, "stale_or_uncertain_environment")
        return EnvironmentState(name, float(conf), True, "verified_context_only")
