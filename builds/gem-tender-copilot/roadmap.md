# GeM Tender Copilot — Roadmap and Validation Plan

This roadmap prioritizes reducing real bid-review effort without making unsafe claims. Stages are gates: proceed only when the previous stage yields evidence that the workflow is useful and the output can be checked.

## Phase 0 — Discovery Before Coding

**Objective:** prove the problem is frequent and painful for a specific initial user group.

Activities:
- Interview a small group of MSME sellers, bid executives, and tender consultants.
- Ask them to walk through a recent tender review with a document pack.
- Observe how they currently record eligibility, evidence, deadlines, amendments, and review sign-off.
- Learn which tender categories, document languages, scan qualities, and evidence formats appear most often.
- Ask what kinds of mistakes or omissions lead to rework, lost time, disqualification risk, or missed opportunities.
- Collect only documents the participants are permitted to share; define safe handling and deletion before collecting samples.
- Review current GeM terms, official notices, procurement policy, and applicable data obligations.
- Map alternative solutions: manual spreadsheets, consultants, tender aggregators, document-review tools, internal checklists. Do not claim the product has no competitors before this research.

**Gate to proceed:** one narrow segment, repeated pain confirmed by real workflows, access to a permitted evaluation corpus, and a clear workflow for human review.

## Phase 1 — PDF Understanding Prototype

**Objective:** show that a tender PDF can become a structured, source-linked requirement list.

Build:
- Secure local or private test upload.
- PDF native-text extraction.
- OCR fallback and page quality warnings.
- Page-linked chunking and table/heading preservation.
- Structured requirement extraction with clause quotes and source page.
- Schema validation and citation existence checks.
- Basic review UI where the user can correct category, threshold, or wording.

Do not build a readiness score or business account system before the requirement extraction is measurable. The first meaningful demonstration is: "Here are the important tender requirements, and click each one to verify the source page."

**Gate:** an adjudicated test set demonstrates acceptable extraction coverage for the initial tender type, including critical clauses and bad scans; reviewers can locate the original text for each finding.

## Phase 2 — Seller Profile and Evidence Linking

**Objective:** connect tender requirements to real seller documents.

Build:
- Seller profile with legal entity and business/product categories.
- Private evidence document vault.
- Evidence metadata extraction (periods, values, expiry, issuer, entity name).
- Manual evidence-to-requirement linking.
- Rule engine for selected high-value checks: numeric thresholds, financial years, project counts where comparable projects have been manually confirmed, certificate presence/expiry, and mandatory forms.
- Multi-state statuses separating evidence absent, potential mismatch, and confirmed rule failure.
- Human corrections and review history.

Start with a small set of rules that can be tested precisely. Do not aim to automate every kind of eligibility clause at once.

**Gate:** rules produce transparent calculations and no known critical false-supported result on the release benchmark; sellers can understand and correct mismatches.

## Phase 3 — Report, Calendar, and Corrigenda

**Objective:** make analysis actionable, not just a list of extracted text.

Build:
- Executive report and priority risk register.
- Mandatory-document checklist.
- Technical compliance matrix.
- Deadline/calendar extraction and explicit verification flag.
- Manual amendment uploads and version comparison.
- Stale-report warning when a new tender version is added.
- Export to PDF and CSV/XLSX with page citations, document versions, and caveats.

**Gate:** the report saves review time in observed workflows and high-impact date/threshold changes are consistently caught or visibly marked for verification.

## Phase 4 — Closed Pilot

**Objective:** validate usability, reliability, and willingness to pay with a small number of real users.

Before pilot:
- Review security and data privacy.
- Document provider terms, retention, deletion, and processing regions.
- Obtain user consent/authorization for their files.
- Establish support, incident, and deletion procedures.
- Train users to treat output as preliminary and verify against official documents.
- Create a process for reporting incorrect extraction and correcting the evidence record.

During pilot, measure:
- Time spent before/after.
- Critical requirement recall and false-supported findings.
- Percentage of statuses accepted or changed by reviewers.
- User task completion, repeat usage, and confidence calibration.
- Cost per analysis and operational support burden.
- Which document types fail and why.

**Gate:** users receive measurable value, high-risk errors are understood, and the product can be operated without uncontrolled data or cost exposure.

## Phase 5 — Improve Product Reliability

Potential work, prioritized using pilot evidence:
- Improve OCR for the languages and scan quality actually encountered.
- Improve table, footnote, and annexure extraction.
- Add reusable evidence profiles and document expiry reminders.
- Add collaboration roles, assignment, and review sign-off.
- Add more tender categories only with separate validation sets.
- Improve report comparison and deadline reminders.
- Add monitoring dashboards for failure stage, processing cost, and extraction regression.

## Phase 6 — Integrations and Scale (Only If Validated)

Possible later capabilities:
- Permitted tender discovery/feed integration.
- Monitoring of official tender changes/corrigenda where an authorized, reliable method exists.
- Consultant workflows across multiple companies.
- Enterprise SSO, configurable retention, and contractual/data-residency options.
- Billing/subscriptions and audit exports.
- Integration with existing document or procurement management systems.

Do not launch a crawler, automated GeM login, or bid-submission bot by default. Establish current portal rules, official interface availability, security requirements, and user authorization before any integration. The first version works from files the seller intentionally uploads.

## Suggested Milestone Sequence

The duration depends on team size, skill, model/vendor choices, and the quality of sample PDFs. A focused solo-developer prototype might take several weeks; a pilot-ready service can take significantly longer. Do not promise a fixed launch date until discovery and a first benchmark establish the true complexity.

1. Problem interviews and permitted document sampling.
2. Upload-to-requirement extraction proof of concept.
3. Citation verification and extraction evaluation harness.
4. Evidence vault and typed evidence facts.
5. Deterministic rule engine and review UI.
6. Calendar, manual corrigendum comparison, and export.
7. Security review and closed pilot.
8. Iterate on measured errors, usability, and economics.

## Product Experiments to Run

### Experiment A — Report usefulness
Give a bid manager a source-linked report for a tender they already reviewed. Compare the report to their manually prepared checklist. Track omitted requirements, false findings, and time spent verifying each item.

### Experiment B — Evidence reuse
Ask the seller to upload a small company-document pack once and reuse it for two tenders. Measure whether the evidence profile saves effort without confusing document validity, period, or legal-entity ownership.

### Experiment C — Corrigendum detection
Take a tender version and a later amendment. Ask a reviewer to identify every material change. Compare with the system's diff and track missed changes that affect deadlines, eligibility, or technical compliance.

### Experiment D — Willingness to pay
Test workflow value before selecting a pricing model. Possible models to investigate include per-tender analysis, a monthly small-business plan, or a consultant workspace. Do not publish pricing before estimating cost-to-serve and validating buyer preference.

## Business Model Hypotheses

Potential models:
- Pay-per-tender report for occasional sellers.
- Monthly plan for sellers reviewing tenders regularly.
- Multi-client workspace for tender consultants.
- Larger team plan with roles, audit trail, and retention controls.

Important pricing variables include document length, OCR usage, LLM usage, analysis retries, support, expert review, storage retention, and export/integration needs. Model margins using measured processing costs rather than assuming each tender costs the same.

## Main Risks and Mitigations

| Risk | Why it matters | Mitigation |
|---|---|---|
| Critical clause missed | User may believe a bid is safer than it is | High critical-requirement recall gate, source links, human review, visible parse warnings |
| Incorrect interpretation | Tender language can be conditional or category-specific | Preserve exact context, allow "needs review", involve procurement expertise |
| Bad scanned PDF | OCR may distort amounts, dates, negation, and identifiers | Per-page OCR quality, original page view, review queue |
| Corrigendum omitted | The analysis may be based on a stale document | Explicit latest-known version warning; seller checks official source; version comparison |
| Sensitive company documents exposed | Trust and legal harm | Tenant isolation, secure storage, limited provider processing, deletion, audit trails |
| Policy rules become stale | Exemptions or procurement guidance can change | Version policy rules; link official sources; review rule updates; never assume universal exemptions |
| Low willingness to pay | Manual alternatives may be sufficient for some users | Discovery interviews, observed workflow tests, paid pilot signal before scaling |
| Variable document-processing cost | Long/scanned PDFs can erode margins | Page limits, provider abstraction, batching, caching where safe, per-job metering |
| Feature scope explodes | Tender types and requirements vary | Pick one initial segment; expand only with benchmark coverage |
| User over-trusts an AI summary | High-stakes procurement decision | Explainability, source evidence, language that avoids guarantees, final human decision |

## Open Decisions / Decision Log

Maintain decisions in this file or as dated issues:
- Initial tender category and buyer/seller segment.
- Initial language coverage.
- PDF page/size limits.
- Which document types can be reused in the company vault.
- Which OCR/LLM provider fits data policy, accuracy, and cost.
- What review level is required for critical clauses.
- Data retention and deletion period.
- Pilot accuracy thresholds and benchmark ownership.
- Pricing and support model.
- When/if permitted official tender discovery or change feeds are feasible.

Any change that affects user-visible risk status should have a written rationale and a regression evaluation.
