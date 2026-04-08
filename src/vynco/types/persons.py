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


class PersonSearchResult(VyncoModel):
    """A person search result."""

    id: str
    full_name: str = ""
    first_name: str | None = None
    last_name: str | None = None
    place_of_origin: str | None = None
    nationality: str | None = None
    role_count: int | None = None


class PersonRoleDetail(VyncoModel):
    """A person's role at a specific company."""

    company_uid: str = ""
    company_name: str | None = None
    role_function: str = ""
    role_category: str = ""
    signing_authority: str | None = None
    start_date: str | None = None
    end_date: str | None = None
    change_action: str | None = None
    is_current: bool | None = None


class PersonDetail(VyncoModel):
    """Detailed person record with roles across companies."""

    id: str
    full_name: str = ""
    first_name: str | None = None
    last_name: str | None = None
    place_of_origin: str | None = None
    residence: str | None = None
    nationality: str | None = None
    roles: list[PersonRoleDetail] = []
