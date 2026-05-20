# VynCo Python SDK — Final API Alignment & Testing

**Date:** 2026-05-20
**Status:** Approved design — pending implementation plan
**SDK:** `vynco` (currently 3.2.1) → target **4.0.0**
**API reference:** `/home/michael/DEV/Repos/VyncCorpApi/VynCorpApi` (Rust/axum, OpenAPI 2.0.0)

## Goal

Align the Python SDK with the now-stabilized VynCo API, then verify it against the
real API. Scope: reconcile every endpoint the SDK already exposes **plus** add the
high-value endpoints the API serves but the SDK is missing. Out of scope: web-app,
SEO, and internal endpoints (see Out of Scope).

## Source of Truth

The OpenAPI document (`https://vynco.ch/api/openapi.json`, 103 paths) is **incomplete** —
the live axum router exposes ~40 additional routes not annotated with `utoipa::path`.
Therefore the source-of-truth precedence is:

1. **Primary:** the axum router in `src/routes/mod.rs` + the handler function
   signatures (query structs, request bodies, response types) in `src/routes/*.rs`.
2. **Secondary:** `openapi.json` component schemas — for field shapes/nullability
   where a handler maps directly to a documented schema.
3. **Tertiary:** the live production API (via the user's prod API key) — to confirm
   real response shapes and catch anything the static analysis misses.

A small, committed diff script (Workstream 1) makes the route-vs-SDK comparison
reproducible rather than a one-time manual pass.

## Reconciliation Findings (baseline)

Diff of SDK wire paths vs the live router:

**Confirmed correct (were suspected phantom against OpenAPI, but exist in router):**
`ai/risk-score/batch`, `analytics/{benchmark,flows,migrations}`, `alerts`,
`changes/{id}/review`, `companies/{uid}/{diff,classification,full,media,media/analyze,similar,timeline,timeline/summary,ubo}`,
`persons/{search,{id},{id}/network}`, `pipelines/*`, `sanctions`, `exports/bulk-profiles`.
These need **field-level** verification, not removal.

**Genuinely phantom (remove):** `credits.py` → `/v1/credits/{balance,usage,history}`
do not exist in the router. The live replacement is `/v1/usage/current`.

**Missing from SDK, live in API, in scope to add:**
- Account/operational: `usage/current`, `settings/preferences` (GET/PUT),
  `notifications` (list, read, preferences, test), `sync/status`.
- Intelligence: `audit/playbook/{uid}`, `compliance/scope/{uid}`,
  `ownership/{uid}/analytics`, `risk/v2/{uid}`, `analytics/prospects`.
- Bulk (Enterprise): `bulk/export`, `bulk/screening`, `bulk/watchlist/{id}`.
- `watches` + `watches/{company_uid}` (lightweight per-company watch, distinct from watchlists).

## Out of Scope (explicitly excluded)

These exist in the router but are not part of the consumer data SDK:
`auth/*` (web-app login/registration; SDK is API-key based), `auth/e2e-session`,
`blog/*` (content admin), `widget/*` (JS embed), `public/*` (SEO sitemaps),
`webhooks/stripe` (internal Stripe callback), `monitoring/runs`,
`sync/trigger/{pipeline_id}` (internal ops trigger).

## Workstreams

### 1. Gap artifact (reproducible diff)
A script (e.g. `scripts/api_gap.py`) that parses `mod.rs` route registrations and
the SDK resource wire paths, emitting a categorized report: correct / phantom /
missing-in-scope / out-of-scope. Used to drive reconciliation and to re-check after
future API changes.

### 2. Drift fixes — existing resources
- **credits → usage:** delete `credits.py`, `types/credits.py`, drop `client.credits`;
  add a `usage` resource hitting `/v1/usage/current` with a `UsageSnapshot` type
  modeled on the handler's response (per-group rate-limit snapshot).
- **Tier enum rename:** `starter` → `basic` across billing/teams/types. Accept the
  legacy `starter` value on inbound parsing (the API keeps it as a fallback alias) but
  emit/normalize to `basic`.
- **Per-resource field reconciliation:** for each existing resource, compare method
  params, request body, and response model against the handler signature + openapi
  schema. Fix renamed/added/removed/nullable fields. Track each resource as a checklist
  item in the implementation plan.

### 3. High-value additions
New resources, each following existing conventions (sync + async classes in one file,
keyword-only args, `VyncoModel` camelCase types, `query`→`search` mapping where
relevant), with matching `types/*.py`:
`usage`, `settings`, `notifications`, `sync`, `audit`, `compliance`, `risk` (v2),
`bulk`; plus `ownership.analytics` and `analytics.prospects` methods on existing
resources; plus a `watches` resource. Each wired into `Client`/`AsyncClient` and
`__init__` exports.

### 4. Testing — spec-driven unit (respx, default CI)
- One happy-path test + at least one error-path test (e.g. 403 tier-gate, 404, 429)
  per method.
- Fixtures derived from `openapi.json` component schemas where available; otherwise
  from live sample responses captured during smoke testing.
- Assert: correct wire path + method, query/body serialization (incl. `query`→`search`
  and camelCase aliases), and full Pydantic model round-trip (no extra/missing fields).
- Runs offline, deterministic. This is the gate for the release.

### 5. Testing — live smoke (opt-in)
- `@pytest.mark.live`, collected only when `VYNCO_API_KEY` is set; otherwise skipped.
- Read-only / idempotent endpoints by default. Destructive verbs (POST/PUT/DELETE)
  only against throwaway resources the test itself created (create→assert→delete),
  never against pre-existing data.
- Tier-aware: treat `403` on a not-unlocked group as `skip`, not failure. Respect
  `X-RateLimit-*`/`Retry-After`; back off rather than hammering.
- Purpose: confirm the SDK's reconciled shapes match production reality and seed
  realistic fixtures for the unit suite. Not run in default CI.

### 6. Verification & release
- `uv run ruff check src/`, `uv run ruff format --check src/`, `uv run mypy src/`,
  `uv run pytest` all green (unit suite).
- Live smoke run once manually against prod with the user's key; record results.
- Bump to **4.0.0** (`_constants.py` + `pyproject.toml`), update README resource table,
  write a CHANGELOG entry enumerating breaking changes (credits removal, tier rename,
  any field changes) and additions.

## Risks & Mitigations
- **OpenAPI incompleteness** → router is primary source; live probing as backstop.
- **Tier gating blocks live verification of some endpoints** → unit suite covers shape;
  live smoke skips gracefully on 403; note any endpoint that could not be live-verified.
- **Hidden field drift in "correct" endpoints** → per-resource reconciliation is an
  explicit checklist, not assumed-good.
- **Method-verb ambiguity in static analysis** → confirm each handler's HTTP method
  from its `#[utoipa::path]`/router line, not from heuristics.

## Success Criteria
- No SDK method targets a non-existent route; no in-scope live route lacks SDK coverage.
- Every SDK model round-trips against a real or schema-derived sample.
- Unit suite green in CI; live smoke green (or documented skips) against prod.
- 4.0.0 released with an accurate README and CHANGELOG.
