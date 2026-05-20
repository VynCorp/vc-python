from __future__ import annotations

from vynco.types.dossiers import Citation
from vynco.types.shared import VyncoModel


class UboPerson(VyncoModel):
    """A natural person identified as an ultimate beneficial owner.

    ``controlling_entity_uid`` is the company the person directly controls.
    For Swiss entities this is a ``CHE-xxx.xxx.xxx`` UID. For non-Swiss
    parent entities resolved through GLEIF the identifier has the form
    ``LEI:<20-char-lei>`` — these are synthetic identifiers that do not
    resolve as UIDs against the companies endpoint.
    """

    person_id: str = ""
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
    ultimate_parent_lei: str | None = None
    ultimate_parent_name: str | None = None
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


class OpacityContributor(VyncoModel):
    """A single factor contributing to an opacity score."""

    code: str = ""
    description: str = ""
    points: int = 0


class ShellCompanyFlag(VyncoModel):
    """Shell-company heuristic outcome for the focus company."""

    depth: int = 0
    has_industry: bool = False
    rationale: str = ""


class FocusAnalytics(VyncoModel):
    """Graph-analytics metrics for the focus company."""

    pagerank: float = 0.0
    pagerank_rank: int = 0
    betweenness: float = 0.0
    community_index: int | None = None
    community_size: int = 0
    ubo_chain_depth: int = 0
    has_circular_ownership: bool = False
    shell_company: ShellCompanyFlag | None = None


class AnalysisAlgorithm(VyncoModel):
    """Provenance of the graph-analytics computation."""

    networkx_version: str = ""
    pagerank_alpha: float = 0.0
    louvain_seed: int = 0
    computed_at: str = ""


class GraphAnalyticsResponse(VyncoModel):
    """Network graph analytics for an ownership neighbourhood."""

    focus: FocusAnalytics = FocusAnalytics()
    node_count: int = 0
    edge_count: int = 0
    algorithm: AnalysisAlgorithm = AnalysisAlgorithm()
    pagerank: dict[str, float] = {}
    betweenness: dict[str, float] = {}
    communities: list[list[str]] = []


class UboAnalytics(VyncoModel):
    """Ownership opacity analytics for a company.

    ``opacity_level`` is one of ``transparent``, ``normal``, ``opaque``,
    ``highly_opaque``.
    """

    uid: str = ""
    company_name: str = ""
    opacity_score: int = 0
    opacity_level: str = ""
    pyramiding: bool = False
    pyramiding_rationale: str | None = None
    contributors: list[OpacityContributor] = []
    citations: list[Citation] = []
    obligation_refs: list[str] = []
    peer_percentile: int | None = None
    peer_sample_size: int = 0
    graph_analytics: GraphAnalyticsResponse | None = None
    assessed_at: str = ""
