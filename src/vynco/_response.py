from __future__ import annotations

from dataclasses import dataclass, field
from typing import Generic, TypeVar

T = TypeVar("T")


@dataclass
class ResponseMeta:
    """Metadata extracted from VynCo API response headers."""

    request_id: str | None = None
    """Unique request identifier for tracing (X-Request-Id)."""

    rate_limit_group: str | None = None
    """Endpoint group this request was metered against (X-RateLimit-Group)."""

    rate_limit_window: str | None = None
    """Rate-limit window for the group: "hour" or "day" (X-RateLimit-Window)."""

    rate_limit_limit: int | None = None
    """Request quota for the current group and window (X-RateLimit-Limit)."""

    rate_limit_remaining: int | None = None
    """Remaining requests in the current rate limit window (X-RateLimit-Remaining)."""

    rate_limit_reset: int | None = None
    """Seconds until the rate limit window resets (X-RateLimit-Reset)."""

    data_source: str | None = None
    """Data source attribution (X-Data-Source)."""


@dataclass
class Response(Generic[T]):
    """API response containing typed data and header metadata."""

    data: T
    meta: ResponseMeta = field(default_factory=ResponseMeta)


@dataclass
class ExportFile:
    """Downloaded export file with raw bytes and metadata."""

    meta: ResponseMeta
    bytes: bytes
    content_type: str
    filename: str
