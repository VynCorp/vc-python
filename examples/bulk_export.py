"""Bulk Export — Export filtered company data to Excel or CSV.

Demonstrates two export approaches: quick Excel export of specific companies,
and an async bulk export job with polling.

Usage:
    export VYNCO_API_KEY=vc_live_...
    python examples/bulk_export.py
"""

from __future__ import annotations

import time
from pathlib import Path

import vynco


def main() -> None:
    client = vynco.Client()

    output_dir = Path("exports")
    output_dir.mkdir(exist_ok=True)

    # --- Find some companies to export ---
    print("=== Data Export ===\n")
    uids = []
    for query in ["ABB", "UBS", "Novartis"]:
        results = client.companies.list(query=query, page_size=1)
        if results.data.items:
            co = results.data.items[0]
            uids.append(co.uid)
            print(f"  Found: {co.name} ({co.uid})")

    # --- Quick export of specific companies ---
    print("\n1. Quick Export (specific companies)")
    export = client.companies.export_excel(
        uids=uids,
        fields=["name", "canton", "status", "legal_form", "share_capital", "industry"],
    )
    path = output_dir / export.filename
    path.write_bytes(export.bytes)
    print(f"   Saved: {path} ({len(export.bytes):,} bytes, {export.content_type})")
    print(f"   Credits used: {export.meta.credits_used}\n")

    # --- Bulk export with filters ---
    print("2. Bulk Export (filtered by canton)")
    job = client.exports.create(
        format="csv",
        canton="ZH",
        status="active",
        max_rows=100,
    )
    print(f"   Export job created: {job.data.id}")
    print(f"   Status: {job.data.status}")

    # Poll until complete
    while True:
        download = client.exports.get(job.data.id)
        current_status = download.data.job.status
        print(f"   Status: {current_status}...")
        if current_status in ("completed", "failed"):
            break
        time.sleep(2)

    if current_status == "completed":
        job_info = download.data.job
        print(f"   Rows: {job_info.total_rows}, Size: {job_info.file_size_bytes} bytes")
        try:
            export_file = client.exports.download(job.data.id)
            path = output_dir / export_file.filename
            path.write_bytes(export_file.bytes)
            print(f"   Saved: {path} ({len(export_file.bytes):,} bytes)")
        except vynco.NotFoundError:
            # Some export jobs return data inline via exports.get()
            if download.data.data:
                path = output_dir / f"export-{job.data.id}.csv"
                path.write_text(download.data.data)
                print(f"   Saved (inline): {path}")
            else:
                print("   Export completed but download not available")
    else:
        print(f"   Export failed: {download.data.job.error_message}")

    # --- Company statistics ---
    print("\n3. Database Statistics")
    stats = client.companies.statistics()
    s = stats.data
    print(f"   Total companies: {s.total:,}")
    print("   By status:")
    for status_name, count in sorted(s.by_status.items(), key=lambda x: -x[1])[:5]:
        print(f"     {status_name:<20} {count:>8,}")
    print("   By canton (top 5):")
    for canton, count in sorted(s.by_canton.items(), key=lambda x: -x[1])[:5]:
        print(f"     {canton:<20} {count:>8,}")


if __name__ == "__main__":
    main()
