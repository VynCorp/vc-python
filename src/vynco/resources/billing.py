from __future__ import annotations

from typing import TYPE_CHECKING

from vynco._response import Response
from vynco.types.billing import CheckoutSessionResponse, PortalSessionResponse

if TYPE_CHECKING:
    from vynco._client import AsyncClient, Client


class AsyncBilling:
    """Async billing operations."""

    def __init__(self, client: AsyncClient) -> None:
        self._client = client

    async def create_checkout(self, tier: str) -> Response[CheckoutSessionResponse]:
        """Create a Stripe checkout session for a plan upgrade."""
        return await self._client._request_model(
            "POST", "/billing/checkout", json={"tier": tier},
            response_type=CheckoutSessionResponse,
        )

    async def create_portal(self) -> Response[PortalSessionResponse]:
        """Create a Stripe billing portal session."""
        return await self._client._request_model(
            "POST", "/billing/portal",
            response_type=PortalSessionResponse,
        )


class Billing:
    """Sync billing operations."""

    def __init__(self, client: Client) -> None:
        self._client = client

    def create_checkout(self, tier: str) -> Response[CheckoutSessionResponse]:
        """Create a Stripe checkout session for a plan upgrade."""
        return self._client._request_model(
            "POST", "/billing/checkout", json={"tier": tier},
            response_type=CheckoutSessionResponse,
        )

    def create_portal(self) -> Response[PortalSessionResponse]:
        """Create a Stripe billing portal session."""
        return self._client._request_model(
            "POST", "/billing/portal",
            response_type=PortalSessionResponse,
        )
