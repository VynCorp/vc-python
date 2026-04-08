from __future__ import annotations

from dataclasses import dataclass, field
from typing import Generic, TypeVar

T = TypeVar("T")


@dataclass
class ResponseMeta:
    """Metadata extracted from VynCo API response headers."""

    request_id: str | None = None
    """Unique request identifier for tracing (X-Request-Id)."""

    credits_used: int | None = None
    """Credits consumed by this request (X-Credits-Used)."""

    credits_remaining: int | None = None
    """Remaining credit balance after this request (X-Credits-Remaining)."""

    rate_limit_limit: int | None = None
    """Maximum requests per minute for the current tier (X-RateLimit-Limit)."""

    rate_limit_remaining: int | None = None
    """Remaining requests in the current rate limit window (X-RateLimit-Remaining)."""

    rate_limit_reset: int | None = None
    """Unix timestamp when the rate limit window resets (X-RateLimit-Reset)."""

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
