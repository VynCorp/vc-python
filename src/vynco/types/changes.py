from __future__ import annotations

from typing import Any

from pydantic import Field

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


class DiffEntry(VyncoModel):
    """A single field-level change in a company diff."""

    field: str = ""
    # Wire key is the reserved word ``from``; expose it as ``from_value``.
    from_value: str | None = Field(None, alias="from")
    to: str | None = None
    changed_at: str = ""
    change_type: str = ""


class CompanyDiffResponse(VyncoModel):
    """Structured field-by-field diff for a company over a time range."""

    uid: str = ""
    since: str = ""
    until: str = ""
    changes: list[DiffEntry] = []
    total_changes: int = 0
