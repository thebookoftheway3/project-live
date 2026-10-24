"""Versioned, read-only observations from the Loop G6 research variant.

No Bluetooth, account, pump or network interface. Real files require local consent;
existing synthetic beverage models remain synthetic-only (ADRs 0001–0003).
"""

import hashlib
import json
import os
import stat
from dataclasses import dataclass, replace
from datetime import datetime, timezone
from math import isfinite
from pathlib import Path

from .sensing import instant

SCHEMA = "project-live.cgm-observation"
REQUIRED = {
    "schema",
    "schema_version",
    "id",
    "event_at",
    "received_at",
    "source",
    "source_version",
    "unit",
    "glucose",
    "quality",
    "synthetic",
    "shadow_only",
    "may_actuate_insulin",
}


@dataclass(frozen=True)
class LoopGlucose:
    id: str
    event_at: datetime
    received_at: datetime
    value: float
    display_only: bool
    user_entered: bool
    condition: str | None
    trend: str | None
    synthetic: bool

    @classmethod
    def parse(cls, obj: dict) -> "LoopGlucose":
        if type(obj) is not dict or set(obj) != REQUIRED:
            raise ValueError("observation fields do not match v1")
        if (
            obj["schema"] != SCHEMA
            or type(obj["schema_version"]) is not int
            or obj["schema_version"] != 1
        ):
            raise ValueError("unsupported observation schema")
        if (
            obj["source"] != "loop.dexcom-g6"
            or obj["source_version"] != "loop-g6-passive-v1"
            or obj["unit"] != "mg/dL"
            or obj["shadow_only"] is not True
            or obj["may_actuate_insulin"] is not False
            or type(obj["synthetic"]) is not bool
        ):
            raise ValueError("unsupported source, unit or authority")
        if (
            type(obj["id"]) is not str
            or len(obj["id"]) != 64
            or any(c not in "0123456789abcdef" for c in obj["id"])
        ):
            raise ValueError("hashed observation id required")
        value = obj["glucose"]
        if type(value) not in (int, float) or not isfinite(value) or not 0 < value <= 1000:
            raise ValueError("invalid numeric glucose")
        quality = obj["quality"]
        if type(quality) is not dict or set(quality) != {
            "is_display_only",
            "was_user_entered",
            "condition",
            "trend",
        }:
            raise ValueError("explicit quality fields required")
        if any(type(quality[k]) is not bool for k in ("is_display_only", "was_user_entered")):
            raise ValueError("explicit quality booleans required")
        if any(
            quality[k] is not None and (type(quality[k]) is not str or len(quality[k]) > 64)
            for k in ("condition", "trend")
        ):
            raise ValueError("bounded optional quality labels required")
        event, received = instant(obj["event_at"]), instant(obj["received_at"])
        if event > received:
            raise ValueError("event time is after reception")
        return cls(
            obj["id"],
            event,
            received,
            float(value),
            quality["is_display_only"],
            quality["was_user_entered"],
            quality["condition"],
            quality["trend"],
            obj["synthetic"],
        )


def decode_observations(raw: bytes, *, consent: bool = False) -> tuple[LoopGlucose, ...]:
    if len(raw) > 25_000_000:
        raise ValueError("observation file exceeds 25MB limit")
    try:
        lines = raw.decode("utf-8").splitlines()
    except UnicodeError:
        raise ValueError("observation file must be UTF-8") from None
    if len(lines) > 50_000:
        raise ValueError("observation file exceeds 50000 records")
    by_id = {}
    for number, line in enumerate(lines, 1):
        if not line.strip():
            continue
        try:
            item = LoopGlucose.parse(json.loads(line))
        except (ValueError, KeyError, TypeError, OverflowError):
            raise ValueError(
                f"invalid observation at line {number}; raw content withheld"
            ) from None
        if not item.synthetic and (not consent or os.environ.get("GITHUB_ACTIONS") == "true"):
            raise ValueError(
                "real observations require local consent and are forbidden in GitHub Actions"
            )
        if item.id in by_id:
            previous = by_id[item.id]
            if replace(item, received_at=previous.received_at) != previous:
                raise ValueError(f"conflicting observation ID at line {number}")
            if item.received_at < previous.received_at:
                by_id[item.id] = item
            continue
        by_id[item.id] = item
    items = tuple(by_id.values())
    if len({i.synthetic for i in items}) > 1:
        raise ValueError("do not mix real and synthetic observations")
    return tuple(items)


def analyse_observations(
    items: tuple[LoopGlucose, ...], *, as_of: datetime, generated_at: datetime
) -> dict:
    """Availability-order Bayesian local-level baseline; fixed unvalidated assumptions.

    A delayed sample remains in history but does not retroactively update an issued
    online belief. No model is fitted on future observations or selected by its score.
    """
    if as_of.tzinfo is None or generated_at.tzinfo is None or as_of > generated_at:
        raise ValueError("aware cutoff no later than generation required")
    pending = sorted(
        (i for i in items if i.received_at <= as_of),
        key=lambda i: (i.received_at, i.event_at, i.id),
    )
    history, snapshots, scores, issues = [], [], [], []
    seen_times, mean, variance, previous, parent = {}, None, 25.0, None, None
    # Conflicting same-time values are quarantined before any update at that arrival time.
    for item in pending:
        seen_times.setdefault((item.received_at, item.event_at), set()).add(
            (item.value, item.condition)
        )
    used_events = {}
    for item in pending:
        history.append(
            {
                "id": item.id,
                "event_at": item.event_at.isoformat(),
                "received_at": item.received_at.isoformat(),
                "mg_dl": item.value,
                "display_only": item.display_only,
                "was_user_entered": item.user_entered,
                "condition": item.condition,
                "trend": item.trend,
            }
        )
        if item.display_only or item.user_entered or item.condition is not None:
            issues.append({"id": item.id, "reason": "quality_excluded_from_model"})
            continue
        if len(seen_times[(item.received_at, item.event_at)]) > 1:
            issues.append({"id": item.id, "reason": "conflicting_same_time_reading"})
            continue
        if item.event_at in used_events:
            issues.append(
                {
                    "id": item.id,
                    "reason": "duplicate_event"
                    if used_events[item.event_at] == item.value
                    else "later_conflicting_revision",
                }
            )
            continue
        if previous and item.event_at <= previous.event_at:
            issues.append({"id": item.id, "reason": "delayed_sample_history_only"})
            continue
        if previous:
            elapsed = (item.event_at - previous.event_at).total_seconds() / 60
            prior_variance = variance + 4.0 * elapsed
            if elapsed > 7.5:
                issues.append({"id": item.id, "reason": "gap", "minutes": elapsed})
            # Previous belief predicts this event only if issued before the event itself.
            if previous.received_at < item.event_at:
                scores.append(
                    {
                        "input_snapshot_id": parent,
                        "observation_id": item.id,
                        "issued_at": previous.received_at.isoformat(),
                        "target_at": item.event_at.isoformat(),
                        "mean_mg_dl": mean,
                        "observed_mg_dl": item.value,
                        "error_mg_dl": item.value - mean,
                        "horizon_minutes": elapsed,
                        "variance_mg_dl2": prior_variance + 25.0,
                    }
                )
            gain = prior_variance / (prior_variance + 25.0)
            mean += gain * (item.value - mean)
            variance = (1 - gain) * prior_variance
        else:
            mean = item.value
        used_events[item.event_at] = item.value
        identifier = "glucose-" + item.id
        snapshots.append(
            {
                "snapshot_id": identifier,
                "parent_snapshot_id": parent,
                "added_observation_id": item.id,
                "target_at": item.event_at.isoformat(),
                "evidence_cutoff": item.received_at.isoformat(),
                "model_version": "g6-local-level-v1",
                "mean_mg_dl": mean,
                "variance_mg_dl2": variance,
                "inference_kind": "availability_order_replay",
                "calibration": "UNVALIDATED_ASSUMPTIONS",
                "shadow_only": True,
                "may_actuate_insulin": False,
            }
        )
        parent, previous = identifier, item
    return {
        "schema_version": 1,
        "label": "RESEARCH ONLY — NOT TREATMENT RECOMMENDATIONS",
        "generated_at": generated_at.isoformat(),
        "as_of": as_of.isoformat(),
        "history": history,
        "snapshots": snapshots,
        "comparisons": scores,
        "quality": issues,
        "unavailable_records": len(items) - len(pending),
        "latest_usable_age_minutes": (as_of - previous.event_at).total_seconds() / 60
        if previous
        else None,
        "assumptions": {
            "process_variance_mg_dl2_per_minute": 4.0,
            "measurement_variance_mg_dl2": 25.0,
        },
        "limitations": [
            "uncalibrated statistical baseline; no physiological or dosing model",
            "phone reception time is not LIVE Mac availability time",
            "delayed samples retained, not backdated into issued beliefs",
            "retrospective replay is not prospective clinical validation",
        ],
        "shadow_only": True,
        "may_actuate_insulin": False,
    }


def replay_file(
    path: str,
    output: str,
    *,
    consent: bool,
    synthetic_only: bool = False,
    cutoff: str | None = None,
) -> None:
    """Owner-selected local file in, exclusive private derivative out; no stdout data."""
    if consent == synthetic_only or (consent and os.environ.get("GITHUB_ACTIONS") == "true"):
        raise ValueError(
            "choose synthetic input or explicit local health-data consent; no real data in CI"
        )
    source, target = Path(path).expanduser().absolute(), Path(output).expanduser().absolute()
    if any(
        part in {"CloudStorage", "Mobile Documents", "Dropbox", "OneDrive", "Google Drive"}
        or part.startswith("OneDrive - ")
        for candidate in (source, target)
        for part in candidate.parts
    ):
        raise ValueError("choose local storage outside cloud-sync folders")
    for candidate in (source, target):
        if any(p.is_symlink() for p in (candidate, *candidate.parents)):
            raise ValueError("symlink paths are not accepted")
    for candidate in (target, source) if consent else (target,):
        if any((p / ".git").exists() for p in (candidate, *candidate.parents)):
            raise ValueError("keep private observations and outputs outside Git repositories")
    descriptor = os.open(source, os.O_RDONLY | os.O_NOFOLLOW | os.O_NONBLOCK)
    with os.fdopen(descriptor, "rb") as stream:
        metadata = os.fstat(stream.fileno())
        if not stat.S_ISREG(metadata.st_mode):
            raise ValueError("observation source must be a regular local file")
        if metadata.st_size > 25_000_000:
            raise ValueError("observation file exceeds 25MB limit")
        raw = stream.read(25_000_001)
    items = decode_observations(raw, consent=consent)
    now = datetime.now(timezone.utc)
    result = analyse_observations(items, as_of=instant(cutoff) if cutoff else now, generated_at=now)
    result["input_sha256"] = hashlib.sha256(raw).hexdigest()
    result["live_mac_available_at"] = now.isoformat()
    result["duplicate_records"] = sum(bool(line.strip()) for line in raw.splitlines()) - len(items)
    # Keep the phone's raw observations unchanged; never replace an earlier report.
    descriptor = os.open(target, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
    with os.fdopen(descriptor, "w") as stream:
        json.dump(result, stream, sort_keys=True, allow_nan=False)
        stream.write("\n")
