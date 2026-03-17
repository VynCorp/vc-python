from __future__ import annotations

from vynco.types.shared import VyncoModel


class Team(VyncoModel):
    """A team/organization in VynCo."""

    id: str
    name: str = ""
    slug: str = ""
    tier: str = ""
    credit_balance: int = 0
    monthly_credits: int = 0
    overage_rate: float = 0.0
    created_at: str = ""
