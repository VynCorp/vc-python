from __future__ import annotations

from typing import TYPE_CHECKING

from vynco._response import Response
from vynco.types.compliance import ComplianceScope

if TYPE_CHECKING:
    from vynco._client import AsyncClient, Client


class AsyncCompliance:
    """Async regulatory compliance scope."""

    def __init__(self, client: AsyncClient) -> None:
        self._client = client

    async def scope(self, uid: str) -> Response[ComplianceScope]:
        """Get the regulatory compliance scope (regulations → controls) for a company."""
        return await self._client._request_model(
            "GET", f"/v1/compliance/scope/{uid}", response_type=ComplianceScope
        )


class Compliance:
    """Sync regulatory compliance scope."""

    def __init__(self, client: Client) -> None:
        self._client = client

    def scope(self, uid: str) -> Response[ComplianceScope]:
        """Get the regulatory compliance scope (regulations → controls) for a company."""
        return self._client._request_model(
            "GET", f"/v1/compliance/scope/{uid}", response_type=ComplianceScope
        )
