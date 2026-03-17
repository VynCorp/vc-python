# vynco

Python SDK for the [VynCo](https://vynco.ch) Swiss Corporate Intelligence API.

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

# Search companies
result = client.companies.search(query="Novartis", canton="BS")
for company in result.data.items:
    print(f"{company.name} ({company.uid}) - {company.status}")

# Get company details
company = client.companies.get("CHE-100.023.968")
print(f"{company.data.name}: {company.data.purpose}")

# Check credit balance
balance = client.credits.balance()
print(f"Balance: {balance.data.balance} credits")
print(f"Credits used: {result.meta.credits_used}")
```

## Async Usage

```python
import vynco

async def main():
    async with vynco.AsyncClient("vc_live_your_api_key") as client:
        result = await client.companies.search(query="Novartis")
        print(result.data.items[0].name)

        balance = await client.credits.balance()
        print(f"Balance: {balance.data.balance}")
```

## Resources

| Resource | Methods |
|----------|---------|
| `client.companies` | `search`, `get`, `count`, `statistics`, `compare`, `persons`, `dossier`, `relationships`, `hierarchy`, `changes`, `batch_get`, `news` |
| `client.persons` | `get`, `search` |
| `client.dossiers` | `generate` |
| `client.changes` | `list`, `by_company`, `statistics` |
| `client.credits` | `balance`, `usage`, `history` |
| `client.api_keys` | `list`, `create`, `revoke` |
| `client.billing` | `create_checkout`, `create_portal` |
| `client.webhooks` | `list`, `create`, `get`, `update`, `delete`, `test` |
| `client.teams` | `me`, `create` |
| `client.users` | `me`, `update_profile` |
| `client.settings` | `get`, `update` |
| `client.analytics` | `cantons`, `auditors`, `rfm_segments`, `velocity` |

## Response Metadata

Every response includes header metadata:

```python
resp = client.companies.get("CHE-100.023.968")

print(f"Request ID: {resp.meta.request_id}")
print(f"Credits used: {resp.meta.credits_used}")
print(f"Credits remaining: {resp.meta.credits_remaining}")
print(f"Rate limit: {resp.meta.rate_limit_limit}")
print(f"Data source: {resp.meta.data_source}")  # "Zefix" or "LINDAS"
```

## Configuration

```python
client = vynco.Client(
    api_key="vc_live_xxx",
    base_url="https://api.vynco.ch/v1",  # default
    timeout=30.0,                          # seconds, default
    max_retries=2,                         # default, retries on 429/5xx
)
```

The API key can also be set via the `VYNCO_API_KEY` environment variable:

```bash
export VYNCO_API_KEY=vc_live_your_api_key
```

```python
client = vynco.Client()  # reads from VYNCO_API_KEY
```

## Error Handling

```python
try:
    company = client.companies.get("CHE-000.000.000")
except vynco.NotFoundError as e:
    print(f"Not found: {e.detail}")
except vynco.RateLimitError:
    print("Rate limited, try again later")
except vynco.InsufficientCreditsError:
    print("Top up credits")
except vynco.AuthenticationError:
    print("Check your API key")
except vynco.VyncoError as e:
    print(f"Error ({e.status}): {e.detail}")
```

| Exception | HTTP Status |
|-----------|-------------|
| `AuthenticationError` | 401 |
| `InsufficientCreditsError` | 402 |
| `ForbiddenError` | 403 |
| `NotFoundError` | 404 |
| `ValidationError` | 400, 422 |
| `RateLimitError` | 429 |
| `ServerError` | 5xx |
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
