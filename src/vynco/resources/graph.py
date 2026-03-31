from __future__ import annotations

from typing import TYPE_CHECKING

from vynco._base_client import _build_params
from vynco._response import Response
from vynco.types.graph import GraphResponse, NetworkAnalysisResponse

if TYPE_CHECKING:
    from vynco._client import AsyncClient, Client


class AsyncGraph:
    """Async graph/network operations."""

    def __init__(self, client: AsyncClient) -> None:
        self._client = client

    async def get(self, uid: str) -> Response[GraphResponse]:
        """Get the network graph for a company."""
        return await self._client._request_model(
            "GET",
            f"/v1/graph/{uid}",
            response_type=GraphResponse,
        )

    async def export(self, uid: str, *, format: str) -> Response[bytes]:
        """Export a company graph in a specific format."""
        params = _build_params({"format": format})
        return await self._client._request_model(
            "GET",
            f"/v1/graph/{uid}/export",
            params=params,
            response_type=bytes,
        )

    async def analyze(
        self,
        *,
        uids: list[str],
        overlay: str,
    ) -> Response[NetworkAnalysisResponse]:
        """Run network analysis across multiple companies."""
        return await self._client._request_model(
            "POST",
            "/v1/network/analyze",
            json={"uids": uids, "overlay": overlay},
            response_type=NetworkAnalysisResponse,
        )


class Graph:
    """Sync graph/network operations."""

    def __init__(self, client: Client) -> None:
        self._client = client

    def get(self, uid: str) -> Response[GraphResponse]:
        """Get the network graph for a company."""
        return self._client._request_model(
            "GET",
            f"/v1/graph/{uid}",
            response_type=GraphResponse,
        )

    def export(self, uid: str, *, format: str) -> Response[bytes]:
        """Export a company graph in a specific format."""
        params = _build_params({"format": format})
        return self._client._request_model(
            "GET",
            f"/v1/graph/{uid}/export",
            params=params,
            response_type=bytes,
        )

    def analyze(
        self,
        *,
        uids: list[str],
        overlay: str,
    ) -> Response[NetworkAnalysisResponse]:
        """Run network analysis across multiple companies."""
        return self._client._request_model(
            "POST",
            "/v1/network/analyze",
            json={"uids": uids, "overlay": overlay},
            response_type=NetworkAnalysisResponse,
        )
