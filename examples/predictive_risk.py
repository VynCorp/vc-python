"""Predictive Risk — AI-powered dissolution probability and credit risk scoring.

Combines predictive risk analysis with industry reports and sanctions browsing
to build a comprehensive risk assessment pipeline.

Usage:
    export VYNCO_API_KEY=vc_live_...
    python examples/predictive_risk.py
"""

from __future__ import annotations

import vynco


def main() -> None:
    client = vynco.Client()

    # Find target company
    results = client.companies.list(query="UBS", page_size=1)
    target_uid = results.data.items[0].uid
    company_name = results.data.items[0].name
    print(f"=== Predictive Risk Assessment: {company_name} ===\n")

    # --- Step 1: Predictive risk scoring ---
    print("1. Predictive Risk Score")
    risk = client.ai.predictive_risk(uid=target_uid)
    r = risk.data
    print(f"   Dissolution probability: {r.dissolution_probability:.1f}%")
    print(f"   Risk level:              {r.risk_level}")
    print(f"   Credit risk score:       {r.credit_risk_score}/100")
    print(f"   Recommendation:          {r.recommendation}")
    print(f"\n   Pre-dissolution indicators:")
    for ind in r.pre_dissolution_indicators:
        triggered = "TRIGGERED" if ind.triggered else "clear"
        print(
            f"     [{triggered:>9}] {ind.signal:<30} "
            f"severity={ind.severity:<6} contribution={ind.contribution:.1f}%"
        )
    print()

    # --- Step 2: AI comparative analysis ---
    print("2. Comparative Analysis (UBS vs ABB)")
    abb = client.companies.list(query="ABB", canton="ZH", page_size=1).data.items[0]
    try:
        comp = client.ai.comparative(
            uids=[target_uid, abb.uid],
            focus="governance",
        )
        c = comp.data
        print(f"   Focus: {c.focus}")
        print(f"   Governance scores:")
        for gs in c.governance_scores:
            print(f"     {gs.company_name}: {gs.score}/100")
        if c.board_overlaps:
            print(f"   Board overlaps: {len(c.board_overlaps)} shared persons")
        print(
            f"   Auditor concentration: {'YES' if c.auditor_analysis and c.auditor_analysis.concentration_flag else 'no'}"
        )
        print(f"   Report: {len(c.report)} chars")
    except (vynco.ServerError, Exception) as e:
        print(
            f"   (Comparative analysis unavailable: {type(e).__name__} — "
            "LLM endpoints may need a higher client timeout)"
        )
    print()

    # --- Step 3: Browse sanctions ---
    print("3. Sanctions Database Browse")
    sanctions = client.screening.browse_sanctions(search="bank", page_size=5)
    print(f"   Total matches: {sanctions.data.total}")
    for s in sanctions.data.items[:5]:
        print(f"     {s.name} ({s.entity_type}) — program: {s.program}")
    print()

    # --- Step 4: Industry report ---
    print("4. Industry Intelligence")
    industries = client.reports.industries()
    print(f"   Available industries: {industries.data.total}")
    if industries.data.industries:
        top = sorted(industries.data.industries, key=lambda i: -i.company_count)[:5]
        for ind in top:
            print(f"     {ind.industry}: {ind.company_count:,} companies")
    print()

    # --- Step 5: Company PDF profile ---
    print("5. PDF Profile Data")
    pdf = client.companies.pdf(target_uid)
    p = pdf.data
    print(f"   Company: {p.company.name}")
    print(f"   Board members: {len(p.board_members)}")
    print(f"   Recent events: {len(p.recent_events)}")
    print(f"   Auditor history: {len(p.auditor_history)}")
    print(f"   Generated at: {p.generated_at}")


if __name__ == "__main__":
    main()
