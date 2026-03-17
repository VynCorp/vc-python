from __future__ import annotations

from vynco.types.shared import VyncoModel


class CreditBalance(VyncoModel):
    """Current credit balance and tier information."""

    balance: int
    monthly_credits: int
    used_this_month: int
    tier: str = ""
    overage_rate: float = 0.0


class UsageOperation(VyncoModel):
    """A single operation's credit usage."""

    operation: str = ""
    count: int = 0
    credits: int = 0


class UsageBreakdown(VyncoModel):
    """Credit usage breakdown by operation type."""

    operations: list[UsageOperation] = []
    total_debited: int = 0
    period: str | None = None
