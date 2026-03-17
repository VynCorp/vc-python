# VynCo Python SDK

Python client for the [VynCo](https://vynco.ch) Swiss Corporate Intelligence API.

- Async and sync clients
- Pydantic v2 models with full type safety
- 12 resource modules covering the full API surface
- Automatic retry with exponential backoff
- Response metadata (credits, rate limits, request tracing)

## Installation

```bash
pip install vynco
```

## Quick Start

```python
import vynco

# Sync client
client = vynco.Client("vc_live_your_api_key")
result = client.companies.search(query="Novartis", canton="BS")
for company in result.data.items:
    print(f"{company.name} ({company.uid}) - {company.status}")

# Check remaining credits
print(f"Credits remaining: {result.meta.credits_remaining}")
```

### Async

```python
import vynco

async def main():
    async with vynco.AsyncClient("vc_live_your_api_key") as client:
        result = await client.companies.search(query="Novartis")
        print(result.data.items[0].name)
```

### Environment Variable

```bash
export VYNCO_API_KEY=vc_live_your_api_key
```

```python
client = vynco.Client()  # reads VYNCO_API_KEY from environment
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

## Usage Examples

### Search Companies

```python
result = client.companies.search(
    query="pharma",
    canton="BS",
    status="ACTIVE",
    page=1,
    page_size=50,
)
print(f"Found {result.data.total} companies")
```

### Get Company Details

```python
company = client.companies.get("CHE-100.023.968")
print(f"{company.data.name} - Capital: {company.data.capital_nominal} {company.data.capital_currency}")
```

### Generate AI Dossier

```python
dossier = client.dossiers.generate("CHE-100.023.968", level="comprehensive")
print(dossier.data.executive_summary)
for insight in dossier.data.key_insights:
    print(f"  - {insight}")
```

### Error Handling

```python
try:
    result = client.companies.get("CHE-000.000.000")
except vynco.NotFoundError as e:
    print(f"Not found: {e.detail}")
except vynco.InsufficientCreditsError:
    print("Top up your credits")
except vynco.RateLimitError:
    print("Slow down, retry later")
except vynco.AuthenticationError:
    print("Check your API key")
except vynco.VyncoError as e:
    print(f"API error ({e.status}): {e.detail}")
```

### Credit Management

```python
balance = client.credits.balance()
print(f"Balance: {balance.data.balance}/{balance.data.monthly_credits}")
print(f"Tier: {balance.data.tier}")
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

## Development

```bash
uv sync
uv run pytest
uv run ruff check src/
uv run mypy src/
```

## License

Apache-2.0
