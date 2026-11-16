# SPDX-License-Identifier: AGPL-3.0-only
"""Research quality labels, not diagnoses or permission to alter treatment."""

from dataclasses import dataclass
from enum import Enum
from math import isfinite


class Health(str, Enum):
    UNKNOWN = "UNKNOWN"
    WARMUP_DEGRADED = "WARMUP_DEGRADED"
    ARTIFACT_SUSPECT = "ARTIFACT_SUSPECT"
    NOMINAL = "NOMINAL"


@dataclass(frozen=True)
class HealthResult:
    state: Health
    reasons: tuple[str, ...]
    variance_multiplier: float | None


def assess_health(
    *,
    sensor_age_hours: float | None,
    fresh: bool,
    nocturnal: bool,
    low_candidate: bool,
    bed_motion: bool | None,
) -> HealthResult:
    """12h and 4x variance are uncalibrated hypotheses; input is never rewritten.

    Motion co-occurrence nominates an artifact hypothesis, never proves compression
    or rules out a true low. UNKNOWN and suspected artifacts have no usable variance.
    """
    if any(type(v) is not bool for v in (fresh, nocturnal, low_candidate)):
        raise ValueError("explicit quality booleans required")
    if bed_motion is not None and type(bed_motion) is not bool:
        raise ValueError("motion must be a boolean or unknown")
    if sensor_age_hours is not None and (
        type(sensor_age_hours) not in (int, float)
        or not isfinite(sensor_age_hours)
        or sensor_age_hours < 0
    ):
        raise ValueError("finite nonnegative sensor age required")
    if not fresh or sensor_age_hours is None:
        return HealthResult(Health.UNKNOWN, ("stale_or_unknown_age",), None)
    reasons = []
    if sensor_age_hours < 12:
        reasons.append("first_12_hours_unvalidated_variance")
    if nocturnal and low_candidate:
        if bed_motion is None:
            return HealthResult(Health.UNKNOWN, (*reasons, "motion_unavailable"), None)
        if bed_motion:
            return HealthResult(Health.ARTIFACT_SUSPECT, (*reasons, "motion_cooccurrence"), None)
    if reasons:
        return HealthResult(Health.WARMUP_DEGRADED, tuple(reasons), 4.0)
    return HealthResult(Health.NOMINAL, (), 1.0)
