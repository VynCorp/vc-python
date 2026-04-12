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

    # --- Enrichment provenance (v3.1+) ---
    # ``role_source`` is ``"zefix"`` for source-extracted roles or ``"llm"``
    # for AI-inferred roles. Use ``role_confidence`` to gate UI treatment
    # (e.g. grey out low-confidence AI classifications).
    role_source: str | None = None
    role_confidence: float | None = None
    role_inferred_at: str | None = None


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

    # --- Enrichment provenance (v3.1+) ---
    role_source: str | None = None
    role_confidence: float | None = None
    role_inferred_at: str | None = None


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


class NetworkPerson(VyncoModel):
    """Summary of a person in a network response."""

    id: str
    full_name: str = ""
    first_name: str | None = None
    last_name: str | None = None


class NetworkCompany(VyncoModel):
    """A company in a person's network."""

    uid: str = ""
    name: str | None = None
    role: str = ""
    role_category: str = ""
    is_current: bool | None = None
    since: str | None = None
    until: str | None = None

    # --- Enrichment provenance (v3.1+) ---
    role_source: str | None = None
    role_confidence: float | None = None
    role_inferred_at: str | None = None


class CoDirectorCompany(VyncoModel):
    """A company shared between a person and a co-director."""

    uid: str = ""
    name: str | None = None


class CoDirector(VyncoModel):
    """A person who shares company directorships with the primary person."""

    person_id: str = ""
    name: str = ""
    shared_companies: int = 0
    companies: list[CoDirectorCompany] = []


class NetworkStats(VyncoModel):
    """Aggregate statistics for a person's network."""

    total_companies: int = 0
    active_roles: int = 0
    co_director_count: int = 0


class PersonNetworkResponse(VyncoModel):
    """Response for a person-centric network view."""

    person: NetworkPerson
    companies: list[NetworkCompany] = []
    co_directors: list[CoDirector] = []
    stats: NetworkStats
