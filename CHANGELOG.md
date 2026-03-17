# Changelog

## 0.1.0 (2026-03-17)

- Initial release
- Async and sync clients (`AsyncClient`, `Client`)
- 12 resource modules: Companies, Persons, Dossiers, Changes, Credits, Billing, ApiKeys, Webhooks, Teams, Users, Settings, Analytics
- Pydantic v2 models with camelCase alias support
- Typed error hierarchy mirroring the Rust SDK
- Response metadata from API headers (credits, rate limits, request ID)
- Retry logic with exponential backoff on 429/5xx
- Environment variable support (`VYNCO_API_KEY`)
