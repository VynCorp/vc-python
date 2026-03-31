from __future__ import annotations

import builtins
from typing import TYPE_CHECKING, Any

from vynco._response import Response, ResponseMeta
from vynco.types.dossiers import Dossier, DossierSummary

if TYPE_CHECKING:
    from vynco._client import AsyncClient, Client

_list = builtins.list


class AsyncDossiers:
    """Async dossier operations."""

    def __init__(self, client: AsyncClient) -> None:
        self._client = client

    async def create(
        self,
        *,
        uid: str,
        level: str | None = None,
    ) -> Response[Dossier]:
        """Create a managed dossier for a company."""
        body: dict[str, Any] = {"uid": uid}
        if level is not None:
            body["level"] = level
        return await self._client._request_model(
            "POST",
            "/v1/dossiers",
            json=body,
            response_type=Dossier,
        )

    async def list(self) -> Response[_list[DossierSummary]]:
        """List all dossiers."""
        return await self._client._request_model(
            "GET",
            "/v1/dossiers",
            response_type=list[DossierSummary],
        )

    async def get(self, id_or_uid: str) -> Response[Dossier]:
        """Get a dossier by ID or company UID."""
        return await self._client._request_model(
            "GET",
            f"/v1/dossiers/{id_or_uid}",
            response_type=Dossier,
        )

    async def delete(self, id: str) -> ResponseMeta:
        """Delete a dossier."""
        return await self._client._request_empty("DELETE", f"/v1/dossiers/{id}")


class Dossiers:
    """Sync dossier operations."""

    def __init__(self, client: Client) -> None:
        self._client = client

    def create(
        self,
        *,
        uid: str,
        level: str | None = None,
    ) -> Response[Dossier]:
        """Create a managed dossier for a company."""
        body: dict[str, Any] = {"uid": uid}
        if level is not None:
            body["level"] = level
        return self._client._request_model(
            "POST",
            "/v1/dossiers",
            json=body,
            response_type=Dossier,
        )

    def list(self) -> Response[_list[DossierSummary]]:
        """List all dossiers."""
        return self._client._request_model(
            "GET",
            "/v1/dossiers",
            response_type=list[DossierSummary],
        )

    def get(self, id_or_uid: str) -> Response[Dossier]:
        """Get a dossier by ID or company UID."""
        return self._client._request_model(
            "GET",
            f"/v1/dossiers/{id_or_uid}",
            response_type=Dossier,
        )

    def delete(self, id: str) -> ResponseMeta:
        """Delete a dossier."""
        return self._client._request_empty("DELETE", f"/v1/dossiers/{id}")
