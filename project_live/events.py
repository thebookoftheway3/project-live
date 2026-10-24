"""Canonical read-only observations for offline deterministic replay.

This is an experimental data structure, not a medical-device interface.
"""
from __future__ import annotations
import json
from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Any, Mapping

OBSERVATION_KINDS = frozenset({
    "environment", "glucose", "pump_telemetry", "audio_feature", "vision_feature",
    "motion_feature", "bolus_observed", "sleep_feature", "system_health"
})


def _validate_json_value(value: Any, ancestors: set[int]) -> None:
    """Accept only JSON value trees, without invoking user-defined conversion hooks."""
    if type(value) in (str, int, float, bool, type(None)):
        return
    if type(value) not in (dict, list):
        raise ValueError("Payload values must be built-in JSON types")
    if id(value) in ancestors:
        raise ValueError("Payload must not contain cycles")
    ancestors.add(id(value))
    try:
        if type(value) is dict:
            for key, item in value.items():
                if type(key) is not str:
                    raise ValueError("Payload object keys must be strings")
                _validate_json_value(item, ancestors)
        else:
            for item in value:
                _validate_json_value(item, ancestors)
    finally:
        ancestors.remove(id(value))


class _PayloadSnapshot:
    """Dataclass field descriptor preserving the public dict/list value contract.

    Construction stores only immutable JSON text; every read returns a fresh tree.
    Keeping payload as a dataclass field preserves generated init/equality/asdict.
    This protects ordinary references, not against hostile code in this process.
    """

    def __get__(self, instance, owner=None):
        if instance is None:
            # Dataclasses interprets this as a required field (no default value).
            raise AttributeError("payload has no default")
        return json.loads(instance._payload_json)

    def __set__(self, instance, value):
        if type(value) is not dict:
            raise ValueError("Payload must be a built-in object")
        try:
            _validate_json_value(value, set())
            # Preserve key/list order and scalar types; reject NaN and infinity.
            snapshot = json.dumps(value, allow_nan=False, separators=(",", ":"))
        except RecursionError as ex:
            raise ValueError("Payload is too deeply nested") from ex
        object.__setattr__(instance, "_payload_json", snapshot)


@dataclass(frozen=True)
class Observation:
    id: str
    at: datetime
    kind: str
    source: str
    payload: Mapping[str, Any] = _PayloadSnapshot()
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
