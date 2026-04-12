from __future__ import annotations

from typing import TYPE_CHECKING

from vynco._response import Response
from vynco.types.ubo import OwnershipResponse

if TYPE_CHECKING:
    from vynco._client import AsyncClient, Client


class AsyncOwnership:
    """Async ownership trace operations.

    For ultimate beneficial owner resolution use :meth:`AsyncCompanies.ubo` —
    this resource exposes the lower-level ownership-chain trace endpoint.
    """

    def __init__(self, client: AsyncClient) -> None:
        self._client = client

    async def trace(
        self,
        uid: str,
        *,
        max_depth: int | None = None,
    ) -> Response[OwnershipResponse]:
        """Trace the ownership chain upward from a company.

        Walks head-office / branch-office relationships up to ``max_depth``
        levels (default 10, max 20), detecting circular ownership and
        identifying key persons along the chain.
        """
        body: dict[str, object] = {}
        if max_depth is not None:
            body["maxDepth"] = max_depth
        return await self._client._request_model(
            "POST",
            f"/v1/ownership/{uid}",
            json=body,
            response_type=OwnershipResponse,
        )


class Ownership:
    """Sync ownership trace operations."""

    def __init__(self, client: Client) -> None:
        self._client = client

    def trace(
        self,
        uid: str,
        *,
        max_depth: int | None = None,
    ) -> Response[OwnershipResponse]:
        """Trace the ownership chain upward from a company."""
        body: dict[str, object] = {}
        if max_depth is not None:
            body["maxDepth"] = max_depth
        return self._client._request_model(
            "POST",
            f"/v1/ownership/{uid}",
            json=body,
            response_type=OwnershipResponse,
        )
