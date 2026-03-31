from __future__ import annotations

import builtins
from typing import TYPE_CHECKING

from vynco._base_client import _build_params
from vynco._response import Response
from vynco.types.companies import (
    Company,
    CompanyCount,
    CompanyReport,
    CompanyStatistics,
    CompareResponse,
    EventListResponse,
    Fingerprint,
    HierarchyResponse,
    NearbyCompany,
    NewsItem,
    Relationship,
)
from vynco.types.shared import PaginatedResponse

if TYPE_CHECKING:
    from vynco._client import AsyncClient, Client

_list = builtins.list


class AsyncCompanies:
    """Async company operations."""

    def __init__(self, client: AsyncClient) -> None:
        self._client = client

    async def list(
        self,
        *,
        query: str | None = None,
        canton: str | None = None,
        changed_since: str | None = None,
        page: int | None = None,
        page_size: int | None = None,
    ) -> Response[PaginatedResponse[Company]]:
        """List companies with optional filtering and pagination."""
        params = _build_params({k: v for k, v in locals().items() if k != "self"})
        return await self._client._request_model(
            "GET",
            "/v1/companies",
            params=params or None,
            response_type=PaginatedResponse[Company],
        )

    async def get(self, uid: str) -> Response[Company]:
        """Get a company by its Swiss UID (e.g. 'CHE-105.805.080')."""
        return await self._client._request_model(
            "GET",
            f"/v1/companies/{uid}",
            response_type=Company,
        )

    async def count(self) -> Response[CompanyCount]:
        """Get the total count of companies."""
        return await self._client._request_model(
            "GET",
            "/v1/companies/count",
            response_type=CompanyCount,
        )

    async def events(self, uid: str, *, limit: int | None = None) -> Response[EventListResponse]:
        """Get events for a company."""
        params = _build_params({"limit": limit})
        return await self._client._request_model(
            "GET",
            f"/v1/companies/{uid}/events",
            params=params or None,
            response_type=EventListResponse,
        )

    async def statistics(self) -> Response[CompanyStatistics]:
        """Get aggregate statistics about companies."""
        return await self._client._request_model(
            "GET",
            "/v1/companies/statistics",
            response_type=CompanyStatistics,
        )

    async def compare(self, uids: _list[str]) -> Response[CompareResponse]:
        """Compare multiple companies side-by-side."""
        return await self._client._request_model(
            "POST",
            "/v1/companies/compare",
            json={"uids": uids},
            response_type=CompareResponse,
        )

    async def news(self, uid: str) -> Response[_list[NewsItem]]:
        """Get news articles related to a company."""
        return await self._client._request_model(
            "GET",
            f"/v1/companies/{uid}/news",
            response_type=list[NewsItem],
        )

    async def reports(self, uid: str) -> Response[_list[CompanyReport]]:
        """Get financial reports for a company."""
        return await self._client._request_model(
            "GET",
            f"/v1/companies/{uid}/reports",
            response_type=list[CompanyReport],
        )

    async def relationships(self, uid: str) -> Response[_list[Relationship]]:
        """Get company relationships."""
        return await self._client._request_model(
            "GET",
            f"/v1/companies/{uid}/relationships",
            response_type=list[Relationship],
        )

    async def hierarchy(self, uid: str) -> Response[HierarchyResponse]:
        """Get parent/subsidiary hierarchy."""
        return await self._client._request_model(
            "GET",
            f"/v1/companies/{uid}/hierarchy",
            response_type=HierarchyResponse,
        )

    async def fingerprint(self, uid: str) -> Response[Fingerprint]:
        """Get data fingerprint for a company."""
        return await self._client._request_model(
            "GET",
            f"/v1/companies/{uid}/fingerprint",
            response_type=Fingerprint,
        )

    async def nearby(
        self,
        *,
        lat: float,
        lng: float,
        radius_km: float | None = None,
        limit: int | None = None,
    ) -> Response[_list[NearbyCompany]]:
        """Find companies near a geographic point."""
        params = _build_params({k: v for k, v in locals().items() if k != "self"})
        return await self._client._request_model(
            "GET",
            "/v1/companies/nearby",
            params=params or None,
            response_type=list[NearbyCompany],
        )


class Companies:
    """Sync company operations."""

    def __init__(self, client: Client) -> None:
        self._client = client

    def list(
        self,
        *,
        query: str | None = None,
        canton: str | None = None,
        changed_since: str | None = None,
        page: int | None = None,
        page_size: int | None = None,
    ) -> Response[PaginatedResponse[Company]]:
        """List companies with optional filtering and pagination."""
        params = _build_params({k: v for k, v in locals().items() if k != "self"})
        return self._client._request_model(
            "GET",
            "/v1/companies",
            params=params or None,
            response_type=PaginatedResponse[Company],
        )

    def get(self, uid: str) -> Response[Company]:
        """Get a company by its Swiss UID (e.g. 'CHE-105.805.080')."""
        return self._client._request_model(
            "GET",
            f"/v1/companies/{uid}",
            response_type=Company,
        )

    def count(self) -> Response[CompanyCount]:
        """Get the total count of companies."""
        return self._client._request_model(
            "GET",
            "/v1/companies/count",
            response_type=CompanyCount,
        )

    def events(self, uid: str, *, limit: int | None = None) -> Response[EventListResponse]:
        """Get events for a company."""
        params = _build_params({"limit": limit})
        return self._client._request_model(
            "GET",
            f"/v1/companies/{uid}/events",
            params=params or None,
            response_type=EventListResponse,
        )

    def statistics(self) -> Response[CompanyStatistics]:
        """Get aggregate statistics about companies."""
        return self._client._request_model(
            "GET",
            "/v1/companies/statistics",
            response_type=CompanyStatistics,
        )

    def compare(self, uids: _list[str]) -> Response[CompareResponse]:
        """Compare multiple companies side-by-side."""
        return self._client._request_model(
            "POST",
            "/v1/companies/compare",
            json={"uids": uids},
            response_type=CompareResponse,
        )

    def news(self, uid: str) -> Response[_list[NewsItem]]:
        """Get news articles related to a company."""
        return self._client._request_model(
            "GET",
            f"/v1/companies/{uid}/news",
            response_type=list[NewsItem],
        )

    def reports(self, uid: str) -> Response[_list[CompanyReport]]:
        """Get financial reports for a company."""
        return self._client._request_model(
            "GET",
            f"/v1/companies/{uid}/reports",
            response_type=list[CompanyReport],
        )

    def relationships(self, uid: str) -> Response[_list[Relationship]]:
        """Get company relationships."""
        return self._client._request_model(
            "GET",
            f"/v1/companies/{uid}/relationships",
            response_type=list[Relationship],
        )

    def hierarchy(self, uid: str) -> Response[HierarchyResponse]:
        """Get parent/subsidiary hierarchy."""
        return self._client._request_model(
            "GET",
            f"/v1/companies/{uid}/hierarchy",
            response_type=HierarchyResponse,
        )

    def fingerprint(self, uid: str) -> Response[Fingerprint]:
        """Get data fingerprint for a company."""
        return self._client._request_model(
            "GET",
            f"/v1/companies/{uid}/fingerprint",
            response_type=Fingerprint,
        )

    def nearby(
        self,
        *,
        lat: float,
        lng: float,
        radius_km: float | None = None,
        limit: int | None = None,
    ) -> Response[_list[NearbyCompany]]:
        """Find companies near a geographic point."""
        params = _build_params({k: v for k, v in locals().items() if k != "self"})
        return self._client._request_model(
            "GET",
            "/v1/companies/nearby",
            params=params or None,
            response_type=list[NearbyCompany],
        )
