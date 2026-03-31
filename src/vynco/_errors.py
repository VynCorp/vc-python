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


class ConflictError(VyncoError):
    """409 — Request conflicts with existing state."""


class ServerError(VyncoError):
    """5xx — Server-side error."""


class ServiceUnavailableError(ServerError):
    """503 — API temporarily unavailable."""


class ConfigError(VyncoError):
    """Client misconfiguration."""


class DeserializationError(VyncoError):
    """Failed to parse API response."""


STATUS_ERROR_MAP: dict[int, type[VyncoError]] = {
    400: ValidationError,
    401: AuthenticationError,
    402: InsufficientCreditsError,
    403: ForbiddenError,
    404: NotFoundError,
    409: ConflictError,
    422: ValidationError,
    429: RateLimitError,
    503: ServiceUnavailableError,
}
