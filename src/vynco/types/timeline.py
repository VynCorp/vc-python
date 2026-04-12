from __future__ import annotations

from vynco.types.shared import VyncoModel


class TimelineEvent(VyncoModel):
    """A single event on a company timeline."""

    id: str
    category: str = ""
    field_name: str | None = None
    old_value: str | None = None
    new_value: str | None = None
    summary: str | None = None
    source: str | None = None
    severity: str | None = None
    date: str = ""


class TimelineResponse(VyncoModel):
    """Chronological timeline of a company's changes and events."""

    uid: str = ""
    company_name: str = ""
    events: list[TimelineEvent] = []
    total_events: int = 0


class TimelineSummaryResponse(VyncoModel):
    """AI-generated narrative summary of a company timeline."""

    uid: str = ""
    company_name: str = ""
    summary: str = ""
    event_count: int = 0
    generated_at: str = ""
