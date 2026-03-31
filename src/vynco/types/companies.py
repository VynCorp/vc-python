from __future__ import annotations

from typing import Any

from vynco.types.shared import VyncoModel


class Company(VyncoModel):
    """A Swiss company record."""

    uid: str
    name: str
    canton: str | None = None
    status: str | None = None
    legal_form: str | None = None
    share_capital: float | None = None
    industry: str | None = None
    auditor_category: str | None = None
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
    url: str | None = None


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
