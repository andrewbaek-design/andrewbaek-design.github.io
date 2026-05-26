#!/usr/bin/env python3
"""
Create CA stub pages for every new v11 surface that doesn't yet exist
under src/ca/. Same design-system template as the US stubs — Montserrat,
seashell hero, h-display, kicker, locked CTAs per Christine's strategy doc.

CA-specific differences from US:
  - Platform overview labeled "MedMe Care Platform"
  - No Medical Billing Suite (US-only)
  - Networks subtext: "Banners & Co-ops" (no PSAOs)
  - Partners: Provincial Associations (not Pharmacy Associations)
  - L4 sub-page: Nova Scotia / PANS, nested under Enterprises

Usage:  python3 scripts/create-stubs-ca.py
"""

import os
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SRC  = ROOT / "src"

# (file path, page title, breadcrumb path, kicker, h1, lede)
STUBS = [
    # PHARMACY
    ("ca/pharmacy/networks.html",
     "For Pharmacy Networks",
     [("/ca", "Home"), ("/ca/pharmacy/networks", "Pharmacy"), ("Networks", None)],
     "For banners &amp; co-ops",
     "One platform for the whole network.<br>Visible, standardized, flexible.",
     "Unlock your member data, standardize the clinical workflow across stores, and run commercial models that fit your network &mdash; member discount, volume rebate, or network-paid subscription."),

    ("ca/pharmacy/specialty.html",
     "For Specialty Pharmacy",
     [("/ca", "Home"), ("/ca/pharmacy/specialty", "Pharmacy"), ("Specialty", None)],
     "For specialty &amp; payer partners",
     "Specialty workflows, built in.<br>Prior-auth, outcomes, monitoring.",
     "Oncology, HIV, transplant, infusion &mdash; the specialty therapy workflows specialty pharmacies actually run, with prior-auth tracking, manufacturer outcomes reporting, and patient adherence monitoring baked in."),

    # PHARMACY → Enterprises → Nova Scotia / PANS (CA-only L4)
    ("ca/pharmacy/enterprises/nova-scotia-pans.html",
     "Nova Scotia / PANS",
     [("/ca", "Home"), ("/ca/pharmacy/enterprises", "Pharmacy"), ("/ca/pharmacy/enterprises", "Enterprises"), ("Nova Scotia / PANS", None)],
     "Featured · Nova Scotia",
     "PANS &amp; MedMe.<br>The province-wide rollout.",
     "How Nova Scotia&rsquo;s pharmacists, with PANS, made province-wide clinical service rollout the new operating standard. The deep-dive on what it took, how it scaled, and what it&rsquo;s done for community pharmacy in Atlantic Canada."),

    # PLATFORM — module sub-pages (overview already exists as platform/index.html)
    ("ca/platform/patient-intake.html",
     "Patient Intake Form",
     [("/ca", "Home"), ("/ca/platform", "Platform"), ("Patient Intake Form", None)],
     "Patient Intake Form",
     "Forms that fill themselves<br>before the visit starts.",
     "Pre-visit intake captured digitally and pre-filled from the patient&rsquo;s chart. By the time they walk in, the pharmacist already has the picture &mdash; no clipboards, no re-keying."),

    ("ca/platform/assisted-documentation.html",
     "Assisted Documentation",
     [("/ca", "Home"), ("/ca/platform", "Platform"), ("Assisted Documentation", None)],
     "Assisted Documentation",
     "SOAP, care plans, transitions &mdash;<br>drafted as the encounter happens.",
     "Pharmacy-tuned templates for MedsCheck, minor ailments, POC testing, immunizations, and transitions-of-care. The chart writes itself in the background so pharmacists can stay with the patient."),

    ("ca/platform/messaging-follow-ups.html",
     "Messaging &amp; Follow-Ups",
     [("/ca", "Home"), ("/ca/platform", "Platform"), ("Messaging & Follow-Ups", None)],
     "Messaging &amp; Follow-Ups",
     "Multi-channel patient messaging,<br>without a separate inbox.",
     "Email, SMS, and patient-portal messages from one interface. Confirmation, reminder, follow-up cadences set by visit type &mdash; running quietly in the background."),

    # PLATFORM — AI Assistants hub (sub-pages already moved into folder)
    ("ca/platform/ai-assistants/index.html",
     "AI Assistants",
     [("/ca", "Home"), ("/ca/platform", "Platform"), ("AI Assistants", None)],
     "AI Assistants",
     "AI woven through the platform,<br>not bolted on top.",
     "Patient Concierge handles inbound triage, outreach, and rebooking. Admin Clerk runs back-office tasks and bridges legacy PMS data into MedMe. Both are sibling modules to MedMe Care Platform &mdash; not nested inside it."),

    # RESOURCES
    ("ca/resources/events.html",
     "Events",
     [("/ca", "Home"), ("/ca/resources", "Resources"), ("Events", None)],
     "Events",
     "Where you&rsquo;ll see MedMe<br>across Canada this year.",
     "Conference booths, partner dinners, regional roundtables. Pharmacy operators come up to us; we don&rsquo;t run booth bingo."),

    ("ca/resources/white-papers.html",
     "White Papers",
     [("/ca", "Home"), ("/ca/resources", "Resources"), ("White Papers", None)],
     "White Papers",
     "Research and policy briefs<br>for Canadian pharmacy operators.",
     "Province-by-province scope of practice, pharmacist remuneration benchmarks, MedsCheck impact, and the case studies behind them."),

    ("ca/resources/webinars.html",
     "Webinars",
     [("/ca", "Home"), ("/ca/resources", "Resources"), ("Webinars", None)],
     "Webinars",
     "Live + on-demand<br>for Canadian pharmacy operators.",
     "Quarterly webinars on provincial scope expansion, clinical service rollouts, and the platform features built around them."),

    # PARTNERS
    ("ca/partners/index.html",
     "Partners",
     [("/ca", "Home"), ("/ca/partners", "Partners")],
     "Partners",
     "How we work with the rest<br>of Canadian pharmacy.",
     "Provincial associations, networks, and the partners who push the strategic agenda for community pharmacy across Canada."),

    ("ca/partners/provincial-associations.html",
     "Provincial Associations",
     [("/ca", "Home"), ("/ca/partners", "Partners"), ("Provincial Associations", None)],
     "Provincial Associations",
     "Provincial associations,<br>pushing the agenda together.",
     "PANS, OPA, BCPhA, and more &mdash; embedded in association strategy across Canada. Test-and-treat rollouts, MedsCheck program expansions, research sponsorships, and the Impact Fund."),

    # COMPANY (footer-only)
    ("ca/company/our-team.html",
     "Our Team",
     [("/ca", "Home"), ("/ca/company/our-team", "Company"), ("Our Team", None)],
     "Our Team",
     "Founders + operators<br>building this with you.",
     "The leadership team behind MedMe: founders, clinical leaders, and the operators who came up through pharmacy."),
]

TEMPLATE = """<!DOCTYPE html>
<html lang="en-CA">
<head>
<meta charset="UTF-8" />
<meta name="viewport" content="width=device-width, initial-scale=1.0" />
<title>{title} — MedMe Health</title>
<meta name="description" content="{lede_meta}" />
<link rel="preconnect" href="https://fonts.googleapis.com" />
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
<link href="https://fonts.googleapis.com/css2?family=Montserrat:wght@400;500;600;700;800&display=swap" rel="stylesheet" />
<link rel="stylesheet" href="/assets/brand.css?v=34" />
<style>
  /* TODO: content pass — replace stub hero with full page structure. */
  .stub-hero {{ background: var(--seashell, #FFF7F2); padding: 3.5rem 0 2.5rem; }}
  .stub-hero__inner {{ max-width: 1080px; margin: 0 auto; padding: 0 2rem; text-align: center; }}
  .stub-hero__breadcrumb {{ font-size: 13px; color: rgba(6, 62, 84, 0.55); margin-bottom: 1.5rem; }}
  .stub-hero__breadcrumb a {{ color: rgba(6, 62, 84, 0.55); text-decoration: none; }}
  .stub-hero__breadcrumb a:hover {{ color: var(--indigo, #063E54); }}
  .stub-hero__breadcrumb .sep {{ margin: 0 0.5rem; opacity: 0.4; }}
  .stub-hero h1.h-display {{ margin: 0.75rem auto 1rem; max-width: 880px; }}
  .stub-hero__lede {{ font-size: 1.1rem; line-height: 1.55; color: rgba(6, 62, 84, 0.78); max-width: 720px; margin: 0 auto 2rem; }}
  .stub-hero__cta {{ display: inline-flex; gap: 14px; flex-wrap: wrap; justify-content: center; }}
  .stub-todo {{ max-width: 720px; margin: 2rem auto 0; padding: 1.25rem 1.5rem; background: rgba(195, 196, 48, 0.12); border: 1px dashed rgba(195, 196, 48, 0.55); border-radius: 12px; color: #5a5b14; font-size: 0.875rem; line-height: 1.55; text-align: left; }}
  .stub-todo b {{ color: var(--indigo, #063E54); font-weight: 700; }}
</style>
</head>
<body>
<a href="#main" class="skip-link">Skip to main content</a>
{{{{> partials/util-bar-ca }}}}
{{{{> partials/nav-ca }}}}

<main id="main">
<section class="stub-hero">
  <div class="stub-hero__inner">
    <div class="stub-hero__breadcrumb">{breadcrumb}</div>
    <span class="kicker kicker--matcha">{kicker}</span>
    <h1 class="h-display h-display--xl">{h1}</h1>
    <p class="stub-hero__lede">{lede}</p>
    <div class="stub-hero__cta">
      <a class="btn btn-primary" href="/ca/contact">{cta_primary} <span class="arrow">→</span></a>
    </div>
    <!-- TODO: content pass — full page sections go here. -->
    <div class="stub-todo">
      <b>Stub page (CA).</b> Full content lands during the per-page content pass. Hero copy and breadcrumb are wired to v11 naming. CA-specific differences (MedMe Care Platform terminology, no Medical Billing Suite, Provincial Associations) applied.
    </div>
  </div>
</section>
</main>

{{{{> partials/footer-ca }}}}
<script src="/assets/site.js" defer></script>
</body>
</html>
"""

def crumb_html(crumbs):
    parts = []
    for i, c in enumerate(crumbs):
        href, label = c
        if label is None:
            parts.append(f"<span>{href}</span>")
        else:
            parts.append(f'<a href="{href}">{label}</a>')
        if i < len(crumbs) - 1:
            parts.append('<span class="sep">/</span>')
    return "".join(parts)

def main():
    for stub in STUBS:
        path, title, crumbs, kicker, h1, lede = stub
        cta_primary = "Book a demo"
        if "enterprises" in path or "pans" in path:
            cta_primary = "Talk to enterprise team"
        elif "networks" in path:
            cta_primary = "Talk to our partnerships team"
        elif "specialty" in path:
            cta_primary = "Talk to specialty team"
        elif "provincial-associations" in path:
            cta_primary = "Partnerships inquiry"

        out = SRC / path
        out.parent.mkdir(parents=True, exist_ok=True)

        if out.exists():
            print(f"skip (exists)  {path}")
            continue

        content = TEMPLATE.format(
            title=title.replace("&amp;", "&"),
            lede_meta=lede.replace('"', "'").replace("<br>", " ").replace("&mdash;", "—").replace("&ndash;", "–").replace("&rsquo;", "'").replace("&amp;", "&"),
            breadcrumb=crumb_html(crumbs),
            kicker=kicker,
            h1=h1,
            lede=lede,
            cta_primary=cta_primary,
        )
        out.write_text(content, encoding="utf-8")
        print(f"created       {path}")

if __name__ == "__main__":
    main()
