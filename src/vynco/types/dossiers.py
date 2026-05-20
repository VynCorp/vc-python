from __future__ import annotations

from vynco.types.shared import VyncoModel


class Citation(VyncoModel):
    """A regulatory citation anchored to a methodology obligation.

    Inline ``[[obl:...]]`` tags inside a dossier's ``content`` map to entries
    in the dossier's ``citations`` list.
    """

    id: str = ""
    regulation_id: str = ""
    regulation_title: str = ""
    article: str = ""
    jurisdiction: str = ""
    source_url: str | None = None
    excerpt: str = ""


class Dossier(VyncoModel):
    """A managed company dossier."""

    id: str
    user_id: str = ""
    company_uid: str = ""
    company_name: str = ""
    level: str = ""
    content: str = ""
    sources: list[str] = []
    citations: list[Citation] = []
    created_at: str = ""


class DossierSummary(VyncoModel):
    """Dossier summary (used in list responses)."""

    id: str
    company_uid: str = ""
    company_name: str = ""
    level: str = ""
    created_at: str = ""
