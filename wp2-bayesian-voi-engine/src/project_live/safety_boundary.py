"""Physically disconnected simulated command boundary.

Intentional strong limitation: every pump command is denied, in all environments.
Never replace this class with a permissive adapter for clinical use.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class Authorization:
    permitted: bool
    reason: str


class NoPumpAccess:
    def authorize(self, action: str, environment: str = "mobile") -> Authorization:
        return Authorization(False, "SIMULATION_ONLY_NO_PUMP_CONNECTION")

    def execute(self, action: str) -> None:
        raise PermissionError("NoPumpAccess: live insulin delivery intentionally unavailable")
