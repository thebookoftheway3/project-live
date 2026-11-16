# SPDX-License-Identifier: AGPL-3.0-only
"""Finite EVSI oracle and deterministic synthetic prompt budget; no notifications."""

from collections import deque
from dataclasses import dataclass
from math import isclose, isfinite


def nonnegative(value: float) -> bool:
    return type(value) in (int, float) and isfinite(value) and value >= 0


def expected_value_of_sample_information(prior, likelihood, utilities) -> float:
    """EVSI = sum_y max_a sum_s p(s)p(y|s)u(a,s) - max_a sum_s p(s)u(a,s).

    Rows of likelihood are states, columns are possible answers. Utilities share
    one declared scale with attention cost. This is decision utility, not entropy.
    """
    if not prior or not all(nonnegative(p) for p in prior) or not isclose(sum(prior), 1):
        raise ValueError("normalized prior required")
    if len(likelihood) != len(prior) or not likelihood[0]:
        raise ValueError("state/answer matrix required")
    answers = len(likelihood[0])
    if any(
        len(row) != answers or not all(nonnegative(p) for p in row) or not isclose(sum(row), 1)
        for row in likelihood
    ):
        raise ValueError("normalized answer likelihoods required")
    if not utilities or any(
        len(row) != len(prior) or any(type(u) not in (int, float) or not isfinite(u) for u in row)
        for row in utilities
    ):
        raise ValueError("finite action/state utilities required")
    baseline = max(sum(p * u for p, u in zip(prior, row)) for row in utilities)
    informed = sum(
        max(
            sum(prior[s] * likelihood[s][y] * row[s] for s in range(len(prior)))
            for row in utilities
        )
        for y in range(answers)
    )
    result = informed - baseline
    if not isfinite(result):
        raise ValueError("utility arithmetic overflow")
    return max(0.0, result)


def attention_cost(base: float, context_multiplier: float, recent_interruptions: int) -> float:
    if (
        not nonnegative(base)
        or not nonnegative(context_multiplier)
        or type(recent_interruptions) is not int
        or recent_interruptions < 0
    ):
        raise ValueError("finite nonnegative costs and integer count required")
    result = base * context_multiplier * (1 + recent_interruptions)
    if not isfinite(result):
        raise ValueError("cost arithmetic overflow")
    return result


@dataclass(frozen=True)
class Decision:
    dispatch: bool
    reason: str
    answers: tuple[str, str] = ("Yes", "No")


class AttentionGate:
    """One session, one caller; emitted candidates consume budget, even unanswered.

    The caller owns monotonic time and explicit consent. No clinical alarms enter
    this gate. State is not durable; restarting is not a valid production reset.
    """

    def __init__(self, *, cooldown_seconds: float = 900, daily_limit: int = 3):
        if not nonnegative(cooldown_seconds) or cooldown_seconds <= 0:
            raise ValueError("positive finite cooldown required")
        if type(daily_limit) is not int or not 1 <= daily_limit <= 100:
            raise ValueError("daily limit must be 1..100")
        self.cooldown = cooldown_seconds
        self.limit = daily_limit
        self._emitted = deque()
        self._last_time = None
        self._last_dispatch = None

    def consider(self, *, now: float, evidence_id: str, evsi: float, cost: float, consent: bool):
        if not all(nonnegative(v) for v in (now, evsi, cost)):
            raise ValueError("finite nonnegative time, EVSI and cost required")
        if type(evidence_id) is not str or not 1 <= len(evidence_id) <= 128:
            raise ValueError("bounded evidence ID required")
        if type(consent) is not bool:
            raise ValueError("explicit boolean consent required")
        if self._last_time is not None and now < self._last_time:
            raise ValueError("clock regression")
        self._last_time = now
        while self._emitted and now - self._emitted[0][0] >= 86400:
            self._emitted.popleft()
        if not consent:
            return Decision(False, "consent_denied")
        if any(identifier == evidence_id for _, identifier in self._emitted):
            return Decision(False, "duplicate_evidence")
        if evsi <= cost:
            return Decision(False, "insufficient_value")
        if self._last_dispatch is not None and now - self._last_dispatch < self.cooldown:
            return Decision(False, "cooldown")
        if len(self._emitted) >= self.limit:
            return Decision(False, "daily_budget")
        self._emitted.append((now, evidence_id))
        self._last_dispatch = now
        return Decision(True, "synthetic_candidate_only")
