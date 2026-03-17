"""Tests for all remaining resource operations."""

from __future__ import annotations

import httpx
import respx

import vynco

BASE_URL = "https://api.vynco.ch/v1"


# ---------------------------------------------------------------------------
# Credits
# ---------------------------------------------------------------------------


async def test_credit_balance():
    with respx.mock(base_url=BASE_URL) as mock:
        mock.get("/credits/balance").mock(
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
        assert resp.data.monthly_credits == 5000
        assert resp.data.used_this_month == 500
        assert resp.data.tier == "professional"


# ---------------------------------------------------------------------------
# API Keys
# ---------------------------------------------------------------------------


async def test_api_key_creation():
    with respx.mock(base_url=BASE_URL) as mock:
        mock.post("/api-keys").mock(
            return_value=httpx.Response(
                201,
                json={
                    "id": "key_abc123",
                    "name": "CI Pipeline",
                    "rawKey": "vc_live_abcdefghijklmnop1234567890ABCDEF",
                    "keyPrefix": "vc_live_",
                    "permissions": ["read"],
                    "createdAt": "2026-03-17T12:00:00Z",
                },
            )
        )

        client = vynco.AsyncClient("vc_test_key", base_url=BASE_URL, max_retries=0)
        resp = await client.api_keys.create(name="CI Pipeline", permissions=["read"])

        assert resp.data.id == "key_abc123"
        assert resp.data.name == "CI Pipeline"
        assert resp.data.raw_key.startswith("vc_live_")


async def test_api_key_list():
    with respx.mock(base_url=BASE_URL) as mock:
        mock.get("/api-keys").mock(
            return_value=httpx.Response(
                200,
                json=[
                    {
                        "id": "key_001",
                        "name": "Production",
                        "keyPrefix": "vc_live_",
                        "keyHint": "****ABCD",
                        "permissions": ["read", "write"],
                        "isActive": True,
                        "createdAt": "2026-01-01T00:00:00Z",
                    }
                ],
            )
        )

        client = vynco.AsyncClient("vc_test_key", base_url=BASE_URL, max_retries=0)
        resp = await client.api_keys.list()

        assert len(resp.data) == 1
        assert resp.data[0].is_active is True


async def test_api_key_revoke():
    with respx.mock(base_url=BASE_URL) as mock:
        mock.delete("/api-keys/key_001").mock(
            return_value=httpx.Response(204)
        )

        client = vynco.AsyncClient("vc_test_key", base_url=BASE_URL, max_retries=0)
        meta = await client.api_keys.revoke("key_001")
        assert isinstance(meta, vynco.ResponseMeta)


# ---------------------------------------------------------------------------
# Persons
# ---------------------------------------------------------------------------


async def test_person_get():
    with respx.mock(base_url=BASE_URL) as mock:
        mock.get("/persons/p-001").mock(
            return_value=httpx.Response(
                200,
                json={
                    "id": "p-001",
                    "firstName": "Vasant",
                    "lastName": "Narasimhan",
                    "roles": [
                        {
                            "personId": "p-001",
                            "firstName": "Vasant",
                            "lastName": "Narasimhan",
                            "role": "CEO",
                            "since": "2018-02-01",
                        }
                    ],
                },
            )
        )

        client = vynco.AsyncClient("vc_test_key", base_url=BASE_URL, max_retries=0)
        resp = await client.persons.get("p-001")

        assert resp.data.first_name == "Vasant"
        assert len(resp.data.roles) == 1


async def test_person_search():
    with respx.mock(base_url=BASE_URL) as mock:
        mock.post("/persons/search").mock(
            return_value=httpx.Response(
                200,
                json=[
                    {
                        "id": "p-001",
                        "firstName": "Vasant",
                        "lastName": "Narasimhan",
                        "roles": [],
                    }
                ],
            )
        )

        client = vynco.AsyncClient("vc_test_key", base_url=BASE_URL, max_retries=0)
        resp = await client.persons.search(name="Narasimhan")

        assert len(resp.data) == 1
        assert resp.data[0].last_name == "Narasimhan"


# ---------------------------------------------------------------------------
# Dossiers
# ---------------------------------------------------------------------------


async def test_dossier_generate():
    with respx.mock(base_url=BASE_URL) as mock:
        mock.post("/dossiers").mock(
            return_value=httpx.Response(
                200,
                json={
                    "id": "d-001",
                    "companyUid": "CHE-100.023.968",
                    "status": "completed",
                    "executiveSummary": "Novartis is a global healthcare company.",
                    "keyInsights": ["Leading pharma", "Swiss HQ"],
                    "riskFactors": ["Patent cliffs"],
                    "generatedAt": "2026-03-17T12:00:00Z",
                },
            )
        )

        client = vynco.AsyncClient("vc_test_key", base_url=BASE_URL, max_retries=0)
        resp = await client.dossiers.generate("CHE-100.023.968", level="comprehensive")

        assert resp.data.status == "completed"
        assert resp.data.executive_summary is not None
        assert len(resp.data.key_insights) == 2


# ---------------------------------------------------------------------------
# Teams
# ---------------------------------------------------------------------------


async def test_team_me():
    with respx.mock(base_url=BASE_URL) as mock:
        mock.get("/teams/me").mock(
            return_value=httpx.Response(
                200,
                json={
                    "id": "team_001",
                    "name": "Acme Corp",
                    "slug": "acme-corp",
                    "tier": "enterprise",
                    "creditBalance": 10000,
                    "monthlyCredits": 10000,
                    "overageRate": 0.002,
                    "createdAt": "2025-06-01T00:00:00Z",
                },
            )
        )

        client = vynco.AsyncClient("vc_test_key", base_url=BASE_URL, max_retries=0)
        resp = await client.teams.me()

        assert resp.data.name == "Acme Corp"
        assert resp.data.credit_balance == 10000


# ---------------------------------------------------------------------------
# Webhooks
# ---------------------------------------------------------------------------


async def test_webhook_create():
    with respx.mock(base_url=BASE_URL) as mock:
        mock.post("/webhooks").mock(
            return_value=httpx.Response(
                201,
                json={
                    "id": "wh_001",
                    "url": "https://example.com/webhook",
                    "events": ["company.changed"],
                    "secret": "whsec_abc123",
                    "createdAt": "2026-03-17T12:00:00Z",
                },
            )
        )

        client = vynco.AsyncClient("vc_test_key", base_url=BASE_URL, max_retries=0)
        resp = await client.webhooks.create(
            url="https://example.com/webhook", events=["company.changed"],
        )
        assert resp.data.secret == "whsec_abc123"


async def test_webhook_delete():
    with respx.mock(base_url=BASE_URL) as mock:
        mock.delete("/webhooks/wh_001").mock(
            return_value=httpx.Response(204)
        )

        client = vynco.AsyncClient("vc_test_key", base_url=BASE_URL, max_retries=0)
        meta = await client.webhooks.delete("wh_001")
        assert isinstance(meta, vynco.ResponseMeta)


# ---------------------------------------------------------------------------
# Billing
# ---------------------------------------------------------------------------


async def test_billing_create_checkout():
    with respx.mock(base_url=BASE_URL) as mock:
        mock.post("/billing/checkout").mock(
            return_value=httpx.Response(
                200, json={"url": "https://checkout.stripe.com/session_123"},
            )
        )

        client = vynco.AsyncClient("vc_test_key", base_url=BASE_URL, max_retries=0)
        resp = await client.billing.create_checkout("professional")
        assert "stripe.com" in resp.data.url


# ---------------------------------------------------------------------------
# Users
# ---------------------------------------------------------------------------


async def test_user_me():
    with respx.mock(base_url=BASE_URL) as mock:
        mock.get("/users/me").mock(
            return_value=httpx.Response(
                200,
                json={
                    "id": "user_001",
                    "name": "John Doe",
                    "email": "john@example.com",
                    "avatar": "",
                    "plan": "professional",
                    "creditBalance": 4500,
                },
            )
        )

        client = vynco.AsyncClient("vc_test_key", base_url=BASE_URL, max_retries=0)
        resp = await client.users.me()

        assert resp.data.name == "John Doe"
        assert resp.data.plan == "professional"


# ---------------------------------------------------------------------------
# Settings
# ---------------------------------------------------------------------------


async def test_settings_get():
    with respx.mock(base_url=BASE_URL) as mock:
        mock.get("/settings").mock(
            return_value=httpx.Response(
                200, json={"theme": "dark", "language": "en"},
            )
        )

        client = vynco.AsyncClient("vc_test_key", base_url=BASE_URL, max_retries=0)
        resp = await client.settings.get()
        assert resp.data["theme"] == "dark"


# ---------------------------------------------------------------------------
# Changes
# ---------------------------------------------------------------------------


async def test_changes_list():
    with respx.mock(base_url=BASE_URL) as mock:
        mock.get("/changes").mock(
            return_value=httpx.Response(
                200,
                json={
                    "items": [
                        {
                            "id": "c-001",
                            "companyUid": "CHE-100.023.968",
                            "changeType": "AUDITOR_CHANGE",
                            "fieldName": "auditorName",
                            "detectedAt": "2026-03-17T12:00:00Z",
                        }
                    ],
                    "total": 1,
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
        mock.get("/analytics/cantons").mock(
            return_value=httpx.Response(
                200,
                json=[
                    {
                        "canton": "ZH",
                        "companyCount": 50000,
                        "activeCount": 45000,
                        "changeCount": 1200,
                    },
                    {
                        "canton": "BS",
                        "companyCount": 15000,
                        "activeCount": 13000,
                        "changeCount": 800,
                    },
                ],
            )
        )

        client = vynco.AsyncClient("vc_test_key", base_url=BASE_URL, max_retries=0)
        resp = await client.analytics.cantons()

        assert len(resp.data) == 2
        assert resp.data[0].canton == "ZH"
        assert resp.data[0].company_count == 50000
