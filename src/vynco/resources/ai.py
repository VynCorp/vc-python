from __future__ import annotations

from typing import TYPE_CHECKING, Any

from vynco._response import Response
from vynco.types.ai import (
    AiSearchResponse,
    BatchRiskScoreResponse,
    DossierResponse,
    RiskScoreResponse,
)

if TYPE_CHECKING:
    from vynco._client import AsyncClient, Client


class AsyncAi:
    """Async AI operations."""

    def __init__(self, client: AsyncClient) -> None:
        self._client = client

    async def dossier(
        self,
        *,
        uid: str,
        depth: str | None = None,
    ) -> Response[DossierResponse]:
        """Generate an AI dossier for a company."""
        body: dict[str, Any] = {"uid": uid}
        if depth is not None:
            body["depth"] = depth
        return await self._client._request_model(
            "POST",
            "/v1/ai/dossier",
            json=body,
            response_type=DossierResponse,
        )

    async def search(self, *, query: str) -> Response[AiSearchResponse]:
        """AI-powered natural language search."""
        return await self._client._request_model(
            "POST",
            "/v1/ai/search",
            json={"query": query},
            response_type=AiSearchResponse,
        )

    async def risk_score(self, *, uid: str) -> Response[RiskScoreResponse]:
        """Get AI risk score for a company."""
        return await self._client._request_model(
            "POST",
            "/v1/ai/risk-score",
            json={"uid": uid},
            response_type=RiskScoreResponse,
        )

    async def risk_score_batch(self, *, uids: list[str]) -> Response[BatchRiskScoreResponse]:
        """Get AI risk scores for up to 50 companies in a single call."""
        return await self._client._request_model(
            "POST",
            "/v1/ai/risk-score/batch",
            json={"uids": uids},
            response_type=BatchRiskScoreResponse,
        )


class Ai:
    """Sync AI operations."""

    def __init__(self, client: Client) -> None:
        self._client = client

    def dossier(
        self,
        *,
        uid: str,
        depth: str | None = None,
    ) -> Response[DossierResponse]:
        """Generate an AI dossier for a company."""
        body: dict[str, Any] = {"uid": uid}
        if depth is not None:
            body["depth"] = depth
        return self._client._request_model(
            "POST",
            "/v1/ai/dossier",
            json=body,
            response_type=DossierResponse,
        )

    def search(self, *, query: str) -> Response[AiSearchResponse]:
        """AI-powered natural language search."""
        return self._client._request_model(
            "POST",
            "/v1/ai/search",
            json={"query": query},
            response_type=AiSearchResponse,
        )

    def risk_score(self, *, uid: str) -> Response[RiskScoreResponse]:
        """Get AI risk score for a company."""
        return self._client._request_model(
            "POST",
            "/v1/ai/risk-score",
            json={"uid": uid},
            response_type=RiskScoreResponse,
        )

    def risk_score_batch(self, *, uids: list[str]) -> Response[BatchRiskScoreResponse]:
        """Get AI risk scores for up to 50 companies in a single call."""
        return self._client._request_model(
            "POST",
            "/v1/ai/risk-score/batch",
            json={"uids": uids},
            response_type=BatchRiskScoreResponse,
        )
