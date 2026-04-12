from __future__ import annotations

from vynco.types.shared import VyncoModel


class SimilarCompanyResult(VyncoModel):
    """A company similar to a given query company."""

    uid: str
    name: str
    canton: str | None = None
    industry: str | None = None
    legal_form: str | None = None
    share_capital: float | None = None
    status: str | None = None
    similarity_score: int = 0
    matching_dimensions: list[str] = []


class SimilarCompaniesResponse(VyncoModel):
    """Response containing companies similar to a query company."""

    company_uid: str = ""
    company_name: str = ""
    results: list[SimilarCompanyResult] = []
