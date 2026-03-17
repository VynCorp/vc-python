"""Tests for company resource operations."""

from __future__ import annotations

import httpx
import respx

import vynco

BASE_URL = "https://api.vynco.ch/v1"


async def test_company_search_parses_paginated_response():
    with respx.mock(base_url=BASE_URL) as mock:
        mock.get("/companies").mock(
            return_value=httpx.Response(
                200,
                json={
                    "items": [
                        {
                            "uid": "CHE-100.023.968",
                            "name": "Novartis AG",
                            "legalSeat": "Basel",
                            "canton": "BS",
                            "legalForm": "AG",
                            "status": "ACTIVE",
                            "purpose": "Pharmaceutical company",
                            "capitalNominal": 1320000000.0,
                            "capitalCurrency": "CHF",
                            "auditorName": "KPMG AG",
                            "registrationDate": "1996-12-20",
                            "dataSource": "Zefix",
                            "lastModified": "2026-01-15T10:30:00Z",
                        }
                    ],
                    "total": 1,
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
        resp = await client.companies.search(query="Novartis", canton="BS")

        assert resp.data.total == 1
        assert len(resp.data.items) == 1
        assert resp.data.items[0].uid == "CHE-100.023.968"
        assert resp.data.items[0].name == "Novartis AG"
        assert resp.data.items[0].canton == "BS"
        assert resp.data.items[0].legal_form == "AG"

        assert resp.meta.request_id == "req-abc-123"
        assert resp.meta.credits_used == 1
        assert resp.meta.credits_remaining == 499
        assert resp.meta.rate_limit_limit == 60
        assert resp.meta.data_source == "Zefix"


async def test_company_search_with_total_count():
    """Test that PaginatedResponse accepts 'totalCount' as an alias for 'total'."""
    with respx.mock(base_url=BASE_URL) as mock:
        mock.get("/companies").mock(
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
        resp = await client.companies.search()
        assert resp.data.total == 42


async def test_company_get_by_uid():
    with respx.mock(base_url=BASE_URL) as mock:
        mock.get("/companies/CHE-100.023.968").mock(
            return_value=httpx.Response(
                200,
                json={
                    "uid": "CHE-100.023.968",
                    "name": "Novartis AG",
                    "legalSeat": "Basel",
                    "canton": "BS",
                    "legalForm": "AG",
                    "status": "ACTIVE",
                    "capitalNominal": 1320000000.0,
                    "capitalCurrency": "CHF",
                    "dataSource": "Zefix",
                    "lastModified": "2026-01-15T10:30:00Z",
                },
            )
        )

        client = vynco.AsyncClient("vc_test_key", base_url=BASE_URL, max_retries=0)
        resp = await client.companies.get("CHE-100.023.968")

        assert resp.data.name == "Novartis AG"
        assert resp.data.status == "ACTIVE"
        assert resp.data.capital_nominal == 1_320_000_000.0


async def test_company_count():
    with respx.mock(base_url=BASE_URL) as mock:
        mock.get("/companies/count").mock(
            return_value=httpx.Response(200, json={"count": 320000})
        )

        client = vynco.AsyncClient("vc_test_key", base_url=BASE_URL, max_retries=0)
        resp = await client.companies.count()
        assert resp.data.count == 320000


async def test_company_persons():
    with respx.mock(base_url=BASE_URL) as mock:
        mock.get("/companies/CHE-100.023.968/persons").mock(
            return_value=httpx.Response(
                200,
                json=[
                    {
                        "personId": "p-001",
                        "firstName": "Vasant",
                        "lastName": "Narasimhan",
                        "role": "CEO",
                        "since": "2018-02-01",
                    }
                ],
            )
        )

        client = vynco.AsyncClient("vc_test_key", base_url=BASE_URL, max_retries=0)
        resp = await client.companies.persons("CHE-100.023.968")

        assert len(resp.data) == 1
        assert resp.data[0].first_name == "Vasant"
        assert resp.data[0].role == "CEO"


async def test_company_changes():
    with respx.mock(base_url=BASE_URL) as mock:
        mock.get("/companies/CHE-100.023.968/changes").mock(
            return_value=httpx.Response(
                200,
                json=[
                    {
                        "id": "c-001",
                        "companyUid": "CHE-100.023.968",
                        "changeType": "AUDITOR_CHANGE",
                        "fieldName": "auditorName",
                        "oldValue": "PwC AG",
                        "newValue": "KPMG AG",
                        "detectedAt": "2026-01-15T10:30:00Z",
                    }
                ],
            )
        )

        client = vynco.AsyncClient("vc_test_key", base_url=BASE_URL, max_retries=0)
        resp = await client.companies.changes("CHE-100.023.968")

        assert len(resp.data) == 1
        assert resp.data[0].change_type == "AUDITOR_CHANGE"
        assert resp.data[0].new_value == "KPMG AG"


async def test_company_search_sends_query_as_search_param():
    with respx.mock(base_url=BASE_URL) as mock:
        route = mock.get("/companies").mock(
            return_value=httpx.Response(
                200, json={"items": [], "total": 0, "page": 1, "pageSize": 20},
            )
        )

        client = vynco.AsyncClient("vc_test_key", base_url=BASE_URL, max_retries=0)
        await client.companies.search(query="Novartis")

        assert route.called
        request = route.calls[0].request
        assert "search=Novartis" in str(request.url)


def test_sync_company_search():
    with respx.mock(base_url=BASE_URL) as mock:
        mock.get("/companies").mock(
            return_value=httpx.Response(
                200,
                json={
                    "items": [
                        {"uid": "CHE-100.023.968", "name": "Novartis AG", "canton": "BS"}
                    ],
                    "total": 1,
                    "page": 1,
                    "pageSize": 20,
                },
            )
        )

        client = vynco.Client("vc_test_key", base_url=BASE_URL, max_retries=0)
        resp = client.companies.search(query="Novartis")
        assert resp.data.items[0].name == "Novartis AG"
