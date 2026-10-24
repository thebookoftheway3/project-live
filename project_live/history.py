"""One synthetic historical episode, under ADRs 0001/0002/0003; no storage service.

The static two-node trajectory is (earlier beverage state, later explanation).
All probabilities are declared toy assumptions, not physiological likelihoods.
"""

import json
from dataclasses import dataclass
from datetime import datetime, timedelta
from pathlib import Path

from .bayes import PRIOR, STATES, Evidence, likelihoods
from .safety_boundary import NoPumpAccess
from .sensing import MockImageProvider, Policy, Sample, instant

EXPLANATIONS = ("earlier_beverage", "activity", "sensor_or_model_error", "unresolved")
MODEL = "history-two-node-toy-v1"
QUESTION = "retained-beverage-identity-v1"


def trajectory_prior() -> tuple[float, ...]:
    weights = []
    for state, probability in zip(STATES, PRIOR):
        compatible = state[0] == "regular" and state[1] != "none" and state[2] == "self"
        conditional = (0.6, 0.15, 0.15, 0.1) if compatible else (0.05, 0.3, 0.3, 0.35)
        weights.extend(probability * p for p in conditional)
    return tuple(weights)


@dataclass(frozen=True)
class BeliefView:
    """Immutable JSON value; each export is detached (ADR 0003 ownership rule)."""

    serialized: str

    def record(self) -> dict:
        return json.loads(self.serialized)


def view(identifier, target, cutoff, evidence, *, retrospective=False, parents=()) -> BeliefView:
    """Reconstruct once from unique independent leaves actually available by cutoff."""
    if target.tzinfo is None or cutoff.tzinfo is None or target > cutoff:
        raise ValueError("aware target no later than knowledge cutoff required")
    weights = trajectory_prior()
    admitted, withheld = [], []
    ids, leaves, groups = {}, set(), set()
    for item in sorted(evidence, key=lambda e: (e.available_at, e.id)):
        if item.available_at > cutoff:
            continue
        if item.id in ids:
            if ids[item.id] != item:
                raise ValueError("conflicting evidence ID")
            continue
        ids[item.id] = item
        if leaves.intersection(item.source_ids) or groups.intersection(item.dependence_groups):
            withheld.append(item.id)
            continue
        if item.finding == "scripted_mismatch":
            factor = (0.8, 0.6, 0.4, 0.2) * len(STATES)
        else:
            factor = tuple(p for p in likelihoods(item.finding) for _ in EXPLANATIONS)
        products = tuple(p * q for p, q in zip(weights, factor))
        total = sum(products)
        if total <= 0:
            raise ValueError("impossible synthetic trajectory evidence")
        weights = tuple(p / total for p in products)
        leaves.update(item.source_ids)
        groups.update(item.dependence_groups)
        admitted.append(item)
    record = {
        "snapshot_id": identifier,
        "inference_kind": "retrospective_smoother" if retrospective else "online_filter",
        "target_at": target.isoformat(),
        "evidence_cutoff": cutoff.isoformat(),
        "parent_snapshot_ids": list(parents),
        "model_version": MODEL,
        "likelihood_version": "history-toy-tables-v1",
        "calibration": "SYNTHETIC_UNCALIBRATED",
        "shadow_only": True,
        "may_actuate_insulin": False,
        "physiological_forecast": None,
        "posterior": [
            {
                "identity": s[0],
                "quantity": s[1],
                "actor": s[2],
                "explanation": c,
                "p": weights[i * 4 + j],
            }
            for i, s in enumerate(STATES)
            for j, c in enumerate(EXPLANATIONS)
        ],
        "evidence_manifest": [
            {
                "id": e.id,
                "finding": e.finding,
                "source_ids": list(e.source_ids),
                "dependence_groups": list(e.dependence_groups),
                "available_at": e.available_at.isoformat(),
                "sensor_version": e.sensor_version,
            }
            for e in admitted
        ],
        "dependent_evidence_withheld": withheld,
    }
    return BeliefView(json.dumps(record, sort_keys=True, allow_nan=False))


@dataclass(frozen=True)
class RetainedFrame:
    sample: Sample
    representation: str
    payload_present: bool

    def __post_init__(self):
        if self.sample.kind != "frame" or type(self.payload_present) is not bool:
            raise ValueError("frame and explicit payload availability required")
        if type(self.representation) is not str:
            raise ValueError("representation identifier required")


@dataclass(frozen=True)
class Retrieval:
    frames: tuple[RetainedFrame, ...]
    exclusions: tuple[tuple[str | None, str], ...]

    def record(self):
        return {
            "eligible_ids": [f.sample.id for f in self.frames],
            "exclusions": [{"id": i, "reason": r} for i, r in self.exclusions],
            "coverage": "partial" if self.frames else "unavailable",
            "completeness": "not_established",
            "absence_is_negative_evidence": False,
        }


def retrieve(frames, start, end, as_of, now, policy) -> Retrieval:
    """Filter metadata before ranking or mock payload access; inclusive bounded window."""
    if any(t.tzinfo is None for t in (start, end, as_of, now)):
        raise ValueError("aware query timestamps required")
    if not start <= end <= as_of <= now or end - start > timedelta(hours=1):
        raise ValueError("bounded historical query no longer than one hour required")
    unique = {}
    for frame in frames:
        if frame.sample.id in unique and unique[frame.sample.id] != frame:
            raise ValueError("conflicting retained frame ID")
        unique[frame.sample.id] = frame
    eligible, excluded = [], []
    for frame in sorted(unique.values(), key=lambda f: (f.sample.event_at, f.sample.id)):
        sample = frame.sample
        if not start <= sample.event_at <= end:
            continue
        if sample.available_at > as_of:
            reason = "after_knowledge_cutoff"
        elif not policy.permits(now):
            reason = "current_permission_denied"
        elif sample.access_reason(now):
            reason = sample.access_reason(now)
        elif sample.source != "synthetic-camera" or frame.representation != "inert-frame-v1":
            reason = "incompatible_representation"
        elif not frame.payload_present:
            reason = "metadata_only"
        else:
            eligible.append(frame)
            continue
        # Revoked/expired metadata is not returned merely to explain a denial.
        visible_id = (
            None
            if reason in {"current_permission_denied", "permission_denied", "expired"}
            else sample.id
        )
        excluded.append((visible_id, reason))
    return Retrieval(tuple(eligible), tuple(excluded))


def run_history_fixture(path: str | Path, *, cutoff: str | None = None) -> dict:
    return run_history(
        json.loads(Path(path).read_text()), cutoff=instant(cutoff) if cutoff else None
    )


def run_history(obj: dict, *, cutoff: datetime | None = None) -> dict:
    """Replay a fixed synthetic schedule. Truth labels never enter inference."""
    if obj.get("synthetic") is not True or obj.get("schema_version") != 1:
        raise ValueError("versioned synthetic history fixture required")
    times = {
        key: instant(obj[key])
        for key in ("target_at", "online_at", "mismatch_at", "query_at", "execute_at", "smooth_at")
    }
    target, online, mismatch, query, execute, smooth = times.values()
    if not target <= online < mismatch < query <= execute < smooth:
        raise ValueError("chronological fixture schedule required")
    cutoff = smooth if cutoff is None else cutoff
    if cutoff.tzinfo is None or cutoff < online:
        raise ValueError("cutoff must include the first online snapshot")
    policy = Policy.parse(obj.get("policy", {}))
    provider = MockImageProvider(obj.get("mock_outcome", "ok"))
    sensor_available = instant(obj["sensor_available_at"])
    forecast = obj["scripted_forecast"]
    # A sealed fixture stimulus, not a computed physiological prediction.
    if (
        forecast.get("id") != "synthetic-forecast-v1"
        or instant(forecast["issued_at"]) > online
        or forecast.get("expected") != "stable"
    ):
        raise ValueError("known scripted forecast sealed by online time required")
    forecast_record = {
        "id": forecast["id"],
        "issued_at": forecast["issued_at"],
        "expected": "stable",
        "kind": "supplied_synthetic_stimulus",
    }
    evidence = []
    trigger = tuple(Sample.parse(s) for s in obj["trigger_samples"])
    if len(trigger) != 2 or trigger[0].kind != "door" or trigger[1].kind != "audio":
        raise ValueError("one ordered door/audio pair required")
    door, audio = trigger
    if door.id == audio.id or not target <= door.event_at <= audio.event_at <= online:
        raise ValueError("distinct trigger leaves within online episode required")
    if (
        all(s.access_reason(online) is None for s in trigger)
        and door.value == "open"
        and audio.value == "can_opening"
    ):
        evidence.append(
            Evidence(
                "opening",
                "can_opening",
                (door.id, audio.id),
                tuple(sorted({s.dependence_group for s in trigger})),
                max(s.available_at for s in trigger),
                "cheap-opening-v1",
            )
        )
    first = view("online_1230", target, online, evidence)
    snapshots = [first]
    decisions = [{"at": online.isoformat(), "selected": "stop", "reason": "low_interest_fixture"}]
    retrieval_record, interpretation = None, None
    if mismatch <= cutoff:
        evidence.append(
            Evidence(
                "mismatch",
                "scripted_mismatch",
                ("synthetic-later-observation",),
                ("later-observation",),
                mismatch,
                "scripted-comparator-v1",
            )
        )
        second = view("online_1430", target, mismatch, evidence)
        snapshots.append(second)
    if query <= cutoff:
        # Fixed fixture utilities, not estimated information gain or a general planner.
        candidates = {
            "bounded_history": 0.7,
            "fresh_sample": 0.2,
            "similar_episodes": 0.0,
            "stop": 0.0,
        }
        selected = "bounded_history"
        reason = "declared_fixture_utility"
        if not policy.permits(query):
            selected, reason = "stop", "current_permission_denied"
        elif policy.max_calls == 0:
            selected, reason = "stop", "budget_exhausted"
        elif policy.min_benefit >= candidates[selected]:
            selected, reason = "stop", "insufficient_benefit"
        elif sensor_available > online:
            selected, reason = "stop", "sensor_not_in_original_model"
        decisions.append(
            {
                "at": query.isoformat(),
                "trigger_evidence_id": "mismatch",
                "candidates": candidates,
                "selected": selected,
                "reason": reason,
            }
        )
        if selected == "bounded_history":
            frames = tuple(
                RetainedFrame(Sample.parse(f["sample"]), f["representation"], f["payload_present"])
                for f in obj["retained_frames"]
            )
            found = retrieve(
                frames,
                instant(obj["window_start"]),
                instant(obj["window_end"]),
                query,
                query,
                policy,
            )
            retrieval_record = found.record()
            retrieval_record.update(
                {
                    "window_start": instant(obj["window_start"]).isoformat(),
                    "window_end": instant(obj["window_end"]).isoformat(),
                    "knowledge_as_of": query.isoformat(),
                    "query_at": query.isoformat(),
                }
            )
            ranked = sorted(
                found.frames, key=lambda f: (abs(f.sample.event_at - target), f.sample.id)
            )
            if ranked and execute + timedelta(seconds=1) <= cutoff:
                frame = ranked[0].sample
                result = provider.infer(frame, execute, policy)
                interpretation = {
                    "status": result.status,
                    "target_at": frame.event_at.isoformat(),
                    "execution_started_at": execute.isoformat(),
                    "available_at": result.available_at.isoformat(),
                    "question_version": QUESTION,
                    "sensor_version": provider.version,
                    "sensor_available_at": sensor_available.isoformat(),
                    "source_ids": [frame.id],
                    "finding": result.finding,
                }
                if result.finding:
                    evidence.append(
                        Evidence(
                            "interpretation_later",
                            result.finding,
                            (frame.id,),
                            (frame.dependence_group,),
                            result.available_at,
                            provider.version,
                        )
                    )
            else:
                decisions.append(
                    {
                        "at": query.isoformat(),
                        "selected": "stop",
                        "reason": "no_usable_history" if not ranked else "result_after_cutoff",
                    }
                )
    if smooth <= cutoff:
        snapshots.append(
            view(
                "smoothed_1230_at_1431",
                target,
                smooth,
                evidence,
                retrospective=True,
                parents=(first.record()["snapshot_id"], second.record()["snapshot_id"]),
            )
        )
    return {
        "schema_version": 1,
        "fixture_id": "synthetic-history-v1",
        "status": "PARTIAL_LIVE_022",
        "shadow_only": True,
        "may_actuate_insulin": False,
        "policy_version": "history-single-call-heuristic-v1",
        "scripted_forecast": forecast_record,
        "knowledge_cutoff": cutoff.isoformat(),
        "snapshots": [s.record() for s in snapshots],
        "decisions": decisions,
        "retrieval": retrieval_record,
        "interpretation": interpretation,
        "provider_calls": provider.calls,
        "payload_reads": provider.payload_reads,
        "pump_authorization": NoPumpAccess().authorize("synthetic-history").permitted,
        "unimplemented": [
            "next_day_backfill",
            "sensor_version_comparison",
            "similar_episode_search",
            "fresh_policy_comparison",
            "physiological_forecasting",
            "clinical_calibration",
            "persistent_retention_or_erasure",
            "live_sensing",
        ],
    }
