"""Tests for company resource operations."""

from __future__ import annotations

import httpx
import respx

import vynco

BASE_URL = "https://api.vynco.ch"


async def test_company_list_parses_paginated_response():
    with respx.mock(base_url=BASE_URL) as mock:
        mock.get("/v1/companies").mock(
            return_value=httpx.Response(
                200,
                json={
                    "items": [
                        {
                            "uid": "CHE-105.805.080",
                            "name": "Novartis AG",
                            "canton": "BS",
                            "legalForm": "AG",
                            "status": "Active",
                            "shareCapital": 1000000.0,
                            "industry": "Pharmaceuticals",
                            "auditorCategory": "State-regulated",
                            "updatedAt": "2026-01-15T10:30:00Z",
                        }
                    ],
                    "totalCount": 1,
                    "page": 1,
                    "pageSize": 20,
                },
                headers={
                    "X-Request-Id": "req-abc-123",
                    "X-Credits-Used": "1",
                    "X-Credits-Remaining": "499",
                    "X-Rate-Limit-Limit": "60",
                    "X-Data-Source": "Zefix",
                },
            )
        )

        client = vynco.AsyncClient("vc_test_key", base_url=BASE_URL, max_retries=0)
        resp = await client.companies.list(query="Novartis", canton="BS")

        assert resp.data.total == 1
        assert len(resp.data.items) == 1
        assert resp.data.items[0].uid == "CHE-105.805.080"
        assert resp.data.items[0].name == "Novartis AG"
        assert resp.data.items[0].canton == "BS"
        assert resp.data.items[0].legal_form == "AG"

        assert resp.meta.request_id == "req-abc-123"
        assert resp.meta.credits_used == 1
        assert resp.meta.credits_remaining == 499
        assert resp.meta.rate_limit_limit == 60
        assert resp.meta.data_source == "Zefix"


async def test_company_list_with_total_count():
    """Test that PaginatedResponse accepts 'totalCount' as an alias for 'total'."""
    with respx.mock(base_url=BASE_URL) as mock:
        mock.get("/v1/companies").mock(
            return_value=httpx.Response(
                200,
                json={
                    "items": [],
                    "totalCount": 42,
                    "page": 1,
                    "pageSize": 20,
                },
            )
        )

        client = vynco.AsyncClient("vc_test_key", base_url=BASE_URL, max_retries=0)
        resp = await client.companies.list()
        assert resp.data.total == 42


async def test_company_get_by_uid():
    with respx.mock(base_url=BASE_URL) as mock:
        mock.get("/v1/companies/CHE-105.805.080").mock(
            return_value=httpx.Response(
                200,
                json={
                    "uid": "CHE-105.805.080",
                    "name": "Novartis AG",
                    "canton": "BS",
                    "legalForm": "AG",
                    "status": "Active",
                    "updatedAt": "2026-01-15T10:30:00Z",
                },
            )
        )

        client = vynco.AsyncClient("vc_test_key", base_url=BASE_URL, max_retries=0)
        resp = await client.companies.get("CHE-105.805.080")

        assert resp.data.name == "Novartis AG"
        assert resp.data.status == "Active"


async def test_company_count():
    with respx.mock(base_url=BASE_URL) as mock:
        mock.get("/v1/companies/count").mock(
            return_value=httpx.Response(200, json={"count": 320000})
        )

        client = vynco.AsyncClient("vc_test_key", base_url=BASE_URL, max_retries=0)
        resp = await client.companies.count()
        assert resp.data.count == 320000


async def test_company_statistics():
    with respx.mock(base_url=BASE_URL) as mock:
        mock.get("/v1/companies/statistics").mock(
            return_value=httpx.Response(
                200,
                json={
                    "total": 320000,
                    "byStatus": {"Active": 280000, "Dissolved": 40000},
                    "byCanton": {"ZH": 50000, "BS": 15000},
                    "byLegalForm": {"AG": 120000, "GmbH": 80000},
                },
            )
        )

        client = vynco.AsyncClient("vc_test_key", base_url=BASE_URL, max_retries=0)
        resp = await client.companies.statistics()
        assert resp.data.total == 320000


async def test_company_compare():
    with respx.mock(base_url=BASE_URL) as mock:
        mock.post("/v1/companies/compare").mock(
            return_value=httpx.Response(
                200,
                json={
                    "uids": ["CHE-105.805.080", "CHE-109.340.740"],
                    "names": ["Novartis AG", "Roche Holding AG"],
                    "dimensions": [
                        {"field": "canton", "label": "Canton", "values": ["BS", "BS"]},
                    ],
                },
            )
        )

        client = vynco.AsyncClient("vc_test_key", base_url=BASE_URL, max_retries=0)
        resp = await client.companies.compare(["CHE-105.805.080", "CHE-109.340.740"])
        assert len(resp.data.uids) == 2
        assert resp.data.names[0] == "Novartis AG"


async def test_company_list_sends_query_as_search_param():
    with respx.mock(base_url=BASE_URL) as mock:
        route = mock.get("/v1/companies").mock(
            return_value=httpx.Response(
                200,
                json={"items": [], "totalCount": 0, "page": 1, "pageSize": 20},
            )
        )

        client = vynco.AsyncClient("vc_test_key", base_url=BASE_URL, max_retries=0)
        await client.companies.list(query="Novartis")

        assert route.called
        request = route.calls[0].request
        assert "search=Novartis" in str(request.url)


def test_sync_company_list():
    with respx.mock(base_url=BASE_URL) as mock:
        mock.get("/v1/companies").mock(
            return_value=httpx.Response(
                200,
                json={
                    "items": [
                        {"uid": "CHE-105.805.080", "name": "Novartis AG", "canton": "BS"}
                    ],
                    "totalCount": 1,
                    "page": 1,
                    "pageSize": 20,
                },
            )
        )

        client = vynco.Client("vc_test_key", base_url=BASE_URL, max_retries=0)
        resp = client.companies.list(query="Novartis")
        assert resp.data.items[0].name == "Novartis AG"
