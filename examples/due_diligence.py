"""Due Diligence — KYC/AML screening, risk scoring, and AI dossier generation.

Demonstrates a typical compliance workflow: screen a company against sanctions
lists, compute a risk score, and generate an AI-powered intelligence dossier.

Some steps require the Professional tier; on a lower tier they are skipped with
a note rather than failing.

Usage:
    export VYNCO_API_KEY=vc_live_...
    python examples/due_diligence.py
"""

from __future__ import annotations

from _common import get_client, section


def main() -> None:
    client = get_client()

    # Find target company by search (Free tier)
    results = client.companies.list(query="ABB", canton="ZH", page_size=1)
    if not results.data.items:
        print("No company found for the search; try a different query.")
        return
    target_uid = results.data.items[0].uid
    company = client.companies.get(target_uid).data
    print(f"=== Due Diligence Report: {company.name} ===\n")

    # --- Step 1: Sanctions screening ---
    with section("1. Sanctions Screening"):
        s = client.screening.screen(name=company.name, uid=target_uid).data
        print(f"   Risk level:      {s.risk_level}")
        print(f"   Hits:            {s.hit_count}")
        print(f"   Sources checked: {', '.join(s.sources_checked)}")
        for hit in s.hits:
            print(f"   - {hit.matched_name} (source: {hit.source}, score: {hit.score:.2f})")
    print()

    # --- Step 2: AI risk score (Professional) ---
    with section("2. AI Risk Score"):
        r = client.ai.risk_score(uid=target_uid).data
        print(f"   Overall score:   {r.overall_score}/100")
        print(f"   Risk level:      {r.risk_level}")
        print("   Breakdown:")
        for factor in r.breakdown:
            bar = "█" * (factor.score // 5) + "░" * (20 - factor.score // 5)
            print(f"     {factor.factor:<25} {bar} {factor.score:>3}/100  ({factor.description})")
    print()

    # --- Step 3: Classification ---
    with section("3. Industry Classification"):
        cl = client.companies.classification(target_uid).data
        print(f"   Sector:          {cl.sector_name} ({cl.sector_code})")
        print(f"   Group:           {cl.group_name} ({cl.group_code})")
        print(f"   Industry:        {cl.industry_name} ({cl.industry_code})")
        print(f"   FINMA regulated: {cl.is_finma_regulated}")
    print()

    # --- Step 4: Company fingerprint ---
    with section("4. Company Fingerprint"):
        f = client.companies.fingerprint(target_uid).data
        print(f"   Size category:   {f.size_category}")
        print(f"   Employee est.:   {f.employee_count_estimate}")
        print(f"   Board size:      {f.board_size}")
        print(f"   Subsidiary count:{f.subsidiary_count}")
        print(f"   Company age:     {f.company_age} years")
        print(f"   Change frequency:{f.change_frequency}")
    print()

    # --- Step 5: Recent corporate changes ---
    with section("5. Recent Corporate Changes"):
        changes = client.changes.by_company(target_uid)
        for ch in changes.data[:5]:
            print(
                f"   [{ch.detected_at}] {ch.change_type}: "
                f"{ch.field_name} — {ch.old_value} → {ch.new_value}"
            )
    print()

    # --- Step 6: AI dossier (Professional) ---
    with section("6. AI Intelligence Dossier"):
        d = client.ai.dossier(uid=target_uid, depth="detailed").data
        print(f"   Generated at: {d.generated_at}")
        print(f"   Sources:      {len(d.sources)}")
        print(f"   Citations:    {len(d.citations)}")
        print(f"\n{d.dossier[:500]}...")


if __name__ == "__main__":
    main()
