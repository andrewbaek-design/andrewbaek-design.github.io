---
title: "HIPAA at MedMe, MedMe Health"
description: "MedMe Health HIPAA Compliance. Business Associate Agreement, Security Rule mapping, breach notification, and audit rights for US pharmacy customers."
kicker: "Trust"
headline: 'HIPAA at <span class="accent">MedMe</span>.'
lede: |
  As a Business Associate to US pharmacy customers, MedMe handles Protected Health Information ("PHI") under HIPAA's Privacy, Security, and Breach Notification Rules. Last reviewed: April 2026.
cta_primary_label: "Request our BAA →"
cta_primary_href: "mailto:hipaa@medmehealth.com"
cta_secondary_label: "Security overview"
cta_secondary_href: "/legal/security"
---

## Business Associate Agreement

MedMe executes a HIPAA-compliant **Business Associate Agreement (BAA)** with every US pharmacy customer. The BAA is included as part of our standard onboarding package and is signed before any Protected Health Information is created, received, maintained, or transmitted by MedMe on the customer's behalf. A redlined version of our standard BAA is available on request from [hipaa@medmehealth.com](mailto:hipaa@medmehealth.com).

Our BAA addresses each requirement of 45 CFR § 164.504(e), including permitted uses and disclosures, safeguard obligations, sub-contractor flow-down, breach notification timelines, and obligations on termination.

## Our role as a Business Associate

MedMe acts as a Business Associate to our pharmacy customers (who are Covered Entities under HIPAA). We process PHI only as necessary to provide the contracted services and only for purposes documented in the customer's instructions or in the BAA. We do not use PHI for our own commercial purposes, do not disclose PHI to third parties except to qualified sub-processors under their own BAAs, and do not de-identify PHI for sale or marketing.

Our employees and contractors with access to PHI are subject to background checks, sign confidentiality agreements, complete annual HIPAA training, and operate under the principle of least privilege.

## What we cover, administrative, physical, and technical safeguards

Below is a summary of how MedMe addresses the HIPAA Security Rule's required and addressable implementation specifications. This is not a substitute for the full BAA or our SOC 2 / HITRUST attestations, which are available under NDA.

### Administrative safeguards

- **Security management process**, annual risk analysis aligned to NIST 800-30; risk register reviewed quarterly by the Security Steering Committee.
- **Workforce security**, role-based access, documented onboarding/offboarding procedures, mandatory annual training.
- **Information access management**, least-privilege defaults, just-in-time access for engineering, customer-tenant isolation enforced at multiple layers.
- **Contingency plan**, documented business-continuity and disaster-recovery plans, tested annually; data-backup, recovery, and emergency-mode procedures.
- **Evaluation**, annual SOC 2 Type II audit; HITRUST CSF r2 certification refreshed annually.

### Physical safeguards

- **Facility access controls**, production infrastructure hosted in AWS data centers (us-east-1) with 24×7 staffing, biometric access, and SOC 2 / ISO 27001 attestation. MedMe corporate offices use badge access, visitor logging, and clean-desk policies.
- **Workstation security**, full-disk encryption, EDR, and automated patching mandatory on all employee devices. No PHI on employee endpoints under normal operation.
- **Device &amp; media controls**, secure-disposal procedures for retired hardware; media inventory tracked.

### Technical safeguards

- **Access control**, unique user IDs, automatic logoff, encryption / decryption with AWS KMS.
- **Audit controls**, tamper-evident logs of PHI access; logs retained 7 years.
- **Integrity controls**, checksum verification, immutable backups, write-once log storage.
- **Person or entity authentication**, SSO + MFA for administrative access; password complexity and rotation policies for non-SSO accounts.
- **Transmission security**, TLS 1.3 with strong cipher suites for data in transit; integrity controls on all API requests.

## Breach notification commitments

If MedMe discovers a breach of unsecured PHI, we will notify the affected Covered Entity without unreasonable delay and in any case no later than **30 days** from discovery, significantly faster than the 60-day statutory maximum under the HIPAA Breach Notification Rule. Our notification will include, to the extent known, the identification of each individual whose PHI was breached, the nature of the breach, the date(s) of breach and discovery, the types of PHI involved, and steps the individual should take to protect themselves.

## Audit rights

Covered Entity customers have the right, on reasonable advance notice, to:

- Receive copies of MedMe's most recent SOC 2 Type II report, HITRUST certificate, penetration-test summary, and policies relevant to PHI handling;
- Conduct an audit of MedMe's compliance with the BAA, either directly or through an independent third-party auditor under NDA, no more than once per twelve-month period;
- Receive cooperation from MedMe in any HHS-OCR investigation, audit, or enforcement action.

## HIPAA Security Rule mapping

The table below maps key HIPAA Security Rule citations to corresponding MedMe controls. This is a summary; the BAA and our internal policy library document each control more fully.

<div style="overflow-x:auto; margin: 2rem 0;">
<table class="table">
<thead>
<tr>
<th>Citation</th>
<th>HIPAA requirement</th>
<th>MedMe control</th>
</tr>
</thead>
<tbody>
<tr><td>164.308(a)(1)(ii)(A)</td><td>Risk analysis</td><td>Annual NIST 800-30 risk analysis with quarterly register reviews</td></tr>
<tr><td>164.308(a)(1)(ii)(B)</td><td>Risk management</td><td>Documented mitigation plans tracked to closure; SLA by severity</td></tr>
<tr><td>164.308(a)(3)(ii)(A)</td><td>Authorization &amp; supervision</td><td>RBAC + approval workflow for production access; manager review</td></tr>
<tr><td>164.308(a)(4)(ii)(B)</td><td>Access authorization</td><td>Tenant isolation; least-privilege defaults; JIT escalation</td></tr>
<tr><td>164.308(a)(5)(ii)(B)</td><td>Protection from malware</td><td>EDR on all endpoints; SIEM with anomaly alerting</td></tr>
<tr><td>164.308(a)(6)(ii)</td><td>Response &amp; reporting</td><td>24×7 IR rotation; quarterly tabletop exercises; documented runbooks</td></tr>
<tr><td>164.308(a)(7)(ii)(A)</td><td>Data backup plan</td><td>Encrypted, cross-AZ snapshot backups every 15 min; restoration tested</td></tr>
<tr><td>164.310(a)(1)</td><td>Facility access controls</td><td>AWS-managed data centers; corporate badge access + visitor log</td></tr>
<tr><td>164.310(d)(2)(i)</td><td>Disposal</td><td>NIST SP 800-88 media sanitization; destruction certificates retained</td></tr>
<tr><td>164.312(a)(1)</td><td>Access control</td><td>Unique IDs; SSO + MFA; auto-logoff; KMS-managed encryption</td></tr>
<tr><td>164.312(b)</td><td>Audit controls</td><td>Tamper-evident PHI access logs; 7-year retention</td></tr>
<tr><td>164.312(c)(1)</td><td>Integrity</td><td>Checksums on stored objects; immutable backups; write-once logs</td></tr>
<tr><td>164.312(d)</td><td>Person or entity authentication</td><td>SSO + MFA; complexity / rotation for any non-SSO accounts</td></tr>
<tr><td>164.312(e)(1)</td><td>Transmission security</td><td>TLS 1.3 in transit; cipher-suite hardening; integrity checks</td></tr>
<tr><td>164.314(a)(1)</td><td>BAA with sub-contractors</td><td>BAA flow-down with every sub-processor handling PHI</td></tr>
<tr><td>164.404 / 164.410</td><td>Breach notification</td><td>30-day notification commitment; full content per § 164.404(c)</td></tr>
</tbody>
</table>
</div>

## HIPAA contact

For HIPAA-related questions, including BAA negotiation, audit requests, breach notifications, or to report a concern, please contact:

<p>
<strong>MedMe Health, Inc., HIPAA Officer</strong><br />
Email: <a href="mailto:hipaa@medmehealth.com">hipaa@medmehealth.com</a><br />
Mailing address: 200 State Street, Boston, MA 02109, United States
</p>

For complaints, US-based individuals also have the right to contact the US Department of Health and Human Services, Office for Civil Rights (HHS-OCR), at [hhs.gov/hipaa/filing-a-complaint](https://www.hhs.gov/hipaa/filing-a-complaint/).
