from __future__ import annotations

from pydantic import Field

from vynco.types.shared import VyncoModel


class GraphNode(VyncoModel):
    """A node in a company network graph."""

    id: str
    name: str = ""
    uid: str = ""
    node_type: str = Field("", alias="type")
    capital: float | None = None
    canton: str | None = None
    status: str | None = None
    role: str | None = None
    person_id: str | None = None


class GraphLink(VyncoModel):
    """A link in a company network graph."""

    source: str = ""
    target: str = ""
    link_type: str = Field("", alias="type")
    label: str = ""


class GraphResponse(VyncoModel):
    """Network graph response."""

    nodes: list[GraphNode] = []
    links: list[GraphLink] = []


class NetworkCluster(VyncoModel):
    """A cluster in a network analysis."""

    id: int = 0
    company_uids: list[str] = []
    shared_persons: list[str] = []


class NetworkAnalysisResponse(VyncoModel):
    """Network analysis response."""

    nodes: list[GraphNode] = []
    links: list[GraphLink] = []
    clusters: list[NetworkCluster] = []
