from __future__ import annotations

from vynco.types.shared import VyncoModel


class CompanyRelationship(VyncoModel):
    """A relationship between two companies."""

    id: str
    source_company_uid: str
    source_company_name: str = ""
    target_company_uid: str
    target_company_name: str = ""
    relationship_type: str = ""
    source_lei: str | None = None
    target_lei: str | None = None
    data_source: str = ""
    is_active: bool = True
    start_date: str | None = None
    end_date: str | None = None


class RelationshipsResponse(VyncoModel):
    """Wrapper returned by relationships and hierarchy endpoints."""

    company_uid: str
    relationships: list[CompanyRelationship] = []
    total: int = 0
