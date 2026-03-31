from __future__ import annotations

from typing import Any

from vynco.types.shared import VyncoModel


class CompanyChange(VyncoModel):
    """A change recorded against a company."""

    id: str
    company_uid: str = ""
    company_name: str | None = None
    change_type: str = ""
    field_name: str | None = None
    old_value: str | None = None
    new_value: str | None = None
    description: str | None = None
    source: str | None = None
    detected_at: str = ""


class ChangeStatistics(VyncoModel):
    """Aggregate change statistics."""

    total_changes: int = 0
    changes_this_week: int = 0
    changes_this_month: int = 0
    by_type: Any = None
