# GST Reconciliation Copilot — Evaluation and Test Plan

## 1. Why evaluation matters

A reconciliation tool can look convincing while silently matching the wrong invoice, missing a duplicate, mishandling a credit note, or presenting a misleading total. Evaluate data import, matching, arithmetic, exception classification, traceability, and reviewer workflow separately.

Do not advertise "99% accurate" or similar without a representative, documented benchmark and a clearly defined metric.

## 2. Build a labelled benchmark

Create synthetic and authorized, de-identified examples representing the actual formats used by pilot firms. Start with 100–300 paired/single-side scenarios as an engineering test set, then expand based on observed error classes. This is a starting plan, not a statistically guaranteed sample size.

Include:
- Exact invoice match.
- Same supplier and invoice number but different taxable value.
- Same value but wrong supplier GSTIN.
- Invoice number formatting differences (spaces, hyphens, leading zeros, prefixes).
- Different document types with similar numbers.
- Different dates with otherwise identical fields.
- IGST mismatch, CGST mismatch, SGST mismatch, cess mismatch.
- Rounding differences within and outside a configured tolerance.
- Duplicate rows within purchase register.
- Duplicate rows within GSTR-2B.
- Duplicate-looking but legitimate separate invoices.
- Books-only and 2B-only rows.
- Same invoice appearing in another period.
- Supplier filed after the statement cutoff.
- Credit note, debit note, amended invoice, and original/amended references.
- Reverse-charge, ISD, e-commerce, import/BoE rows where the declared scope supports them.
- Missing GSTIN/invoice number/date/tax values.
- Negative values and zero values.
- Commas, Indian number formatting, currency symbols, formulas, blank cells, hidden rows/sheets, merged cells, and formula cells without cached values.
- CSV encoding, delimiter and newline variants.
- Wrong GSTIN/period files selected together.
- Same invoice on both sides but only a partial tax head is available.

Keep a holdout set separate from tuning. Do not tune the rules against every test case and then present the same cases as independent validation.

## 3. Ground-truth annotation

For each source record, annotate:
- Canonical identity and document category.
- Whether the row is valid and supported by the current parser.
- Correct counterpart, if any.
- Exact versus candidate match classification.
- Expected field-level differences.
- Duplicate relationship, if any.
- Period/cutoff caveats.
- Whether human review is required.
- Source row references.
- Correct summary category and treatment in totals.

For complex amendments or legal/tax interpretation, have a qualified professional define expected treatment. Annotators should not infer tax eligibility from matching alone.

## 4. Metrics

| Metric | Definition | Why it matters |
|---|---|---|
| Import success | Supported files successfully parsed | Usability/reliability |
| Row accounting completeness | Imported = included + skipped + invalid, under the declared rules | Prevents hidden row loss |
| Source traceability | Results with valid source file/sheet/row links | Auditability |
| Exact-match precision | Predicted exact matches that are correct | Prevents false certainty |
| Exact-match recall | True exact matches detected | Measures missed matches |
| Candidate-pair precision | Suggested pairs that reviewers confirm are correct | Candidate usefulness |
| Wrong auto-match rate | Incorrect pairs labelled exact without review | Critical safety metric |
| Mismatch classification accuracy | Correct tax/value/date/document mismatch categories | Helps route investigations |
| Duplicate precision/recall | Correct duplicate flags and missed duplicates | Prevents double counting |
| Tax arithmetic accuracy | Correct differences by tax head | Core correctness |
| Summary reconciliation | Summary totals equal the defined aggregation of line-level results | Financial integrity |
| Unsupported-case handling | Unsupported categories flagged rather than silently misprocessed | Scope honesty |
| Review effort | Time/clicks needed to resolve a sample batch | Product value |
| Reopen rate | Resolved exceptions later reopened | Resolution quality |
| Export consistency | Exported values match on-screen/run records | Deliverable reliability |

Report metrics by source format, tax period, document category, and discrepancy type. An aggregate score can hide a catastrophic failure in one important category.

## 5. Provisional release gates

These are suggested internal gates, not measured results or legal standards:
- 100% of displayed match/exception rows have valid source references.
- 100% of tax differences use fixed-precision arithmetic and the documented sign convention.
- 100% of summary values reproduce from the saved line-level results and run configuration.
- Zero silent wrong exact matches in the release regression suite; any such failure blocks release.
- Unsupported document categories are flagged or handled by a tested rule, never silently treated as ordinary invoices.
- Candidate pairs remain distinguishable from exact matches.
- All import rows are accounted for in included/skipped/invalid totals.
- Cross-workspace access tests pass for every resource type.
- Exports pass formula-injection tests.
- Qualified reviewers approve the supported treatment of credit notes, debit notes, amendments, and reverse-charge cases before these are included in production calculations.

Set quantitative precision/recall targets with pilot users based on the cost of false matches versus manual review. Never claim that these initial gates establish tax-law compliance.

## 6. Test plan

### Spreadsheet ingestion
- Empty, corrupt, wrong-format, huge, and password-protected file.
- Many sheets, hidden sheets, hidden rows, merged cells, blank header rows.
- Formula cells with/without cached values.
- Unexpected columns and duplicate column names.
- Ambiguous date formats and locale-specific numbers.
- Numeric invoice number that loses leading zeros.
- Special characters, long strings, CSV injection-like values.
- Invalid encoding and unusual newline sequences.
- File name containing path separators or control characters.
- Same file uploaded twice.

### Matching engine
- Exact composite key and equal fields.
- Same key with tax/value mismatch.
- Conflicting GSTIN and same amount.
- Multiple candidate rows with similar scores.
- Candidate pair crosses document type or period.
- Duplicate row is not paired to two counterpart rows.
- Candidate accepted/rejected by reviewer.
- Rule/tolerance configuration changes produce a new run version.
- Re-running the same imports/configuration produces reproducible output.

### Tax and aggregation
- Each tax head differs independently.
- Credit/debit note sign handling.
- Null versus zero.
- Negative amendment/delta value.
- Decimal precision and rounding boundaries.
- Totals across mutually exclusive categories.
- Ensure books-only and 2B-only totals are not double-counted as matched mismatch totals.
- Verify summary versus detailed export.

### Workflow and security
- User from another workspace requests file, source row, exception, or export.
- Role permissions: preparer versus reviewer versus read-only.
- Import job retries and cancellation.
- Concurrent review of one exception.
- Deleted source file with derived rows and exports.
- Expired export URL.
- Audit history survives state changes.
- Malicious formula-like source text in export.
- Secret and sensitive invoice data absent from logs.

## 7. Pilot protocol

Before the product is used, gather a baseline from consenting CA/finance teams:
- Time spent on one period's reconciliation.
- Number of records and spreadsheet formats.
- Number of manual exceptions.
- Common reasons for mismatch.
- Time spent preparing a client report.
- Existing tool or GSTN offline matching workflow.
- Review effort and error correction process.

During the pilot:
1. Run the product on a copy of the same period's source files.
2. Have an experienced reviewer compare outputs against their normal process.
3. Record every wrong match, missed match, duplicate alert, and unsupported category.
4. Measure review time, not just compute time.
5. Validate exports against source data.
6. Ask whether the evidence panel improves confidence and client follow-up.
7. Estimate onboarding and support effort per client.
8. Review data security, retention, and deletion before using confidential files.

Do not use live filing decisions solely from the product's result during an early pilot. Maintain the firm's existing review controls.

## 8. Regression policy

For each parser, normalization, rule, or model change:
1. Run unit tests for parsing, normalization, decimals, and tax differences.
2. Run the full labelled benchmark.
3. Compare exact-match precision and wrong auto-match rate.
4. Inspect amendment, duplicate, period-cutoff, and tax-head regressions.
5. Verify exports and summary invariants.
6. Record rule/model/parser version and benchmark version.
7. Block release on unresolved financial-integrity or tenant-isolation failures.

## 9. Claims to avoid

Do not claim:
- "All ITC is eligible if matched."
- "A books-only invoice proves supplier non-compliance."
- "No invoice will ever be missed."
- "100% GST compliant."
- "Guaranteed tax savings."
- "Official GST portal integration" for a file-only MVP.
- "AI replaces the CA."

A defensible statement is: "Upload supported purchase-register and GSTR-2B files to generate a traceable, reviewable reconciliation with field-level differences and exception reports."
