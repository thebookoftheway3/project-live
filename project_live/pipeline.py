"""First executable LIVE-022 increment: offline synthetic sensing, no actuation."""

import json
from datetime import datetime, timedelta
from pathlib import Path

from .bayes import Evidence, JointBelief
from .safety_boundary import NoPumpAccess
from .sensing import MockImageProvider, Policy, Sample, instant


def run_fixture(path: str | Path, *, cutoff: str | None = None) -> dict:
    fixture = json.loads(Path(path).read_text(encoding="utf-8"))
    if fixture.get("schema_version") != 1 or fixture.get("synthetic") is not True:
        raise ValueError("synthetic beverage fixture version 1 required")
    if type(fixture.get("fixture_id")) is not str or not fixture["fixture_id"]:
        raise ValueError("nonempty fixture version identifier required")
    samples = [Sample.parse(item) for item in fixture["samples"]]
    # Reference truth labels intentionally never reach the runner or estimator.
    result = run_samples(
        samples,
        Policy.parse(fixture.get("policy", {})),
        MockImageProvider(fixture.get("mock_outcome", "ok")),
        cutoff=instant(cutoff) if cutoff else None,
    )
    result["fixture_id"] = fixture["fixture_id"]
    return result


def run_samples(
    samples: list[Sample],
    policy: Policy,
    provider: MockImageProvider,
    *,
    cutoff: datetime | None = None,
) -> dict:
    if provider.calls or provider.payload_reads:
        raise ValueError("a fresh mock provider is required for reproducible run counters")
    unique = {}
    for sample in samples:
        if sample.id in unique and unique[sample.id] != sample:
            raise ValueError("conflicting observation ID")
        unique[sample.id] = sample
    ordered = sorted(unique.values(), key=lambda item: (item.available_at, item.sequence, item.id))
    order_keys = [(s.available_at, s.sequence) for s in ordered]
    if len(order_keys) != len(set(order_keys)):
        raise ValueError("equal-time observations require distinct recorded sequence numbers")
    belief = JointBelief()
    evidence_log, snapshots, decisions, observed = [], [], [], []
    door = None
    triggered = False
    frame = None
    scale_before = None
    attempted = False
    now = None

    def admit(identifier, finding, sources, at, sensor):
        evidence = Evidence(
            identifier,
            finding,
            tuple(s.id for s in sources),
            tuple(sorted({s.dependence_group for s in sources})),
            at,
            sensor,
        )
        outcome = belief.admit(evidence, at)
        evidence_log.append(
            {
                "id": identifier,
                "finding": finding,
                "status": outcome,
                "source_ids": list(evidence.source_ids),
                "dependence_groups": list(evidence.dependence_groups),
                "available_at": at.isoformat(),
                "sensor_version": sensor,
                "score_semantics": "DECLARED_SYNTHETIC_LIKELIHOOD_TABLE",
            }
        )

    for sample in ordered:
        if cutoff is not None and sample.available_at > cutoff:
            continue
        now = max(now, sample.available_at) if now else sample.available_at
        reason = sample.access_reason(now)
        observed.append(
            {
                "id": sample.id,
                "kind": sample.kind,
                "event_at": sample.event_at.isoformat(),
                "available_at": sample.available_at.isoformat(),
                "status": reason or "available",
            }
        )
        if reason:
            continue
        if sample.kind == "door" and sample.value == "open":
            door = sample
        elif (
            sample.kind == "audio"
            and door is not None
            and not door.access_reason(now)
            and sample.value == "can_opening"
        ):
            triggered = True
            admit(f"can:{sample.id}", "can_opening", [door, sample], now, "can-detector-v1")
        elif sample.kind == "frame":
            frame = sample
        elif sample.kind == "scale":
            if triggered and scale_before is not None and not scale_before.access_reason(now):
                if scale_before.source == sample.source and scale_before.value - sample.value >= 10:
                    admit(
                        f"weight:{sample.id}",
                        "weight_decrease",
                        [scale_before, sample],
                        now,
                        "weight-detector-v1",
                    )
            scale_before = sample
        if triggered and frame is not None and not attempted:
            benefit = belief.image_benefit()
            blocked = (
                frame.access_reason(now)
                or ("permission_denied" if not policy.permits(now) else None)
                or ("budget_exhausted" if provider.calls >= policy.max_calls else None)
                or ("no_expected_value" if benefit <= policy.min_benefit else None)
                or ("cutoff_deadline" if cutoff and now + timedelta(seconds=1) > cutoff else None)
            )
            decisions.append(
                {
                    "at": now.isoformat(),
                    "policy_version": "ambiguity-cost-v1",
                    "candidates": [
                        {"action": "stop", "benefit": 0, "cost": 0},
                        {"action": "repeat_audio", "benefit": 0, "cost": 1},
                        {"action": "mock_image", "benefit": benefit, "cost": 1},
                    ],
                    "selected": "stop" if blocked else "mock_image",
                    "reason": blocked or "highest_feasible_benefit_per_cost",
                }
            )
            attempted = True
            if not blocked:
                result = provider.infer(frame, now, policy)
                now = result.available_at
                if result.status == "ok":
                    admit(f"image:{frame.id}", result.finding, [frame], now, provider.version)
                else:
                    evidence_log.append(
                        {
                            "id": f"image:{frame.id}",
                            "status": result.status,
                            "finding": None,
                            "source_ids": [frame.id],
                            "available_at": now.isoformat(),
                            "sensor_version": provider.version,
                        }
                    )
        snapshots.append(belief.snapshot(f"online-{len(snapshots)}", now).record())
    decisions.append(
        {
            "selected": "stop",
            "policy_version": "ambiguity-cost-v1",
            "reason": "missing_camera"
            if triggered and frame is None
            else "no_trigger"
            if not triggered
            else "no_remaining_useful_candidate",
        }
    )
    return {
        "status": "PARTIAL_LIVE_022_SYNTHETIC_ONLY",
        "fixture_schema": 1,
        "run_policy": {
            "max_calls": policy.max_calls,
            "min_benefit": policy.min_benefit,
            "allow_image": policy.allow_image,
            "revoked_at": policy.revoked_at.isoformat() if policy.revoked_at else None,
        },
        "requested_cutoff": cutoff.isoformat() if cutoff else None,
        "observations": observed,
        "evidence": evidence_log,
        "snapshots": snapshots,
        "decisions": decisions,
        "provider_calls": provider.calls,
        "provider_payload_reads": provider.payload_reads,
        "costs": {
            "provenance": "SIMULATED",
            "logical_provider_seconds": provider.calls,
            "hardware_energy": None,
            "money": None,
            "human_attention": None,
        },
        "pump_authorization": NoPumpAccess().authorize("any_pump_action").permitted,
        "unimplemented": [
            "historical_query",
            "retrospective_smoothing",
            "next_day_backfill",
            "policy_comparison",
            "physiological_forecast",
            "clinical_calibration",
        ],
    }
