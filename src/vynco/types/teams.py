from __future__ import annotations

from vynco.types.shared import VyncoModel


class Team(VyncoModel):
    """A team/organization in VynCo."""

    id: str
    name: str = ""
    slug: str = ""
    tier: str = ""
    stripe_subscription_id: str | None = None
    current_period_end: str | None = None
    cancellation_effective_at: str | None = None


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
    """A team member listed in the billing summary."""

    user_id: str
    name: str = ""


class BillingSummary(VyncoModel):
    """Team billing summary."""

    tier: str = ""
    members: list[MemberUsage] = []


class JoinTeamResponse(VyncoModel):
    """Response from joining a team."""

    team_id: str = ""
    team_name: str = ""
    role: str = ""
