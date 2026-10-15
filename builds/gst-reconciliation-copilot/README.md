# GST Reconciliation Copilot — Project Blueprint

> **Status:** researched product/implementation blueprint. This folder documents a proposed project; it does not mean the application has been built or validated with real CA firms.

## At a glance

**Problem:** CA firms and finance teams must compare purchase-register records with GSTR-2B, identify missing or inconsistent documents, avoid duplicate credit, and investigate exceptions.

**Proposed solution:** Upload supported purchase-register and GSTR-2B files, run a deterministic reconciliation engine, inspect a source-linked exception workbench, and export a reviewable report.

**Initial customer hypothesis:** small CA firms handling many GST clients. Validate the segment and its pain through interviews before treating it as proven.

**MVP:** XLSX/CSV upload → mapping/validation → exact matching + conservative candidate suggestions → discrepancy dashboard → evidence-backed review → downloadable report.

**Not in MVP:** GST portal login, GSTN/GSP API, return filing, automated ITC decisions, or automatic supplier contact.

## Why this workflow exists

GSTR-2B is an auto-drafted ITC statement based on documents furnished by suppliers and other applicable sources. The official GST Portal advises taxpayers to reconcile GSTR-2B with their own records/books and explicitly warns against taking credit twice. It also explains that supplier-filed documents may appear in the next open GSTR-2B depending on cut-off timing. These details make **period context and careful interpretation of missing records** important.

Sources:
- [GST Portal — GSTR-2B FAQ](https://tutorial.gst.gov.in/userguide/returns/FAQ_gstr2b.htm)
- [GSTN matching tool guide (PDF)](https://tutorial.gst.gov.in/downloads/matchingtool.pdf)
- [CBIC — Input Tax Credit rules](https://cbic-gst.gov.in/input-tax-credit-rules.html)

The GSTN portal already provides an official offline matching tool. Therefore, the product must not claim that matching software does not exist. Its differentiation should be validated around the broader workflow: flexible input mapping, multi-client CA operations, source-linked exception explanations, reviewer history, task follow-up, and clear reports.

The official e-Invoice system has also published a 30-day reporting restriction effective April 1, 2025 for businesses with annual aggregate turnover (AATO) of ₹10 crore or more. This is relevant context, but the MVP should not attempt to make legal compliance determinations from spreadsheet rows. Re-check the official advisory and current rules before any future date-warning feature:
- [Official e-Invoice advisory](https://einvoice6.gst.gov.in/content/revised-time-limit-for-e-invoice-reporting-for-businesses-with-aato-of-%E2%82%B910-crores-above/)

## Read the documents in this order

1. [Product requirements](product-requirements.md) — who it serves, exact MVP, requirements, acceptance criteria, and scope boundaries.
2. [Technical architecture](technical-architecture.md) — ingestion, normalization, reconciliation passes, exports, and security boundaries.
3. [Data model](data-model.md) — source records, normalized records, match groups, exceptions, reviews, and audit trail.
4. [UX and workflows](ux-and-workflows.md) — upload/mapping, dashboard, side-by-side evidence, duplicate review, and exports.
5. [Evaluation plan](evaluation-plan.md) — labelled benchmark, metrics, test cases, release gates, and pilot measurement.
6. [Security and compliance](security-and-compliance.md) — file safety, tenant isolation, confidentiality, AI guardrails, and GST-specific limitations.
7. [Roadmap](roadmap.md) — discovery, staged build, pilot, differentiation hypotheses, business risks, and official references.

## Example output

The following values are fictional and demonstrate the intended UI only.

### MATCHED
- Invoice: `INV-1042`
- Supplier GSTIN: fictional masked value
- Taxable value: ₹82,000
- GST total: ₹14,760
- Evidence: purchase-register sheet/row ↔ GSTR-2B table/row
- Result: exact match under the configured fields

### TAX MISMATCH
- Invoice: `INV-871`
- Books GST: ₹18,400
- GSTR-2B GST: ₹16,400
- Difference: ₹2,000 (books minus GSTR-2B)
- Next step: inspect tax-head values and source rows

### BOOKS ONLY
- Invoice: `INV-991`
- Found in purchase register.
- No match found in the supplied GSTR-2B records for this run.
- Next step: verify GSTIN, tax period/cutoff, amendments, file completeness, and supplier reporting before deciding what it means.

### POSSIBLE DUPLICATE
- Similar GSTIN, document number, date, and amount appear more than once in one source.
- Both original rows remain visible.
- A reviewer confirms whether it is a duplicate or a legitimate separate entry.

## Non-negotiable product principles

- **Evidence, not opaque AI conclusions:** show the source file, sheet, row, fields, and calculations.
- **Deterministic tax arithmetic:** use fixed-precision decimal calculations and documented tolerances.
- **Candidate is not exact:** uncertain pairs require review.
- **Missing in supplied data is not proof of non-compliance:** consider periods, cutoff dates, amendments, categories, and import quality.
- **Matched is not eligible ITC:** reconciliation does not replace all legal/accounting eligibility checks.
- **Never auto-delete duplicate-looking records.**
- **Keep special categories explicit:** credit/debit notes, amendments, reverse charge, ISD, imports, and other categories need tested rules or manual review.
- **No silent data loss:** every source row is accounted for as included, skipped, invalid, or unsupported.
- **Privacy by default:** client files are confidential; no real client data belongs in this public repository.
- **No portal actions in MVP:** no GST credentials, API calls, return filing, or automated supplier communication.

## Definition of a successful MVP

A successful MVP is not merely a dashboard that looks polished. It must:
- Import supported files reliably and report data-quality problems.
- Account for every source row.
- Find exact matches without silently forcing ambiguous pairs.
- Calculate every tax-head difference correctly.
- Detect and surface duplicate candidates.
- Show evidence for every match and exception.
- Generate exports whose totals reproduce from the line-level results.
- Preserve reviewer decisions and run configuration.
- Pass security/tenant-isolation tests.
- Demonstrate measurable review-effort improvement in a controlled CA/finance pilot.

## Important limitations

- This is a product blueprint, not tax advice.
- Official GST guidance, notifications, schemas, and portal behavior can change; verify current sources before implementation and launch.
- Exact matching rules depend on the supported GSTR-2B export structure and the actual purchase-register formats.
- The proposed target of 50–500 GST clients is a discovery hypothesis, not a validated market fact.
- The MVP must clearly disclose unsupported categories rather than imply complete GST coverage.
