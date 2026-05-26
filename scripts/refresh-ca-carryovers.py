#!/usr/bin/env python3
"""
Replace existing CA pages that survived the v11 rename/remove pass with
design-system-aligned stubs. Same shell as create-stubs-ca.py — so US
and CA look visually identical until the content pass.

These pages keep their slugs (the rename was already done in a prior
step) but had pre-v11 content; this overwrites them with consistent
v11-compliant shells.

Usage:  python3 scripts/refresh-ca-carryovers.py
"""

import os
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SRC  = ROOT / "src"

# These are EXISTING files that need their bodies refreshed to the new
# design system. We're overwriting on purpose — the v11 content pass
# will replace stubs with real copy.
CARRYOVERS = [
    # CA HOME — the marquee page
    ("ca/index.html",
     "MedMe Health · Canada",
     None,  # No breadcrumb on home
     "MedMe · Canada",
     "The clinical operating system<br>for Canadian community pharmacy.",
     "MedsCheck, minor ailments, immunizations, POC testing &mdash; one workflow that captures the clinical service, codes it, and submits it. Built with Canadian pharmacists, deployed across 4,500+ stores nation-wide."),

    # ABOUT
    ("ca/about.html",
     "About MedMe Health",
     [("/ca", "Home"), ("About", None)],
     "About MedMe Health",
     "Built in Canada.<br>Built for Canadian pharmacy.",
     "Founded in Toronto in 2020 by Nick Hui, Rui Su, and Purya Sarmadi after the COVID immunization rollout exposed how little clinical software pharmacy actually had. Today, the platform runs in 4,500+ Canadian pharmacies."),

    # CONTACT
    ("ca/contact.html",
     "Contact MedMe Health",
     [("/ca", "Home"), ("Contact", None)],
     "Book a demo",
     "15 minutes, your service mix,<br>a written estimate.",
     "Tell us about your pharmacy. We&rsquo;ll walk through the platform live on your service catalog and leave you with a clinical-revenue estimate &mdash; no follow-up commitment required."),

    # PHARMACY
    ("ca/pharmacy/independents.html",
     "For Independent Pharmacies",
     [("/ca", "Home"), ("/ca/pharmacy/independents", "Pharmacy"), ("Independents", None)],
     "For independent owner-operators",
     "Built for the operator<br>who owns the floor.",
     "MedsCheck, minor ailments, immunizations &mdash; the clinical work you&rsquo;re already doing, all in one workflow that&rsquo;s tuned for the Canadian pharmacy bench. No medical-group EMR shoehorning."),

    ("ca/pharmacy/enterprises.html",
     "For Enterprise Pharmacy",
     [("/ca", "Home"), ("/ca/pharmacy/enterprises", "Pharmacy"), ("Enterprises", None)],
     "For chains &amp; health systems",
     "Strategic partner<br>for clinical services at scale.",
     "Top chains, regional groups, and health-system pharmacies across Canada run MedMe to standardize the clinical workflow, surface utilization to head office, and grow service revenue across stores."),

    # PLATFORM OVERVIEW (renamed from clinical-services.html)
    ("ca/platform/index.html",
     "MedMe Care Platform",
     [("/ca", "Home"), ("/ca/platform", "Platform"), ("MedMe Care Platform", None)],
     "MedMe Care Platform",
     "Scheduled, consulted,<br>documented &mdash; one platform.",
     "Each module is best-in-class. Together, they remove the swivel-chair between booking, intake, encounter, documentation, and follow-up &mdash; for the clinical services Canadian pharmacy actually delivers."),

    # PLATFORM MODULES (renamed)
    ("ca/platform/scheduling-queuing.html",
     "Scheduling &amp; Queuing",
     [("/ca", "Home"), ("/ca/platform", "Platform"), ("Scheduling & Queuing", None)],
     "Scheduling &amp; Queuing",
     "Online booking that fills<br>your clinical schedule.",
     "Patient-facing booking, intake forms, and eligibility verification &mdash; live before the patient walks in. No no-shows, no double bookings between dispense and consult."),

    ("ca/platform/ai-clinical-assistant.html",
     "AI Clinical Assistant",
     [("/ca", "Home"), ("/ca/platform", "Platform"), ("AI Clinical Assistant", None)],
     "AI Clinical Assistant",
     "A SOAP note in the time<br>it takes to walk them out.",
     "Pharmacy-tuned ambient AI captures the encounter as it happens. Drafts the note, suggests the code, stamps the time. The pharmacist reviews and signs &mdash; minutes, not the rest of the afternoon."),

    ("ca/platform/pms-integrations.html",
     "PMS Integrations",
     [("/ca", "Home"), ("/ca/platform", "Platform"), ("PMS Integrations", None)],
     "PMS Integrations",
     "Sits next to your stack,<br>not on top of it.",
     "MedMe doesn&rsquo;t replace Kroll, Fillware, BD Pharmacy Management, or any of the other Canadian PMS systems. We connect to all of them &mdash; pre-built &mdash; so your dispensing workflow doesn&rsquo;t change."),

    # PLATFORM AI ASSISTANTS sub-pages (moved into folder)
    ("ca/platform/ai-assistants/patient-concierge.html",
     "Patient Concierge",
     [("/ca", "Home"), ("/ca/platform", "Platform"), ("/ca/platform/ai-assistants", "AI Assistants"), ("Patient Concierge", None)],
     "Patient Concierge",
     "An always-on front desk<br>for the clinical service line.",
     "Inbound triage, appointment outreach, no-show rebooking, refill-driven outreach &mdash; handled by an AI concierge that knows your service catalog and your patient panel."),

    ("ca/platform/ai-assistants/admin-clerk.html",
     "Admin Clerk",
     [("/ca", "Home"), ("/ca/platform", "Platform"), ("/ca/platform/ai-assistants", "AI Assistants"), ("Admin Clerk", None)],
     "Admin Clerk",
     "The bridge to legacy PMS,<br>without an integration project.",
     "Admin Clerk performs back-office tasks and acts as the legacy PMS bridge &mdash; reading and writing into Kroll, Fillware, and other systems where a true API doesn&rsquo;t exist."),

    # CUSTOMERS
    ("ca/customers/index.html",
     "Customer Stories",
     [("/ca", "Home"), ("/ca/customers", "Customers"), ("Case Studies", None)],
     "Case Studies",
     "Stories from Canadian<br>community pharmacy.",
     "How Canadian operators &mdash; from single-store independents to province-wide rollouts &mdash; built clinical service lines on MedMe."),

    ("ca/customers/whole-health.html",
     "Whole Health Pharmacy",
     [("/ca", "Home"), ("/ca/customers", "Customers"), ("Whole Health", None)],
     "Customer story",
     "Whole Health Pharmacy.<br>One workflow, every service.",
     "How Whole Health rolled MedMe across their footprint to standardize MedsCheck, minor ailments, and immunization workflows &mdash; with measurable utilization gains in the first quarter."),

    # RESOURCES
    ("ca/resources/index.html",
     "Resources",
     [("/ca", "Home"), ("Resources", None)],
     "Resources",
     "Pharmacy-specific content,<br>built for Canadian operators.",
     "ROI calculators, white papers, policy briefs, and field-tested workflows &mdash; written for Canadian community pharmacy operators."),

    ("ca/resources/blog.html",
     "Blog",
     [("/ca", "Home"), ("/ca/resources", "Resources"), ("Blog", None)],
     "Blog",
     "Stories from clinical<br>community pharmacy.",
     "Operator playbooks, policy explainers, and customer-facing stories from the Canadian pharmacy field."),

    ("ca/resources/roi-calculator.html",
     "ROI Calculator",
     [("/ca", "Home"), ("/ca/resources", "Resources"), ("ROI Calculator", None)],
     "ROI Calculator",
     "Estimate your clinical<br>service revenue.",
     "Interactive calculator based on your visit volume, service mix, and provincial reimbursement schedule. No email gate."),
]

TEMPLATE = """<!DOCTYPE html>
<html lang="en-CA">
<head>
<meta charset="UTF-8" />
<meta name="viewport" content="width=device-width, initial-scale=1.0" />
<title>{title} — MedMe Health</title>
<meta name="description" content="{lede_meta}" />
<link rel="alternate" hreflang="en-us" href="https://medmehealth.com{us_alt}" />
<link rel="alternate" hreflang="en-ca" href="https://medmehealth.ca{ca_alt}" />
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
  .stub-hero h1.h-display {{ margin: 0.75rem auto 1rem; max-width: 920px; }}
  .stub-hero__lede {{ font-size: 1.1rem; line-height: 1.55; color: rgba(6, 62, 84, 0.78); max-width: 760px; margin: 0 auto 2rem; }}
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
    {breadcrumb_html}
    <span class="kicker kicker--matcha">{kicker}</span>
    <h1 class="h-display h-display--xl">{h1}</h1>
    <p class="stub-hero__lede">{lede}</p>
    <div class="stub-hero__cta">
      <a class="btn btn-primary" href="/ca/contact">{cta_primary} <span class="arrow">→</span></a>
      {cta_secondary}
    </div>
    <!-- TODO: content pass — full page sections go here. -->
    <div class="stub-todo">
      <b>Carryover (CA).</b> Page was migrated from the pre-v11 design system. Hero, breadcrumb, and nav/footer are now v11-compliant. Full content pass to replace the stub body with sections matching Christine&rsquo;s direction.
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
    if crumbs is None:
        return ""
    parts = []
    for i, c in enumerate(crumbs):
        href, label = c
        if label is None:
            parts.append(f"<span>{href}</span>")
        else:
            parts.append(f'<a href="{href}">{label}</a>')
        if i < len(crumbs) - 1:
            parts.append('<span class="sep">/</span>')
    return f'<div class="stub-hero__breadcrumb">{"".join(parts)}</div>'

def main():
    for stub in CARRYOVERS:
        path, title, crumbs, kicker, h1, lede = stub

        # CTAs per Christine's locked routing
        cta_primary = "Book a demo"
        cta_secondary = ""
        if "enterprises" in path:
            cta_primary = "Talk to enterprise team"
        elif "networks" in path:
            cta_primary = "Talk to our partnerships team"
        elif "specialty" in path:
            cta_primary = "Talk to specialty team"
        elif "/about" in path:
            cta_secondary = '<a class="btn btn-ghost" href="/company/careers">See open roles</a>'
        elif path == "ca/index.html":
            cta_secondary = '<a class="btn btn-ghost" href="/ca/platform">See the platform</a>'

        # hreflang alternates: keep light
        us_alt = "/us/" + path.replace("ca/", "").replace("/index.html", "/").replace(".html", "/")
        ca_alt = "/" + path.replace("/index.html", "/").replace(".html", "/")

        out = SRC / path
        out.parent.mkdir(parents=True, exist_ok=True)

        content = TEMPLATE.format(
            title=title.replace("&amp;", "&"),
            lede_meta=lede.replace('"', "'").replace("<br>", " ").replace("&mdash;", "—").replace("&ndash;", "–").replace("&rsquo;", "'").replace("&amp;", "&"),
            breadcrumb_html=crumb_html(crumbs),
            kicker=kicker,
            h1=h1,
            lede=lede,
            cta_primary=cta_primary,
            cta_secondary=cta_secondary,
            us_alt=us_alt,
            ca_alt=ca_alt,
        )
        out.write_text(content, encoding="utf-8")
        print(f"refreshed     {path}")

if __name__ == "__main__":
    main()
