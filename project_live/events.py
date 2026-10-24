"""Canonical read-only observations for offline deterministic replay.

This is an experimental data structure, not a medical-device interface.
"""
from __future__ import annotations
from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Any, Mapping

OBSERVATION_KINDS = frozenset({
    "environment", "glucose", "pump_telemetry", "audio_feature", "vision_feature",
    "motion_feature", "bolus_observed", "sleep_feature", "system_health"
})

@dataclass(frozen=True)
class Observation:
    id: str
    at: datetime
    kind: str
    source: str
    payload: Mapping[str, Any]
    synthetic: bool

    @staticmethod
    def parse(obj: Mapping[str, Any]) -> "Observation":
        if obj.get("schema_version") != 1:
            raise ValueError("Unsupported schema version")
        at = datetime.fromisoformat(str(obj["at"]).replace("Z", "+00:00"))
        if at.tzinfo is None:
            raise ValueError("Every observation needs a timezone-aware timestamp")
        if not isinstance(obj.get("id"), str) or not obj["id"]:
            raise ValueError("Nonempty observation id required")
        if obj.get("kind") not in OBSERVATION_KINDS:
            raise ValueError("Unknown observation kind")
        if not isinstance(obj.get("source"), str) or not obj["source"]:
            raise ValueError("Nonempty source required")
        if not isinstance(obj.get("payload"), dict):
            raise ValueError("Payload must be object")
        if obj.get("synthetic") is not True:
            # Initial model deliberately rejects real patient data.
            raise ValueError("Prototype accepts synthetic data only")
        return Observation(obj["id"], at.astimezone(timezone.utc), obj["kind"], obj["source"], obj["payload"], True)
