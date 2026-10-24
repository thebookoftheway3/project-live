"""Finite synthetic joint belief; in-process module boundaries follow ADR 0001."""

from dataclasses import dataclass
from datetime import datetime
from itertools import product
from math import isfinite

MODEL_VERSION = "beverage-toy-v1"
LIKELIHOOD_VERSION = "synthetic-table-v1"
STATES = tuple(
    product(
        ("regular", "diet", "unknown"), ("none", "partial", "full"), ("self", "other", "unknown")
    )
)
PRIOR = tuple(a * b * c for a, b, c in product((0.25, 0.25, 0.5), (0.5, 0.3, 0.2), (0.4, 0.3, 0.3)))


def condition(prior: tuple[float, ...], likelihood: tuple[float, ...]) -> tuple[float, ...] | None:
    """Bayes' rule over the complete joint table; impossible evidence stays unknown."""
    if len(prior) != len(STATES) or len(likelihood) != len(STATES):
        raise ValueError("one probability/likelihood per joint state required")
    if any(not isfinite(x) or x < 0 for x in prior + likelihood):
        raise ValueError("finite nonnegative probabilities and likelihoods required")
    if abs(sum(prior) - 1) > 1e-9 or any(x > 1 for x in likelihood):
        raise ValueError("normalized prior and observation probabilities required")
    weights = tuple(p * likelihood[i] for i, p in enumerate(prior))
    total = sum(weights)
    return tuple(x / total for x in weights) if total > 0 else None


def likelihoods(finding: str) -> tuple[float, ...]:
    """Declared toy observation probabilities, never a provider score conversion."""
    if finding == "can_opening":
        return tuple(
            (0.8 if identity != "unknown" else 0.4) * (0.3 if amount == "none" else 0.6)
            for identity, amount, _ in STATES
        )
    if finding in ("regular_image", "diet_image"):
        matching = finding.split("_")[0]
        return tuple(
            0.8 if identity == matching else 0.2 if identity == "unknown" else 0.1
            for identity, _, _ in STATES
        )
    if finding == "weight_decrease":
        return tuple({"none": 0.2, "partial": 0.7, "full": 0.5}[amount] for _, amount, _ in STATES)
    raise ValueError("no declared likelihood mapping for finding")


@dataclass(frozen=True)
class Evidence:
    id: str
    finding: str
    source_ids: tuple[str, ...]
    dependence_groups: tuple[str, ...]
    available_at: datetime
    sensor_version: str

    def __post_init__(self):
        if not self.id or not self.sensor_version or self.available_at.tzinfo is None:
            raise ValueError("versioned evidence with an aware availability time required")
        for items in (self.source_ids, self.dependence_groups):
            if (
                type(items) is not tuple
                or not items
                or any(type(x) is not str or not x for x in items)
            ):
                raise ValueError("immutable nonempty provenance tuples required")
            if len(items) != len(set(items)):
                raise ValueError("duplicate provenance entries")


@dataclass(frozen=True)
class Snapshot:
    id: str
    cutoff: datetime
    probabilities: tuple[float, ...]
    evidence: tuple[Evidence, ...]

    def record(self) -> dict:
        return {
            "snapshot_id": self.id,
            "inference_kind": "online_filter",
            "evidence_cutoff": self.cutoff.isoformat(),
            "model_version": MODEL_VERSION,
            "likelihood_version": LIKELIHOOD_VERSION,
            "calibration": "SYNTHETIC_UNCALIBRATED",
            "shadow_only": True,
            "may_actuate_insulin": False,
            "physiological_forecast": None,
            "posterior": [
                {"identity": s[0], "quantity": s[1], "actor": s[2], "p": p}
                for s, p in zip(STATES, self.probabilities)
            ],
            "evidence_manifest": [
                {
                    "id": e.id,
                    "source_ids": list(e.source_ids),
                    "available_at": e.available_at.isoformat(),
                    "dependence_groups": list(e.dependence_groups),
                    "sensor_version": e.sensor_version,
                }
                for e in self.evidence
            ],
        }


class JointBelief:
    def __init__(self):
        self.probabilities = PRIOR
        self.evidence: tuple[Evidence, ...] = ()

    def admit(self, evidence: Evidence, cutoff: datetime) -> str:
        if cutoff.tzinfo is None:
            raise ValueError("aware evidence cutoff required")
        if evidence.available_at > cutoff:
            return "future_evidence_withheld"
        for previous in self.evidence:
            if previous.id == evidence.id:
                if previous != evidence:
                    raise ValueError("conflicting evidence ID")
                return "duplicate"
        leaves = {leaf for item in self.evidence for leaf in item.source_ids}
        groups = {group for item in self.evidence for group in item.dependence_groups}
        if leaves.intersection(evidence.source_ids) or groups.intersection(
            evidence.dependence_groups
        ):
            return "dependent_evidence_withheld"
        posterior = condition(self.probabilities, likelihoods(evidence.finding))
        if posterior is None:
            return "impossible_evidence_unknown"
        self.probabilities = posterior
        self.evidence += (evidence,)
        return "admitted"

    def snapshot(self, identifier: str, cutoff: datetime) -> Snapshot:
        if cutoff.tzinfo is None:
            raise ValueError("aware snapshot cutoff required")
        if any(item.available_at > cutoff for item in self.evidence):
            raise ValueError("cannot backdate a snapshot after admitting later evidence")
        return Snapshot(identifier, cutoff, self.probabilities, self.evidence)

    def image_benefit(self) -> float:
        # A deterministic ambiguity heuristic, not measured value of information.
        masses = [
            sum(p for state, p in zip(STATES, self.probabilities) if state[0] == identity)
            for identity in ("regular", "diet", "unknown")
        ]
        return 1 - max(masses)
