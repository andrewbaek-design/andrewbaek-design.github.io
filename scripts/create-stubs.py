#!/usr/bin/env python3
"""
One-shot script: create minimal stub pages for every new v11 surface
that doesn't yet exist. Each stub uses the existing design system
(brand.css + nav-us + footer-us) and carries a TODO marker so the
content pass can target it.

Usage:  python3 scripts/create-stubs.py
"""

import os
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SRC  = ROOT / "src"

# (file path, page title, breadcrumb path, kicker, h1, lede)
STUBS = [
    # PHARMACY
    ("us/pharmacy/multi-store.html",
     "For Multi-Store Pharmacy",
     [("/us", "Home"), ("/us/pharmacy/multi-store", "Pharmacy"), ("Multi-store", None)],
     "For multi-store operators",
     "Built for regional groups<br>and small chains.",
     "4&ndash;25 store operators &mdash; you have most of an enterprise's complexity without the enterprise IT team. MedMe gives you cross-store rollups, region-level dashboards, and predictable per-store pricing."),

    ("us/pharmacy/networks.html",
     "For Pharmacy Networks",
     [("/us", "Home"), ("/us/pharmacy/networks", "Pharmacy"), ("Networks", None)],
     "For banners, co-ops &amp; PSAOs",
     "One platform for the whole network.<br>Visible, standardized, flexible.",
     "Unlock your member data, standardize the clinical workflow across stores, and run commercial models that fit your network &mdash; member discount, volume rebate, or network-paid subscription."),

    ("us/pharmacy/specialty.html",
     "For Specialty Pharmacy",
     [("/us", "Home"), ("/us/pharmacy/specialty", "Pharmacy"), ("Specialty", None)],
     "For specialty &amp; payvider partners",
     "Specialty workflows, built in.<br>Prior-auth, outcomes, monitoring.",
     "Oncology, HIV, transplant, infusion &mdash; the specialty therapy workflows specialty pharmacies actually run, with prior-auth tracking, manufacturer outcomes reporting, and patient adherence monitoring baked in."),

    # PLATFORM — module sub-pages (overview already exists as platform/index.html)
    ("us/platform/scheduling-queuing.html",
     "Scheduling &amp; Queuing",
     [("/us", "Home"), ("/us/platform", "Platform"), ("Scheduling & Queuing", None)],
     "Scheduling &amp; Queuing",
     "Online booking that fills<br>your clinical schedule.",
     "Patient-facing booking, intake forms, and eligibility verification &mdash; live before the patient walks in. No no-shows, no unbillable encounters, no double bookings between dispense and consult."),

    ("us/platform/patient-intake.html",
     "Patient Intake Form",
     [("/us", "Home"), ("/us/platform", "Platform"), ("Patient Intake Form", None)],
     "Patient Intake Form",
     "Forms that fill themselves<br>before the visit starts.",
     "Pre-visit intake captured digitally and pre-filled from the patient's chart. By the time they walk in, the pharmacist already has the picture &mdash; no clipboards, no re-keying."),

    ("us/platform/assisted-documentation.html",
     "Assisted Documentation",
     [("/us", "Home"), ("/us/platform", "Platform"), ("Assisted Documentation", None)],
     "Assisted Documentation",
     "SOAP, care plans, transitions &mdash;<br>drafted as the encounter happens.",
     "Pharmacy-tuned templates for CCM, MTM, immunizations, POCT, and transitions-of-care. The chart writes itself in the background so pharmacists can stay with the patient."),

    ("us/platform/messaging-follow-ups.html",
     "Messaging &amp; Follow-Ups",
     [("/us", "Home"), ("/us/platform", "Platform"), ("Messaging & Follow-Ups", None)],
     "Messaging &amp; Follow-Ups",
     "Multi-channel patient messaging,<br>without a separate inbox.",
     "Email, SMS, and patient-portal messages from one interface. Confirmation, reminder, follow-up cadences set by visit type &mdash; running quietly in the background."),

    # PLATFORM — AI Assistants
    ("us/platform/ai-assistants/index.html",
     "AI Assistants",
     [("/us", "Home"), ("/us/platform", "Platform"), ("AI Assistants", None)],
     "AI Assistants",
     "AI woven through the platform,<br>not bolted on top.",
     "Patient Concierge handles inbound triage, outreach, and rebooking. Admin Clerk runs back-office tasks and bridges legacy PMS data into MedMe. Both are sibling modules to Pharmacy EHR &mdash; not nested inside it."),

    ("us/platform/ai-assistants/patient-concierge.html",
     "Patient Concierge",
     [("/us", "Home"), ("/us/platform", "Platform"), ("/us/platform/ai-assistants", "AI Assistants"), ("Patient Concierge", None)],
     "Patient Concierge",
     "An always-on front desk<br>for the clinical service line.",
     "Inbound triage, appointment outreach, no-show rebooking, refill-driven CCM nudges &mdash; handled by an AI concierge that knows your service catalog and your patient panel."),

    ("us/platform/ai-assistants/admin-clerk.html",
     "Admin Clerk",
     [("/us", "Home"), ("/us/platform", "Platform"), ("/us/platform/ai-assistants", "AI Assistants"), ("Admin Clerk", None)],
     "Admin Clerk",
     "The bridge to legacy PMS,<br>without an integration project.",
     "Admin Clerk performs back-office tasks and acts as the legacy PMS bridge &mdash; reading and writing into PioneerRx, BestRx, McKesson, and other systems where a true API doesn't exist."),

    # PLATFORM — PMS Integrations (already exists, renamed)
    # Already created via rename

    # RESOURCES
    ("us/resources/events.html",
     "Events",
     [("/us", "Home"), ("/us/resources", "Resources"), ("Events", None)],
     "Events",
     "Where you'll see MedMe<br>in person this year.",
     "Conference booths, partner dinners, regional roundtables. Pharmacy operators come up to us; we don't run booth bingo."),

    ("us/resources/white-papers.html",
     "White Papers",
     [("/us", "Home"), ("/us/resources", "Resources"), ("White Papers", None)],
     "White Papers",
     "Research and policy briefs<br>for pharmacy operators.",
     "Written for the operator on the floor, not the policy wonk. State-by-state scope of practice, payer-mix benchmarks, RHTP impact, and the case studies behind them."),

    # PARTNERS
    ("us/partners/index.html",
     "Partners",
     [("/us", "Home"), ("/us/partners", "Partners")],
     "Partners",
     "How we work with the rest<br>of the pharmacy ecosystem.",
     "Pharmacy associations, networks, and the partners who push the strategic agenda for community pharmacy. The most-endorsed clinical services platform in pharmacy &mdash; here's why."),

    ("us/partners/pharmacy-associations.html",
     "Pharmacy Associations",
     [("/us", "Home"), ("/us/partners", "Partners"), ("Pharmacy Associations", None)],
     "Pharmacy Associations",
     "State and national associations,<br>pushing the agenda together.",
     "Endorsed and embedded in association strategy &mdash; MTMS rollouts, test-and-treat playbooks, research sponsorships, and the Impact Fund."),

    # COMPANY (footer-only surfaces)
    ("us/company/our-team.html",
     "Our Team",
     [("/us", "Home"), ("/us/company/our-team", "Company"), ("Our Team", None)],
     "Our Team",
     "Founders + operators<br>building this with you.",
     "The leadership team behind MedMe: founders, clinical leaders, and the operators who came up through pharmacy."),

    # LEGAL HUB
    ("legal/index.html",
     "Legal",
     [("/us", "Home"), ("Legal", None)],
     "Legal",
     "MedMe legal notices.",
     "The legal documents that govern MedMe Health products and our customer relationships. Reach out to <a href=\"mailto:legal@medmehealth.com\">legal@medmehealth.com</a> with questions."),
]

# Legal hub has a special body — list out the legal docs.
LEGAL_HUB_BODY = """
    <div class="legal-hub-list">
      <a class="legal-hub-card" href="/legal/privacy"><h3>Privacy Policy</h3><p>How we collect, use, and protect personal data.</p></a>
      <a class="legal-hub-card" href="/legal/terms"><h3>Terms of Service</h3><p>The contract that governs your use of MedMe products.</p></a>
      <a class="legal-hub-card" href="/legal/security"><h3>Security</h3><p>Our security posture, audits, and certifications.</p></a>
      <a class="legal-hub-card" href="/legal/hipaa"><h3>HIPAA</h3><p>Our HIPAA program and BAA process for covered entities.</p></a>
      <a class="legal-hub-card" href="/legal/pipeda"><h3>PIPEDA</h3><p>Canadian privacy law compliance for our Canada customers.</p></a>
    </div>
"""

TEMPLATE = """<!DOCTYPE html>
<html lang="en-US">
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
  .legal-hub-list {{ max-width: 760px; margin: 2.5rem auto 0; display: grid; grid-template-columns: 1fr 1fr; gap: 1rem; padding: 0 2rem; }}
  .legal-hub-card {{ background: #fff; border: 1px solid rgba(6, 62, 84, 0.08); border-radius: 12px; padding: 1.5rem; text-decoration: none; color: inherit; transition: border-color .18s ease, transform .18s ease; display: block; }}
  .legal-hub-card:hover {{ border-color: rgba(6, 62, 84, 0.25); transform: translateY(-2px); }}
  .legal-hub-card h3 {{ margin: 0 0 0.35rem; font-size: 1.05rem; font-weight: 700; color: var(--indigo, #063E54); }}
  .legal-hub-card p {{ margin: 0; font-size: 0.875rem; color: rgba(6, 62, 84, 0.7); line-height: 1.5; }}
  @media (max-width: 600px) {{ .legal-hub-list {{ grid-template-columns: 1fr; }} }}
</style>
</head>
<body>
<a href="#main" class="skip-link">Skip to main content</a>
{{{{> partials/util-bar-us }}}}
{{{{> partials/nav-us }}}}

<main id="main">
<section class="stub-hero">
  <div class="stub-hero__inner">
    <div class="stub-hero__breadcrumb">{breadcrumb}</div>
    <span class="kicker kicker--matcha">{kicker}</span>
    <h1 class="h-display h-display--xl">{h1}</h1>
    <p class="stub-hero__lede">{lede}</p>
    <div class="stub-hero__cta">
      <a class="btn btn-primary" href="/us/contact">{cta_primary} <span class="arrow">→</span></a>
    </div>
    <!-- TODO: content pass — full page sections go here. -->
    <div class="stub-todo">
      <b>Stub page.</b> Full content lands during the per-page content pass. Hero copy and breadcrumb are wired to v11 naming — body sections, mocks, and CTAs to follow.
    </div>
    {extra_body}
  </div>
</section>
</main>

{{{{> partials/footer-us }}}}
<script src="/assets/site.js" defer></script>
</body>
</html>
"""

def crumb_html(crumbs):
    parts = []
    for i, c in enumerate(crumbs):
        href, label = c
        if label is None:
            # Last item, plain text
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
        extra_body = ""
        # Customize CTAs per spec routing
        if "enterprises" in path:
            cta_primary = "Talk to enterprise team"
        elif "networks" in path:
            cta_primary = "Talk to our partnerships team"
        elif "specialty" in path:
            cta_primary = "Talk to specialty team"
        elif "pharmacy-associations" in path:
            cta_primary = "Partnerships inquiry"
        elif "multi-store" in path:
            cta_primary = "Talk to our team"

        # Legal hub: list of legal docs
        if path == "legal/index.html":
            extra_body = LEGAL_HUB_BODY

        out = SRC / path
        out.parent.mkdir(parents=True, exist_ok=True)

        # Skip if file exists AND is not a stub-renamed page (we want fresh
        # stubs for genuinely new pages, not overwrite the renamed pages)
        if out.exists():
            print(f"skip (exists)  {path}")
            continue

        content = TEMPLATE.format(
            title=title.replace("&amp;", "&"),
            lede_meta=lede.replace('"', "'").replace("<br>", " ").replace("&mdash;", "—").replace("&ndash;", "–"),
            breadcrumb=crumb_html(crumbs),
            kicker=kicker,
            h1=h1,
            lede=lede,
            cta_primary=cta_primary,
            extra_body=extra_body,
        )
        out.write_text(content, encoding="utf-8")
        print(f"created       {path}")

if __name__ == "__main__":
    main()
