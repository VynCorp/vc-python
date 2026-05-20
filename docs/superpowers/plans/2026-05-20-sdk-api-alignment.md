# VynCo Python SDK — API Alignment & Testing Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Align the `vynco` Python SDK with the stabilized VynCo API (axum router as source of truth), removing dead endpoints, fixing field drift, adding the missing in-scope endpoints, and verifying everything with a spec-driven unit suite plus an opt-in live smoke suite. Ship as 4.0.0.

**Architecture:** The axum router in `VynCorpApi/src/routes/mod.rs` plus the handler signatures in `src/routes/*.rs` are the source of truth (the OpenAPI doc is incomplete). Each SDK resource is reconciled against its handler. New resources follow the existing dual sync+async pattern with `VyncoModel` types. Tests use `respx` mocks (default CI) plus a `@pytest.mark.live` suite gated on `VYNCO_API_KEY`.

**Tech Stack:** Python 3.11+, httpx, pydantic v2, pytest, pytest-asyncio, respx, ruff, mypy, uv.

**Reference paths:**
- SDK: `/home/michael/DEV/Repos/VynCorp-python/vc-python`
- API: `/home/michael/DEV/Repos/VyncCorpApi/VynCorpApi`
- Design spec: `docs/superpowers/specs/2026-05-20-sdk-api-alignment-design.md`

---

## Conventions every task must follow

- All API models subclass `VyncoModel` (from `vynco.types.shared`) — Pydantic v2 with camelCase alias generation. Python attributes are `snake_case`; the wire is camelCase.
- Resource files contain BOTH classes: `AsyncFoo` then `Foo` (sync). Methods are keyword-only after any path arg.
- Query params are built with `_build_params({k: v for k, v in locals().items() if k != "self"})` from `vynco._base_client`. The Python `query` arg maps to wire `search` (see existing companies resource).
- Requests go through `self._client._request_model("METHOD", "/v1/path", params=..., json=..., response_type=Model)`. For empty/204 responses use `_request_empty`; for binary use `_request_bytes`.
- `from __future__ import annotations` at the top of every module.
- A new resource `foo` must be registered in BOTH `AsyncClient.__init__` and `Client.__init__` in `src/vynco/_client.py`, imported at the top of that file, and its types exported in `src/vynco/types/__init__.py` and `src/vynco/__init__.py`.
- Tests live in `tests/test_resources.py` (resource behavior) or `tests/test_client.py` (client/transport). Use `respx.mock(base_url=BASE_URL)` and `vynco.AsyncClient("vc_test_key", base_url=BASE_URL, max_retries=0)`. `BASE_URL` is imported from `tests.conftest` or defined locally as `"https://vynco.ch/api"`.
- Commit after each task with a conventional-commit message ending:
  `Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>`

## Reusable procedures

### PROCEDURE-A — Reconcile an existing resource against its handler
For a resource file `src/vynco/resources/<res>.py` + types `src/vynco/types/<res>.py` against handler file `VynCorpApi/src/routes/<handler>.rs`:

1. Open the handler file. For each SDK method, locate the handler fn it maps to (match the wire path against the `.route(...)` lines in `mod.rs`).
2. For each method, compare:
   - **HTTP method** — confirm GET/POST/PUT/DELETE matches the router line.
   - **Path** — exact string incl. param names (`{uid}`, `{id}`).
   - **Query params** — the handler's `Query<SomeParams>` struct fields → SDK keyword args. Add missing, remove gone, fix names.
   - **Request body** — the handler's `Json<SomeReq>` struct → SDK `json=` payload and any request-side typed model.
   - **Response** — the handler's response struct (its `#[serde(rename_all="camelCase")]` fields, and which are `Option<...>` → Optional/nullable in the Pydantic model). Fix the `types/<res>.py` model: field names, types, and nullability. A Rust `Option<T>` MUST be `T | None = None` (not a defaulted non-optional).
3. Update the respx test(s) for that resource so the mock JSON matches the real response struct, and assert on at least one field that changed.
4. Run `uv run pytest tests/test_resources.py -k <res> -v` (green), then `uv run mypy src/vynco/resources/<res>.py src/vynco/types/<res>.py`.
5. Commit.

### PROCEDURE-B — Add a new resource
To add resource `foo` for handler `VynCorpApi/src/routes/<handler>.rs`:

1. Read the handler fn(s) to get exact path, method, query/body fields, and response struct (note every `Option<...>`).
2. Write the failing respx test in `tests/test_resources.py` first (mock the endpoint with a realistic JSON body matching the response struct; assert on key fields).
3. Run it: `uv run pytest tests/test_resources.py -k foo -v` → expect FAIL (AttributeError / no such resource).
4. Create `src/vynco/types/foo.py` with the `VyncoModel` response model(s).
5. Create `src/vynco/resources/foo.py` with `AsyncFoo` and `Foo` (mirror `resources/dashboard.py` shape).
6. Register in `src/vynco/_client.py`: add the import line, and `self.foo = AsyncFoo(self)` / `self.foo = Foo(self)` in both client `__init__`s.
7. Export types in `src/vynco/types/__init__.py` and `src/vynco/__init__.py` (both the `from ... import` and the `__all__` entries).
8. Run the test → PASS. Run `uv run mypy src/`.
9. Commit.

---

## Phase 0 — Tooling & baseline

### Task 1: Reproducible route-gap script

**Files:**
- Create: `scripts/api_gap.py`

- [ ] **Step 1: Write the script**

```python
#!/usr/bin/env python3
"""Diff the VynCo API axum router against SDK resource wire paths.

Source of truth = VynCorpApi/src/routes/mod.rs route registrations.
Usage: python scripts/api_gap.py [path-to-VynCorpApi]
Outputs four buckets: correct / sdk-only (phantom) / api-only (missing) / known-out-of-scope.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

OUT_OF_SCOPE_PREFIXES = (
    "/auth", "/blog", "/widget", "/public", "/webhooks/stripe",
    "/monitoring", "/sync/trigger",
)


def api_routes(api_root: Path) -> set[str]:
    txt = (api_root / "src/routes/mod.rs").read_text()
    routes: set[str] = set()
    for m in re.finditer(r'\.route\(\s*"([^"]+)"', txt):
        p = m.group(1)
        routes.add(p if p.startswith("/health") else p)
    return routes


def sdk_paths(sdk_root: Path) -> set[str]:
    paths: set[str] = set()
    res = sdk_root / "src/vynco/resources"
    for f in res.glob("*.py"):
        if f.name == "__init__.py":
            continue
        txt = f.read_text()
        for m in re.finditer(r'["\'](/v1/[A-Za-z0-9_\-/{}.]+|/health)["\']', txt):
            paths.add(m.group(1))
    return paths


def norm(p: str) -> str:
    # collapse {param} names so /v1/x/{uid} == /x/{id}
    p = re.sub(r"\{[^}]+\}", "{}", p)
    return p[3:] if p.startswith("/v1") else p


def main() -> None:
    api_root = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(
        "/home/michael/DEV/Repos/VyncCorpApi/VynCorpApi"
    )
    sdk_root = Path(__file__).resolve().parent.parent
    api = {norm(p) for p in api_routes(api_root)}
    sdk = {norm(p) for p in sdk_paths(sdk_root)}

    def scoped(s: set[str]) -> set[str]:
        return {p for p in s if not any(("/v1" + p if not p.startswith("/v1") else p)
                                        .startswith("/v1" + pre[3:] if pre.startswith("/v1") else pre)
                                        for pre in ())}

    in_scope_api = {p for p in api
                    if not any(("/" + p).startswith(pre) or p.startswith(pre.lstrip("/"))
                               for pre in OUT_OF_SCOPE_PREFIXES)}
    print("== SDK-only (phantom — fix or remove) ==")
    for p in sorted(sdk - api):
        print("  ", p)
    print("\n== API-only & in-scope (missing from SDK) ==")
    for p in sorted(in_scope_api - sdk):
        print("  ", p)
    print(f"\nTotals: api={len(api)} sdk={len(sdk)} "
          f"phantom={len(sdk - api)} missing={len(in_scope_api - sdk)}")


if __name__ == "__main__":
    main()
```

- [ ] **Step 2: Run it**

Run: `cd /home/michael/DEV/Repos/VynCorp-python/vc-python && python scripts/api_gap.py`
Expected: prints a "phantom" bucket containing the `/v1/credits/*` paths, and a "missing" bucket containing `/v1/usage/current`, `/v1/audit/playbook/{}`, `/v1/compliance/scope/{}`, `/v1/risk/v2/{}`, `/v1/settings/preferences`, `/v1/notifications*`, `/v1/sync/status`, `/v1/bulk/*`, `/v1/ownership/{}/analytics`, `/v1/analytics/prospects`, `/v1/watches*`.

- [ ] **Step 3: Commit**

```bash
git add scripts/api_gap.py
git commit -m "chore: add reproducible API route-gap diff script

Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>"
```

---

## Phase 1 — Breaking drift fixes

### Task 2: Remove `credits`, add `usage` resource

The `/v1/credits/*` endpoints do not exist in the router. The live replacement is `GET /v1/usage/current` returning `{tier, groups: [{group, used?, limit?, window, resetSeconds}]}` (from `VynCorpApi/src/routes/usage.rs` — `used` and `limit` are `Option<u64>`, i.e. nullable when the tier blocks that group).

**Files:**
- Delete: `src/vynco/resources/credits.py`, `src/vynco/types/credits.py`
- Create: `src/vynco/resources/usage.py`, `src/vynco/types/usage.py`
- Modify: `src/vynco/_client.py`, `src/vynco/types/__init__.py`, `src/vynco/__init__.py`, `tests/test_resources.py`

- [ ] **Step 1: Write the failing test for `usage`** (in `tests/test_resources.py`, replacing the credits tests)

```python
async def test_usage_current():
    with respx.mock(base_url=BASE_URL) as mock:
        mock.get("/v1/usage/current").mock(
            return_value=httpx.Response(
                200,
                json={
                    "tier": "professional",
                    "groups": [
                        {"group": "search", "used": 12, "limit": 600,
                         "window": "hour", "resetSeconds": 1800},
                        {"group": "bulk", "used": None, "limit": None,
                         "window": "day", "resetSeconds": 40000},
                    ],
                },
            )
        )
        client = vynco.AsyncClient("vc_test_key", base_url=BASE_URL, max_retries=0)
        resp = await client.usage.current()
        assert resp.data.tier == "professional"
        assert resp.data.groups[0].group == "search"
        assert resp.data.groups[0].limit == 600
        assert resp.data.groups[1].used is None  # blocked group → null
```

- [ ] **Step 2: Run it, expect failure**

Run: `uv run pytest tests/test_resources.py -k test_usage_current -v`
Expected: FAIL — `AttributeError: 'AsyncClient' object has no attribute 'usage'`.

- [ ] **Step 3: Create `src/vynco/types/usage.py`**

```python
from __future__ import annotations

from vynco.types.shared import VyncoModel


class GroupUsage(VyncoModel):
    """Rate-limit usage for one endpoint group."""

    group: str = ""
    used: int | None = None
    limit: int | None = None
    window: str = ""
    reset_seconds: int = 0


class UsageSnapshot(VyncoModel):
    """Snapshot of every rate-limit bucket for the authenticated user."""

    tier: str = ""
    groups: list[GroupUsage] = []
```

- [ ] **Step 4: Create `src/vynco/resources/usage.py`**

```python
from __future__ import annotations

from typing import TYPE_CHECKING

from vynco._response import Response
from vynco.types.usage import UsageSnapshot

if TYPE_CHECKING:
    from vynco._client import AsyncClient, Client


class AsyncUsage:
    """Async usage / rate-limit snapshot."""

    def __init__(self, client: AsyncClient) -> None:
        self._client = client

    async def current(self) -> Response[UsageSnapshot]:
        """Snapshot of every rate-limit bucket for the authenticated user."""
        return await self._client._request_model(
            "GET", "/v1/usage/current", response_type=UsageSnapshot
        )


class Usage:
    """Sync usage / rate-limit snapshot."""

    def __init__(self, client: Client) -> None:
        self._client = client

    def current(self) -> Response[UsageSnapshot]:
        """Snapshot of every rate-limit bucket for the authenticated user."""
        return self._client._request_model(
            "GET", "/v1/usage/current", response_type=UsageSnapshot
        )
```

- [ ] **Step 5: Delete credits files**

```bash
git rm src/vynco/resources/credits.py src/vynco/types/credits.py
```

- [ ] **Step 6: Rewire `src/vynco/_client.py`**

Replace the credits import (line ~19) with:
```python
from vynco.resources.usage import AsyncUsage, Usage
```
In `AsyncClient.__init__` replace `self.credits = AsyncCredits(self)` with `self.usage = AsyncUsage(self)`.
In `Client.__init__` replace `self.credits = Credits(self)` with `self.usage = Usage(self)`.

- [ ] **Step 7: Fix exports**

In `src/vynco/types/__init__.py`: remove the `from vynco.types.credits import ...` line and the `CreditBalance/CreditUsage/CreditHistory/CreditLedgerEntry` entries from `__all__`; add `from vynco.types.usage import GroupUsage, UsageSnapshot` and add `"GroupUsage", "UsageSnapshot"` to `__all__`.
In `src/vynco/__init__.py`: do the same (remove the four Credit* imports + `__all__` entries; add `GroupUsage`, `UsageSnapshot`).

- [ ] **Step 8: Resolve `InsufficientCreditsError`**

Run: `grep -rn "InsufficientCreditsError\|insufficient_credits\|402" src/vynco /home/michael/DEV/Repos/VyncCorpApi/VynCorpApi/src/errors.rs`
- If the API still returns a 402 / insufficient-credit error code, KEEP the exception class and its mapping.
- If nothing in the API produces it, remove `InsufficientCreditsError` from `_errors.py`, its mapping in `_base_client.py`, and its exports in `__init__.py`.
Document which path you took in the commit message.

- [ ] **Step 9: Remove the old credit tests**

Delete `test_credit_balance`, `test_credit_history`, and any other `test_credit*` from `tests/test_resources.py`.

- [ ] **Step 10: Run tests + types**

Run: `uv run pytest tests/test_resources.py -k "usage or credit" -v` (usage passes; no credit tests remain)
Run: `uv run mypy src/`
Expected: green.

- [ ] **Step 11: Commit**

```bash
git add -A
git commit -m "feat!: replace credits resource with usage/current (BREAKING)

Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>"
```

### Task 3: Rename tier enum `starter` → `basic`

The billing model renamed the `starter` tier to `basic` (API keeps `starter` as an inbound alias). Find every SDK occurrence and normalize to `basic`, while still accepting `starter` on parse.

**Files:**
- Modify: whichever SDK files reference `"starter"` (discover in Step 1), plus tests.

- [ ] **Step 1: Find occurrences**

Run: `grep -rn "starter\|Starter\|STARTER" src/vynco tests`
Record the list. Likely in `types/billing.py`, `types/teams.py`, docstrings, and any literal tier validation.

- [ ] **Step 2: Update tier references**

For any documented tier list / enum / docstring, change `starter` → `basic`. If a model validates tier against a fixed set, include both (`basic`, and accept legacy `starter`) — e.g. a validator that maps `"starter"` → `"basic"` on input. If tiers are just free-form `str` fields, only update docstrings/examples and any hardcoded `"starter"` literals to `"basic"`.

- [ ] **Step 3: Update tests**

Change any test fixture using `"starter"` to `"basic"`; if you added a legacy-alias validator, add a test asserting `"starter"` parses to `"basic"`.

- [ ] **Step 4: Run**

Run: `grep -rn "starter" src/vynco` (expect only legacy-alias handling, no stray references)
Run: `uv run pytest -q && uv run mypy src/`
Expected: green.

- [ ] **Step 5: Commit**

```bash
git add -A
git commit -m "feat!: rename tier 'starter' to 'basic', accept legacy alias

Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>"
```

---

## Phase 2 — Per-resource field reconciliation

Apply **PROCEDURE-A** to each resource below. Each is its own task + commit. Handler-file mapping (from `mod.rs`):

### Task 4: Reconcile `companies`
Handler files: `VynCorpApi/src/routes/companies.rs`, `company_extended.rs`, `analytics.rs` (statistics), `changes.rs` (diff), `timeline.rs`, `similar.rs`. Apply PROCEDURE-A. Watch-items: `search`/`query`→`search` param, `count`, `statistics`, `nearby` (lat/lng/radius params), `full`, `classification`, `media`/`media_analyze`, `similar`, `timeline`/`timeline_summary`, `ubo`, `diff`, notes/tags CRUD path params (`{id}` vs `{note_id}`/`{tag_id}`). Commit `fix: reconcile companies resource with API`.

### Task 5: Reconcile `analytics`
Handler: `analytics.rs`. Methods: `cantons, auditors, cluster, anomalies, rfm_segments, cohorts, candidates, flows, migrations, benchmark`. Confirm `benchmark` response nullability (median/percentile nullable, `peersWithData` present — see SDK commit f7c07fc). Apply PROCEDURE-A. Commit `fix: reconcile analytics resource with API`.

### Task 6: Reconcile `ai`
Handler: `ai.rs`, `ai_comparative.rs`, `ai_risk.rs`, `ai_search.rs`, `predictive_risk.rs`. Methods: `dossier, search, risk_score, risk_score_batch, comparative, predictive_risk`. Apply PROCEDURE-A. Commit `fix: reconcile ai resource with API`.

### Task 7: Reconcile `changes`
Handler: `changes.rs`. Methods: `list, by_company, statistics, review (PUT /changes/{id}/review), diff`. Apply PROCEDURE-A. Commit `fix: reconcile changes resource with API`.

### Task 8: Reconcile `persons`
Handler: `persons.rs`. Methods: `board_members, search, get (/persons/{id}), network`. Apply PROCEDURE-A. Commit `fix: reconcile persons resource with API`.

### Task 9: Reconcile `screening`
Handler: `screening.rs`. Methods: `screen (POST /screening), batch (/screening/batch), browse_sanctions (GET /sanctions)`. Apply PROCEDURE-A. Commit `fix: reconcile screening resource with API`.

### Task 10: Reconcile `exports`
Handler: `exports.rs`. Methods: `create, get, download, bulk_profiles (/exports/bulk-profiles)`. Confirm `download` returns binary via `_request_bytes`. Apply PROCEDURE-A. Commit `fix: reconcile exports resource with API`.

### Task 11: Reconcile `pipelines`
Handler: `pipelines.rs`. Methods: `list, create, get, delete, add_entry, update_entry, remove_entry, stats`. Apply PROCEDURE-A. Commit `fix: reconcile pipelines resource with API`.

### Task 12: Reconcile `teams`
Handler: `teams.rs`. Methods: `me, create, members, invite_member, update_member_role, remove_member, billing_summary, join`. Note member path param is `{member_id}` in the router — confirm SDK uses the right name. Apply PROCEDURE-A. Commit `fix: reconcile teams resource with API`.

### Task 13: Reconcile `watchlists`
Handler: `watchlists.rs`. Methods: `list, create, delete, companies, add_companies, remove_company, events`. Apply PROCEDURE-A. Commit `fix: reconcile watchlists resource with API`.

### Task 14: Reconcile `webhooks`
Handler: `webhooks.rs`. Methods: `list, create, update, delete, test, deliveries`. Apply PROCEDURE-A. Commit `fix: reconcile webhooks resource with API`.

### Task 15: Reconcile `dossiers`
Handler: `dossiers.rs`. Methods: `create, list, get (/{id_or_uid}), delete, generate`. Apply PROCEDURE-A. Commit `fix: reconcile dossiers resource with API`.

### Task 16: Reconcile `ownership`
Handler: `ownership.rs`. Existing method: `trace (POST /ownership/{uid})`. (The new `/ownership/{uid}/analytics` method is added in Task 24 — do not duplicate.) Apply PROCEDURE-A to `trace`. Commit `fix: reconcile ownership resource with API`.

### Task 17: Reconcile `graph`
Handler: `graph.rs`. Methods: `get, export, analyze (POST /network/analyze)`. Apply PROCEDURE-A. Commit `fix: reconcile graph resource with API`.

### Task 18: Reconcile `reports`
Handler: `industry_reports.rs`. Methods: `industries, get, generate`. Apply PROCEDURE-A. Commit `fix: reconcile reports resource with API`.

### Task 19: Reconcile `saved_searches`, `alerts`, `api_keys`, `auditors`, `billing`, `dashboard`, `health`
Small/stable resources. Handlers: `saved_searches.rs`, `alerts` (search router lines `/alerts`), `api_keys.rs`, `auditors.rs`, `billing.rs`, `dashboard.rs`, `health.rs`. Apply PROCEDURE-A to each (group into one task; one commit per resource is fine, or a single `fix: reconcile remaining stable resources with API`). For `alerts`: confirm the `/v1/alerts` + `/v1/alerts/{id}` shapes against the router's alerts handler. Commit `fix: reconcile remaining stable resources with API`.

---

## Phase 3 — New in-scope resources & methods

### Task 20: Add `settings` resource
Handler: `VynCorpApi/src/routes/settings.rs`. Endpoints: `GET /v1/settings/preferences`, `PUT /v1/settings/preferences`. Apply **PROCEDURE-B** with methods `get_preferences()` and `update_preferences(**fields)` (read the handler's preferences struct for exact fields). Commit `feat: add settings resource`.

### Task 21: Add `notifications` resource
Handler: `VynCorpApi/src/routes/notifications.rs` + `notification_preferences.rs`. Endpoints: `GET /v1/notifications`, `POST /v1/notifications/read`, `GET/PUT /v1/notifications/preferences`, `POST /v1/notifications/test`. Apply **PROCEDURE-B** with methods `list()`, `mark_read(*, ids=...)`, `get_preferences()`, `update_preferences(...)`, `test()`. Read handlers for exact request/response shapes. Commit `feat: add notifications resource`.

### Task 22: Add `sync` resource
Handler: `VynCorpApi/src/routes/sync.rs`. In-scope endpoint: `GET /v1/sync/status`. (Exclude `/sync/trigger/{pipeline_id}` and `/monitoring/runs` — out of scope.) Apply **PROCEDURE-B** with method `status()`. Commit `feat: add sync resource`.

### Task 23: Add `audit` resource
Handler: `VynCorpApi/src/routes/audit.rs`. Endpoint: `GET /v1/audit/playbook/{uid}`. Apply **PROCEDURE-B** with method `playbook(uid)`. Commit `feat: add audit resource`.

### Task 24: Add `compliance` resource + `ownership.analytics`
Handlers: `VynCorpApi/src/routes/compliance.rs` (`GET /v1/compliance/scope/{uid}`) and `ownership.rs`/`ownership_analytics.rs` (`GET /v1/ownership/{uid}/analytics`).
- Apply **PROCEDURE-B** to create a `compliance` resource with method `scope(uid)`.
- Add an `analytics(uid)` method to the EXISTING `AsyncOwnership`/`Ownership` classes hitting `GET /v1/ownership/{uid}/analytics`, with a new `OwnershipAnalytics` type in `types/ownership.py` (or `types/ubo.py` if that's where ownership types live — check imports first).
Commit `feat: add compliance resource and ownership analytics`.

### Task 25: Add `risk.v2` method
Handler: `VynCorpApi/src/routes/risk_v2.rs`. Endpoint: `GET /v1/risk/v2/{uid}`. The SDK currently exposes `ai.predictive_risk` (POST /v1/risk/predictive/{uid}) — keep that. Add a new `risk` resource with method `v2(uid)` (or `score_v2(uid)`), new type in `types/risk.py` (create) modeled on the handler's response. Apply **PROCEDURE-B**. Commit `feat: add risk v2 resource`.

### Task 26: Add `analytics.prospects` method
Handler: `VynCorpApi/src/routes/prospects.rs`. Endpoint: `GET /v1/analytics/prospects`. Add a `prospects(**filters)` method to the EXISTING `analytics` resource (not a new resource), with a `Prospects`/`ProspectList` type in `types/analytics.py`. Write the failing respx test first, then implement. Commit `feat: add analytics prospects method`.

### Task 27: Add `bulk` resource
Handler: `VynCorpApi/src/routes/bulk.rs`. Endpoints: `POST /v1/bulk/export`, `POST /v1/bulk/screening`, `POST /v1/bulk/watchlist/{id}`. Apply **PROCEDURE-B** with methods `export(...)`, `screening(...)`, `add_to_watchlist(id, *, uids=...)`. Read the handler for exact request bodies and response shapes (these are Enterprise-tier batch ops). Commit `feat: add bulk resource`.

### Task 28: Add `watches` resource
Handler: `VynCorpApi/src/routes/watches.rs`. Endpoints: `GET /v1/watches`, `POST /v1/watches`, `DELETE /v1/watches/{company_uid}` (confirm exact verbs against `mod.rs`). This is the lightweight per-company watch, distinct from watchlists. Apply **PROCEDURE-B** with methods `list()`, `add(*, company_uid=...)`, `remove(company_uid)`. Commit `feat: add watches resource`.

---

## Phase 4 — Live smoke suite

### Task 29: Live smoke harness + marker
**Files:**
- Modify: `pyproject.toml` (register `live` marker), `tests/conftest.py`
- Create: `tests/live/__init__.py`, `tests/live/conftest.py`, `tests/live/test_smoke.py`

- [ ] **Step 1: Register the marker + asyncio mode** in `pyproject.toml` under `[tool.pytest.ini_options]` (create the table if absent):

```toml
[tool.pytest.ini_options]
markers = [
    "live: hits the real VynCo API; requires VYNCO_API_KEY (deselected by default)",
]
addopts = "-m 'not live'"
asyncio_mode = "auto"
```
(If `asyncio_mode`/`addopts` already exist, merge — do not duplicate keys.)

- [ ] **Step 2: Create `tests/live/conftest.py`**

```python
from __future__ import annotations

import os

import pytest

import vynco

LIVE_BASE_URL = os.environ.get("VYNCO_BASE_URL", "https://vynco.ch/api")


@pytest.fixture(scope="session")
def api_key() -> str:
    key = os.environ.get("VYNCO_API_KEY")
    if not key:
        pytest.skip("VYNCO_API_KEY not set; skipping live tests")
    return key


@pytest.fixture()
def client(api_key: str):
    c = vynco.Client(api_key, base_url=LIVE_BASE_URL)
    yield c
    c.close()
```

- [ ] **Step 3: Create `tests/live/test_smoke.py`** (read-only endpoints; skip on tier-gate)

```python
"""Live smoke tests against the real API. Run with: uv run pytest -m live

Read-only / idempotent only. A 403 means the tier doesn't unlock the group;
that is a skip, not a failure.
"""
from __future__ import annotations

import pytest

import vynco

pytestmark = pytest.mark.live


def _maybe_skip_tiergate(exc: Exception) -> None:
    if isinstance(exc, vynco.AuthorizationError):  # 403 group not unlocked
        pytest.skip(f"tier-gated: {exc}")
    raise exc


def test_health(client: vynco.Client) -> None:
    resp = client.health.check()
    assert resp.data is not None


def test_usage_current(client: vynco.Client) -> None:
    try:
        resp = client.usage.current()
    except vynco.VyncoError as exc:
        _maybe_skip_tiergate(exc)
    assert resp.data.tier


def test_company_search(client: vynco.Client) -> None:
    try:
        resp = client.companies.list(query="bank", limit=3)
    except vynco.VyncoError as exc:
        _maybe_skip_tiergate(exc)
    assert isinstance(resp.data, object)
```
(Confirm the real exception class names against `src/vynco/_errors.py` — use the actual 403 class. Adjust `companies.list` arg names to the reconciled signature from Task 4.)

- [ ] **Step 4: Verify default run excludes live**

Run: `uv run pytest -q`
Expected: live tests NOT collected (deselected by `-m 'not live'`); unit suite green.

- [ ] **Step 5: Commit**

```bash
git add -A
git commit -m "test: add opt-in live smoke suite gated on VYNCO_API_KEY

Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>"
```

### Task 30: Run live smoke against prod & capture findings
- [ ] **Step 1:** With the user's key exported (`export VYNCO_API_KEY=...`), run: `uv run pytest -m live -v`
- [ ] **Step 2:** Record results in `docs/superpowers/plans/2026-05-20-sdk-api-alignment.md` under a "Live verification" appendix: which endpoints passed, which were tier-skipped, and any shape mismatches discovered.
- [ ] **Step 3:** For any mismatch found, fix the corresponding resource/type and its unit test (re-apply PROCEDURE-A), then re-run that live test.
- [ ] **Step 4:** Commit `test: record live smoke results and fix discovered drift`.

> NOTE FOR AUTONOMOUS EXECUTION: this task needs a real API key. If `VYNCO_API_KEY` is not available in the environment, mark this task BLOCKED, complete everything else, and surface it to the user rather than fabricating results.

---

## Phase 5 — Verification & release

### Task 31: Full verification gate
- [ ] **Step 1:** `uv run ruff format src/ tests/ scripts/`
- [ ] **Step 2:** `uv run ruff check src/ tests/ scripts/` → fix any findings
- [ ] **Step 3:** `uv run mypy src/` → green
- [ ] **Step 4:** `uv run pytest -q` → green (unit suite)
- [ ] **Step 5:** `python scripts/api_gap.py` → phantom bucket EMPTY; missing bucket contains only deliberately-deferred items (none, if all phase 3 done)
- [ ] **Step 6:** Commit any formatting/lint fixes: `style: format and lint pass`.

### Task 32: README, CHANGELOG, version bump to 4.0.0
**Files:** `src/vynco/_constants.py`, `pyproject.toml`, `README.md`, `CHANGELOG.md` (create if absent)

- [ ] **Step 1:** Set `__version__ = "4.0.0"` in `_constants.py` and `version = "4.0.0"` in `pyproject.toml`.
- [ ] **Step 2:** Update the README resource table: remove `client.credits`; add `client.usage`, `client.settings`, `client.notifications`, `client.sync`, `client.audit`, `client.compliance`, `client.risk`, `client.bulk`, `client.watches`; note `ownership.analytics` and `analytics.prospects`.
- [ ] **Step 3:** Write `CHANGELOG.md` `## 4.0.0` entry:
  - **Breaking:** removed `client.credits` (use `client.usage.current()`); tier `starter` renamed to `basic`; (list any field renames/nullability changes found in Phase 2 and the `InsufficientCreditsError` decision from Task 2 Step 8).
  - **Added:** the new resources/methods from Phase 3.
  - **Fixed:** field/nullability drift across reconciled resources.
- [ ] **Step 4:** `uv run pytest -q && uv run mypy src/` → green.
- [ ] **Step 5:** Commit `release: v4.0.0 — API alignment, usage resource, new endpoints`.

---

## Self-review notes (author)
- Spec coverage: source-of-truth precedence (Task 1 + PROCEDURE-A/B), credits→usage (Task 2), tier rename (Task 3), per-resource reconciliation (Tasks 4–19), all high-value additions — account/usage set (20–22), intelligence set (23–26), bulk (27), watches (28) — unit tests woven into every task, live smoke (29–30), verification + 4.0.0 release (31–32). All design sections mapped.
- Out-of-scope endpoints (auth/blog/widget/public/stripe/monitoring/sync-trigger) are excluded by the gap script's `OUT_OF_SCOPE_PREFIXES` and never given a task.
- Live verification depends on a real key; Task 30 is explicitly marked BLOCKABLE.

---

## Discovered during execution

### Task 3b: Reconcile `ResponseMeta` rate-limit headers (BREAKING)
Found during Task 2. The API emits `X-RateLimit-Group/-Window/-Limit/-Remaining/-Reset`
(see `VynCorpApi/src/middleware/rate_limit_headers.rs`) and emits **no** `X-Credits-*`
headers anywhere. The SDK's `ResponseMeta` (`src/vynco/_response.py`) and header parser
(`src/vynco/_base_client.py`) still read `X-Credits-Used` / `X-Credits-Remaining`, which
are always absent now.

**Files:** `src/vynco/_response.py`, `src/vynco/_base_client.py`, `tests/test_client.py`, `tests/test_companies.py`.
- Replace `ResponseMeta.credits_used` / `credits_remaining` with rate-limit fields:
  `rate_limit_group: str | None`, `rate_limit_window: str | None`,
  `rate_limit_limit: int | None`, `rate_limit_remaining: int | None`,
  `rate_limit_reset: int | None`.
- Update the meta builder in `_base_client.py` to parse the `X-RateLimit-*` headers.
- Update tests that assert on `meta.credits_used` / mock `X-Credits-*` headers to use the
  `X-RateLimit-*` set instead.
- Breaking change → belongs in the 4.0.0 CHANGELOG (Task 32).

### Phase 2 reconciliation outcome (Tasks 4–19)
Driven by 5 parallel read-only analyst passes. Fully-aligned (no change): exports,
reports, graph, webhooks, saved_searches, alerts, api_keys, auditors, billing,
dashboard, health. Fixed (committed in waves):
- P0 correctness: `UboPerson.person_id` int→str; `UboResponse` parent LEI/name;
  `DiffEntry.from` alias; `Dossier.citations`.
- Model completion / nullability: Company (5 fields), AuditCandidate (5),
  BenchmarkDimension nullability, MigrationResponse note, persons nationality_iso/
  display, teams (phantom credits → subscription fields), BillingSummary/MemberUsage,
  watchlists name, comparative auditor_analysis, ai.search → AiSearchResult.
- Params: companies.list (17 filters), include_internal on companies.events /
  changes.list / changes.by_company / watchlists.events, persons.search (8 filters).
- Resource gap: pipelines.update().
- Bug: screening.browse_sanctions leaked `_build_params` into the query via `locals()`.

**Deliberately left as-is:** harmless "ghost" fields the SDK declares but the API
doesn't currently return (Company GLEIF-provenance fields, PersonEntry/PersonRoleDetail/
NetworkCompany role_* enrichment stubs). They are `extra="ignore"`-safe and removing
them would be a needless breaking change.

### API inconsistency to flag (not an SDK bug)
`GET /v1/sanctions` (`SanctionsSearchParams`) is the only query-param struct using a
snake_case key (`entity_type`) while every other endpoint is camelCase. The SDK now
sends snake_case for this one endpoint. Recommend the API add
`#[serde(rename_all = "camelCase")]` (or `#[serde(rename = "entityType")]`) to that
struct for consistency, after which the SDK special-case can be removed.

### Live verification (Task 30)
- **Connectivity (unauthenticated):** verified end-to-end against production
  `https://vynco.ch/api/health` via the SDK — parsed `status="healthy"`,
  `database="connected"`, `version="0.1.0"`. Confirms URL building, request,
  response parsing, and (for the no-key path) error handling all work against the
  real server. Note: `/health` emits no `X-RateLimit-*` headers (expected).
- **Authenticated smoke suite:** BLOCKED pending a real key in the environment.
  `VYNCO_API_KEY` was not set during the autonomous run, so the `@pytest.mark.live`
  suite was collected-but-skipped (verified). To run it:
  `VYNCO_API_KEY=vc_live_... uv run pytest -m live -v`.
- **`audit-log` endpoint:** the only in-router endpoint left unmodelled (Enterprise
  admin console). Deliberately out of the selected scope; the gap script reports it
  as the sole "missing" entry.
