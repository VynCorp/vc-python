from __future__ import annotations

from vynco.types.shared import VyncoModel


class UboPerson(VyncoModel):
    """A natural person identified as an ultimate beneficial owner.

    ``controlling_entity_uid`` is the company the person directly controls.
    For Swiss entities this is a ``CHE-xxx.xxx.xxx`` UID. For non-Swiss
    parent entities resolved through GLEIF the identifier has the form
    ``LEI:<20-char-lei>`` — these are synthetic identifiers that do not
    resolve as UIDs against the companies endpoint.
    """

    person_id: int = 0
    name: str = ""
    controlling_entity_uid: str = ""
    controlling_entity_name: str = ""
    role: str = ""
    signing_authority: str | None = None
    path_length: int = 0


class ChainLink(VyncoModel):
    """A single link in an ownership chain.

    ``from_uid`` and ``to_uid`` are normally ``CHE-xxx.xxx.xxx`` UIDs, but
    foreign parents resolved through GLEIF appear as ``LEI:<20-char-lei>``
    synthetic identifiers. Use ``uid.startswith("LEI:")`` to detect these
    — they are not resolvable via ``companies.get()``.
    """

    from_uid: str = ""
    from_name: str = ""
    to_uid: str = ""
    to_name: str = ""
    depth: int = 0


class UboResponse(VyncoModel):
    """Ultimate beneficial owner resolution response.

    When the backend cannot fully resolve the chain (e.g. before the weekly
    GLEIF enrichment has run for this company, or because the company has
    no registered parent), ``data_coverage_note`` contains a human-readable
    explanation of what's populated and what's pending.
    """

    uid: str = ""
    company_name: str = ""
    ubo_persons: list[UboPerson] = []
    ownership_chain: list[ChainLink] = []
    chain_depth: int = 0
    risk_flags: list[str] = []
    data_coverage_note: str | None = None


class OwnershipEntity(VyncoModel):
    """A company entity in an ownership chain."""

    uid: str = ""
    name: str = ""
    canton: str | None = None
    status: str | None = None
    legal_form: str | None = None
    share_capital: float | None = None


class OwnershipLink(VyncoModel):
    """A single directional relationship in an ownership chain.

    ``source_uid`` and ``target_uid`` are usually Swiss UIDs but may be
    ``LEI:<lei>`` synthetic identifiers for non-Swiss parent entities
    resolved through GLEIF. ``relationship_type`` is one of
    ``head_office``, ``branch_office``, ``acquisition``, or ``gleif_parent``.
    """

    source_uid: str = ""
    source_name: str = ""
    target_uid: str = ""
    target_name: str = ""
    relationship_type: str = ""
    depth: int = 0


class PersonCompanyRole(VyncoModel):
    """A person's role at a specific company in an ownership chain."""

    company_uid: str = ""
    company_name: str = ""
    role: str = ""


class KeyPerson(VyncoModel):
    """A person with significant roles across the ownership chain."""

    name: str = ""
    companies: list[PersonCompanyRole] = []


class CircularFlag(VyncoModel):
    """A detected circular ownership pattern."""

    loop_uids: list[str] = []
    description: str = ""


class OwnershipResponse(VyncoModel):
    """Full ownership trace response (from POST /ownership/{uid})."""

    uid: str = ""
    company_name: str = ""
    ownership_chain: list[OwnershipLink] = []
    ultimate_parent: OwnershipEntity | None = None
    key_persons: list[KeyPerson] = []
    circular_flags: list[CircularFlag] = []
    risk_level: str = ""
    assessed_at: str = ""
