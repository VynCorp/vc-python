# VynCo Python SDK v1.0.0 — Design Spec

## Overview

Update the VynCo Python SDK from v0.1.0 to v1.0.0 to match the production OpenAPI 1.0.0 spec. Add CI/CD via GitHub Actions with PyPI publishing.

## Changes Summary

### Base URL
- Old: `https://api.vynco.ch/v1`
- New: `https://api.vynco.ch/api/v1`

### Resources — Removed (3)
- `Webhooks` — replaced by Watches in API
- `Users` — removed from API
- `Settings` — removed from API

### Resources — New (3)
- **Watches** (3 endpoints): list, add, remove company watches
- **Notifications** (1 endpoint): list change notifications
- **News** (1 endpoint): recent news across all companies

### Resources — Updated (8)

**Companies** (8→11): Add `search` (POST full-text), `reports`, `batch`/`compare` now POST with body. Add `auditor_category` and `target_status` query params.

**Changes** (3→6): Add `by_sogc`, `batch` (POST), `review` (PUT). Main `list` gains `company_uid` filter.

**Persons** (2→6): Add `list`, `roles`, `connections`, `board_members`, `network_stats`.

**Analytics** (4→7): Add `cohorts`, `cluster` (POST), `anomalies` (POST).

**Dossiers** (1→4): Add `list`, `get`, `statistics`. Generate `level` param → `type` enum.

**Teams** (2→7): Add `billing_summary`, `list_members`, `invite_member`, `update_member_role`, `remove_member`. Create gains `owner_email`/`owner_name`.

**Billing** (2→3): Add `stripe_webhook`. Checkout `tier` now enum.

**Credits** (3→3): History returns `list[CreditLedgerEntry]` instead of `dict`.

### Resources — Unchanged (1)
- **API Keys** (3 endpoints): No changes needed

### Models — New
- `CompanyWatch`: id, team_id, company_uid, company_name, channel (enum), webhook_url, watched_change_types, created_at
- `TeamMember`: id, name, email, role (enum), is_active, invited_at, joined_at
- `ChangeNotification`: id, company_uid, company_name, change_id, change_type, summary, channel, status, created_at, sent_at
- `CreditLedgerEntry`: id, type (enum), amount, operation, created_at

### Models — Updated
- `Company`: Remove capital_nominal, capital_currency, auditor_name, registration_date, deletion_date, data_source, last_modified. Add address, auditor_category, created_at, updated_at. Status becomes enum.
- `CompanyChange`: Remove source_date. Add company_name, sogc_id, is_reviewed, is_flagged.
- `Person`: Change from id/first_name/last_name/roles to id/name/roles/companies.
- `Dossier`: Change from id/company_uid/status/executive_summary/key_insights/risk_factors/generated_at to company_uid/company_name/summary/risk_score/generated_at.
- `ApiKeyInfo` → `ApiKey`: Simplify to id/name/prefix/is_test_key/created_at/last_used_at.
- `Team`: Remove slug field? No — keep. Add updated_at.
- `PaginatedResponse`: Rename total→total_count, remove total_pages/has_previous_page/has_next_page.

### Models — Removed
- `PersonRole` — replaced by Person model
- `ApiKeyCreated` — merge into ApiKey (POST returns key field)
- `CompanyComparison` — compare returns dict
- `CompanyNews` — news returns dict
- `CheckoutSessionResponse` / `PortalSessionResponse` — returns dict with url
- `Webhook` / `WebhookCreated` — resource removed
- `UserProfile` — resource removed
- `CantonAnalytics` / `AuditorAnalytics` / `RfmSegment` — analytics returns dict
- `UsageOperation` / `UsageBreakdown` — usage returns dict
- `CreditBalance` — balance returns dict
- `ChangeStatistics` — returns dict
- `RelationshipsResponse` / `CompanyRelationship` — keep CompanyRelationship, relationships returns dict

### Error Handling
- Adopt ProblemDetails format: type, title, status, detail
- Add `ConflictError` for 409 status code
- Add `ServiceUnavailableError` for 503 status code

### CI/CD Pipeline
GitHub Actions workflow:
- **ci.yml**: On push/PR to main — lint (ruff), typecheck (mypy), test (pytest) on Python 3.11/3.12/3.13
- **publish.yml**: On version tag push (v*) — build with hatch, publish to PyPI via trusted publisher

## Architecture Decisions

1. Keep the existing architecture (base client, resources, types pattern)
2. Models that return unstructured/variable data use `dict[str, Any]` — don't over-model
3. Keep both sync and async variants in same resource file
4. Stripe webhook endpoint excluded from SDK (server-side only)
5. Version 1.0.0 signals API stability alignment
