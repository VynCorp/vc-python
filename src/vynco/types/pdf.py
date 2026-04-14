from __future__ import annotations

from vynco.types.shared import VyncoModel


class PdfBoardMember(VyncoModel):
    """A board member entry in a PDF profile response."""

    first_name: str | None = None
    last_name: str | None = None
    role: str = ""
    signing_authority: str | None = None
    since: str | None = None
    until: str | None = None


class PdfEvent(VyncoModel):
    """A company event in a PDF profile response."""

    id: str = ""
    category: str = ""
    summary: str = ""
    severity: str = ""
    detected_at: str = ""
    source_date: str | None = None


class PdfAuditorTenure(VyncoModel):
    """An auditor tenure entry in a PDF profile response."""

    auditor_name: str = ""
    appointed_at: str | None = None
    resigned_at: str | None = None
    tenure_years: float | None = None
    is_current: bool = False


class PdfCompanyData(VyncoModel):
    """Core company data within a PDF profile response."""

    uid: str = ""
    name: str = ""
    canton: str | None = None
    status: str | None = None
    legal_form: str | None = None
    share_capital: float | None = None
    currency: str | None = None
    purpose: str | None = None
    founding_date: str | None = None
    registration_date: str | None = None
    legal_seat: str | None = None
    municipality: str | None = None
    address_street: str | None = None
    address_house_number: str | None = None
    address_zip_code: str | None = None
    address_city: str | None = None
    website: str | None = None
    industry: str | None = None
    sub_industry: str | None = None
    employee_count: int | None = None
    auditor_name: str | None = None
    auditor_category: str | None = None
    sanctions_hit: bool | None = None
    is_finma_regulated: bool | None = None
    old_names: list[str] | None = None
    translations: list[str] | None = None


class PdfProfileResponse(VyncoModel):
    """Structured company profile data suitable for PDF rendering."""

    company: PdfCompanyData = PdfCompanyData()
    board_members: list[PdfBoardMember] = []
    recent_events: list[PdfEvent] = []
    auditor_history: list[PdfAuditorTenure] = []
    generated_at: str = ""
