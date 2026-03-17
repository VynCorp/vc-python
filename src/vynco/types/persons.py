from __future__ import annotations

from vynco.types.shared import VyncoModel


class PersonRole(VyncoModel):
    """A person's role within a company."""

    person_id: str
    first_name: str = ""
    last_name: str = ""
    role: str = ""
    since: str | None = None
    until: str | None = None


class Person(VyncoModel):
    """A person with their associated company roles."""

    id: str
    first_name: str = ""
    last_name: str = ""
    roles: list[PersonRole] = []
