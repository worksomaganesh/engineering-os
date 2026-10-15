# GeM Tender Copilot — Product Requirements

This document turns the project idea into requirements that can guide UX design, implementation, and acceptance testing.

## 1. Product Statement

For Indian MSME sellers who need to evaluate a government tender, GeM Tender Copilot converts tender documents and seller evidence into an explainable bid-readiness workspace. It identifies requirements, links each finding to the source page, compares the requirements against available evidence, highlights unresolved risks, tracks deadlines and manually provided corrigenda, and helps the seller prepare a final human-reviewed checklist.

**It must not promise an award, replace the official GeM workflow, or issue an unreviewable legal eligibility verdict.**

## 2. User Personas and Jobs to Be Done

### Persona A — Owner of an MSME

- Handles sales and operations, possibly without a dedicated bid-compliance department.
- Needs a quick, reliable first-pass answer to "Is this tender worth spending time on?"
- Needs to know which documents to collect from finance, operations, or the OEM.
- Wants obvious blockers surfaced early.

### Persona B — Tender executive / bid manager

- Reviews multiple tender packs and seller evidence.
- Needs source citations, exact clause language, clear status changes, and a repeatable workflow.
- Wants less manual copying into spreadsheets and fewer missed requirements.

### Persona C — Technical / finance evidence contributor

- Supplies product datasheets, certificates, audited figures, past orders, completion certificates, or declarations.
- Needs to know the exact proof requested and where it will be used.

### Core jobs
1. Understand the tender requirements without losing the clause context.
2. See which seller evidence actually supports each requirement.
3. Distinguish "not supplied" from "fails the tender threshold."
4. Identify hard blockers and unresolved questions before bid preparation.
5. Notice what changed when a corrigendum arrives.
6. Delegate actions and track completion before the deadline.

## 3. Main User Journey

1. **Create workspace:** seller creates a workspace and enters basic company details, business category, relevant registrations, products/services, and optional MSE/startup/OEM claims.
2. **Upload tender:** upload a PDF or, in a later phase, supported document formats. System validates the file and creates an immutable original record.
3. **Review parsing:** show page count, whether each page yielded text, low-OCR-quality warnings, and extraction completeness.
4. **Review extracted tender profile:** title/bid ID if found, buyer, category, dates, estimated quantities/value if present, delivery location, and document/version date. Unknown fields remain unknown.
5. **Upload seller evidence:** add evidence files with document types and optional metadata. The system must not infer an unverified certificate is valid simply because it is present.
6. **Review requirement matrix:** each row shows requirement, type, exact clause, page/section, severity, status, linked proof, explanation, and next action.
7. **Resolve uncertainty:** user confirms facts, selects alternative evidence, marks a finding as reviewed, or records why a requirement is not applicable.
8. **Add corrigendum:** upload a subsequent notice/file; system compares versions and flags changed clauses and dates for human confirmation.
9. **Prepare report:** export the matrix, missing-document checklist, risk register, date schedule, and analysis metadata.
10. **Final human decision:** seller checks the official GeM tender page and current documents before deciding whether and how to submit.

## 4. Required Report Sections

### A. Executive summary
- Tender reference and buyer, if clearly extracted.
- Tender document version and latest uploaded corrigendum known to the workspace.
- Key dates and any date-extraction warning.
- Counts of satisfied-with-evidence, missing-evidence, potential-mismatch, and review-required items.
- Top high-severity blockers.
- Data-quality warnings, including OCR and unresolved contradictions.
- Clear statement that this is a preliminary analysis, not an official decision.

### B. Eligibility and qualification matrix
Each row should contain:
- Requirement ID and category.
- Exact tender text or a short quote.
- Clause/section heading and page number.
- Extracted threshold and applicable condition, if any.
- Required evidence type.
- Seller evidence linked to the row.
- Result/status and explanation.
- Confidence and review state.
- Suggested next action.

### C. Mandatory-document checklist
At minimum, the extraction taxonomy should be able to recognize common categories such as:
- GST registration and PAN details.
- Udyam/MSE documentation if relevant and required.
- Audited financial statements, CA/turnover certificates, and specified financial years.
- Past purchase orders/work orders and completion/performance certificates.
- OEM authorization, dealership/distributor letters, or manufacturer credentials where required.
- Technical datasheets, product literature, test reports, or quality certificates.
- Declarations, undertakings, affidavits, bid-specific forms, signatures, stamps, and prescribed formats.
- Bid security/EMD evidence or explicitly applicable exemption documentation.
- Performance-security obligations after award, when specified.
- Any tender-specific document not included in the generic taxonomy.

This list is a starting taxonomy, not a universal mandatory checklist. Only the uploaded tender determines what is required for that bid.

### D. Disqualification-risk register
For each risk:
- The triggering clause.
- Why it matters.
- Evidence reviewed and its source.
- What is known vs unknown.
- Severity and time sensitivity.
- Affected requirement(s).
- Recommended action and reviewer decision.

Examples include an explicit turnover threshold above evidenced turnover, required project-count evidence not found, mandatory certificate absent, product specification conflict, unsigned form, expired certificate, or unresolved deadline contradiction. These must be presented as findings needing confirmation, not as a guaranteed rejection prediction.

### E. Technical compliance matrix
For each material technical specification:
- Tender specification in the tender's own units/terms.
- Seller product/service specification from a named evidence document.
- Comparison method and normalized value/unit if appropriate.
- Match, mismatch, unknown, or non-comparable result.
- Source passage on both sides.
- Any assumption the user must verify.

### F. Bid calendar
- Clarification/question deadline.
- Pre-bid meeting date/time and attendance instructions, if specified.
- Bid end date/time.
- Technical/financial opening dates when published.
- Document-specific validity dates and post-award deadlines when relevant.
- Time zone as written or explicitly normalized.
- Source page, source version, extracted text, and a confirmation flag.
- Reminder status.

A date should never be invented from a typical tender pattern. If ambiguous or absent, display "Not found / verify on official bid page." GeM's bid listing states that Global Tender Enquiry schedules and communications use IST (UTC+05:30); still preserve what the specific notice says and distinguish portal-wide convention from tender-specific wording.

### G. Corrigendum comparison
- Base document version and amendment version.
- Changed, added, deleted, and apparently unchanged clauses.
- Before/after quoted text and page/section.
- Affected requirement IDs and deadline records.
- Whether the impact is understood, uncertain, or awaiting human review.
- A warning to verify that all relevant official amendments have been uploaded.

## 5. Requirement Status Model

Do not reduce the result to a single green/red label. Use statuses such as:

| Status | Meaning |
|---|---|
| Supported / appears to meet | Current supplied evidence appears to satisfy the extracted condition; still needs appropriate review |
| Missing evidence | No supporting document has been linked; this alone does not prove that the company fails the condition |
| Potential mismatch | Supplied evidence seems inconsistent with a requirement |
| Not established | The evidence is insufficient to decide |
| Conflicting evidence | Documents, versions, or extracted values disagree |
| Not applicable — reviewable | A documented rule or condition makes it appear inapplicable; reason must be shown and may require review |
| Human verification required | Interpretation, authenticity, legal/policy application, or technical equivalence requires a qualified reviewer |
| Rejected / fails test rule | A narrowly defined and validated rule appears to fail; must show the exact source and comparison |

Prefer "appears to meet" to an absolute "eligible." For a high-severity condition, unresolved interpretation or low-quality extraction must not silently become a green status.

## 6. Requirement Taxonomy

The system should classify extracted clauses into flexible categories, including:
- Bidder identity and legal status.
- Registrations, licences, statutory obligations, and debarment declarations.
- Financial capacity, turnover, net worth, and financial years.
- Prior experience, completed projects, contract values, and performance.
- OEM/manufacturer, brand, dealership, and authorization conditions.
- Technical specifications and functional requirements.
- Quality, safety, testing, certificates, and standards.
- EMD/bid security, exemption declarations, and performance security.
- Delivery, installation, support, warranty, and service levels.
- Declarations, undertakings, signed formats, and annexures.
- Submission method, format, file requirements, and deadlines.
- Evaluation method, commercial terms, and post-award obligations.

Do not assume every tender contains every category or that one generic category definition applies identically to goods, works, and services.

## 7. Functional Requirements

### P0 — MVP must-have
- Authenticated workspace and private upload.
- PDF format checks, page-count and size limits, malware/safety scanning where supported.
- Text extraction for text-based PDFs and OCR fallback for scanned documents.
- A parse-quality screen identifying unreadable/failed pages.
- Requirement extraction using a schema with page/section provenance.
- Automated validation that every shown requirement's cited page exists and its source excerpt can be located.
- Seller profile and seller evidence vault, separated by tenant.
- Evidence-to-requirement linking.
- Deterministic checks for dates, exact numeric thresholds, financial-year coverage, required counts, and explicit yes/no conditions when the facts are sufficiently structured.
- Unknown/unresolved states instead of guessed values.
- Report screen with matrix, missing evidence, high-priority risks, dates, and suggested next actions.
- Manual upload of corrigendum files and versioned change comparison.
- User review/edit/confirm workflow and audit record.
- Export to a useful PDF/CSV/XLSX format, with sources and limitations.
- Delete/export workspace data and delete uploaded files, subject to a documented retention and backup policy.

### P1 — after validation
- Email/calendar reminders for dates the user confirms.
- Multiple company members with roles and assignments.
- Reusable templates by procurement/tender category.
- Comparison across several tenders.
- OCR language improvements and additional Indian-language support based on real documents.
- Clause library and reusable evidence types with expiry alerts.
- Integrations only where permitted and supported by official interfaces.

### P2 — later, only if users need it
- Official bid discovery or change monitoring from permitted feeds/APIs.
- Larger procurement workflow support for consultants.
- More advanced technical-equivalence rules.
- Enterprise identity, customer-managed keys, or data residency options.
- Carefully governed integrations with existing tender-management systems.

## 8. Non-Functional Requirements

- **Traceability:** every important result links to an original file, page, and quoted clause.
- **Reliability:** jobs survive transient failures and can be retried without duplicating records.
- **Tenant isolation:** one company can never access another company's files or reports.
- **Security:** protected uploads, least-privilege access, secure secrets, encryption in transit and at rest, audit logs.
- **Performance:** upload and analysis are asynchronous for large files; user sees progress and can return later.
- **Accessibility:** readable tables, keyboard navigation, clear labels, and non-color status indicators.
- **Explainability:** show why a status was assigned and which evidence influenced it.
- **Versioning:** each analysis records which tender, amendment, company evidence, rule-set, and model/provider version it used.
- **Maintainability:** extraction providers and LLM vendors can be swapped behind stable interfaces.
- **Cost control:** page/document limits, quota monitoring, caching where safe, and per-analysis cost measurements.

## 9. MVP Acceptance Criteria

A release candidate is not accepted merely because the model generates a plausible summary. It should satisfy these observable conditions:

1. A user can upload a supported PDF and see a reliable processing status.
2. Text and scanned pages are distinguished; poor extraction is explicitly flagged.
3. Every displayed tender requirement includes a source page and an excerpt from the uploaded source.
4. No requirement can be marked "supported" without a specific seller evidence link or explicitly stated basis.
5. Numeric comparisons show the source threshold, the extracted/evidenced value, units, applicable period, and calculation.
6. Missing proof is distinguished from confirmed non-compliance.
7. Ambiguous, conflicting, conditional, or low-confidence cases are escalated to review.
8. Corrigendum comparison identifies version changes and flags changes to dates and requirements.
9. The report identifies its analysis timestamp, source-document versions, and known limitations.
10. Tenant-isolation, upload-validation, authorization, and delete-path tests pass.
11. A human-reviewed reference dataset meets the evaluation gates defined in [evaluation-plan.md](evaluation-plan.md).
12. A user can understand how to reach the cited page in the original PDF without relying on an unsupported AI paraphrase.

## 10. Discovery Questions Before Building Too Much

Interview MSME sellers, active GeM bidders, and bid consultants to learn:
- Which tender categories do they bid for most often?
- How many tender documents do they review per month?
- Which clauses cause the most rework or rejection?
- Which seller documents are reused and how are their expiry dates tracked?
- How often do amendments arrive close to deadlines?
- Which language(s), scans, tables, annexures, and file sizes are common?
- Who performs the final review and signs off on bid/no-bid?
- What does a mistake cost in time, fees, lost opportunity, or compliance risk?
- Would users pay per analysis, by monthly seat, or through a consultant workflow?
- What retention, confidentiality, and deployment expectations are non-negotiable?

Validate the workflow before choosing a price or claiming a large addressable revenue market.

## 11. Open Product Decisions

Record decisions rather than letting implementation code decide them accidentally:
- Initial supported tender type: goods, services, works, or one narrow subcategory?
- English-only first release or selected multilingual support?
- Allowed PDF file size, page count, and processing timeout?
- Which evidence formats are accepted beyond PDF?
- Which OCR/LLM vendors can process confidential seller files under acceptable terms?
- Default data retention period and deletion behavior across backups?
- Whether user workspaces store company documents long-term or only per tender?
- How many expert reviewers are needed for the gold-label benchmark?
- What minimum accuracy is required before calling the product suitable for a pilot?
