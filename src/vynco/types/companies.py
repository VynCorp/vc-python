from __future__ import annotations

from typing import Any

from pydantic import Field

from vynco.types.shared import VyncoModel


class Company(VyncoModel):
    """A Swiss company record."""

    uid: str
    name: str
    canton: str | None = None
    status: str | None = None
    legal_form: str | None = None
    share_capital: float | None = None
    currency: str | None = None
    purpose: str | None = None
    founding_date: str | None = None
    registration_date: str | None = None
    deletion_date: str | None = None
    legal_seat: str | None = None
    municipality: str | None = None
    data_source: str | None = None
    enrichment_level: str | None = None
    address_street: str | None = None
    address_house_number: str | None = None
    address_zip_code: str | None = None
    address_city: str | None = None
    address_canton: str | None = None
    website: str | None = None
    industry: str | None = None
    sub_industry: str | None = None
    employee_count: int | None = None
    auditor_name: str | None = None
    auditor_category: str | None = None
    latitude: float | None = None
    longitude: float | None = None
    geo_precision: str | None = None
    noga_code: str | None = None
    sanctions_hit: bool | None = None
    last_screened_at: str | None = None
    is_finma_regulated: bool | None = None
    ehraid: int | None = None
    chid: str | None = None
    cantonal_excerpt_url: str | None = None
    old_names: list[str] | None = None
    translations: list[str] | None = None
    updated_at: str | None = None


class CompanyCount(VyncoModel):
    """Company count response."""

    count: int


class CompanyStatistics(VyncoModel):
    """Aggregate company statistics."""

    total: int = 0
    by_status: dict[str, int] = {}
    by_canton: dict[str, int] = {}
    by_legal_form: dict[str, int] = {}


class CompanyEvent(VyncoModel):
    """A CloudEvent-style company event."""

    id: str
    ce_type: str = ""
    ce_source: str = ""
    ce_time: str = ""
    company_uid: str = ""
    company_name: str = ""
    category: str = ""
    severity: str = ""
    summary: str = ""
    detail_json: Any = None
    created_at: str = ""


class EventListResponse(VyncoModel):
    """Response wrapper for event listing."""

    events: list[CompanyEvent] = []
    count: int = 0


class CompareResponse(VyncoModel):
    """Company comparison response."""

    uids: list[str] = []
    names: list[str] = []
    dimensions: list[ComparisonDimension] = []


class ComparisonDimension(VyncoModel):
    """A single comparison dimension."""

    field: str = ""
    label: str = ""
    values: list[str | None] = []


class NewsItem(VyncoModel):
    """A news article related to a company."""

    id: str
    title: str = ""
    summary: str | None = None
    source: str | None = None
    source_type: str = ""
    published_at: str = ""
    url: str | None = Field(None, alias="sourceUrl")


class CompanyReport(VyncoModel):
    """A financial report for a company."""

    report_type: str = ""
    fiscal_year: int | None = None
    description: str = ""
    source_url: str | None = None
    publication_date: str = ""


class Relationship(VyncoModel):
    """A company relationship."""

    related_uid: str = ""
    related_name: str = ""
    relationship_type: str = ""
    shared_persons: list[str] = []


class HierarchyResponse(VyncoModel):
    """Parent/subsidiary hierarchy response."""

    parent: Any = None
    subsidiaries: list[Any] = []
    siblings: list[Any] = []


class Fingerprint(VyncoModel):
    """Company data fingerprint."""

    company_uid: str = ""
    name: str = ""
    industry_sector: str | None = None
    industry_group: str | None = None
    industry: str | None = None
    size_category: str | None = None
    employee_count_estimate: int | None = None
    capital_amount: float | None = None
    capital_currency: str | None = None
    revenue: float | None = None
    net_income: float | None = None
    auditor_tier: str | None = None
    change_frequency: int = 0
    board_size: int = 0
    company_age: int = 0
    canton: str = ""
    legal_form: str = ""
    has_parent_company: bool = False
    subsidiary_count: int = 0
    generated_at: str = ""
    fingerprint_version: str = ""


class NearbyCompany(VyncoModel):
    """A nearby company result."""

    uid: str
    name: str
    distance: float = 0.0
    latitude: float = 0.0
    longitude: float = 0.0


class Classification(VyncoModel):
    """Industry classification for a company."""

    company_uid: str = ""
    sector_code: str | None = None
    sector_name: str | None = None
    group_code: str | None = None
    group_name: str | None = None
    industry_code: str | None = None
    industry_name: str | None = None
    sub_industry_code: str | None = None
    sub_industry_name: str | None = None
    method: str = ""
    classified_at: str = ""
    auditor_category: str | None = None
    is_finma_regulated: bool = False


class RelatedCompanyEntry(VyncoModel):
    """A related company entry in a corporate structure."""

    uid: str = ""
    name: str = ""


class CorporateStructure(VyncoModel):
    """Corporate structure showing head offices, branches, and M&A relationships."""

    head_offices: list[RelatedCompanyEntry] = []
    branch_offices: list[RelatedCompanyEntry] = []
    acquisitions: list[RelatedCompanyEntry] = []
    acquired_by: list[RelatedCompanyEntry] = []


class Acquisition(VyncoModel):
    """An M&A relationship record."""

    acquirer_uid: str = ""
    acquired_uid: str = ""
    acquirer_name: str | None = None
    acquired_name: str | None = None
    created_at: str = ""


class Note(VyncoModel):
    """A user note on a company."""

    id: str
    company_uid: str = ""
    content: str = ""
    note_type: str = ""
    rating: int | None = None
    is_private: bool = False
    created_at: str = ""
    updated_at: str = ""


class Tag(VyncoModel):
    """A user tag on a company."""

    id: str
    company_uid: str = ""
    tag_name: str = ""
    color: str | None = None
    created_at: str = ""


class TagSummary(VyncoModel):
    """Summary of a user's tag usage across companies."""

    tag_name: str = ""
    count: int = 0


class PersonEntry(VyncoModel):
    """A person entry in a company's full response."""

    person_id: str | None = None
    first_name: str | None = None
    last_name: str | None = None
    role: str = ""
    since: str | None = None
    until: str | None = None


class ChangeEntry(VyncoModel):
    """A recent change entry in a company's full response."""

    id: str
    company_uid: str = ""
    change_type: str | None = None
    field_name: str | None = None
    old_value: str | None = None
    new_value: str | None = None
    detected_at: str = ""
    source_date: str | None = None


class RelationshipEntry(VyncoModel):
    """A relationship entry in a company's full response."""

    related_uid: str = ""
    related_name: str | None = None
    relationship_type: str = ""


class CompanyFullResponse(VyncoModel):
    """Full company details with persons, changes, and relationships."""

    company: Company
    persons: list[PersonEntry] = []
    recent_changes: list[ChangeEntry] = []
    relationships: list[RelationshipEntry] = []
