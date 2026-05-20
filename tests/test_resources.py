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
# Usage
# ---------------------------------------------------------------------------


async def test_usage_current():
    with respx.mock(base_url=BASE_URL) as mock:
        mock.get("/v1/usage/current").mock(
            return_value=httpx.Response(
                200,
                json={
                    "tier": "professional",
                    "groups": [
                        {
                            "group": "search",
                            "used": 12,
                            "limit": 600,
                            "window": "hour",
                            "resetSeconds": 1800,
                        },
                        {
                            "group": "bulk",
                            "used": None,
                            "limit": None,
                            "window": "day",
                            "resetSeconds": 40000,
                        },
                    ],
                },
            )
        )

        client = vynco.AsyncClient("vc_test_key", base_url=BASE_URL, max_retries=0)
        resp = await client.usage.current()

        assert resp.data.tier == "professional"
        assert resp.data.groups[0].group == "search"
        assert resp.data.groups[0].limit == 600
        assert resp.data.groups[1].used is None


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
                    "stripeSubscriptionId": "sub_123",
                    "currentPeriodEnd": "2026-12-31T00:00:00Z",
                    "cancellationEffectiveAt": None,
                },
            )
        )

        client = vynco.AsyncClient("vc_test_key", base_url=BASE_URL, max_retries=0)
        resp = await client.teams.me()

        assert resp.data.name == "Acme Corp"
        assert resp.data.tier == "enterprise"
        assert resp.data.stripe_subscription_id == "sub_123"
        assert resp.data.current_period_end == "2026-12-31T00:00:00Z"
        assert resp.data.cancellation_effective_at is None


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


# ---------------------------------------------------------------------------
# Reconciliation regression tests (API alignment v4)
# ---------------------------------------------------------------------------


async def test_ubo_person_id_is_uuid_string_and_parent_fields():
    # Regression: person_id is a UUID string on the wire, not an int; and the
    # response carries ultimate_parent_lei / ultimate_parent_name.
    with respx.mock(base_url=BASE_URL) as mock:
        mock.get("/v1/companies/CHE-105.805.080/ubo").mock(
            return_value=httpx.Response(
                200,
                json={
                    "uid": "CHE-105.805.080",
                    "companyName": "Novartis AG",
                    "uboPersons": [
                        {
                            "personId": "3f2504e0-4f89-41d3-9a0c-0305e82c3301",
                            "name": "Jane Doe",
                            "controllingEntityUid": "CHE-105.805.080",
                            "controllingEntityName": "Novartis AG",
                            "role": "beneficial_owner",
                            "pathLength": 1,
                        }
                    ],
                    "ownershipChain": [],
                    "chainDepth": 1,
                    "riskFlags": [],
                    "ultimateParentLei": "5493000IBP32UQZ0KL24",
                    "ultimateParentName": "Novartis Holding",
                },
            )
        )

        client = vynco.AsyncClient("vc_test_key", base_url=BASE_URL, max_retries=0)
        resp = await client.companies.ubo("CHE-105.805.080")

        assert resp.data.ubo_persons[0].person_id == "3f2504e0-4f89-41d3-9a0c-0305e82c3301"
        assert resp.data.ultimate_parent_lei == "5493000IBP32UQZ0KL24"
        assert resp.data.ultimate_parent_name == "Novartis Holding"


async def test_company_diff_from_field_alias():
    # Regression: the wire key is the reserved word "from"; it must populate
    # DiffEntry.from_value (previously aliased to "fromValue" → always None).
    with respx.mock(base_url=BASE_URL) as mock:
        mock.get("/v1/companies/CHE-105.805.080/diff").mock(
            return_value=httpx.Response(
                200,
                json={
                    "uid": "CHE-105.805.080",
                    "since": "2026-01-01",
                    "until": "2026-05-01",
                    "changes": [
                        {
                            "field": "address",
                            "from": "Old St 1",
                            "to": "New Ave 2",
                            "changedAt": "2026-03-01T00:00:00Z",
                            "changeType": "address_change",
                        }
                    ],
                    "totalChanges": 1,
                },
            )
        )

        client = vynco.AsyncClient("vc_test_key", base_url=BASE_URL, max_retries=0)
        resp = await client.changes.diff("CHE-105.805.080", since="2026-01-01")

        assert resp.data.changes[0].from_value == "Old St 1"
        assert resp.data.changes[0].to == "New Ave 2"


async def test_dossier_includes_citations():
    # Regression: managed dossiers carry a citations array (was dropped).
    with respx.mock(base_url=BASE_URL) as mock:
        mock.get("/v1/dossiers/dos-001").mock(
            return_value=httpx.Response(
                200,
                json={
                    "id": "dos-001",
                    "userId": "user-1",
                    "companyUid": "CHE-105.805.080",
                    "companyName": "Novartis AG",
                    "level": "detailed",
                    "content": "Body with [[obl:aml-1]] tag.",
                    "sources": ["zefix"],
                    "citations": [
                        {
                            "id": "aml-1",
                            "regulationId": "GwG",
                            "regulationTitle": "Anti-Money Laundering Act",
                            "article": "Art. 3",
                            "jurisdiction": "CH",
                            "sourceUrl": "https://example.ch/gwg",
                            "excerpt": "Due diligence obligations...",
                        }
                    ],
                    "createdAt": "2026-05-01T00:00:00Z",
                },
            )
        )

        client = vynco.AsyncClient("vc_test_key", base_url=BASE_URL, max_retries=0)
        resp = await client.dossiers.get("dos-001")

        assert len(resp.data.citations) == 1
        assert resp.data.citations[0].regulation_id == "GwG"
        assert resp.data.citations[0].source_url == "https://example.ch/gwg"


async def test_company_list_new_filters_serialize_to_camelcase():
    # Regression: new SearchParams filters must hit the camelCase wire keys.
    with respx.mock(base_url=BASE_URL) as mock:
        route = mock.get("/v1/companies").mock(
            return_value=httpx.Response(200, json={"items": [], "total": 0})
        )

        client = vynco.AsyncClient("vc_test_key", base_url=BASE_URL, max_retries=0)
        await client.companies.list(
            is_finma_regulated=True,
            noga_section="K",
            data_quality_min=0.5,
            has_lei=True,
            status_canonical="active",
            uids="CHE-1,CHE-2",
        )

        params = route.calls[0].request.url.params
        assert params["isFinmaRegulated"] == "true"
        assert params["nogaSection"] == "K"
        assert params["dataQualityMin"] == "0.5"
        assert params["hasLei"] == "true"
        assert params["statusCanonical"] == "active"
        assert params["uids"] == "CHE-1,CHE-2"


# ---------------------------------------------------------------------------
# New resources (API alignment v4)
# ---------------------------------------------------------------------------


async def test_settings_get_and_update_preferences():
    with respx.mock(base_url=BASE_URL) as mock:
        body = {"theme": "dark", "language": "de", "customKey": 42}
        mock.get("/v1/settings/preferences").mock(return_value=httpx.Response(200, json=body))
        put = mock.put("/v1/settings/preferences").mock(return_value=httpx.Response(200, json=body))

        client = vynco.AsyncClient("vc_test_key", base_url=BASE_URL, max_retries=0)
        got = await client.settings.get_preferences()
        assert got.data.theme == "dark"
        # extra="allow" preserves unknown keys
        assert got.data.model_extra["customKey"] == 42

        await client.settings.update_preferences({"theme": "dark"})
        import json as _json

        assert _json.loads(put.calls[0].request.content)["theme"] == "dark"


async def test_notifications_list_and_mark_read_all():
    with respx.mock(base_url=BASE_URL) as mock:
        mock.get("/v1/notifications").mock(
            return_value=httpx.Response(
                200,
                json={
                    "items": [
                        {
                            "id": "n1",
                            "title": "Change detected",
                            "body": "Auditor changed",
                            "category": "change",
                            "isRead": False,
                            "link": None,
                            "createdAt": "2026-05-01T00:00:00Z",
                        }
                    ],
                    "total": 1,
                    "unreadCount": 1,
                },
            )
        )
        read = mock.post("/v1/notifications/read").mock(
            return_value=httpx.Response(200, json={"updated": 5})
        )

        client = vynco.AsyncClient("vc_test_key", base_url=BASE_URL, max_retries=0)
        lst = await client.notifications.list(unread=True)
        assert lst.data.unread_count == 1
        assert lst.data.items[0].is_read is False

        res = await client.notifications.mark_read(mark_all=True)
        assert res.data.updated == 5
        import json as _json

        assert _json.loads(read.calls[0].request.content) == {"all": True}


async def test_notifications_preferences_and_test():
    with respx.mock(base_url=BASE_URL) as mock:
        prefs = {
            "id": "00000000-0000-0000-0000-000000000000",
            "userId": "u1",
            "isEnabled": True,
            "deliveryMode": "DailyDigest",
            "channel": "Email",
            "emailAddress": "a@b.ch",
            "digestTime": "08:00:00",
            "watchedChangeTypes": ["auditor_change"],
            "createdAt": "2026-01-01T00:00:00Z",
            "updatedAt": "2026-01-01T00:00:00Z",
        }
        mock.get("/v1/notifications/preferences").mock(return_value=httpx.Response(200, json=prefs))
        put = mock.put("/v1/notifications/preferences").mock(
            return_value=httpx.Response(200, json=prefs)
        )
        mock.post("/v1/notifications/test").mock(
            return_value=httpx.Response(200, json={"message": "Test notification sent"})
        )

        client = vynco.AsyncClient("vc_test_key", base_url=BASE_URL, max_retries=0)
        got = await client.notifications.get_preferences()
        assert got.data.delivery_mode == "DailyDigest"
        assert got.data.watched_change_types == ["auditor_change"]

        await client.notifications.update_preferences(channel="Both", is_enabled=False)
        import json as _json

        sent = _json.loads(put.calls[0].request.content)
        assert sent == {"channel": "Both", "isEnabled": False}

        t = await client.notifications.test()
        assert t.data.message == "Test notification sent"


async def test_sync_status():
    with respx.mock(base_url=BASE_URL) as mock:
        mock.get("/v1/sync/status").mock(
            return_value=httpx.Response(
                200,
                json={
                    "pipelines": [
                        {
                            "pipeline": "zefix",
                            "status": "ok",
                            "itemsProcessed": 100,
                            "itemsTotal": 100,
                            "lastCompletedAt": "2026-05-01T00:00:00Z",
                            "lastStartedAt": None,
                            "health": "fresh",
                            "expectedRunIntervalMinutes": 1440,
                            "alertThresholdMinutes": None,
                            "dependsOn": None,
                            "minutesSinceCompletion": 12.5,
                        }
                    ]
                },
            )
        )

        client = vynco.AsyncClient("vc_test_key", base_url=BASE_URL, max_retries=0)
        resp = await client.sync.status()
        assert resp.data.pipelines[0].health == "fresh"
        assert resp.data.pipelines[0].alert_threshold_minutes is None
        assert resp.data.pipelines[0].minutes_since_completion == 12.5


async def test_audit_playbook():
    with respx.mock(base_url=BASE_URL) as mock:
        route = mock.get("/v1/audit/playbook/CHE-105.805.080").mock(
            return_value=httpx.Response(
                200,
                json={
                    "companyUid": "CHE-105.805.080",
                    "companyName": "Novartis AG",
                    "methodologyVersion": "2026.1",
                    "profile": {
                        "tiers": ["complex"],
                        "overlays": ["finma"],
                        "jurisdiction": "CH",
                        "rationale": ["listed entity"],
                    },
                    "totals": {"procedures": 1, "steps": 1, "standards": 1},
                    "phases": [
                        {
                            "phase": "planning",
                            "procedures": [
                                {
                                    "id": "p1",
                                    "title": "Understand entity",
                                    "topicId": None,
                                    "sourceTopic": "ISA315",
                                    "tiers": ["complex"],
                                    "overlays": [],
                                    "isUniversal": True,
                                    "stepCount": 1,
                                    "steps": [],
                                    "standards": [],
                                }
                            ],
                        }
                    ],
                },
            )
        )

        client = vynco.AsyncClient("vc_test_key", base_url=BASE_URL, max_retries=0)
        resp = await client.audit.playbook("CHE-105.805.080", tiers="complex,core")
        assert resp.data.profile.jurisdiction == "CH"
        assert resp.data.phases[0].procedures[0].is_universal is True
        assert route.calls[0].request.url.params["tiers"] == "complex,core"


async def test_compliance_scope():
    with respx.mock(base_url=BASE_URL) as mock:
        mock.get("/v1/compliance/scope/CHE-105.805.080").mock(
            return_value=httpx.Response(
                200,
                json={
                    "companyUid": "CHE-105.805.080",
                    "companyName": "Novartis AG",
                    "jurisdictions": ["ch", "intl"],
                    "totals": {
                        "regulations": 1,
                        "articles": 1,
                        "obligations": 1,
                        "controls": 0,
                        "evidence": 0,
                    },
                    "regulations": [
                        {
                            "id": "gwg",
                            "title": "AMLA",
                            "jurisdiction": "ch",
                            "regulationType": "law",
                            "status": "active",
                            "sourceUrl": None,
                            "effectiveDate": None,
                            "articles": [],
                            "unassignedObligations": [],
                        }
                    ],
                },
            )
        )

        client = vynco.AsyncClient("vc_test_key", base_url=BASE_URL, max_retries=0)
        resp = await client.compliance.scope("CHE-105.805.080")
        assert resp.data.jurisdictions == ["ch", "intl"]
        assert resp.data.regulations[0].title == "AMLA"


async def test_ownership_analytics():
    with respx.mock(base_url=BASE_URL) as mock:
        mock.get("/v1/ownership/CHE-105.805.080/analytics").mock(
            return_value=httpx.Response(
                200,
                json={
                    "uid": "CHE-105.805.080",
                    "companyName": "Novartis AG",
                    "opacityScore": 30,
                    "opacityLevel": "normal",
                    "pyramiding": False,
                    "pyramidingRationale": None,
                    "contributors": [{"code": "depth", "description": "Chain depth", "points": 10}],
                    "citations": [],
                    "obligationRefs": [],
                    "peerPercentile": None,
                    "peerSampleSize": 0,
                    "graphAnalytics": None,
                    "assessedAt": "2026-05-01T00:00:00Z",
                },
            )
        )

        client = vynco.AsyncClient("vc_test_key", base_url=BASE_URL, max_retries=0)
        resp = await client.ownership.analytics("CHE-105.805.080")
        assert resp.data.opacity_level == "normal"
        assert resp.data.contributors[0].points == 10
        assert resp.data.peer_percentile is None


async def test_risk_v2():
    with respx.mock(base_url=BASE_URL) as mock:
        mock.get("/v1/risk/v2/CHE-105.805.080").mock(
            return_value=httpx.Response(
                200,
                json={
                    "uid": "CHE-105.805.080",
                    "companyName": "Novartis AG",
                    "score": 0.42,
                    "riskLevel": "medium",
                    "factors": [
                        {
                            "factor": "auditor_tenure",
                            "category": "governance",
                            "weight": 0.3,
                            "posteriorAlpha": 2.0,
                            "posteriorBeta": 5.0,
                            "posteriorMean": 0.28,
                            "rationale": "long tenure",
                            "obligationRefs": [],
                            "citations": [],
                            "evidenceApplied": True,
                            "evidenceNote": None,
                        }
                    ],
                    "priorsSchemaVersion": "v1",
                    "assessedAt": "2026-05-01T00:00:00Z",
                },
            )
        )

        client = vynco.AsyncClient("vc_test_key", base_url=BASE_URL, max_retries=0)
        resp = await client.risk.v2("CHE-105.805.080")
        assert resp.data.risk_level == "medium"
        assert resp.data.factors[0].posterior_mean == 0.28


async def test_analytics_prospects():
    with respx.mock(base_url=BASE_URL) as mock:
        route = mock.get("/v1/analytics/prospects").mock(
            return_value=httpx.Response(
                200,
                json={
                    "items": [
                        {
                            "companyUid": "CHE-1",
                            "companyName": "Foo AG",
                            "canton": "ZH",
                            "auditorName": "EY",
                            "auditorCategory": "EY",
                            "tenureYears": 12.0,
                            "opportunityScore": 88,
                            "pitchReadiness": "Hot",
                            "estimatedMandateValue": 50000.0,
                            "tenureRisk": "High",
                            "shareCapital": 1000000.0,
                            "currency": "CHF",
                        }
                    ],
                    "total": 1,
                    "page": 1,
                    "pageSize": 25,
                },
            )
        )

        client = vynco.AsyncClient("vc_test_key", base_url=BASE_URL, max_retries=0)
        resp = await client.analytics.prospects(pitch_readiness="Hot", min_score=80.0)
        assert resp.data.items[0].opportunity_score == 88
        assert resp.data.items[0].pitch_readiness == "Hot"
        params = route.calls[0].request.url.params
        assert params["pitchReadiness"] == "Hot"
        assert params["minScore"] == "80.0"


async def test_bulk_export_returns_csv_bytes():
    with respx.mock(base_url=BASE_URL) as mock:
        mock.post("/v1/bulk/export").mock(
            return_value=httpx.Response(
                200,
                content=b"uid,name\nCHE-1,Foo AG\n",
                headers={
                    "content-type": "text/csv; charset=utf-8",
                    "content-disposition": 'attachment; filename="bulk-export.csv"',
                },
            )
        )

        client = vynco.AsyncClient("vc_test_key", base_url=BASE_URL, max_retries=0)
        result = await client.bulk.export(uids=["CHE-1"], fields=["name"])
        assert result.bytes == b"uid,name\nCHE-1,Foo AG\n"
        assert result.filename == "bulk-export.csv"


async def test_bulk_screening():
    with respx.mock(base_url=BASE_URL) as mock:
        route = mock.post("/v1/bulk/screening").mock(
            return_value=httpx.Response(
                200,
                json={
                    "total": 1,
                    "hitsFound": 0,
                    "results": [
                        {
                            "name": "Foo AG",
                            "entityType": "company",
                            "riskLevel": "clear",
                            "hitCount": 0,
                            "topMatches": [],
                        }
                    ],
                    "screenedAt": "2026-05-01T00:00:00Z",
                },
            )
        )

        client = vynco.AsyncClient("vc_test_key", base_url=BASE_URL, max_retries=0)
        resp = await client.bulk.screening(entities=[{"name": "Foo AG", "type": "company"}])
        assert resp.data.total == 1
        assert resp.data.results[0].risk_level == "clear"
        import json as _json

        assert _json.loads(route.calls[0].request.content) == {
            "entities": [{"name": "Foo AG", "type": "company"}]
        }


async def test_bulk_add_to_watchlist_uploads_multipart():
    with respx.mock(base_url=BASE_URL) as mock:
        route = mock.post("/v1/bulk/watchlist/wl-1").mock(
            return_value=httpx.Response(200, json={"added": 2, "skipped": 0, "skippedUids": []})
        )

        client = vynco.AsyncClient("vc_test_key", base_url=BASE_URL, max_retries=0)
        resp = await client.bulk.add_to_watchlist("wl-1", uids=["CHE-1", "CHE-2"])
        assert resp.data.added == 2
        req = route.calls[0].request
        assert req.headers["content-type"].startswith("multipart/form-data")
        assert b"CHE-1\nCHE-2" in req.content


async def test_watches_list_add_remove():
    with respx.mock(base_url=BASE_URL) as mock:
        mock.get("/v1/watches").mock(
            return_value=httpx.Response(
                200,
                json=[{"companyUid": "CHE-1", "addedAt": "2026-05-01T00:00:00Z"}],
            )
        )
        add = mock.post("/v1/watches").mock(return_value=httpx.Response(201))
        mock.delete("/v1/watches/CHE-1").mock(return_value=httpx.Response(204))

        client = vynco.AsyncClient("vc_test_key", base_url=BASE_URL, max_retries=0)
        lst = await client.watches.list()
        assert lst.data[0].company_uid == "CHE-1"

        await client.watches.add(company_uid="CHE-1")
        import json as _json

        assert _json.loads(add.calls[0].request.content) == {"companyUid": "CHE-1"}

        meta = await client.watches.remove("CHE-1")
        assert meta is not None
