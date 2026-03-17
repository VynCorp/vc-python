from __future__ import annotations

from vynco.types.shared import VyncoModel


class UserProfile(VyncoModel):
    """The authenticated user's profile."""

    id: str
    name: str = ""
    email: str = ""
    avatar: str = ""
    plan: str = ""
    credit_balance: int = 0
