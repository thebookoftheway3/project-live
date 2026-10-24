"""Immutable scalar synthetic samples and an inert, local mock image provider."""

from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from math import isfinite


def instant(value: str) -> datetime:
    if not isinstance(value, str):
        raise ValueError("timestamp must be a string")
    result = datetime.fromisoformat(value.replace("Z", "+00:00"))
    if result.tzinfo is None:
        raise ValueError("timezone-aware timestamp required")
    return result.astimezone(timezone.utc)


@dataclass(frozen=True)
class Sample:
    id: str
    kind: str
    source: str
    event_at: datetime
    available_at: datetime
    sequence: int
    value: str | float
    permitted: bool
    retain_until: datetime
    dependence_group: str

    def __post_init__(self):
        if any(type(x) is not str or not x for x in (self.id, self.source, self.dependence_group)):
            raise ValueError("nonempty source identifiers required")
        if self.kind not in {"door", "audio", "frame", "scale"}:
            raise ValueError("unknown synthetic sample kind")
        if type(self.sequence) is not int or self.sequence < 0 or type(self.permitted) is not bool:
            raise ValueError("explicit sequence and permission required")
        if any(t.tzinfo is None for t in (self.event_at, self.available_at, self.retain_until)):
            raise ValueError("aware sample timestamps required")
        if self.available_at < self.event_at:
            raise ValueError("availability cannot predate observation")
        if self.kind == "scale":
            if type(self.value) not in (int, float) or not isfinite(self.value) or self.value < 0:
                raise ValueError("finite nonnegative synthetic weight required")
        elif type(self.value) is not str:
            raise ValueError("immutable scalar feature required")

    @classmethod
    def parse(cls, obj: dict) -> "Sample":
        if obj.get("synthetic") is not True:
            raise ValueError("synthetic samples only")
        for field in ("id", "source", "dependence_group"):
            if type(obj.get(field)) is not str or not obj[field]:
                raise ValueError(f"nonempty {field} required")
        if obj.get("kind") not in {"door", "audio", "frame", "scale"}:
            raise ValueError("unknown synthetic sample kind")
        if type(obj.get("sequence")) is not int or obj["sequence"] < 0:
            raise ValueError("nonnegative integer sequence required")
        if type(obj.get("permitted")) is not bool:
            raise ValueError("explicit permission required")
        value = obj.get("value")
        if obj["kind"] == "scale":
            if type(value) not in (int, float) or not isfinite(value) or value < 0:
                raise ValueError("finite nonnegative synthetic weight required")
            value = float(value)
        elif type(value) is not str:
            raise ValueError("synthetic feature/reference must be a string")
        event_at, available_at = instant(obj["event_at"]), instant(obj["available_at"])
        if available_at < event_at:
            raise ValueError("availability cannot predate observation")
        return cls(
            obj["id"],
            obj["kind"],
            obj["source"],
            event_at,
            available_at,
            obj["sequence"],
            value,
            obj["permitted"],
            instant(obj["retain_until"]),
            obj["dependence_group"],
        )

    def access_reason(self, now: datetime) -> str | None:
        if not self.permitted:
            return "permission_denied"
        if now >= self.retain_until:
            return "expired"
        if now < self.available_at:
            return "unavailable"
        return None


@dataclass(frozen=True)
class Policy:
    max_calls: int = 1
    min_benefit: float = 0.3
    allow_image: bool = True
    revoked_at: datetime | None = None

    def __post_init__(self):
        if type(self.max_calls) is not int or not 0 <= self.max_calls <= 1:
            raise ValueError("at most one mock call")
        if (
            type(self.min_benefit) not in (int, float)
            or not isfinite(self.min_benefit)
            or not 0 <= self.min_benefit <= 1
        ):
            raise ValueError("finite benefit threshold in [0,1] required")
        if type(self.allow_image) is not bool:
            raise ValueError("explicit image permission required")
        if self.revoked_at is not None and self.revoked_at.tzinfo is None:
            raise ValueError("aware revocation timestamp required")

    @classmethod
    def parse(cls, obj: dict) -> "Policy":
        calls, benefit, allow = (
            obj.get("max_calls", 1),
            obj.get("min_benefit", 0.3),
            obj.get("allow_image", True),
        )
        if type(calls) is not int or not 0 <= calls <= 1:
            raise ValueError("this increment permits at most one mock call")
        if type(benefit) not in (int, float) or not isfinite(benefit) or not 0 <= benefit <= 1:
            raise ValueError("finite benefit threshold in [0,1] required")
        if type(allow) is not bool:
            raise ValueError("explicit boolean image permission required")
        revoked = instant(obj["revoked_at"]) if obj.get("revoked_at") else None
        return cls(calls, float(benefit), allow, revoked)

    def permits(self, at: datetime) -> bool:
        return self.allow_image and (self.revoked_at is None or at < self.revoked_at)


@dataclass(frozen=True)
class MockResult:
    status: str
    finding: str | None
    available_at: datetime


class MockImageProvider:
    version = "inert-image-mock-v1"

    def __init__(self, outcome: str = "ok"):
        if outcome not in {"ok", "unknown", "timeout", "refused", "invalid_output"}:
            raise ValueError("unknown mock outcome")
        self.outcome = outcome
        self.calls = 0
        self.payload_reads = 0

    def infer(self, frame: Sample, now: datetime, policy: Policy) -> MockResult:
        # Guard the exposed provider entry point as well as the planner.
        if frame.kind != "frame" or frame.access_reason(now) or not policy.permits(now):
            return MockResult("denied", None, now)
        if self.calls >= policy.max_calls:
            return MockResult("budget_exhausted", None, now)
        self.calls += 1
        self.payload_reads += 1
        completed = now + timedelta(seconds=1)
        if not policy.permits(completed) or frame.access_reason(completed):
            return MockResult("permission_or_retention_changed", None, completed)
        if self.outcome != "ok":
            return MockResult(self.outcome, None, completed)
        finding = {
            "synthetic-frame-regular": "regular_image",
            "synthetic-frame-diet": "diet_image",
        }.get(frame.value)
        return MockResult("ok" if finding else "invalid_output", finding, completed)
