from __future__ import annotations

from typing import TYPE_CHECKING

from vynco._response import Response
from vynco.types.reports import (
    GeneratedIndustryReport,
    IndustryListResponse,
    IndustryReportResponse,
)

if TYPE_CHECKING:
    from vynco._client import AsyncClient, Client


class AsyncReports:
    """Async industry reports operations."""

    def __init__(self, client: AsyncClient) -> None:
        self._client = client

    async def industries(self) -> Response[IndustryListResponse]:
        """List all industries with available reports and company counts."""
        return await self._client._request_model(
            "GET",
            "/v1/reports/industries",
            response_type=IndustryListResponse,
        )

    async def get(self, industry: str) -> Response[IndustryReportResponse]:
        """Get a detailed industry report with analytics."""
        return await self._client._request_model(
            "GET",
            f"/v1/reports/industry/{industry}",
            response_type=IndustryReportResponse,
        )

    async def generate(self, industry: str) -> Response[GeneratedIndustryReport]:
        """Generate an AI-powered narrative industry report."""
        return await self._client._request_model(
            "POST",
            f"/v1/reports/industry/{industry}/generate",
            response_type=GeneratedIndustryReport,
        )


class Reports:
    """Sync industry reports operations."""

    def __init__(self, client: Client) -> None:
        self._client = client

    def industries(self) -> Response[IndustryListResponse]:
        """List all industries with available reports and company counts."""
        return self._client._request_model(
            "GET",
            "/v1/reports/industries",
            response_type=IndustryListResponse,
        )

    def get(self, industry: str) -> Response[IndustryReportResponse]:
        """Get a detailed industry report with analytics."""
        return self._client._request_model(
            "GET",
            f"/v1/reports/industry/{industry}",
            response_type=IndustryReportResponse,
        )

    def generate(self, industry: str) -> Response[GeneratedIndustryReport]:
        """Generate an AI-powered narrative industry report."""
        return self._client._request_model(
            "POST",
            f"/v1/reports/industry/{industry}/generate",
            response_type=GeneratedIndustryReport,
        )
