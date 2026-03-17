from __future__ import annotations

from vynco.types.shared import VyncoModel


class Dossier(VyncoModel):
    """An AI-generated company dossier."""

    id: str
    company_uid: str
    status: str = ""
    executive_summary: str | None = None
    key_insights: list[str] | None = None
    risk_factors: list[str] | None = None
    generated_at: str | None = None
