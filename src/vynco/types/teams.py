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


class TeamMember(VyncoModel):
    """A member of a VynCo team."""

    id: str
    name: str = ""
    email: str = ""
    role: str = ""
    last_login_at: str | None = None


class Invitation(VyncoModel):
    """A team member invitation."""

    id: str
    team_id: str = ""
    email: str = ""
    role: str = ""
    token: str = ""
    status: str = ""
    created_at: str = ""
    expires_at: str = ""


class MemberUsage(VyncoModel):
    """Credit usage by a team member."""

    user_id: str
    name: str = ""
    credits_used: int = 0


class BillingSummary(VyncoModel):
    """Team billing summary."""

    tier: str = ""
    credit_balance: int = 0
    monthly_credits: int = 0
    used_this_month: int = 0
    members: list[MemberUsage] = []
