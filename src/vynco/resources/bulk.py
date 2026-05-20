from __future__ import annotations

import builtins
from typing import TYPE_CHECKING

from vynco._response import ExportFile, Response
from vynco.types.bulk import BulkScreeningResponse, BulkWatchlistResponse

if TYPE_CHECKING:
    from vynco._client import AsyncClient, Client

_list = builtins.list


def _watchlist_file(uids: _list[str]) -> dict[str, tuple[str, str, str]]:
    """Build the multipart payload for a bulk watchlist upload (one UID per line)."""
    csv = "\n".join(uids)
    return {"file": ("uids.csv", csv, "text/csv")}


class AsyncBulk:
    """Async Enterprise bulk operations (export, screening, watchlist import)."""

    def __init__(self, client: AsyncClient) -> None:
        self._client = client

    async def export(self, *, uids: _list[str], fields: _list[str]) -> ExportFile:
        """Export selected fields for up to 500 companies as a CSV file.

        ``fields`` is a subset of: name, canton, capital, auditor, status,
        address, industry.
        """
        return await self._client._request_bytes(
            "POST", "/v1/bulk/export", json={"uids": uids, "fields": fields}
        )

    async def screening(
        self, *, entities: _list[dict[str, str]]
    ) -> Response[BulkScreeningResponse]:
        """Screen up to 100 entities against SECO sanctions.

        Each entity is a dict with ``name`` and ``type`` ("person" or "company").
        """
        return await self._client._request_model(
            "POST",
            "/v1/bulk/screening",
            json={"entities": entities},
            response_type=BulkScreeningResponse,
        )

    async def add_to_watchlist(
        self, id: str, *, uids: _list[str]
    ) -> Response[BulkWatchlistResponse]:
        """Bulk-add companies to a watchlist by uploading their UIDs (max 1000)."""
        return await self._client._request_model(
            "POST",
            f"/v1/bulk/watchlist/{id}",
            files=_watchlist_file(uids),
            response_type=BulkWatchlistResponse,
        )


class Bulk:
    """Sync Enterprise bulk operations (export, screening, watchlist import)."""

    def __init__(self, client: Client) -> None:
        self._client = client

    def export(self, *, uids: _list[str], fields: _list[str]) -> ExportFile:
        """Export selected fields for up to 500 companies as a CSV file.

        ``fields`` is a subset of: name, canton, capital, auditor, status,
        address, industry.
        """
        return self._client._request_bytes(
            "POST", "/v1/bulk/export", json={"uids": uids, "fields": fields}
        )

    def screening(self, *, entities: _list[dict[str, str]]) -> Response[BulkScreeningResponse]:
        """Screen up to 100 entities against SECO sanctions.

        Each entity is a dict with ``name`` and ``type`` ("person" or "company").
        """
        return self._client._request_model(
            "POST",
            "/v1/bulk/screening",
            json={"entities": entities},
            response_type=BulkScreeningResponse,
        )

    def add_to_watchlist(self, id: str, *, uids: _list[str]) -> Response[BulkWatchlistResponse]:
        """Bulk-add companies to a watchlist by uploading their UIDs (max 1000)."""
        return self._client._request_model(
            "POST",
            f"/v1/bulk/watchlist/{id}",
            files=_watchlist_file(uids),
            response_type=BulkWatchlistResponse,
        )
