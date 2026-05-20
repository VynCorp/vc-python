from __future__ import annotations

from vynco.types.shared import VyncoModel


class GroupUsage(VyncoModel):
    """Usage statistics for a single rate-limit group."""

    group: str = ""
    used: int | None = None
    limit: int | None = None
    window: str = ""
    reset_seconds: int = 0


class UsageSnapshot(VyncoModel):
    """Current usage snapshot returned by GET /v1/usage/current."""

    tier: str = ""
    groups: list[GroupUsage] = []
