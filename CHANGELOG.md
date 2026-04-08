# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [3.0.0] - 2026-04-08

### Changed

- **Breaking**: Base URL changed from `https://api.vynco.ch` to `https://vynco.ch/api` — matches the Rust reference SDK
- **Breaking**: Response header names changed — `X-Rate-Limit-Limit` → `X-RateLimit-Limit` (matching Rust SDK)
- **Breaking**: `DashboardResponse.data` model changed — `DataCompleteness` fields updated to `total_companies`, `enriched_companies`, `companies_with_industry`, `companies_with_geo`, `total_persons`, `total_changes`, `total_sogc_publications`
- **Breaking**: `PipelineStatus` model changed — `name` → `id`, `records_processed` → `items_processed`, `duration_seconds` removed
- **Breaking**: `AuditorTenureStats` model rewritten — fields now `total_tracked`, `current_auditors`, `tenures_over_10_years`, `tenures_over_7_years`, `avg_tenure_years`, `longest_tenure`
- **Breaking**: `exports.download()` and `graph.export()` now return `ExportFile` dataclass (with `bytes`, `content_type`, `filename`, `meta`) instead of `Response[bytes]`
- **Company** model expanded with 25+ new fields: `currency`, `purpose`, `founding_date`, `registration_date`, `deletion_date`, `legal_seat`, `municipality`, `data_source`, `enrichment_level`, `address_street`, `address_house_number`, `address_zip_code`, `address_city`, `address_canton`, `website`, `sub_industry`, `employee_count`, `auditor_name`, `latitude`, `longitude`, `geo_precision`, `noga_code`, `sanctions_hit`, `last_screened_at`, `is_finma_regulated`, `ehraid`, `chid`, `cantonal_excerpt_url`, `old_names`, `translations`
- `companies.list()` now accepts `status`, `legal_form`, `capital_min`, `capital_max`, `auditor_category`, `sort_by`, `sort_desc` filter parameters

### Added

- **`ResponseMeta.rate_limit_remaining`** — remaining requests in rate limit window (`X-RateLimit-Remaining`)
- **`ResponseMeta.rate_limit_reset`** — Unix timestamp when rate limit resets (`X-RateLimit-Reset`)
- **`ExportFile`** dataclass — returned by file download endpoints (`exports.download()`, `graph.export()`, `companies.export_excel()`)
- **`companies.get_full(uid)`** — full company details with persons, changes, relationships
- **`companies.classification(uid)`** — industry classification
- **`companies.structure(uid)`** — corporate structure (head offices, branches, M&A)
- **`companies.acquisitions(uid)`** — M&A relationships
- **`companies.notes(uid)`**, **`create_note()`**, **`update_note()`**, **`delete_note()`** — company notes CRUD
- **`companies.tags(uid)`**, **`create_tag()`**, **`delete_tag()`**, **`all_tags()`** — company tags CRUD
- **`companies.export_excel()`** — Excel/CSV export of companies
- **`persons.search(q, page, page_size)`** — search persons by name
- **`persons.get(id)`** — get person detail with all roles
- **`teams.join(token)`** — join a team via invitation token
- **`dossiers.generate(uid)`** — generate a dossier for a company
- New typed models: `CompanyFullResponse`, `PersonEntry`, `ChangeEntry`, `RelationshipEntry`, `Classification`, `CorporateStructure`, `RelatedCompanyEntry`, `Acquisition`, `Note`, `Tag`, `TagSummary`, `PersonSearchResult`, `PersonDetail`, `PersonRoleDetail`, `JoinTeamResponse`, `LongestTenure`
- Retry logic now respects `X-RateLimit-Reset` header in addition to `Retry-After`

## [2.0.0] - 2026-03-31

### Changed

- **Breaking**: Base URL changed from `https://api.vynco.ch/api/v1` to `https://api.vynco.ch` — all resource paths now include `/v1/` prefix, matching the Rust SDK
- **Breaking**: `companies.list()` parameters changed — removed `status`, `auditor_category`, `sort_by`, `sort_desc`; added `changed_since`, `page`, `page_size`
- **Breaking**: `companies.count()` no longer accepts filter parameters
- **Breaking**: `companies.statistics()` now returns typed `CompanyStatistics` model
- **Breaking**: `companies.compare()` now returns typed `CompareResponse` model
- **Breaking**: `companies.news()` and `companies.reports()` now return typed models and no longer accept `limit` parameter
- **Breaking**: `companies.relationships()` and `companies.hierarchy()` now return typed models
- **Breaking**: `persons` resource stripped to single method `board_members(uid)` returning `list[BoardMember]`
- **Breaking**: `dossiers` resource rewritten — `create(uid, level)`, `list()`, `get(id_or_uid)`, `delete(id)` replace old API
- **Breaking**: `changes.list()` parameters changed — now accepts `change_type`, `since`, `until`, `company_search`, `page`, `page_size`
- **Breaking**: `changes.statistics()` now returns typed `ChangeStatistics` model
- **Breaking**: `analytics` resource rewritten — `cluster()` and `anomalies()` now take `algorithm` parameter; `velocity()` removed; `candidates()` added
- **Breaking**: `teams.create()` simplified to `name` only; `list_members()` renamed to `members()`; `invite_member()` now returns `Invitation`
- **Breaking**: `api_keys.create()` parameters changed to `name`, `environment`, `scopes`; returns typed `ApiKeyCreated`
- **Breaking**: `billing.create_checkout()` `tier` parameter now required; returns typed `SessionUrl`
- **Breaking**: `credits.balance()` returns typed `CreditBalance`; `credits.usage()` returns `CreditUsage`; `credits.history()` returns `CreditHistory`
- **Company** model updated — `canton`, `status`, `legal_form` now `Optional`; added `share_capital`, `industry`; removed `address`, `purpose`, `created_at`
- **ApiKey** model updated — added `environment`, `scopes`, `status`; removed `is_test_key`
- **Team** model simplified — removed `overage_rate`, `created_at`, `updated_at`
- **TeamMember** model updated — removed `is_active`, `invited_at`, `joined_at`; added `last_login_at`
- **CompanyChange** model updated — removed `sogc_id`, `is_reviewed`, `is_flagged`; added `description`, `source`; `company_name` now `Optional`

### Added

- **`health`** resource — `check()` for API health status
- **`auditors`** resource — `history(uid)`, `tenures(min_years, canton, page, page_size)`
- **`dashboard`** resource — `get()` for admin dashboard data
- **`screening`** resource — `screen(name, uid, sources)` for sanctions screening
- **`watchlists`** resource — `list`, `create`, `delete`, `companies`, `add_companies`, `remove_company`, `events`
- **`webhooks`** resource — `list`, `create`, `update`, `delete`, `test`, `deliveries`
- **`exports`** resource — `create`, `get`, `download` for bulk data exports
- **`ai`** resource — `dossier`, `search`, `risk_score` for AI-powered analysis
- **`graph`** resource — `get`, `export`, `analyze` for network graphs
- **`companies.events()`** — company event feed (CloudEvents format)
- **`companies.fingerprint()`** — data fingerprint for a company
- **`companies.nearby()`** — find companies near a geographic point
- **`analytics.candidates()`** — audit candidate companies
- **`teams.billing_summary()`** — now returns typed `BillingSummary`
- New typed models: `HealthResponse`, `CompanyStatistics`, `EventListResponse`, `CompanyEvent`, `CompareResponse`, `NewsItem`, `CompanyReport`, `Relationship`, `HierarchyResponse`, `Fingerprint`, `NearbyCompany`, `AuditorHistoryResponse`, `AuditorTenure`, `AuditorTenureStats`, `DashboardResponse`, `DataCompleteness`, `PipelineStatus`, `ScreeningResponse`, `ScreeningHit`, `Watchlist`, `WatchlistSummary`, `WatchlistCompaniesResponse`, `AddCompaniesResponse`, `WebhookSubscription`, `CreateWebhookResponse`, `TestDeliveryResponse`, `WebhookDelivery`, `ExportJob`, `ExportDownload`, `DossierResponse`, `AiSearchResponse`, `RiskScoreResponse`, `RiskFactor`, `ApiKeyCreated`, `CreditBalance`, `CreditUsage`, `CreditHistory`, `SessionUrl`, `Invitation`, `BillingSummary`, `MemberUsage`, `ChangeStatistics`, `BoardMember`, `CantonDistribution`, `AuditorMarketShare`, `ClusterResponse`, `AnomalyResponse`, `RfmSegmentsResponse`, `CohortResponse`, `AuditCandidate`, `DossierSummary`, `GraphResponse`, `GraphNode`, `GraphLink`, `NetworkAnalysisResponse`, `NetworkCluster`

### Removed

- **`watches`** resource — replaced by `watchlists`
- **`notifications`** resource — removed (use webhooks/watchlists instead)
- **`news`** resource (standalone) — company news is now via `companies.news()`
- **`companies.search()`** (POST) — use `companies.list(query=...)` instead
- **`companies.batch_get()`** — removed
- **`persons.list()`**, **`persons.get()`**, **`persons.roles()`**, **`persons.connections()`**, **`persons.network_stats()`** — persons simplified to `board_members()` only
- **`dossiers.statistics()`**, **`dossiers.generate()`** — replaced by `dossiers.create()`
- **`changes.by_sogc()`**, **`changes.batch()`**, **`changes.review()`** — removed
- **`analytics.velocity()`** — removed
- Typed models: `Person`, `CompanyWatch`, `ChangeNotification`, `CompanyRelationship`

## [1.0.0] - 2026-03-18

### Changed

- **Base URL** updated from `/v1` to `/api/v1` to match production API
- **`companies.search()`** renamed to **`companies.list()`** — the GET list endpoint with filtering
- **`companies.compare()`** and **`companies.batch_get()`** now use POST with request body
- **`companies.relationships()`**, **`hierarchy()`**, **`news()`** now return `dict` (unstructured)
- **`dossiers.generate()`** parameter renamed from `level` to `type` (values: `standard`, `comprehensive`); endpoint moved to `POST /dossiers/{uid}/generate`
- **`changes.by_company()`** endpoint updated from `/changes/company/{uid}` to `/changes/{uid}`
- **`analytics`** endpoints now return `dict` instead of typed models (API returns variable structures)
- **`credits.balance()`** and **`credits.usage()`** now return `dict` instead of typed models
- **`credits.history()`** now returns `list[CreditLedgerEntry]` instead of `dict`
- **`billing`** endpoints updated — paths changed to `/billing/checkout-session` and `/billing/portal-session`; return `dict`
- **`api_keys.create()`** simplified — returns `dict` (full key returned once); `is_test` parameter renamed to `is_test_key`
- **`teams.create()`** accepts optional `owner_email` and `owner_name`
- **Company** model updated: removed `legal_seat`, `capital_nominal`, `capital_currency`, `auditor_name`, `registration_date`, `deletion_date`, `data_source`, `last_modified`; added `address`, `auditor_category`, `created_at`, `updated_at`
- **Person** model simplified to `id`, `name`, `roles`, `companies` (from first_name/last_name + PersonRole objects)
- **Dossier** model updated to `company_uid`, `company_name`, `summary`, `risk_score`, `generated_at`
- **CompanyChange** model: removed `source_date`, added `company_name`, `sogc_id`, `is_reviewed`, `is_flagged`
- **ApiKeyInfo** / **ApiKeyCreated** replaced by single **ApiKey** model with `id`, `name`, `prefix`, `is_test_key`, `created_at`, `last_used_at`
- **Team** model: added `updated_at`
- **PaginatedResponse**: removed `total_pages`, `has_previous_page`, `has_next_page`
- Development status classifier updated from Alpha to Production/Stable

### Added

- **`companies.search()`** — new POST full-text search endpoint (FTS5 with Swiss diacritics)
- **`companies.reports()`** — get company financial reports
- **`changes.by_sogc()`** — get changes by SOGC publication ID
- **`changes.batch()`** — batch fetch changes for up to 50 UIDs
- **`changes.review()`** — mark a change as reviewed
- **`persons.list()`** — list persons with optional search
- **`persons.roles()`** — get all roles held by a person
- **`persons.connections()`** — get person network connections
- **`persons.board_members()`** — get board members of a company
- **`persons.network_stats()`** — person network statistics
- **`dossiers.list()`** — list all generated dossiers
- **`dossiers.get()`** — get a specific dossier
- **`dossiers.statistics()`** — dossier generation statistics
- **`analytics.cohorts()`** — cohort analytics with groupBy/canton params
- **`analytics.cluster()`** — K-Means clustering (POST)
- **`analytics.anomalies()`** — anomaly detection (POST)
- **`analytics.velocity()`** now accepts `days` parameter
- **`teams.billing_summary()`** — team billing summary
- **`teams.list_members()`** — list team members
- **`teams.invite_member()`** — invite a team member
- **`teams.update_member_role()`** — update member role
- **`teams.remove_member()`** — remove a team member
- **Watches** resource (`client.watches`) — `list`, `add`, `remove` company watches
- **Notifications** resource (`client.notifications`) — `list` change notifications
- **News** resource (`client.news`) — `recent` news across all companies
- **CompanyWatch** model — watch subscription with channel (InApp/Webhook/Email)
- **TeamMember** model — team member with role and invitation status
- **ChangeNotification** model — change notification record
- **CreditLedgerEntry** model — credit ledger entry (grant/debit/refund/expire)
- **ConflictError** (409) and **ServiceUnavailableError** (503) error types
- **CI/CD pipeline** — GitHub Actions for lint, typecheck, test (Python 3.11/3.12/3.13), and PyPI publishing on version tags

### Removed

- **`webhooks`** resource — replaced by `watches` in the API
- **`users`** resource — removed from the API
- **`settings`** resource — removed from the API
- **`companies.persons()`** — use `persons.board_members()` instead
- **`companies.dossier()`** — use `dossiers.get()` instead
- **`companies.changes()`** — use `changes.by_company()` instead
- Typed models: `PersonRole`, `CompanyComparison`, `CompanyNews`, `Webhook`, `WebhookCreated`, `UserProfile`, `CheckoutSessionResponse`, `PortalSessionResponse`, `CreditBalance`, `UsageBreakdown`, `UsageOperation`, `ChangeStatistics`, `RelationshipsResponse`, `CantonAnalytics`, `AuditorAnalytics`, `RfmSegment`

## [0.1.0] - 2026-03-17

### Added

- **Async client** (`AsyncClient`) with context manager support
- **Sync client** (`Client`) with context manager support
- **12 resource modules** covering the VynCo public API:
  - `companies` — search, get by UID, count, statistics, compare, board members, dossier, relationships, hierarchy, change history, batch get, news
  - `persons` — get by ID, search by name
  - `dossiers` — generate AI company reports (summary/standard/comprehensive)
  - `changes` — list recent changes, get by company, change statistics
  - `credits` — balance, usage breakdown, transaction history
  - `api_keys` — list, create, revoke API keys
  - `billing` — Stripe checkout and portal sessions
  - `webhooks` — list, create, get, update, delete, test
  - `teams` — get current team, create team
  - `users` — get profile, update profile
  - `settings` — get and update user preferences
  - `analytics` — canton analytics, auditor analytics, RFM segmentation, velocity
- **Pydantic v2 models** with camelCase alias generation for all API types
- **Response metadata** via `Response[T]` wrapper exposing API headers:
  - `X-Request-Id` — request tracing
  - `X-Credits-Used` — credits consumed
  - `X-Credits-Remaining` — remaining balance
  - `X-Rate-Limit-Limit` — tier rate limit
  - `X-Data-Source` — OGD compliance (Zefix/LINDAS)
- **Typed error handling** with exception hierarchy mapping HTTP status codes:
  - `AuthenticationError` (401), `InsufficientCreditsError` (402), `ForbiddenError` (403)
  - `NotFoundError` (404), `ValidationError` (400/422), `RateLimitError` (429), `ServerError` (5xx)
  - `ConfigError` (client misconfiguration), `DeserializationError` (response parsing)
- **Automatic retry** with exponential backoff on 429 and 5xx responses
- **Retry-After header** support for rate-limited requests
- **Environment variable** support (`VYNCO_API_KEY`)
- **PEP 561** type stub marker (`py.typed`)
- **41 tests** with respx covering configuration, authentication, error mapping, retry logic, response metadata, and all resource operations
