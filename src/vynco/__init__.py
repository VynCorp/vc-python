"""VynCo Python SDK — Python client for the VynCo Swiss Corporate Intelligence API."""

from __future__ import annotations

from vynco._client import AsyncClient, Client
from vynco._constants import __version__
from vynco._errors import (
    AuthenticationError,
    ConfigError,
    DeserializationError,
    ForbiddenError,
    InsufficientCreditsError,
    NotFoundError,
    RateLimitError,
    ServerError,
    ValidationError,
    VyncoError,
)
from vynco._response import Response, ResponseMeta
from vynco.types import (
    ApiKeyCreated,
    ApiKeyInfo,
    AuditorAnalytics,
    CantonAnalytics,
    ChangeStatistics,
    CheckoutSessionResponse,
    Company,
    CompanyChange,
    CompanyComparison,
    CompanyCount,
    CompanyNews,
    CompanyRelationship,
    CreditBalance,
    Dossier,
    PaginatedResponse,
    Person,
    PersonRole,
    PortalSessionResponse,
    RelationshipsResponse,
    RfmSegment,
    Team,
    UsageBreakdown,
    UsageOperation,
    UserProfile,
    Webhook,
    WebhookCreated,
)

__all__ = [
    # Version
    "__version__",
    # Clients
    "AsyncClient",
    "Client",
    # Errors
    "VyncoError",
    "AuthenticationError",
    "InsufficientCreditsError",
    "ForbiddenError",
    "NotFoundError",
    "ValidationError",
    "RateLimitError",
    "ServerError",
    "ConfigError",
    "DeserializationError",
    # Response
    "Response",
    "ResponseMeta",
    # Types
    "PaginatedResponse",
    "Company",
    "CompanyCount",
    "CompanyComparison",
    "CompanyNews",
    "Person",
    "PersonRole",
    "Dossier",
    "CompanyChange",
    "ChangeStatistics",
    "CreditBalance",
    "UsageBreakdown",
    "UsageOperation",
    "CheckoutSessionResponse",
    "PortalSessionResponse",
    "ApiKeyInfo",
    "ApiKeyCreated",
    "Webhook",
    "WebhookCreated",
    "Team",
    "UserProfile",
    "CompanyRelationship",
    "RelationshipsResponse",
    "CantonAnalytics",
    "AuditorAnalytics",
    "RfmSegment",
]
