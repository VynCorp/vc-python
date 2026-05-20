from __future__ import annotations

from vynco.types.shared import VyncoModel


class ComplianceEvidence(VyncoModel):
    """An evidence artefact supporting a control."""

    id: str = ""
    name: str = ""
    category: str = ""
    format_hint: str | None = None
    retention_period: str | None = None


class ComplianceControl(VyncoModel):
    """A control mitigating an obligation."""

    id: str = ""
    objective: str = ""
    control_type: str = ""
    frequency: str = ""
    evidence: list[ComplianceEvidence] = []


class ComplianceObligation(VyncoModel):
    """A regulatory obligation derived from an article."""

    id: str = ""
    article: str = ""
    deontic_operator: str = ""
    excerpt: str = ""
    full_text: str | None = None
    controls: list[ComplianceControl] = []


class ComplianceArticle(VyncoModel):
    """An article within a regulation."""

    id: str = ""
    number: str = ""
    title: str | None = None
    body: str | None = None
    obligations: list[ComplianceObligation] = []


class ComplianceRegulation(VyncoModel):
    """A regulation in scope for a company."""

    id: str = ""
    title: str = ""
    jurisdiction: str = ""
    regulation_type: str = ""
    status: str = ""
    source_url: str | None = None
    effective_date: str | None = None
    articles: list[ComplianceArticle] = []
    unassigned_obligations: list[ComplianceObligation] = []


class ComplianceTotals(VyncoModel):
    """Aggregate counts for a compliance scope."""

    regulations: int = 0
    articles: int = 0
    obligations: int = 0
    controls: int = 0
    evidence: int = 0


class ComplianceScope(VyncoModel):
    """The regulatory compliance scope for a company."""

    company_uid: str = ""
    company_name: str = ""
    jurisdictions: list[str] = []
    totals: ComplianceTotals = ComplianceTotals()
    regulations: list[ComplianceRegulation] = []
