from __future__ import annotations

from vynco.types.shared import VyncoModel


class BoardMember(VyncoModel):
    """A board member of a company."""

    id: str
    first_name: str | None = None
    last_name: str | None = None
    role: str = ""
    role_category: str = ""
    origin: str | None = None
    residence: str | None = None
    signing_authority: str | None = None
    since: str | None = None
