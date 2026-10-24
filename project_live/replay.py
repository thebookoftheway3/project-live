"""Deterministic synthetic replay with a non-therapeutic advisory output."""
from __future__ import annotations
import json
from pathlib import Path
from .events import Observation
from .context import MealContextEstimator
from .environment import EnvironmentTracker
from .safety_boundary import NoPumpAccess

def load_events(path: str | Path) -> list[Observation]:
    events = []
    for number, line in enumerate(Path(path).read_text(encoding="utf-8").splitlines(), start=1):
        if not line.strip():
            continue
        try:
            events.append(Observation.parse(json.loads(line)))
        except (ValueError, KeyError, TypeError) as ex:
            raise ValueError(f"Invalid event on line {number}: {ex}") from ex
    seen: set[str] = set()
    for event in events:
        if event.id in seen:
            raise ValueError(f"Duplicate event id: {event.id}")
        seen.add(event.id)
    return sorted(events, key=lambda e: (e.at, e.id))

def replay(path: str | Path) -> list[dict]:
    env = EnvironmentTracker()
    meals = MealContextEstimator()
    boundary = NoPumpAccess()
    result = []
    for event in load_events(path):
        env.observe(event)
        meals.observe(event)
        setting = env.state(event.at)
        belief = meals.estimate(event.at)
        result.append({
            "event_id": event.id,
            "at": event.at.isoformat(),
            "environment": setting.name,
            "environment_verified": setting.verified,
            "meal_probability_example_only": belief.probability,
            "evidence": belief.evidence,
            "support_action": "review_possible_meal" if belief.probability >= 0.65 else "none",
            "pump_authorization": boundary.authorize("any_pump_action", setting.name).permitted,
        })
    return result
