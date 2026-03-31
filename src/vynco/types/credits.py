from __future__ import annotations

from vynco.types.shared import VyncoModel


class CreditBalance(VyncoModel):
    """Current credit balance and tier info."""

    balance: int = 0
    monthly_credits: int = 0
    used_this_month: int = 0
    tier: str = ""
    overage_rate: float = 0.0


class UsageRow(VyncoModel):
    """Credit usage for a single operation type."""

    operation: str = ""
    count: int = 0
    total_credits: int = 0


class UsagePeriod(VyncoModel):
    """Time period for usage data."""

    since: str = ""
    until: str = ""


class CreditUsage(VyncoModel):
    """Credit usage breakdown by operation type."""

    operations: list[UsageRow] = []
    total: int = 0
    period: UsagePeriod = UsagePeriod()


class CreditLedgerEntry(VyncoModel):
    """A single entry in the credit ledger."""

    id: int
    entry_type: str = ""
    amount: int = 0
    balance: int = 0
    description: str = ""
    created_at: str = ""


class CreditHistory(VyncoModel):
    """Credit ledger history."""

    items: list[CreditLedgerEntry] = []
    total: int = 0
