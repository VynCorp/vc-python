"""Due Diligence — KYC/AML screening, risk scoring, and AI dossier generation.

Demonstrates a typical compliance workflow: screen a company against sanctions
lists, compute a risk score, and generate an AI-powered intelligence dossier.

Usage:
    export VYNCO_API_KEY=vc_live_...
    python examples/due_diligence.py
"""

from __future__ import annotations

import vynco


def main() -> None:
    client = vynco.Client()

    # Find target company by search
    results = client.companies.list(query="ABB", canton="ZH", page_size=1)
    target_uid = results.data.items[0].uid
    company = client.companies.get(target_uid).data
    print(f"=== Due Diligence Report: {company.name} ===\n")

    # --- Step 1: Sanctions screening ---
    print("1. Sanctions Screening")
    screening = client.screening.screen(name=company.name, uid=target_uid)
    s = screening.data
    print(f"   Risk level:      {s.risk_level}")
    print(f"   Hits:            {s.hit_count}")
    print(f"   Sources checked: {', '.join(s.sources_checked)}")
    if s.hits:
        for hit in s.hits:
            print(f"   - {hit.matched_name} (source: {hit.source}, score: {hit.score:.2f})")
    print()

    # --- Step 2: AI risk score ---
    print("2. AI Risk Score")
    risk = client.ai.risk_score(uid=target_uid)
    r = risk.data
    print(f"   Overall score:   {r.overall_score}/100")
    print(f"   Risk level:      {r.risk_level}")
    print("   Breakdown:")
    for factor in r.breakdown:
        bar = "█" * (factor.score // 5) + "░" * (20 - factor.score // 5)
        print(f"     {factor.factor:<25} {bar} {factor.score:>3}/100  ({factor.description})")
    print()

    # --- Step 3: Classification ---
    print("3. Industry Classification")
    cls = client.companies.classification(target_uid)
    cl = cls.data
    print(f"   Sector:          {cl.sector_name} ({cl.sector_code})")
    print(f"   Group:           {cl.group_name} ({cl.group_code})")
    print(f"   Industry:        {cl.industry_name} ({cl.industry_code})")
    print(f"   FINMA regulated: {cl.is_finma_regulated}")
    print()

    # --- Step 4: Company fingerprint ---
    print("4. Company Fingerprint")
    fp = client.companies.fingerprint(target_uid)
    f = fp.data
    print(f"   Size category:   {f.size_category}")
    print(f"   Employee est.:   {f.employee_count_estimate}")
    print(f"   Board size:      {f.board_size}")
    print(f"   Subsidiary count:{f.subsidiary_count}")
    print(f"   Company age:     {f.company_age} years")
    print(f"   Change frequency:{f.change_frequency}")
    print()

    # --- Step 5: Recent corporate changes ---
    print("5. Recent Corporate Changes")
    changes = client.changes.by_company(target_uid)
    for ch in changes.data[:5]:
        print(
            f"   [{ch.detected_at}] {ch.change_type}: "
            f"{ch.field_name} — {ch.old_value} → {ch.new_value}"
        )

    # --- Step 6: AI dossier (if available) ---
    print("\n6. AI Intelligence Dossier")
    try:
        dossier = client.ai.dossier(uid=target_uid, depth="detailed")
        d = dossier.data
        print(f"   Generated at: {d.generated_at}")
        print(f"   Sources:      {len(d.sources)}")
        print(f"\n{d.dossier[:500]}...")
    except vynco.ServerError:
        print("   (AI dossier generation is currently unavailable)")


if __name__ == "__main__":
    main()
