# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

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
