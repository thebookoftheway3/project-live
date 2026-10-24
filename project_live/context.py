"""Evidence-based *context* estimates; no therapeutic authority.

Simple illustrative Bayes/log-odds calculation with **handchosen, uncalibrated**
likelihood ratios. A real model requires measured evidence and calibration.
"""
from __future__ import annotations
from dataclasses import dataclass
from math import log, exp
from datetime import datetime, timedelta
from .events import Observation

# Grouping prevents multiple correlated detections within the same family
# from being multiplied as though independent.
EXAMPLE_LIKELIHOOD_RATIOS = {
    "audio_meal_speech": ("audio", 3.0),
    "audio_eating_sounds": ("audio", 3.5),
    "vision_table_eating": ("vision", 4.0),
    "vision_food_preparation": ("vision", 1.7),
    "motion_phone_on_table": ("motion", 1.5),
}

@dataclass(frozen=True)
class Belief:
    label: str
    probability: float
    evidence: tuple[str, ...]
    status: str = "ILLUSTRATIVE_NOT_CALIBRATED"

class MealContextEstimator:
    def __init__(self, prior: float = 0.12, evidence_ttl_seconds: int = 180):
        if not 0 < prior < 1:
            raise ValueError("prior must be between zero and one")
        self.prior = prior
        self.ttl = timedelta(seconds=evidence_ttl_seconds)
        self._seen: dict[str, tuple[datetime, str, float, str]] = {}

    def observe(self, event: Observation) -> None:
        if event.kind not in ("audio_feature", "vision_feature", "motion_feature"):
            return
        feature = event.payload.get("feature")
        if feature not in EXAMPLE_LIKELIHOOD_RATIOS:
            return
        group, ratio = EXAMPLE_LIKELIHOOD_RATIOS[feature]
        # Store one observation per feature, discard stale entries when evaluating.
        self._seen[feature] = (event.at, group, ratio, event.id)

    def estimate(self, now: datetime) -> Belief:
        by_group: dict[str, tuple[float, str]] = {}
        for feature, (at, group, ratio, event_id) in self._seen.items():
            age = now - at
            if timedelta(0) <= age <= self.ttl:
                prev = by_group.get(group)
                if prev is None or ratio > prev[0]:
                    by_group[group] = (ratio, event_id)
        log_odds = log(self.prior / (1 - self.prior))
        for ratio, _ in by_group.values():
            log_odds += log(ratio)
        probability = 1 / (1 + exp(-log_odds))
        return Belief("possible_meal", round(probability, 4), tuple(sorted(id for _, id in by_group.values())))
