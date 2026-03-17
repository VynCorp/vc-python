from __future__ import annotations

from typing import TYPE_CHECKING, Any

from vynco._base_client import _build_params
from vynco._response import Response
from vynco.types.credits import CreditBalance, UsageBreakdown

if TYPE_CHECKING:
    from vynco._client import AsyncClient, Client


class AsyncCredits:
    """Async credit operations."""

    def __init__(self, client: AsyncClient) -> None:
        self._client = client

    async def balance(self) -> Response[CreditBalance]:
        """Get current credit balance and tier info."""
        return await self._client._request_model(
            "GET", "/credits/balance", response_type=CreditBalance,
        )

    async def usage(self, *, since: str | None = None) -> Response[UsageBreakdown]:
        """Get credit usage breakdown by operation type."""
        params = _build_params(
            {k: v for k, v in locals().items() if k != "self"}
        )
        return await self._client._request_model(
            "GET", "/credits/usage", params=params or None,
            response_type=UsageBreakdown,
        )

    async def history(
        self, *, limit: int | None = None, offset: int | None = None
    ) -> Response[dict[str, Any]]:
        """Get credit transaction history."""
        params = _build_params(
            {k: v for k, v in locals().items() if k != "self"}
        )
        return await self._client._request_model(
            "GET", "/credits/history", params=params or None,
            response_type=dict,
        )


class Credits:
    """Sync credit operations."""

    def __init__(self, client: Client) -> None:
        self._client = client

    def balance(self) -> Response[CreditBalance]:
        """Get current credit balance and tier info."""
        return self._client._request_model(
            "GET", "/credits/balance", response_type=CreditBalance,
        )

    def usage(self, *, since: str | None = None) -> Response[UsageBreakdown]:
        """Get credit usage breakdown by operation type."""
        params = _build_params(
            {k: v for k, v in locals().items() if k != "self"}
        )
        return self._client._request_model(
            "GET", "/credits/usage", params=params or None,
            response_type=UsageBreakdown,
        )

    def history(
        self, *, limit: int | None = None, offset: int | None = None
    ) -> Response[dict[str, Any]]:
        """Get credit transaction history."""
        params = _build_params(
            {k: v for k, v in locals().items() if k != "self"}
        )
        return self._client._request_model(
            "GET", "/credits/history", params=params or None,
            response_type=dict,
        )
