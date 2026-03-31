from __future__ import annotations

from typing import TYPE_CHECKING, Any

from vynco._response import Response
from vynco.types.exports import ExportDownload, ExportJob

if TYPE_CHECKING:
    from vynco._client import AsyncClient, Client


class AsyncExports:
    """Async export operations."""

    def __init__(self, client: AsyncClient) -> None:
        self._client = client

    async def create(
        self,
        *,
        format: str | None = None,
        canton: str | None = None,
        status: str | None = None,
        changed_since: str | None = None,
        industry: str | None = None,
        max_rows: int | None = None,
    ) -> Response[ExportJob]:
        """Create a data export job."""
        body: dict[str, Any] = {}
        if format is not None:
            body["format"] = format
        if canton is not None:
            body["canton"] = canton
        if status is not None:
            body["status"] = status
        if changed_since is not None:
            body["changedSince"] = changed_since
        if industry is not None:
            body["industry"] = industry
        if max_rows is not None:
            body["maxRows"] = max_rows
        return await self._client._request_model(
            "POST",
            "/v1/exports",
            json=body,
            response_type=ExportJob,
        )

    async def get(self, id: str) -> Response[ExportDownload]:
        """Get export job status and metadata."""
        return await self._client._request_model(
            "GET",
            f"/v1/exports/{id}",
            response_type=ExportDownload,
        )

    async def download(self, id: str) -> Response[bytes]:
        """Download an export file as raw bytes."""
        return await self._client._request_model(
            "GET",
            f"/v1/exports/{id}/download",
            response_type=bytes,
        )


class Exports:
    """Sync export operations."""

    def __init__(self, client: Client) -> None:
        self._client = client

    def create(
        self,
        *,
        format: str | None = None,
        canton: str | None = None,
        status: str | None = None,
        changed_since: str | None = None,
        industry: str | None = None,
        max_rows: int | None = None,
    ) -> Response[ExportJob]:
        """Create a data export job."""
        body: dict[str, Any] = {}
        if format is not None:
            body["format"] = format
        if canton is not None:
            body["canton"] = canton
        if status is not None:
            body["status"] = status
        if changed_since is not None:
            body["changedSince"] = changed_since
        if industry is not None:
            body["industry"] = industry
        if max_rows is not None:
            body["maxRows"] = max_rows
        return self._client._request_model(
            "POST",
            "/v1/exports",
            json=body,
            response_type=ExportJob,
        )

    def get(self, id: str) -> Response[ExportDownload]:
        """Get export job status and metadata."""
        return self._client._request_model(
            "GET",
            f"/v1/exports/{id}",
            response_type=ExportDownload,
        )

    def download(self, id: str) -> Response[bytes]:
        """Download an export file as raw bytes."""
        return self._client._request_model(
            "GET",
            f"/v1/exports/{id}/download",
            response_type=bytes,
        )
