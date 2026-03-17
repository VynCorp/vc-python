from __future__ import annotations

from vynco.types.shared import VyncoModel


class Company(VyncoModel):
    """A Swiss company record from the Zefix registry."""

    uid: str
    name: str
    legal_seat: str = ""
    canton: str = ""
    legal_form: str = ""
    status: str = ""
    purpose: str = ""
    capital_nominal: float | None = None
    capital_currency: str | None = None
    auditor_name: str | None = None
    registration_date: str | None = None
    deletion_date: str | None = None
    data_source: str = ""
    last_modified: str = ""


class CompanyCount(VyncoModel):
    """Company count response."""

    count: int


class CompanyComparison(VyncoModel):
    """Result of comparing multiple companies."""

    companies: list[dict] = []  # type: ignore[type-arg]
    dimensions: list[dict] = []  # type: ignore[type-arg]
    similarities: list[str] = []
    differences: list[str] = []


class CompanyNews(VyncoModel):
    """A news article related to a company."""

    id: str = ""
    title: str = ""
    url: str = ""
    source: str = ""
    published_at: str | None = None
    summary: str | None = None
