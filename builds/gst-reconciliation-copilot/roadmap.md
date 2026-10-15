# GST Reconciliation Copilot — Roadmap and Business Validation

## Product thesis
Start with a file-based, evidence-first reconciliation workbench for CA firms. Validate that it reduces review effort and improves exception follow-up before investing in live integrations, broad tax coverage, or a large accounting platform.

The proposed initial segment—small CA firms managing many GST clients—is a hypothesis. Validate the frequency of reconciliation work, the existing GSTN matching-tool workflow, and willingness to pay before treating it as a business fact.

## Phase 0 — Customer discovery
- Interview CA partners, tax practitioners, and accounts executives.
- Observe one real reconciliation process with authorization.
- Record input formats, row counts, time spent, common exceptions, and output reports.
- Ask how the official GSTN offline matching tool is used today and where it falls short.
- Identify one initial accounting-software/export format.
- Document confidentiality, retention, and client consent/authority requirements.
- Validate whether multi-client management and issue follow-up matter enough to pay for.

**Gate:** a repeated, expensive workflow is demonstrated; the initial user and supported input format are selected; existing alternatives are understood.

## Phase 1 — Import and normalization prototype
Build:
- Purchase register XLSX/CSV upload.
- One supported GSTR-2B export format.
- Sheet/column mapping preview.
- Source row preservation and validation report.
- Decimal arithmetic and normalized record schema.
- Unit tests for dates, identifiers, tax heads, and invalid data.

**Gate:** every input row is accounted for and traceable; totals can be independently reproduced.

## Phase 2 — Deterministic reconciliation engine
Build:
- Composite-key exact matching.
- Field-by-field comparison for date, taxable value, and tax heads.
- Books-only and GSTR-2B-only categories.
- Same-side duplicate candidates.
- Conservative candidate matching.
- Versioned rules and configured tolerances.
- Disjoint/defined summary aggregation.

**Gate:** a labelled benchmark shows reliable exact matching, no silent wrong exact matches in regression tests, and transparent arithmetic.

## Phase 3 — Exception workbench
Build:
- Side-by-side evidence panel.
- Candidate accept/reject.
- Reviewer notes and assignment.
- Issue status lifecycle.
- Supplier/GSTIN grouping.
- Summary/detail exports with source references and run metadata.

**Gate:** experienced reviewers can trace every finding to source data and complete the workflow with less effort than the baseline.

## Phase 4 — Closed pilot
- Pilot with a small number of consenting CA firms.
- Use copies of records and retain their existing professional review/sign-off.
- Compare output with the firm's normal process.
- Track false matches, missed matches, unsupported rows, review time, export corrections, and support needs.
- Confirm client isolation, deletion, backup, and provider terms before confidential production use.

**Gate:** repeat usage, acceptable measured matching quality, demonstrable review-time benefit, and a credible willingness-to-pay signal.

## Phase 5 — Reliability and fit
Prioritize from pilot evidence:
- Saved column mappings for known source formats.
- More accounting-system exports.
- Period-to-period and amendment links.
- Improved duplicate explanation.
- Reviewer approval and audit history.
- Controlled task assignment and supplier follow-up status.
- Large workbook performance and background processing.
- Better export templates requested by actual users.

Do not add every tax scenario at once. Add one category only after documenting its fields, matching semantics, aggregation behavior, and professional review requirements.

## Phase 6 — Optional integrations
Only after file-based value is proven:
- Evaluate official GSTN/GSP integration availability, authorization, cost, contractual terms, and technical scope.
- Add accounting-system connectors if users repeatedly request them.
- Consider client portal/report sharing with strict access controls.
- Add e-invoice-related alerts only where authoritative source data and a clear rule support the feature.

No GST API or filing integration is required for the MVP.

## Suggested first vertical
Start with one narrow workflow, such as monthly purchase-register versus GSTR-2B reconciliation for a CA firm using one common accounting export. The first release should support a small, explicit subset of documents and flag the rest for review rather than pretend to handle every GST case.

## Business model hypotheses
Test, do not assume:
- Per client GSTIN per month.
- Firm-wide subscription with client-count tiers.
- Usage-based pricing by number of source rows or reconciliation runs.
- Team seats for preparers and reviewers.

Measure cost per run, onboarding time, support effort, and reviewer time saved before choosing pricing. GST reconciliation may be seasonal and deadline-sensitive; capacity and support must account for peaks.

## Competitive differentiation to test
GSTN already provides an official offline matching tool and portal workflows. Therefore, do not market this as "the first invoice matching tool." Potential differentiators to validate:
- Mapping heterogeneous purchase registers to a common schema.
- A multi-client CA workspace.
- Explainable field-level exceptions with source row links.
- Task assignment and supplier follow-up tracking.
- Repeatable runs, reviewer history, and client-ready reports.
- Clear handling of duplicate candidates and unsupported categories.

These are hypotheses until customer interviews and pilot comparisons demonstrate that they matter.

## Risks and mitigation

| Risk | Mitigation |
|---|---|
| Wrong exact match | Conservative rules, evidence, benchmark, release block on regressions |
| Complex GST edge cases | Explicit scope, qualified review, unsupported-case handling |
| Source files differ widely | Start with one format; invest in mapping after interviews |
| Users already satisfied with free/official tools | Validate workflow gaps before building |
| Sensitive financial data exposed | Tenant isolation, private storage, retention/deletion, audit |
| False duplicate flags | Show why flagged; never auto-delete source rows |
| Period/cutoff confusion | Show selected period, file provenance, and GSTR-2B context |
| AI hallucinates tax treatment | Keep tax arithmetic deterministic; AI is optional and non-authoritative |
| Large files are slow | Background workers, limits, metrics, realistic load tests |
| Product becomes a full tax suite | Keep MVP limited to reconciliation and exception workflow |
| Pricing does not cover support | Measure onboarding and support cost per firm |

## Success metrics
- Time from upload to validated reconciliation.
- Percentage of rows mapped without manual repair.
- Exact-match precision and recall on labelled data.
- Wrong auto-match rate.
- Percentage of exceptions with complete source evidence.
- Reviewer time per 1,000 rows.
- Export correction rate.
- Repeat usage across periods and client accounts.
- Time to onboard a new client/file format.
- Willingness to pay and renewal intent.
- Processing cost and support hours per client.

## Decision log
Record dated decisions for:
- Initial customer segment and evidence.
- Supported GSTR-2B format and tables.
- Supported purchase-register formats.
- Match keys and tolerances.
- Supported credit/debit-note/amendment behavior.
- Duplicate policy.
- Summary aggregation rules.
- Data retention and deletion.
- Whether/when AI is used.
- Pricing and package.
- Whether integrations are justified.

## Research and official references
- [GST Portal — GSTR-2B FAQ](https://tutorial.gst.gov.in/userguide/returns/FAQ_gstr2b.htm): purpose, download formats, reconciliation guidance, duplicate-credit warning, and period/cutoff behavior.
- [GSTN matching tool guide (PDF)](https://tutorial.gst.gov.in/downloads/matchingtool.pdf): official offline matching-tool documentation; check the current portal for the latest version.
- [CBIC — Input Tax Credit rules](https://cbic-gst.gov.in/input-tax-credit-rules.html): official tax-rule reference; consult current law and qualified professionals for applicability.
- [Official e-Invoice System](https://einvoice.gst.gov.in/).
- [E-Invoice reporting restriction advisory](https://einvoice6.gst.gov.in/content/revised-time-limit-for-e-invoice-reporting-for-businesses-with-aato-of-%E2%82%B910-crores-above/): official portal page describing the 30-day reporting restriction effective April 1, 2025 for AATO ₹10 crore and above. Verify current applicability before using this in product logic.
- [GST Portal](https://www.gst.gov.in/).
