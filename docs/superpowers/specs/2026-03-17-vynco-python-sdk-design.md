# VynCo Python SDK Design

## Overview

Python SDK for the VynCo Swiss Corporate Intelligence API. Mirrors the Rust SDK (`vc-rust`) structure while being idiomatic Python, and extends it with additional endpoints (analytics, relationships, hierarchy, changes, comparison) from the full API surface.

**Package name:** `vynco`
**Python:** 3.11+
**HTTP client:** httpx (async + sync)
**Models:** Pydantic v2
**Tooling:** uv
**License:** Apache-2.0

## Usage Examples

```python
# Async
import vynco

client = vynco.AsyncClient("vc_live_xxx")
result = await client.companies.search(query="Novartis", canton="BS")
for company in result.data.items:
    print(f"{company.name} ({company.uid})")
print(f"Credits remaining: {result.meta.credits_remaining}")

# Sync
client = vynco.Client("vc_live_xxx")
result = client.companies.search(query="Novartis", canton="BS")

# Configuration
client = vynco.AsyncClient(
    api_key="vc_live_xxx",
    base_url="https://api.vynco.ch/v1",  # default
    timeout=30.0,                          # default
    max_retries=2,                         # default
)

# Environment variable (VYNCO_API_KEY)
client = vynco.Client()  # reads from env

# Error handling
try:
    company = await client.companies.get("CHE-000.000.000")
except vynco.NotFoundError as e:
    print(f"Not found: {e.detail}")
except vynco.RateLimitError:
    print("Rate limited, retry later")
except vynco.VyncoError as e:
    print(f"API error ({e.status}): {e.detail}")
```

## Package Structure

```
src/vynco/
├── __init__.py              # Public API: Client, AsyncClient, errors, types
├── _client.py               # AsyncClient + Client
├── _base_client.py          # Shared HTTP logic, retry, error mapping
├── _errors.py               # Exception hierarchy
├── _response.py             # Response[T], ResponseMeta
├── _constants.py            # DEFAULT_BASE_URL, timeouts, version
├── py.typed                 # PEP 561 marker
├── types/
│   ├── __init__.py          # Re-exports all model classes
│   ├── companies.py         # Company, CompanySearchParams, CompanyCount
│   ├── persons.py           # Person, PersonRole, PersonSearchParams
│   ├── dossiers.py          # Dossier, GenerateDossierRequest
│   ├── changes.py           # CompanyChange, ChangeStatistics
│   ├── credits.py           # CreditBalance, UsageBreakdown, UsageOperation
│   ├── billing.py           # CheckoutSessionResponse, PortalSessionResponse
│   ├── api_keys.py          # ApiKeyInfo, ApiKeyCreated, CreateApiKeyRequest
│   ├── webhooks.py          # Webhook, WebhookCreated, CreateWebhookRequest, UpdateWebhookRequest
│   ├── teams.py             # Team, CreateTeamRequest
│   ├── users.py             # UserProfile, UpdateProfileRequest
│   ├── analytics.py         # ClusterResult, AnomalyResult, RfmSegment, CohortResult, etc.
│   ├── relationships.py     # CompanyRelationship, CompanyHierarchy
│   └── shared.py            # PaginatedResponse[T]
└── resources/
    ├── __init__.py
    ├── companies.py         # AsyncCompanies + Companies
    ├── persons.py           # AsyncPersons + Persons
    ├── dossiers.py          # AsyncDossiers + Dossiers
    ├── changes.py           # AsyncChanges + Changes
    ├── credits.py           # AsyncCredits + Credits
    ├── billing.py           # AsyncBilling + Billing
    ├── api_keys.py          # AsyncApiKeys + ApiKeys
    ├── webhooks.py          # AsyncWebhooks + Webhooks
    ├── teams.py             # AsyncTeams + Teams
    ├── users.py             # AsyncUsers + Users
    ├── settings.py          # AsyncSettings + Settings
    └── analytics.py         # AsyncAnalytics + Analytics
```

**Project root:**
```
vc-python/
├── pyproject.toml
├── uv.lock
├── README.md
├── LICENSE
├── CHANGELOG.md
├── CLAUDE.md
├── src/vynco/              # Package source
└── tests/
    ├── conftest.py          # Shared fixtures (mock server, client factories)
    ├── test_client.py       # Client config, auth, retry, error mapping
    ├── test_companies.py
    ├── test_persons.py
    ├── test_dossiers.py
    ├── test_changes.py
    ├── test_credits.py
    ├── test_billing.py
    ├── test_api_keys.py
    ├── test_webhooks.py
    ├── test_teams.py
    ├── test_users.py
    ├── test_settings.py
    └── test_analytics.py
```

## Client Architecture

### Base Client

Shared logic between async and sync clients:

```python
class BaseClient:
    """Shared configuration and HTTP logic."""

    def __init__(
        self,
        api_key: str | None = None,
        base_url: str = DEFAULT_BASE_URL,
        timeout: float = DEFAULT_TIMEOUT,
        max_retries: int = DEFAULT_MAX_RETRIES,
    ):
        self.api_key = api_key or os.environ.get("VYNCO_API_KEY", "")
        if not self.api_key:
            raise ConfigError("API key must not be empty. Pass api_key or set VYNCO_API_KEY.")
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout
        self.max_retries = max_retries

    def _headers(self) -> dict[str, str]:
        return {
            "Authorization": f"Bearer {self.api_key}",
            "User-Agent": f"vynco-python/{__version__}",
        }

    def _url(self, path: str) -> str:
        return f"{self.base_url}{path}"

    def _map_error(self, status: int, body: dict) -> VyncoError: ...
    def _parse_response_meta(self, headers: httpx.Headers) -> ResponseMeta: ...
```

### AsyncClient

```python
class AsyncClient(BaseClient):
    """Async client using httpx.AsyncClient."""

    def __init__(self, api_key: str | None = None, **kwargs):
        super().__init__(api_key, **kwargs)
        self._http = httpx.AsyncClient(
            headers=self._headers(),
            timeout=self.timeout,
        )
        # Resource accessors (lazy properties)
        self.companies = AsyncCompanies(self)
        self.persons = AsyncPersons(self)
        self.dossiers = AsyncDossiers(self)
        self.changes = AsyncChanges(self)
        self.credits = AsyncCredits(self)
        self.billing = AsyncBilling(self)
        self.api_keys = AsyncApiKeys(self)
        self.webhooks = AsyncWebhooks(self)
        self.teams = AsyncTeams(self)
        self.users = AsyncUsers(self)
        self.settings = AsyncSettings(self)
        self.analytics = AsyncAnalytics(self)

    async def _request(self, method, path, **kwargs) -> httpx.Response: ...
    async def close(self): ...
    async def __aenter__(self): ...
    async def __aexit__(self, ...): ...
```

### Client (Sync)

```python
class Client(BaseClient):
    """Sync client using httpx.Client."""

    def __init__(self, api_key: str | None = None, **kwargs):
        super().__init__(api_key, **kwargs)
        self._http = httpx.Client(
            headers=self._headers(),
            timeout=self.timeout,
        )
        self.companies = Companies(self)
        self.persons = Persons(self)
        # ... same pattern ...

    def _request(self, method, path, **kwargs) -> httpx.Response: ...
    def close(self): ...
    def __enter__(self): ...
    def __exit__(self, ...): ...
```

Both clients support context manager usage:
```python
async with vynco.AsyncClient("key") as client:
    result = await client.companies.search(query="Novartis")

with vynco.Client("key") as client:
    result = client.companies.search(query="Novartis")
```

## Resource Design

Each resource has an async variant and a sync variant in the same module. The pattern:

```python
# resources/companies.py

class AsyncCompanies:
    def __init__(self, client: "AsyncClient"):
        self._client = client

    async def search(
        self,
        *,
        query: str | None = None,
        canton: str | None = None,
        legal_form: str | None = None,
        status: str | None = None,
        sort_by: str | None = None,
        sort_desc: bool | None = None,
        page: int | None = None,
        page_size: int | None = None,
    ) -> Response[PaginatedResponse[Company]]:
        params = _build_params(locals())
        return await self._client._request_model(
            "GET", "/companies",
            params=params,
            response_type=PaginatedResponse[Company],
        )

class Companies:
    """Sync version — identical signatures without async/await."""
    def __init__(self, client: "Client"):
        self._client = client

    def search(self, *, query: str | None = None, ...) -> Response[PaginatedResponse[Company]]:
        params = _build_params(locals())
        return self._client._request_model(
            "GET", "/companies",
            params=params,
            response_type=PaginatedResponse[Company],
        )
```

Resource methods use **keyword-only arguments** (not param objects) for better ergonomics:
```python
# Python-idiomatic: keyword args
result = client.companies.search(query="Novartis", canton="BS", page=1)

# Not: param object (Rust-style, less Pythonic)
result = client.companies.search(CompanySearchParams(search="Novartis", canton="BS"))
```

## Resources and Endpoints

### 1. Companies (12 methods)

| Method | HTTP | Path | Returns |
|--------|------|------|---------|
| `search(*, query, canton, legal_form, status, sort_by, sort_desc, page, page_size)` | GET | `/companies` | `Response[PaginatedResponse[Company]]` |
| `get(uid)` | GET | `/companies/{uid}` | `Response[Company]` |
| `count(*, query, canton, legal_form, status)` | GET | `/companies/count` | `Response[CompanyCount]` |
| `statistics()` | GET | `/companies/statistics` | `Response[dict]` |
| `compare(uids)` | POST | `/companies/compare` | `Response[CompanyComparison]` |
| `persons(uid)` | GET | `/companies/{uid}/persons` | `Response[list[PersonRole]]` |
| `dossier(uid)` | GET | `/companies/{uid}/dossier` | `Response[Dossier]` |
| `relationships(uid)` | GET | `/companies/{uid}/relationships` | `Response[list[CompanyRelationship]]` |
| `hierarchy(uid)` | GET | `/companies/{uid}/hierarchy` | `Response[CompanyHierarchy]` |
| `changes(uid)` | GET | `/companies/{uid}/changes` | `Response[list[CompanyChange]]` |
| `batch_get(uids)` | POST | `/companies/batch` | `Response[list[Company]]` |
| `news(uid)` | GET | `/companies/{uid}/news` | `Response[list[CompanyNews]]` |

### 2. Persons (2 methods)

| Method | HTTP | Path | Returns |
|--------|------|------|---------|
| `get(id)` | GET | `/persons/{id}` | `Response[Person]` |
| `search(*, name)` | POST | `/persons/search` | `Response[list[Person]]` |

### 3. Dossiers (1 method)

| Method | HTTP | Path | Returns |
|--------|------|------|---------|
| `generate(uid, *, level)` | POST | `/dossiers` | `Response[Dossier]` |

### 4. Changes (3 methods)

| Method | HTTP | Path | Returns |
|--------|------|------|---------|
| `list(*, page, page_size)` | GET | `/changes` | `Response[PaginatedResponse[CompanyChange]]` |
| `by_company(uid)` | GET | `/changes/company/{uid}` | `Response[list[CompanyChange]]` |
| `statistics()` | GET | `/changes/statistics` | `Response[ChangeStatistics]` |

### 5. Credits (3 methods)

| Method | HTTP | Path | Returns |
|--------|------|------|---------|
| `balance()` | GET | `/credits/balance` | `Response[CreditBalance]` |
| `usage(*, since)` | GET | `/credits/usage` | `Response[UsageBreakdown]` |
| `history(*, limit, offset)` | GET | `/credits/history` | `Response[dict]` |

### 6. API Keys (3 methods)

| Method | HTTP | Path | Returns |
|--------|------|------|---------|
| `list()` | GET | `/api-keys` | `Response[list[ApiKeyInfo]]` |
| `create(*, name, is_test, permissions)` | POST | `/api-keys` | `Response[ApiKeyCreated]` |
| `revoke(id)` | DELETE | `/api-keys/{id}` | `ResponseMeta` |

### 7. Billing (2 methods)

| Method | HTTP | Path | Returns |
|--------|------|------|---------|
| `create_checkout(tier)` | POST | `/billing/checkout` | `Response[CheckoutSessionResponse]` |
| `create_portal()` | POST | `/billing/portal` | `Response[PortalSessionResponse]` |

### 8. Webhooks (6 methods)

| Method | HTTP | Path | Returns |
|--------|------|------|---------|
| `list()` | GET | `/webhooks` | `Response[list[Webhook]]` |
| `create(*, url, events)` | POST | `/webhooks` | `Response[WebhookCreated]` |
| `get(id)` | GET | `/webhooks/{id}` | `Response[Webhook]` |
| `update(id, *, url, events, status)` | PUT | `/webhooks/{id}` | `Response[Webhook]` |
| `delete(id)` | DELETE | `/webhooks/{id}` | `ResponseMeta` |
| `test(id)` | POST | `/webhooks/{id}/test` | `ResponseMeta` |

### 9. Teams (2 methods)

| Method | HTTP | Path | Returns |
|--------|------|------|---------|
| `me()` | GET | `/teams/me` | `Response[Team]` |
| `create(*, name, slug)` | POST | `/teams` | `Response[Team]` |

### 10. Users (2 methods)

| Method | HTTP | Path | Returns |
|--------|------|------|---------|
| `me()` | GET | `/users/me` | `Response[UserProfile]` |
| `update_profile(*, name, email)` | PUT | `/users/me` | `Response[UserProfile]` |

### 11. Settings (2 methods)

| Method | HTTP | Path | Returns |
|--------|------|------|---------|
| `get()` | GET | `/settings` | `Response[dict]` |
| `update(preferences)` | PUT | `/settings` | `Response[dict]` |

### 12. Analytics (7 methods)

| Method | HTTP | Path | Returns |
|--------|------|------|---------|
| `companies()` | GET | `/analytics/companies` | `Response[dict]` |
| `cantons()` | GET | `/analytics/cantons` | `Response[list[CantonAnalytics]]` |
| `auditors()` | GET | `/analytics/auditors` | `Response[list[AuditorAnalytics]]` |
| `cluster(*, params)` | POST | `/analytics/cluster` | `Response[ClusterResult]` |
| `anomalies(*, params)` | POST | `/analytics/anomalies` | `Response[AnomalyResult]` |
| `rfm_segments()` | GET | `/analytics/segments/rfm` | `Response[list[RfmSegment]]` |
| `cohorts()` | GET | `/analytics/cohorts` | `Response[CohortResult]` |

## Type Models (Pydantic v2)

All models use `alias_generator = to_camel` for JSON camelCase ↔ Python snake_case conversion.

```python
from pydantic import BaseModel, ConfigDict
from pydantic.alias_generators import to_camel

class VyncoModel(BaseModel):
    """Base for all API models."""
    model_config = ConfigDict(
        alias_generator=to_camel,
        populate_by_name=True,
    )
```

### Key Models

```python
# types/companies.py
class Company(VyncoModel):
    uid: str
    name: str
    legal_seat: str = ""
    canton: str = ""
    legal_form: str = ""
    status: str = ""
    purpose: str = ""
    capital_nominal: float | None = None
    capital_currency: str | None = None
    auditor_name: str | None = None
    registration_date: str | None = None
    deletion_date: str | None = None
    data_source: str = ""
    last_modified: str = ""

class CompanyCount(VyncoModel):
    count: int

# types/shared.py
class PaginatedResponse(VyncoModel, Generic[T]):
    items: list[T]
    total: int
    page: int
    page_size: int

# types/persons.py
class PersonRole(VyncoModel):
    person_id: str
    first_name: str = ""
    last_name: str = ""
    role: str = ""
    since: str | None = None
    until: str | None = None

class Person(VyncoModel):
    id: str
    first_name: str = ""
    last_name: str = ""
    roles: list[PersonRole] = []

# types/dossiers.py
class Dossier(VyncoModel):
    id: str
    company_uid: str
    status: str = ""
    executive_summary: str | None = None
    key_insights: list[str] | None = None
    risk_factors: list[str] | None = None
    generated_at: str | None = None

# types/credits.py
class CreditBalance(VyncoModel):
    balance: int
    monthly_credits: int
    used_this_month: int
    tier: str = ""
    overage_rate: float = 0.0

class UsageOperation(VyncoModel):
    operation: str = ""
    count: int = 0
    credits: int = 0

class UsagePeriod(VyncoModel):
    start: str
    end: str

class UsageBreakdown(VyncoModel):
    operations: list[UsageOperation] = []
    total_debited: int = 0
    period: UsagePeriod | None = None

# types/api_keys.py
class ApiKeyInfo(VyncoModel):
    id: str
    name: str = ""
    key_prefix: str = ""
    key_hint: str = ""
    permissions: list[str] = []
    is_active: bool = False
    last_used_at: str | None = None
    created_at: str = ""
    expires_at: str | None = None

class ApiKeyCreated(VyncoModel):
    id: str
    name: str = ""
    raw_key: str = ""
    key_prefix: str = ""
    permissions: list[str] = []
    created_at: str = ""
    expires_at: str | None = None

# types/billing.py
class CheckoutSessionResponse(VyncoModel):
    url: str

class PortalSessionResponse(VyncoModel):
    url: str

# types/teams.py
class Team(VyncoModel):
    id: str
    name: str = ""
    slug: str = ""
    tier: str = ""
    credit_balance: int = 0
    monthly_credits: int = 0
    overage_rate: float = 0.0
    created_at: str = ""

# types/webhooks.py
class Webhook(VyncoModel):
    id: str
    url: str = ""
    events: list[str] = []
    status: str = ""
    secret: str | None = None
    created_at: str | None = None
    updated_at: str | None = None

class WebhookCreated(VyncoModel):
    id: str
    url: str = ""
    events: list[str] = []
    secret: str = ""
    created_at: str | None = None

# types/users.py
class UserProfile(VyncoModel):
    id: str
    name: str = ""
    email: str = ""
    avatar: str = ""
    plan: str = ""
    credit_balance: int = 0

# types/changes.py
class CompanyChange(VyncoModel):
    id: str
    company_uid: str
    change_type: str = ""
    field_name: str = ""
    old_value: str | None = None
    new_value: str | None = None
    detected_at: str = ""
    source_date: str | None = None

class ChangeStatistics(VyncoModel):
    total_changes: int = 0
    changes_by_type: dict[str, int] = {}
    period: UsagePeriod | None = None

# types/relationships.py
class CompanyRelationship(VyncoModel):
    id: str
    source_company_uid: str
    source_company_name: str = ""
    target_company_uid: str
    target_company_name: str = ""
    relationship_type: str = ""
    source_lei: str | None = None
    target_lei: str | None = None
    data_source: str = ""
    is_active: bool = True

class CompanyHierarchyNode(VyncoModel):
    uid: str
    name: str = ""
    relationship_type: str = ""
    children: list["CompanyHierarchyNode"] = []

class CompanyHierarchy(VyncoModel):
    root: CompanyHierarchyNode
    total_entities: int = 0

# types/analytics.py
class CantonAnalytics(VyncoModel):
    canton: str
    company_count: int = 0
    active_count: int = 0
    change_count: int = 0

class AuditorAnalytics(VyncoModel):
    auditor_name: str
    client_count: int = 0
    change_count: int = 0

class ClusterResult(VyncoModel):
    clusters: list[dict] = []
    n_clusters: int = 0
    silhouette_score: float | None = None

class AnomalyResult(VyncoModel):
    anomalies: list[dict] = []
    total_anomalies: int = 0

class RfmSegment(VyncoModel):
    segment: str = ""
    count: int = 0
    avg_recency: float = 0.0
    avg_frequency: float = 0.0
    avg_monetary: float = 0.0

class CohortResult(VyncoModel):
    cohorts: list[dict] = []
    retention_matrix: list[list[float]] = []

class CompanyComparison(VyncoModel):
    companies: list[dict] = []
    dimensions: list[dict] = []
    similarities: list[str] = []
    differences: list[str] = []

class CompanyNews(VyncoModel):
    id: str = ""
    title: str = ""
    url: str = ""
    source: str = ""
    published_at: str | None = None
    summary: str | None = None
```

## Error Handling

Exception hierarchy mirroring the Rust SDK's `VyncoError` enum:

```python
class VyncoError(Exception):
    """Base exception for all VynCo SDK errors."""
    status: int
    detail: str
    message: str

class AuthenticationError(VyncoError):     # 401
class InsufficientCreditsError(VyncoError): # 402
class ForbiddenError(VyncoError):           # 403
class NotFoundError(VyncoError):            # 404
class ValidationError(VyncoError):          # 400, 422
class RateLimitError(VyncoError):           # 429
class ServerError(VyncoError):              # 5xx
class ConfigError(VyncoError):              # Client misconfiguration
class DeserializationError(VyncoError):     # Response parsing failure
```

Error mapping from HTTP status:
```python
STATUS_ERROR_MAP = {
    401: AuthenticationError,
    402: InsufficientCreditsError,
    403: ForbiddenError,
    404: NotFoundError,
    400: ValidationError,
    422: ValidationError,
    429: RateLimitError,
}
# 5xx -> ServerError (default)
```

Error body follows RFC 7807 (same as Rust SDK):
```python
class ErrorBody(VyncoModel):
    detail: str = ""
    message: str = ""
    status: int = 0
```

## Response Wrapper

```python
@dataclass
class ResponseMeta:
    """Metadata from VynCo API response headers."""
    request_id: str | None = None        # X-Request-Id
    credits_used: int | None = None      # X-Credits-Used
    credits_remaining: int | None = None # X-Credits-Remaining
    rate_limit_limit: int | None = None  # X-Rate-Limit-Limit
    data_source: str | None = None       # X-Data-Source

@dataclass
class Response(Generic[T]):
    """API response with typed data and metadata."""
    data: T
    meta: ResponseMeta
```

Using `dataclass` (not Pydantic) for Response/ResponseMeta since they're SDK constructs, not API models.

## Retry Logic

Mirrors the Rust SDK exactly:
- Retries on **429** (Too Many Requests) and **5xx** (Server Error)
- **Exponential backoff:** 0.5s * 2^attempt (0.5s, 1s, 2s, ...)
- Respects `Retry-After` header if present
- Default: 2 retries (configurable via `max_retries`)
- Does NOT retry on client errors (4xx except 429)

## Flexible List Extraction

Mirrors the Rust SDK's `extract_list()` for endpoints with inconsistent response shapes:
1. Bare JSON array: `[{...}, {...}]`
2. Data wrapper: `{"data": [{...}, {...}]}`
3. First array-valued key: `{"items": [{...}], ...}`

## Testing

- **Framework:** pytest + pytest-asyncio
- **HTTP mocking:** respx (httpx-native mock library)
- **Coverage:** pytest-cov

Test structure mirrors the Rust SDK's test patterns:
- Client configuration validation (empty API key)
- Authentication header verification
- HTTP status -> exception mapping (401, 402, 403, 404, 429, 5xx)
- Response body parsing for each resource
- Response metadata header extraction
- Retry behavior verification

```python
# Example test pattern
@pytest.mark.asyncio
async def test_company_search():
    async with respx.mock:
        respx.get("https://api.vynco.ch/v1/companies").mock(
            return_value=httpx.Response(200, json={...}, headers={...})
        )
        client = vynco.AsyncClient("vc_test_key")
        result = await client.companies.search(query="Novartis")
        assert result.data.items[0].name == "Novartis AG"
        assert result.meta.credits_used == 1
```

## Dependencies

**Runtime:**
- `httpx >= 0.27` — HTTP client (async + sync)
- `pydantic >= 2.0` — Model validation and serialization

**Development:**
- `pytest >= 8.0`
- `pytest-asyncio >= 0.24`
- `respx >= 0.22` — httpx mock
- `pytest-cov >= 5.0`
- `ruff >= 0.8` — linter + formatter
- `mypy >= 1.11` — type checking

Minimal runtime dependencies (just httpx + pydantic). No need for `anyio`, `tenacity`, or other extras — retry logic is inline, and httpx handles async natively.

## pyproject.toml

```toml
[project]
name = "vynco"
version = "0.1.0"
description = "Python SDK for the VynCo Swiss Corporate Intelligence API"
readme = "README.md"
license = "Apache-2.0"
requires-python = ">=3.11"
authors = [{ name = "VynCo", email = "hello@vynco.ch" }]
keywords = ["vynco", "zefix", "swiss", "corporate", "api", "sdk"]
classifiers = [
    "Development Status :: 3 - Alpha",
    "Intended Audience :: Developers",
    "License :: OSI Approved :: Apache Software License",
    "Programming Language :: Python :: 3.11",
    "Programming Language :: Python :: 3.12",
    "Programming Language :: Python :: 3.13",
    "Typing :: Typed",
]
dependencies = [
    "httpx>=0.27",
    "pydantic>=2.0",
]

[project.urls]
Homepage = "https://github.com/VynCorp/vc-python"
Documentation = "https://docs.vynco.ch"
Repository = "https://github.com/VynCorp/vc-python"

[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

[tool.hatch.build.targets.wheel]
packages = ["src/vynco"]

[dependency-groups]
dev = [
    "pytest>=8.0",
    "pytest-asyncio>=0.24",
    "respx>=0.22",
    "pytest-cov>=5.0",
    "ruff>=0.8",
    "mypy>=1.11",
]

[tool.pytest.ini_options]
asyncio_mode = "auto"
testpaths = ["tests"]

[tool.ruff]
target-version = "py311"
line-length = 100

[tool.ruff.lint]
select = ["E", "F", "I", "UP", "B", "SIM"]

[tool.mypy]
python_version = "3.11"
strict = true
plugins = ["pydantic.mypy"]
```

## Public API (`__init__.py`)

```python
from vynco._client import AsyncClient, Client
from vynco._errors import (
    AuthenticationError,
    ConfigError,
    DeserializationError,
    ForbiddenError,
    InsufficientCreditsError,
    NotFoundError,
    RateLimitError,
    ServerError,
    ValidationError,
    VyncoError,
)
from vynco._response import Response, ResponseMeta
from vynco.types import *  # All Pydantic models

__version__ = "0.1.0"
__all__ = [
    "AsyncClient",
    "Client",
    # Errors
    "VyncoError",
    "AuthenticationError",
    "InsufficientCreditsError",
    "ForbiddenError",
    "NotFoundError",
    "ValidationError",
    "RateLimitError",
    "ServerError",
    "ConfigError",
    "DeserializationError",
    # Response
    "Response",
    "ResponseMeta",
]
```

## Design Decisions

1. **Keyword args over param objects** — More Pythonic. `client.companies.search(query="X")` vs `client.companies.search(CompanySearchParams(search="X"))`. The Rust SDK uses structs because Rust doesn't have keyword args; Python does.

2. **Resource instances as attributes, not methods** — `client.companies.search()` not `client.companies().search()`. Simpler, and Python doesn't need Rust's lifetime/borrowing pattern.

3. **httpx over requests+aiohttp** — Single library for both sync and async. Fewer dependencies, consistent API, modern design.

4. **Pydantic for API models, dataclass for SDK constructs** — Response/ResponseMeta are SDK-internal; Pydantic adds unnecessary overhead there. API models benefit from Pydantic's validation and serialization.

5. **`src/` layout** — Modern Python best practice. Prevents import confusion during development.

6. **Separate Changes resource** — The Rust SDK has `companies.changes(uid)` for per-company changes. We keep that, but add a top-level `Changes` resource for the global change feed and statistics endpoints that aren't company-scoped.

7. **Both async and sync classes per resource** — Small duplication (~5 lines per method), but gives full type safety for both sync and async users without code generation complexity.
