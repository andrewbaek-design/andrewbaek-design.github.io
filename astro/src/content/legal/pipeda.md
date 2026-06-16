---
title: "Canadian Privacy at MedMe, MedMe Health"
description: "MedMe Health PIPEDA and provincial privacy compliance, PHIPA (ON), FIPPA / loi 25 (QC), PHIA (NS / MB / NL), HIA (AB), BC PIPA, ATIPPA (YT/NT/NU). Canadian data residency and pharmacy-act obligations."
kicker: "Trust"
headline: 'Canadian Privacy at <span class="accent">MedMe</span>.'
lede: |
  PIPEDA, provincial privacy laws, and pharmacy-act obligations from coast to coast, addressed at the platform layer so our pharmacy customers can stay focused on care. Last reviewed: April 2026.
cta_primary_label: "Contact our Privacy Officer →"
cta_primary_href: "mailto:privacy@medmehealth.com"
cta_secondary_label: "Security overview"
cta_secondary_href: "/legal/security"
---

## The PIPEDA principles, addressed

The **Personal Information Protection and Electronic Documents Act (PIPEDA)** sets out ten Fair Information Principles. MedMe addresses each principle directly in our platform design, contractual commitments, and operational policies. As a service provider acting on behalf of a pharmacy custodian, we apply these obligations both to our own collection of personal information (e.g., from prospective customers, job applicants, pharmacist users) and to information we process on a customer's behalf.

1. **Accountability.** MedMe has a designated Privacy Officer reachable at [privacy@medmehealth.com](mailto:privacy@medmehealth.com), supported by a cross-functional Privacy Council that meets monthly.
2. **Identifying purposes.** Purposes are identified at or before collection, both on our public site and within our pharmacist-facing product. Service-provider purposes are documented in our contracts with pharmacy customers.
3. **Consent.** We obtain meaningful consent appropriate to the sensitivity of the information. For health information processed on behalf of a custodian, consent is obtained by the custodian in accordance with applicable provincial law.
4. **Limiting collection.** We collect only what is necessary for the identified purpose. Optional fields are clearly marked and never used to gate service delivery.
5. **Limiting use, disclosure, and retention.** We use information only for the purposes consented to, retain it only as long as needed, and delete or de-identify it on schedule.
6. **Accuracy.** Pharmacist users can update their profile at any time. Pharmacy customers control accuracy of patient data through the platform's editing controls.
7. **Safeguards.** Administrative, physical, and technical controls aligned to SOC 2 Type II and HITRUST CSF r2. See our [Security](/legal/security) page.
8. **Openness.** Our privacy policies are publicly available and written in plain language.
9. **Individual access.** Individuals may request access to their personal information by emailing [privacy@medmehealth.com](mailto:privacy@medmehealth.com); for patient information held on behalf of a pharmacy, requests are routed to the pharmacy custodian.
10. **Challenging compliance.** Concerns and complaints can be raised with our Privacy Officer; we acknowledge within 5 business days and respond fully within 30 days.

## Provincial privacy laws covered

MedMe customers operate under a range of provincial and territorial privacy regimes. We design the platform so that, regardless of the customer's home province, the applicable law is honored at the configuration and policy layer. The table below summarizes the laws we map against in the course of onboarding, configuration, and audit.

<div style="overflow-x:auto; margin: 2rem 0;">
<table class="table">
<thead>
<tr>
<th>Jurisdiction</th>
<th>Statute</th>
<th>Scope MedMe addresses</th>
</tr>
</thead>
<tbody>
<tr><td>Federal</td><td>PIPEDA</td><td>Private-sector personal information; cross-border transfers</td></tr>
<tr><td>Ontario (ON)</td><td>PHIPA, Personal Health Information Protection Act</td><td>PHI processing under custodian instruction; agent obligations</td></tr>
<tr><td>Quebec (QC)</td><td>Loi 25 (formerly FIPPA / Act 64)</td><td>Privacy-by-default; cross-border impact assessments; deletion rights</td></tr>
<tr><td>Nova Scotia (NS)</td><td>PHIA, Personal Health Information Act (NS)</td><td>Custodian instructions; security of PHI; breach notification</td></tr>
<tr><td>Manitoba (MB)</td><td>PHIA, Personal Health Information Act (MB)</td><td>Information Manager obligations; access &amp; correction</td></tr>
<tr><td>Alberta (AB)</td><td>HIA, Health Information Act</td><td>Custodian / affiliate obligations; PIA support</td></tr>
<tr><td>Newfoundland &amp; Labrador (NL)</td><td>PHIA, Personal Health Information Act (NL)</td><td>Information Manager Agreement; reporting to OIPC NL</td></tr>
<tr><td>British Columbia (BC)</td><td>PIPA, Personal Information Protection Act (BC)</td><td>Private-sector personal information; service-provider obligations</td></tr>
<tr><td>Saskatchewan (SK)</td><td>HIPA, Health Information Protection Act</td><td>Trustee instructions; access &amp; correction; breach reporting</td></tr>
<tr><td>New Brunswick (NB)</td><td>PHIPAA, Personal Health Information Privacy and Access Act</td><td>Information Manager obligations; PIA support</td></tr>
<tr><td>Prince Edward Island (PE)</td><td>HIA, Health Information Act</td><td>Custodian agency relationships; breach reporting</td></tr>
<tr><td>Yukon (YT) / NWT / Nunavut</td><td>ATIPPA &amp; territorial health-info laws</td><td>Public-body custodian instructions where applicable</td></tr>
</tbody>
</table>
</div>

## Data residency

For Canadian pharmacy customers, all production environments are hosted in **AWS ca-central-1 (Montréal)**. Patient health information processed on behalf of Canadian custodians does not leave Canada in the course of normal operation. Disaster recovery uses additional AWS Canadian availability zones; we do not replicate Canadian PHI to US regions.

Some sub-processors may be headquartered outside of Canada. We disclose these in our public sub-processor list, conduct privacy impact assessments where required (especially under Quebec's Loi 25), and execute information-management or data-processing agreements with each.

## Pharmacy-specific obligations under provincial pharmacy acts

In addition to general privacy statutes, Canadian pharmacies operate under provincial pharmacy acts and the standards set by their provincial colleges (e.g., the Ontario College of Pharmacists, the Ordre des pharmaciens du Québec, the College of Pharmacists of British Columbia). MedMe's product and configuration support these obligations, including:

- Documentation requirements for clinical services (medication reviews, minor ailments, immunizations);
- Record-retention obligations specific to each province (typically 10 years from last interaction, or 10 years past age of majority for minors);
- Provincial billing-routing requirements for OHIP, RAMQ, ASEBP, MSP, and equivalent payers;
- Quality-assurance and audit-trail requirements expected by provincial regulators;
- Specific consent forms and patient acknowledgements where mandated.

## Our role as a service provider

For pharmacy customers, MedMe acts as a service provider, agent, affiliate, or Information Manager (the term varies by statute) to a custodian or trustee under provincial law. We process personal health information only as directed by the custodian, only for the purposes set out in our Information Management Agreement, and only with safeguards equivalent to or greater than those required of the custodian themselves. We do not use PHI for our own marketing, research, or commercial purposes.

## Breach notification

MedMe will notify a Canadian customer of a confirmed privacy breach without unreasonable delay and in any event within **72 hours** of discovery. Where mandated by provincial law (e.g., PHIPA in Ontario), the customer is responsible for notifying the Information and Privacy Commissioner; MedMe will provide all reasonable cooperation, documentation, and forensic detail. We retain breach records for at least 24 months in accordance with PIPEDA's recordkeeping requirements.

## Subject access &amp; correction rights

Individuals (including patients of MedMe-using pharmacies) generally have the right to request access to, and correction of, their personal information. For information that MedMe controls directly (e.g., a pharmacist user account), requests can be made to [privacy@medmehealth.com](mailto:privacy@medmehealth.com). For patient information held on behalf of a pharmacy custodian, requests should be directed to the pharmacy; MedMe will assist the pharmacy in responding.

## Provincial privacy commissioner contacts

Individuals who feel their privacy concerns have not been adequately addressed may contact the relevant privacy oversight authority directly.

<div style="overflow-x:auto; margin: 2rem 0;">
<table class="table">
<thead>
<tr>
<th>Jurisdiction</th>
<th>Authority</th>
<th>Contact</th>
</tr>
</thead>
<tbody>
<tr><td>Federal</td><td>Office of the Privacy Commissioner of Canada (OPC)</td><td>priv.gc.ca · 1-800-282-1376</td></tr>
<tr><td>Ontario</td><td>Information and Privacy Commissioner of Ontario (IPC)</td><td>ipc.on.ca · 1-800-387-0073</td></tr>
<tr><td>Quebec</td><td>Commission d'accès à l'information (CAI)</td><td>cai.gouv.qc.ca · 1-888-528-7741</td></tr>
<tr><td>British Columbia</td><td>Office of the Information and Privacy Commissioner for BC</td><td>oipc.bc.ca · 1-800-663-7867</td></tr>
<tr><td>Alberta</td><td>Office of the Information and Privacy Commissioner of Alberta</td><td>oipc.ab.ca · 1-888-878-4044</td></tr>
<tr><td>Manitoba</td><td>Manitoba Ombudsman / IPC</td><td>ombudsman.mb.ca · 1-800-665-0531</td></tr>
<tr><td>Saskatchewan</td><td>Office of the Saskatchewan Information &amp; Privacy Commissioner</td><td>oipc.sk.ca · 1-877-748-2298</td></tr>
<tr><td>Nova Scotia</td><td>Office of the Information &amp; Privacy Commissioner for NS</td><td>foipop.ns.ca · 1-866-243-1564</td></tr>
<tr><td>New Brunswick</td><td>Office of the Access to Information &amp; Privacy Commissioner</td><td>info-priv-nb.ca · 1-877-755-2811</td></tr>
<tr><td>Newfoundland &amp; Labrador</td><td>Office of the Information &amp; Privacy Commissioner of NL</td><td>oipc.nl.ca · 1-877-729-6309</td></tr>
<tr><td>Prince Edward Island</td><td>Office of the Information &amp; Privacy Commissioner of PEI</td><td>oipc.pe.ca · 1-902-368-4099</td></tr>
<tr><td>Yukon</td><td>Office of the Information &amp; Privacy Commissioner of Yukon</td><td>yukonombudsman.ca · 1-800-661-0408</td></tr>
<tr><td>NWT &amp; Nunavut</td><td>Information &amp; Privacy Commissioner of NWT and NU</td><td>atipp-nt.ca · 1-867-669-0976</td></tr>
</tbody>
</table>
</div>

## Privacy contact

<p>
<strong>MedMe Health, Inc., Privacy Officer (Canada)</strong><br />
Email: <a href="mailto:privacy@medmehealth.com">privacy@medmehealth.com</a><br />
Mailing address: 100 King Street West, Suite 1300, Toronto, ON M5X 1A9, Canada
</p>
