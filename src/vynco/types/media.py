from __future__ import annotations

from vynco.types.shared import VyncoModel


class MediaItem(VyncoModel):
    """A media/news item with optional sentiment analysis."""

    id: str
    title: str = ""
    summary: str | None = None
    source: str | None = None
    published_at: str | None = None
    url: str | None = None
    sentiment_score: float | None = None
    sentiment_label: str | None = None
    topics: list[str] | None = None
    risk_relevance: float | None = None


class MediaResponse(VyncoModel):
    """Response containing a list of media items."""

    items: list[MediaItem] = []
    total: int = 0


class MediaAnalysisResponse(VyncoModel):
    """Response from triggering LLM sentiment analysis on media items."""

    analyzed_count: int = 0
    message: str = ""
