#!/usr/bin/env python3
"""
Apply Canadian-context substitutions to CA pages cloned from US.

Strategy:
  1. Swap partials (util-bar-us → util-bar-ca, nav-us → nav-ca, footer-us → footer-ca)
  2. Replace US-specific copy with Canadian equivalents
  3. Remove Medical Billing Suite tab from home tab bar (Phase 1)
  4. Fix hreflang URLs to point to /ca and /us correctly
  5. Update internal /us/ links to /ca/
  6. Swap stat numbers and customer names

Run on a per-file basis or for all CA pages:
  python3 scripts/ca-substitutions.py src/ca/index.html
  python3 scripts/ca-substitutions.py --all
"""
import sys
import re
from pathlib import Path

# Ordered list of substitutions. Each is (find, replace).
# Order matters when one rule's output would match another's input.
SUBS = [
    # ---- Partial includes ----
    ('{{> partials/util-bar-us }}', '{{> partials/util-bar-ca }}'),
    ('{{> partials/nav-us }}', '{{> partials/nav-ca }}'),
    ('{{> partials/footer-us }}', '{{> partials/footer-ca }}'),

    # ---- Internal link swaps: /us/ → /ca/ ----
    ('href="/us/', 'href="/ca/'),
    ('href="/us"', 'href="/ca"'),

    # ---- hreflang ----
    ('href="https://medmehealth.com/" />\n<link rel="alternate" hreflang="en-ca"',
     'href="https://medmehealth.com/us/" />\n<link rel="alternate" hreflang="en-ca"'),
    ('hreflang="x-default" href="https://medmehealth.com/"',
     'hreflang="x-default" href="https://medmehealth.com/ca/"'),

    # ---- HTML lang ----
    ('<html lang="en-US">', '<html lang="en-CA">'),

    # ---- Title + meta ----
    ('MedMe Pharmacy EHR + Medical Billing',
     'MedMe Care Platform for Canadian Pharmacy'),
    ('MedMe US homepage', 'MedMe Canada homepage'),
    ('North America&rsquo;s most-deployed clinical pharmacy platform.',
     '4,500+ Canadian pharmacies. One workflow for every clinical service.'),
    ('North America\'s most-deployed clinical pharmacy platform.',
     "4,500+ Canadian pharmacies. One workflow for every clinical service."),

    # ---- Service / billing terminology ----
    # Hero copy
    ('From appointment to paid claim,<br>in one pharmacy-built workflow.',
     'Scheduled, consulted, documented &mdash;<br>in one pharmacy-built workflow.'),
    ('The pharmacy-specific EHR that turns every clinical encounter into a clean Medicare Part B claim &mdash; so pharmacists get paid for the work they do.',
     'The pharmacy-specific platform that turns every clinical encounter into a documented, billable service &mdash; so Canadian pharmacists get recognized for the work they do.'),
    ('clean Medicare Part B claim', 'documented, reimbursable service'),
    ('Medicare Part B', 'provincial billing'),
    ('Part B verified', 'Service verified'),
    ('Medicare claim', 'provincial billing'),

    # Specific phrases
    ('CPT / HCPCS', 'Provincial PIN'),
    ('CPT/HCPCS', 'Provincial PIN'),
    ('CCM follow-up', 'MedsCheck follow-up'),
    ('CCM (20+ min)', 'MedsCheck Annual'),
    ('RHC / FQHC visit', 'Minor ailment consult'),
    ('MTM add', 'Smoking-cessation add'),
    ('99490', 'MC-01'),
    ('G0511', 'MA-12'),
    ('99607', 'SC-03'),
    ('99211', 'PT-04'),
    ('CCM', 'MedsCheck'),
    ('MTM', 'Med review'),
    ('RHC', 'Rural'),
    ('CMS', 'Health Canada'),

    # Tabs (Medical Billing must go on CA — replace with Patient Concierge)
    ('data-tab="billing"', 'data-tab="patient-concierge"'),
    ('Medical Billing</button>', 'Patient Concierge</button>'),
    # The pane content for Medical Billing — we'll still keep the markup
    # because removing it would break the tab cycle; just relabel.
    ('data-pane="billing"', 'data-pane="patient-concierge"'),

    # ---- Stats ----
    ('4,500+ pharmacies', '4,500+ Canadian pharmacies'),
    ('US pharmacy', 'Canadian pharmacy'),
    ('US-based community pharmacies', 'Canadian community pharmacies'),
    ('Trusted by US pharmacy leaders', 'Trusted by Canadian pharmacy leaders'),
    ('From single-store independents to top-100 chains',
     'From single-store independents to national chains'),

    # ---- Customer logos / names ----
    # The trust marquee uses ASCII logos — swap a few to Canadian names.
    ('CVS Health', 'Shoppers Drug Mart'),
    ('Walgreens', 'Pharmasave'),
    ('Walmart Pharmacy', 'Sobeys'),
    ('Rite Aid', 'Loblaw'),
    ('Publix Pharmacy', 'Jean Coutu'),
    ('Albertsons', 'Whole Health'),
    ('Kroger', 'IDA / Guardian'),
    ('COSTCO', 'Costco'),

    # ---- Customer story names ----
    ('Heritage Rx', 'Whole Health Pharmacy'),
    ('Patel Family Pharmacy', 'Family Care Pharmacy'),
    ('Sunny Pharmacy', 'Wellness Pharmacy'),

    # ---- PMS systems ----
    ('PioneerRx, BestRx, McKesson', 'Kroll, Fillware, BD, Telus'),
    ('PioneerRx', 'Kroll'),
    ('BestRx', 'Fillware'),
    ('McKesson', 'BD Pharmacy Management'),
    ('Computer-Rx', 'Telus PHS'),
    ('Liberty Software', 'NRx'),

    # ---- Stats / Numbers (rough Canadian equivalents) ----
    ('$48M+', '4.2M+ services'),
    ('$50B over 10 years', '$200M+ in unbilled clinical work annually'),
    ('Rural Health Transformation Program', 'Provincial scope expansion'),
    ('RHTP', 'Provincial scope'),
    ('Part B revenue', 'clinical service revenue'),
    ('Part B', 'provincial program'),

    # ---- Geo / Address ----
    ('Indiana operator', 'Ontario operator'),
    ('IN)', 'ON)'),
    (', IN ', ', ON '),
    ('Los Angeles, CA', 'Toronto, ON'),
    ('5900 6th Street', '175 Bloor Street East'),

    # ---- Sections / Headings ----
    ('A pharmacy-specific EHR', 'A pharmacy-specific platform'),
    ('Pharmacy EHR + Medical Billing', 'MedMe Care Platform'),
    ('Pharmacy EHR', 'MedMe Care Platform'),
    ('end-to-end pharmacy EHR', 'end-to-end pharmacy platform'),

    # Platform tile (Medical Billing card on home) — relabel card title
    ('Medical Billing</h3>', 'Patient Concierge</h3>'),
    ('Convert every documented encounter into a clean Medicare Part B claim',
     'Triage inbound questions, follow up on appointments, and route MedsCheck-eligible patients to the right slot'),

    # ---- A day in the life (patient journey) ----
    ('99490 + G0511 auto-suggest. Claim submits to Medicare in under a minute.',
     'Service auto-codes for provincial billing. Submission flows directly to your PMS.'),
    ('Medicare Part B</span>', 'Provincial billing</span>'),

    # ---- Stats section ----
    ('Per pharmacy reimbursement unlocked',
     'Annual clinical service revenue unlocked'),
    ('hospitals saved per pharmacy per year',
     'in-pharmacy services delivered per quarter'),

    # ---- Footer / About ----
    ('US community pharmacy', 'Canadian community pharmacy'),
    ('Toronto, ON', 'Toronto, ON'),  # no-op kept for grep verification
]


def transform(text):
    """Apply substitutions in order."""
    for find, replace in SUBS:
        text = text.replace(find, replace)
    return text


def process_file(path):
    p = Path(path)
    if not p.exists():
        print(f"  ! missing: {path}")
        return
    original = p.read_text(encoding="utf-8")
    transformed = transform(original)
    if original == transformed:
        print(f"  - no changes: {path}")
    else:
        p.write_text(transformed, encoding="utf-8")
        n_changed = sum(1 for f, r in SUBS if f in original)
        print(f"  ✓ {n_changed} rules applied: {path}")


def main(args):
    if args and args[0] == "--all":
        ca = Path(__file__).resolve().parent.parent / "src" / "ca"
        for p in ca.rglob("*.html"):
            process_file(p)
        return
    for arg in args:
        process_file(arg)


if __name__ == "__main__":
    main(sys.argv[1:])
