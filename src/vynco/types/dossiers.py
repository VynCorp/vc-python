from __future__ import annotations

from vynco.types.shared import VyncoModel


class Dossier(VyncoModel):
    """A managed company dossier."""

    id: str
    user_id: str = ""
    company_uid: str = ""
    company_name: str = ""
    level: str = ""
    content: str = ""
    sources: list[str] = []
    created_at: str = ""


class DossierSummary(VyncoModel):
    """Dossier summary (used in list responses)."""

    id: str
    company_uid: str = ""
    company_name: str = ""
    level: str = ""
    created_at: str = ""
