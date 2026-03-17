from __future__ import annotations


class VyncoError(Exception):
    """Base exception for all VynCo SDK errors."""

    def __init__(self, detail: str = "", message: str = "", status: int = 0) -> None:
        self.detail = detail or message
        self.message = message or detail
        self.status = status
        super().__init__(self.detail)


class AuthenticationError(VyncoError):
    """401 — Invalid or missing API key."""


class InsufficientCreditsError(VyncoError):
    """402 — Not enough credits for this operation."""


class ForbiddenError(VyncoError):
    """403 — Insufficient permissions."""


class NotFoundError(VyncoError):
    """404 — Resource not found."""


class ValidationError(VyncoError):
    """400/422 — Invalid request parameters."""


class RateLimitError(VyncoError):
    """429 — Too many requests."""


class ServerError(VyncoError):
    """5xx — Server-side error."""


class ConfigError(VyncoError):
    """Client misconfiguration."""


class DeserializationError(VyncoError):
    """Failed to parse API response."""


STATUS_ERROR_MAP: dict[int, type[VyncoError]] = {
    401: AuthenticationError,
    402: InsufficientCreditsError,
    403: ForbiddenError,
    404: NotFoundError,
    400: ValidationError,
    422: ValidationError,
    429: RateLimitError,
}
