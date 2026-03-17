from __future__ import annotations

from vynco.types.shared import VyncoModel


class CompanyChange(VyncoModel):
    """A change recorded against a company."""

    id: str
    company_uid: str
    change_type: str = ""
    field_name: str = ""
    old_value: str | None = None
    new_value: str | None = None
    detected_at: str = ""
    source_date: str | None = None


class ChangeStatistics(VyncoModel):
    """Aggregate statistics about company changes."""

    total_changes: int = 0
    changes_by_type: dict[str, int] = {}
    period: str | None = None
