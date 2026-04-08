# vynco

Python SDK for the [VynCo](https://vynco.ch) Swiss Corporate Intelligence API. Access 500,000+ Swiss companies from the commercial register with change tracking, sanctions screening, AI-powered risk analysis, network graphs, watchlists, webhooks, and bulk data exports.

## Installation

```bash
pip install vynco
```

Or with [uv](https://docs.astral.sh/uv/):

```bash
uv add vynco
```

## Quick Start

```python
import vynco

client = vynco.Client("vc_live_your_api_key")

# List companies with filtering
result = client.companies.list(query="Novartis", canton="BS")
print(f"Found {result.data.total} companies")

# Get a single company
company = client.companies.get("CHE-105.805.080")
print(f"{company.data.name}: {company.data.legal_form}")

# Full company details with persons, changes, relationships
full = client.companies.get_full("CHE-105.805.080")
print(f"Board: {len(full.data.persons)} persons")

# Sanctions screening
screening = client.screening.screen(name="Suspicious Corp")
print(f"Risk: {screening.data.risk_level} ({screening.data.hit_count} hits)")

# AI risk score
risk = client.ai.risk_score(uid="CHE-105.805.080")
print(f"Risk score: {risk.data.overall_score}/100 ({risk.data.risk_level})")

# Credit balance
credits = client.credits.balance()
print(f"Credits remaining: {credits.data.balance}")
```

## Async Usage

```python
import vynco

async def main():
    async with vynco.AsyncClient("vc_live_your_api_key") as client:
        result = await client.companies.list(query="Novartis")
        print(result.data.items[0].name)
```

## API Coverage

18 resource modules covering 90+ endpoints:

| Resource | Methods |
|----------|---------|
| `client.health` | `check` |
| `client.companies` | `list`, `get`, `get_full`, `count`, `events`, `statistics`, `compare`, `news`, `reports`, `relationships`, `hierarchy`, `classification`, `fingerprint`, `structure`, `acquisitions`, `nearby`, `notes`, `create_note`, `update_note`, `delete_note`, `tags`, `create_tag`, `delete_tag`, `all_tags`, `export_excel` |
| `client.auditors` | `history`, `tenures` |
| `client.dashboard` | `get` |
| `client.screening` | `screen` |
| `client.watchlists` | `list`, `create`, `delete`, `companies`, `add_companies`, `remove_company`, `events` |
| `client.webhooks` | `list`, `create`, `update`, `delete`, `test`, `deliveries` |
| `client.exports` | `create`, `get`, `download` |
| `client.ai` | `dossier`, `search`, `risk_score` |
| `client.api_keys` | `list`, `create`, `revoke` |
| `client.credits` | `balance`, `usage`, `history` |
| `client.billing` | `create_checkout`, `create_portal` |
| `client.teams` | `me`, `create`, `members`, `invite_member`, `update_member_role`, `remove_member`, `billing_summary`, `join` |
| `client.changes` | `list`, `by_company`, `statistics` |
| `client.persons` | `board_members`, `search`, `get` |
| `client.analytics` | `cantons`, `auditors`, `cluster`, `anomalies`, `rfm_segments`, `cohorts`, `candidates` |
| `client.dossiers` | `create`, `list`, `get`, `delete`, `generate` |
| `client.graph` | `get`, `export`, `analyze` |

## Response Metadata

Every response includes header metadata for credit tracking and rate limiting:

```python
resp = client.companies.get("CHE-105.805.080")

print(f"Request ID: {resp.meta.request_id}")               # X-Request-Id
print(f"Credits used: {resp.meta.credits_used}")            # X-Credits-Used
print(f"Credits remaining: {resp.meta.credits_remaining}")  # X-Credits-Remaining
print(f"Rate limit: {resp.meta.rate_limit_limit}")          # X-RateLimit-Limit
print(f"Rate remaining: {resp.meta.rate_limit_remaining}")  # X-RateLimit-Remaining
print(f"Rate reset: {resp.meta.rate_limit_reset}")          # X-RateLimit-Reset
print(f"Data source: {resp.meta.data_source}")              # X-Data-Source
```

## Configuration

```python
client = vynco.Client(
    api_key="vc_live_xxx",
    base_url="https://vynco.ch/api",  # default
    timeout=30.0,                     # seconds, default
    max_retries=2,                    # default, retries on 429/5xx
)
```

The API key can also be set via the `VYNCO_API_KEY` environment variable:

```bash
export VYNCO_API_KEY=vc_live_your_api_key
```

```python
client = vynco.Client()  # reads from VYNCO_API_KEY
```

The client automatically retries on HTTP 429 (rate limited) and 5xx (server error) with
exponential backoff (500ms x 2^attempt). It respects the `Retry-After` and `X-RateLimit-Reset` headers when present.

## Error Handling

All API errors are mapped to typed exceptions:

```python
try:
    company = client.companies.get("CHE-000.000.000")
except vynco.AuthenticationError:
    print("Invalid API key")
except vynco.InsufficientCreditsError:
    print("Top up credits")
except vynco.ForbiddenError:
    print("Insufficient permissions")
except vynco.NotFoundError as e:
    print(f"Not found: {e.detail}")
except vynco.ValidationError as e:
    print(f"Bad request: {e.detail}")
except vynco.ConflictError:
    print("Resource conflict")
except vynco.RateLimitError:
    print("Rate limited, retry later")
except vynco.ServerError:
    print("Server error")
except vynco.VyncoError as e:
    print(f"Error ({e.status}): {e.detail}")
```

| Exception | HTTP Status |
|-----------|-------------|
| `AuthenticationError` | 401 |
| `InsufficientCreditsError` | 402 |
| `ForbiddenError` | 403 |
| `NotFoundError` | 404 |
| `ConflictError` | 409 |
| `ValidationError` | 400, 422 |
| `RateLimitError` | 429 |
| `ServerError` | 5xx |
| `ServiceUnavailableError` | 503 |
| `ConfigError` | — (client misconfiguration) |

## Requirements

- Python 3.11+
- [httpx](https://www.python-httpx.org/) (async + sync HTTP)
- [Pydantic](https://docs.pydantic.dev/) v2 (model validation)

## Development

```bash
uv sync                     # install dependencies
uv run pytest               # run tests
uv run ruff check src/      # lint
uv run ruff format src/     # format
uv run mypy src/            # type check
```

## License

Apache-2.0
