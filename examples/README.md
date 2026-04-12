# Examples

Runnable Python scripts demonstrating real workflows with the VynCo API.

## Setup

Install the SDK and set your API key:

```bash
pip install vynco
export VYNCO_API_KEY=vc_live_your_api_key
```

All scripts pick up `VYNCO_API_KEY` automatically.

## Scripts

### [quickstart.py](quickstart.py) — Search and fetch

Your first five minutes with the API. Searches the commercial register, fetches a single company, pulls its full profile (persons, changes, relationships), and shows response metadata.

```bash
python examples/quickstart.py
```

---

### [due_diligence.py](due_diligence.py) — KYC/AML compliance workflow

A standard compliance run: sanctions screening → AI risk score → industry classification → company fingerprint → recent changes → AI dossier. Produces a readable due-diligence report with ASCII bar charts for the risk breakdown.

```bash
python examples/due_diligence.py
```

---

### [watchlist_monitor.py](watchlist_monitor.py) — Portfolio monitoring

Creates a watchlist, adds target companies, pulls their recent events, then cross-references with the global change feed. Cleans up after itself.

```bash
python examples/watchlist_monitor.py
```

---

### [company_network.py](company_network.py) — Corporate networks

Explores the network around a company: board members, shared-person relationships, parent/subsidiary hierarchy (now with `confidence` and `sharedPersonCount`), corporate structure, and the full graph. Ends with a multi-company network analysis using `graph.analyze()`.

```bash
python examples/company_network.py
```

---

### [bulk_export.py](bulk_export.py) — Data export

Two export patterns: quick direct CSV export via `companies.export_csv()`, and async bulk export jobs via `exports.create()` + polling + `exports.download()`.

```bash
python examples/bulk_export.py
```

---

### [historical_timeline.py](historical_timeline.py) *(v3.1+)* — Company evolution over time

Pulls a full chronological timeline of every change the company has made (capital moves, board changes, name changes, address updates), groups events by category, and generates an AI narrative summary via `companies.timeline_summary()`.

```bash
python examples/historical_timeline.py
```

---

### [ubo_resolution.py](ubo_resolution.py) *(v3.1+)* — Ultimate beneficial owners

An AML-compliance workflow: resolves UBOs via `companies.ubo()`, traces the full ownership chain with `ownership.trace()` (including circular-ownership detection), then runs batch sanctions screening across every entity in the chain using `screening.batch()`.

```bash
python examples/ubo_resolution.py
```

## Tips

- All scripts search for a company dynamically (they don't hardcode UIDs), so they adapt to the live database.
- Scripts that create resources (watchlist_monitor) clean up after themselves.
- The `bulk_export.py` script writes files into an `exports/` directory; add it to your `.gitignore` if you run it locally.
- Errors surface as typed exceptions (`vynco.AuthenticationError`, `vynco.NotFoundError`, etc.) — see the main [README](../README.md#error-handling) for the full list.
