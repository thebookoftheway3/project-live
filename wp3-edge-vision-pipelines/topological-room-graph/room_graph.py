# SPDX-License-Identifier: AGPL-3.0-only
"""Local synthetic cascade and expiring portal tokens; no raw-media exporter."""

from dataclasses import dataclass
from math import isfinite

STAGES = ("zone", "pose", "targeted_reid", "vlm")


def cascade(stage: str, *, unresolved: bool, consent: bool, remaining_calls: int):
    if stage not in STAGES or type(unresolved) is not bool or type(consent) is not bool:
        raise ValueError("known stage and explicit booleans required")
    if type(remaining_calls) is not int or remaining_calls < 0:
        raise ValueError("nonnegative integer budget required")
    if not consent or not unresolved or remaining_calls == 0 or stage == STAGES[-1]:
        return None
    return STAGES[STAGES.index(stage) + 1]


@dataclass(frozen=True)
class PortalToken:
    source_zone: str
    target_zone: str
    issued_at: float
    expires_at: float


def pass_portal(token: PortalToken, *, now: float, allowed_edges, consent: bool):
    """Tokens contain zone continuity only, never faces, embeddings or identities."""
    if not all(
        type(t) in (int, float) and isfinite(t) for t in (now, token.issued_at, token.expires_at)
    ):
        raise ValueError("finite times required")
    if not 0 <= token.issued_at < token.expires_at or token.expires_at - token.issued_at > 30:
        raise ValueError("positive portal lifetime at most 30 seconds required")
    if consent is not True or not token.issued_at <= now < token.expires_at:
        return None
    if (token.source_zone, token.target_zone) not in allowed_edges:
        return None
    return token.target_zone


def export_event(event):
    """Allowlist a synthetic derived envelope; arbitrary strings cannot carry media.

    Schema rejection is not a network isolation proof. Real-node egress remains
    disabled pending packet-capture and deployment evidence.
    """
    if type(event) is not dict or set(event) != {"schema_version", "kind", "synthetic"}:
        raise ValueError("only the minimal derived envelope may cross this boundary")
    if type(event["schema_version"]) is not int or event["schema_version"] != 1:
        raise ValueError("unsupported schema")
    if event["synthetic"] is not True or event["kind"] not in ("zone_transition", "meal_candidate"):
        raise ValueError("synthetic enumerated events only")
    return dict(event)
