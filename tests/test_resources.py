"""Tests for all resource operations."""

from __future__ import annotations

import httpx
import respx

import vynco

BASE_URL = "https://vynco.ch/api"


# ---------------------------------------------------------------------------
# Health
# ---------------------------------------------------------------------------


async def test_health_check():
    with respx.mock(base_url=BASE_URL) as mock:
        mock.get("/health").mock(
            return_value=httpx.Response(
                200,
                json={
                    "status": "ok",
                    "database": "ok",
                    "redis": "ok",
                    "version": "2.0.0",
                },
            )
        )

        client = vynco.AsyncClient("vc_test_key", base_url=BASE_URL, max_retries=0)
        resp = await client.health.check()

        assert resp.data.status == "ok"
        assert resp.data.version == "2.0.0"


# ---------------------------------------------------------------------------
# Credits
# ---------------------------------------------------------------------------


async def test_credit_balance():
    with respx.mock(base_url=BASE_URL) as mock:
        mock.get("/v1/credits/balance").mock(
            return_value=httpx.Response(
                200,
                json={
                    "balance": 4500,
                    "monthlyCredits": 5000,
                    "usedThisMonth": 500,
                    "tier": "professional",
                    "overageRate": 0.005,
                },
            )
        )

        client = vynco.AsyncClient("vc_test_key", base_url=BASE_URL, max_retries=0)
        resp = await client.credits.balance()

        assert resp.data.balance == 4500
        assert resp.data.tier == "professional"


async def test_credit_history():
    with respx.mock(base_url=BASE_URL) as mock:
        mock.get("/v1/credits/history").mock(
            return_value=httpx.Response(
                200,
                json={
                    "items": [
                        {
                            "id": 1,
                            "entryType": "debit",
                            "amount": -1,
                            "balance": 4999,
                            "description": "company.get",
                            "createdAt": "2026-03-17T12:00:00Z",
                        }
                    ],
                    "total": 1,
                },
            )
        )

        client = vynco.AsyncClient("vc_test_key", base_url=BASE_URL, max_retries=0)
        resp = await client.credits.history(limit=10)

        assert len(resp.data.items) == 1
        assert resp.data.items[0].entry_type == "debit"


# ---------------------------------------------------------------------------
# API Keys
# ---------------------------------------------------------------------------


async def test_api_key_creation():
    with respx.mock(base_url=BASE_URL) as mock:
        mock.post("/v1/api-keys").mock(
            return_value=httpx.Response(
                201,
                json={
                    "id": "key_abc123",
                    "name": "CI Pipeline",
                    "key": "vc_live_abcdefghijklmnop1234567890ABCDEF",
                    "prefix": "vc_live_",
                    "environment": "live",
                    "scopes": [],
                    "createdAt": "2026-03-18T00:00:00Z",
                    "warning": "",
                },
            )
        )

        client = vynco.AsyncClient("vc_test_key", base_url=BASE_URL, max_retries=0)
        resp = await client.api_keys.create(name="CI Pipeline")

        assert resp.data.id == "key_abc123"
        assert resp.data.key.startswith("vc_live_")


async def test_api_key_list():
    with respx.mock(base_url=BASE_URL) as mock:
        mock.get("/v1/api-keys").mock(
            return_value=httpx.Response(
                200,
                json=[
                    {
                        "id": "key_001",
                        "name": "Production",
                        "prefix": "vc_live_",
                        "environment": "live",
                        "scopes": [],
                        "status": "active",
                        "createdAt": "2026-01-01T00:00:00Z",
                    }
                ],
            )
        )

        client = vynco.AsyncClient("vc_test_key", base_url=BASE_URL, max_retries=0)
        resp = await client.api_keys.list()

        assert len(resp.data) == 1
        assert resp.data[0].name == "Production"


async def test_api_key_revoke():
    with respx.mock(base_url=BASE_URL) as mock:
        mock.delete("/v1/api-keys/key_001").mock(return_value=httpx.Response(204))

        client = vynco.AsyncClient("vc_test_key", base_url=BASE_URL, max_retries=0)
        meta = await client.api_keys.revoke("key_001")
        assert isinstance(meta, vynco.ResponseMeta)


# ---------------------------------------------------------------------------
# Persons
# ---------------------------------------------------------------------------


async def test_person_board_members():
    with respx.mock(base_url=BASE_URL) as mock:
        mock.get("/v1/persons/board-members/CHE-105.805.080").mock(
            return_value=httpx.Response(
                200,
                json=[
                    {
                        "id": "p-001",
                        "firstName": "Vasant",
                        "lastName": "Narasimhan",
                        "role": "CEO",
                        "roleCategory": "management",
                    },
                    {
                        "id": "p-002",
                        "firstName": "Joerg",
                        "lastName": "Reinhardt",
                        "role": "Chairman",
                        "roleCategory": "board",
                    },
                ],
            )
        )

        client = vynco.AsyncClient("vc_test_key", base_url=BASE_URL, max_retries=0)
        resp = await client.persons.board_members("CHE-105.805.080")

        assert len(resp.data) == 2
        assert resp.data[0].first_name == "Vasant"
        assert resp.data[1].role == "Chairman"


# ---------------------------------------------------------------------------
# Dossiers
# ---------------------------------------------------------------------------


async def test_dossier_create():
    with respx.mock(base_url=BASE_URL) as mock:
        mock.post("/v1/dossiers").mock(
            return_value=httpx.Response(
                200,
                json={
                    "id": "dos-001",
                    "userId": "u-001",
                    "companyUid": "CHE-105.805.080",
                    "companyName": "Novartis AG",
                    "level": "detailed",
                    "content": "Novartis is a global healthcare company.",
                    "sources": ["zefix", "sogc"],
                    "createdAt": "2026-03-17T12:00:00Z",
                },
            )
        )

        client = vynco.AsyncClient("vc_test_key", base_url=BASE_URL, max_retries=0)
        resp = await client.dossiers.create(uid="CHE-105.805.080", level="detailed")

        assert resp.data.company_uid == "CHE-105.805.080"
        assert "healthcare" in resp.data.content


async def test_dossier_list():
    with respx.mock(base_url=BASE_URL) as mock:
        mock.get("/v1/dossiers").mock(
            return_value=httpx.Response(
                200,
                json=[
                    {
                        "id": "dos-001",
                        "companyUid": "CHE-105.805.080",
                        "companyName": "Novartis AG",
                        "level": "standard",
                        "createdAt": "2026-03-17T12:00:00Z",
                    }
                ],
            )
        )

        client = vynco.AsyncClient("vc_test_key", base_url=BASE_URL, max_retries=0)
        resp = await client.dossiers.list()

        assert len(resp.data) == 1
        assert resp.data[0].company_name == "Novartis AG"


async def test_dossier_delete():
    with respx.mock(base_url=BASE_URL) as mock:
        mock.delete("/v1/dossiers/dos-001").mock(return_value=httpx.Response(204))

        client = vynco.AsyncClient("vc_test_key", base_url=BASE_URL, max_retries=0)
        meta = await client.dossiers.delete("dos-001")
        assert isinstance(meta, vynco.ResponseMeta)


# ---------------------------------------------------------------------------
# Teams
# ---------------------------------------------------------------------------


async def test_team_me():
    with respx.mock(base_url=BASE_URL) as mock:
        mock.get("/v1/teams/me").mock(
            return_value=httpx.Response(
                200,
                json={
                    "id": "team_001",
                    "name": "Acme Corp",
                    "slug": "acme-corp",
                    "tier": "enterprise",
                    "creditBalance": 10000,
                    "monthlyCredits": 10000,
                },
            )
        )

        client = vynco.AsyncClient("vc_test_key", base_url=BASE_URL, max_retries=0)
        resp = await client.teams.me()

        assert resp.data.name == "Acme Corp"
        assert resp.data.credit_balance == 10000


async def test_team_members():
    with respx.mock(base_url=BASE_URL) as mock:
        mock.get("/v1/teams/me/members").mock(
            return_value=httpx.Response(
                200,
                json=[
                    {
                        "id": "m-001",
                        "name": "John Doe",
                        "email": "john@acme.com",
                        "role": "Owner",
                        "lastLoginAt": "2026-03-17T12:00:00Z",
                    }
                ],
            )
        )

        client = vynco.AsyncClient("vc_test_key", base_url=BASE_URL, max_retries=0)
        resp = await client.teams.members()

        assert len(resp.data) == 1
        assert resp.data[0].role == "Owner"


async def test_team_invite_member():
    with respx.mock(base_url=BASE_URL) as mock:
        mock.post("/v1/teams/me/members").mock(
            return_value=httpx.Response(
                201,
                json={
                    "id": "inv-001",
                    "teamId": "team_001",
                    "email": "jane@acme.com",
                    "role": "member",
                    "token": "tok-abc",
                    "status": "pending",
                    "createdAt": "2026-03-18T00:00:00Z",
                    "expiresAt": "2026-03-25T00:00:00Z",
                },
            )
        )

        client = vynco.AsyncClient("vc_test_key", base_url=BASE_URL, max_retries=0)
        resp = await client.teams.invite_member(email="jane@acme.com", role="member")

        assert resp.data.email == "jane@acme.com"
        assert resp.data.status == "pending"


async def test_team_remove_member():
    with respx.mock(base_url=BASE_URL) as mock:
        mock.delete("/v1/teams/me/members/m-002").mock(return_value=httpx.Response(204))

        client = vynco.AsyncClient("vc_test_key", base_url=BASE_URL, max_retries=0)
        meta = await client.teams.remove_member("m-002")
        assert isinstance(meta, vynco.ResponseMeta)


# ---------------------------------------------------------------------------
# Screening
# ---------------------------------------------------------------------------


async def test_screening():
    with respx.mock(base_url=BASE_URL) as mock:
        mock.post("/v1/screening").mock(
            return_value=httpx.Response(
                200,
                json={
                    "queryName": "Suspicious Corp",
                    "screenedAt": "2026-03-18T00:00:00Z",
                    "hitCount": 0,
                    "riskLevel": "clear",
                    "hits": [],
                    "sourcesChecked": ["seco", "opensanctions"],
                },
            )
        )

        client = vynco.AsyncClient("vc_test_key", base_url=BASE_URL, max_retries=0)
        resp = await client.screening.screen(name="Suspicious Corp")

        assert resp.data.risk_level == "clear"
        assert resp.data.hit_count == 0


# ---------------------------------------------------------------------------
# AI
# ---------------------------------------------------------------------------


async def test_ai_risk_score():
    with respx.mock(base_url=BASE_URL) as mock:
        mock.post("/v1/ai/risk-score").mock(
            return_value=httpx.Response(
                200,
                json={
                    "uid": "CHE-105.805.080",
                    "companyName": "Novartis AG",
                    "overallScore": 15,
                    "riskLevel": "low",
                    "breakdown": [
                        {
                            "factor": "auditor",
                            "score": 5,
                            "weight": 0.3,
                            "description": "Big 4 auditor",
                        },
                    ],
                    "assessedAt": "2026-03-18T00:00:00Z",
                },
            )
        )

        client = vynco.AsyncClient("vc_test_key", base_url=BASE_URL, max_retries=0)
        resp = await client.ai.risk_score(uid="CHE-105.805.080")

        assert resp.data.overall_score == 15
        assert resp.data.risk_level == "low"


# ---------------------------------------------------------------------------
# Watchlists
# ---------------------------------------------------------------------------


async def test_watchlist_create():
    with respx.mock(base_url=BASE_URL) as mock:
        mock.post("/v1/watchlists").mock(
            return_value=httpx.Response(
                201,
                json={
                    "id": "wl-001",
                    "name": "Key Clients",
                    "description": "Top clients to monitor",
                    "createdAt": "2026-03-18T00:00:00Z",
                    "updatedAt": "2026-03-18T00:00:00Z",
                },
            )
        )

        client = vynco.AsyncClient("vc_test_key", base_url=BASE_URL, max_retries=0)
        resp = await client.watchlists.create(
            name="Key Clients", description="Top clients to monitor"
        )

        assert resp.data.name == "Key Clients"


async def test_watchlist_list():
    with respx.mock(base_url=BASE_URL) as mock:
        mock.get("/v1/watchlists").mock(
            return_value=httpx.Response(
                200,
                json=[
                    {
                        "id": "wl-001",
                        "name": "Key Clients",
                        "description": "",
                        "companyCount": 5,
                        "createdAt": "2026-03-18T00:00:00Z",
                    }
                ],
            )
        )

        client = vynco.AsyncClient("vc_test_key", base_url=BASE_URL, max_retries=0)
        resp = await client.watchlists.list()

        assert len(resp.data) == 1
        assert resp.data[0].company_count == 5


async def test_watchlist_delete():
    with respx.mock(base_url=BASE_URL) as mock:
        mock.delete("/v1/watchlists/wl-001").mock(return_value=httpx.Response(204))

        client = vynco.AsyncClient("vc_test_key", base_url=BASE_URL, max_retries=0)
        meta = await client.watchlists.delete("wl-001")
        assert isinstance(meta, vynco.ResponseMeta)


# ---------------------------------------------------------------------------
# Billing
# ---------------------------------------------------------------------------


async def test_billing_create_checkout():
    with respx.mock(base_url=BASE_URL) as mock:
        mock.post("/v1/billing/checkout-session").mock(
            return_value=httpx.Response(
                200,
                json={"url": "https://checkout.stripe.com/session_123"},
            )
        )

        client = vynco.AsyncClient("vc_test_key", base_url=BASE_URL, max_retries=0)
        resp = await client.billing.create_checkout(tier="professional")
        assert "stripe.com" in resp.data.url


# ---------------------------------------------------------------------------
# Changes
# ---------------------------------------------------------------------------


async def test_changes_list():
    with respx.mock(base_url=BASE_URL) as mock:
        mock.get("/v1/changes").mock(
            return_value=httpx.Response(
                200,
                json={
                    "items": [
                        {
                            "id": "c-001",
                            "companyUid": "CHE-105.805.080",
                            "companyName": "Novartis AG",
                            "changeType": "AUDITOR_CHANGE",
                            "fieldName": "auditorName",
                            "detectedAt": "2026-03-17T12:00:00Z",
                        }
                    ],
                    "totalCount": 1,
                    "page": 1,
                    "pageSize": 20,
                },
            )
        )

        client = vynco.AsyncClient("vc_test_key", base_url=BASE_URL, max_retries=0)
        resp = await client.changes.list()

        assert resp.data.total == 1
        assert resp.data.items[0].change_type == "AUDITOR_CHANGE"


# ---------------------------------------------------------------------------
# Analytics
# ---------------------------------------------------------------------------


async def test_analytics_cantons():
    with respx.mock(base_url=BASE_URL) as mock:
        mock.get("/v1/analytics/cantons").mock(
            return_value=httpx.Response(
                200,
                json=[
                    {"canton": "ZH", "count": 50000, "percentage": 15.6},
                    {"canton": "BS", "count": 15000, "percentage": 4.7},
                ],
            )
        )

        client = vynco.AsyncClient("vc_test_key", base_url=BASE_URL, max_retries=0)
        resp = await client.analytics.cantons()

        assert len(resp.data) == 2
        assert resp.data[0].canton == "ZH"


async def test_analytics_cluster():
    with respx.mock(base_url=BASE_URL) as mock:
        mock.post("/v1/analytics/cluster").mock(
            return_value=httpx.Response(
                200,
                json={
                    "clusters": [
                        {"id": 0, "centroid": {}, "companyCount": 150, "sampleCompanies": []},
                    ]
                },
            )
        )

        client = vynco.AsyncClient("vc_test_key", base_url=BASE_URL, max_retries=0)
        resp = await client.analytics.cluster(algorithm="kmeans", k=3)

        assert len(resp.data.clusters) == 1
        assert resp.data.clusters[0].company_count == 150


async def test_analytics_cohorts():
    with respx.mock(base_url=BASE_URL) as mock:
        mock.get("/v1/analytics/cohorts").mock(
            return_value=httpx.Response(
                200,
                json={
                    "cohorts": [{"group": "2020", "count": 5000, "metric": "count"}],
                    "groupBy": "year",
                    "metric": "count",
                },
            )
        )

        client = vynco.AsyncClient("vc_test_key", base_url=BASE_URL, max_retries=0)
        resp = await client.analytics.cohorts(group_by="year")

        assert len(resp.data.cohorts) == 1
        assert resp.data.group_by == "year"
