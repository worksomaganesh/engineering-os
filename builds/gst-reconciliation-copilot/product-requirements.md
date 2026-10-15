# GST Reconciliation Copilot — Product Requirements

## 1. Product definition

**For CA firms and finance teams, GST Reconciliation Copilot compares the purchase register with GSTR-2B, classifies invoice-level differences, shows evidence for each finding, and prepares a reviewable action list and export.**

This is a proposed specification, not a live application or a substitute for tax-professional review.

## 2. Initial customer and user

**Initial segment hypothesis:** small CA firms managing roughly 50–500 GST client accounts. This is a hypothesis to validate through interviews—not a proven market-size estimate.

- **CA / tax practitioner:** reviews matches, investigates exceptions, approves client-ready reports.
- **Accounts executive:** imports registers, resolves spreadsheet issues, contacts vendors, and records explanations.
- **Finance manager / bookkeeper:** needs a timely books-versus-2B view.
- **Client owner / finance lead:** needs an understandable summary of open issues and next actions.

The central job is: "Tell me which records match, which differ, which are missing on either side, which may be duplicates, what the difference is, and exactly where to investigate."

## 3. Product position

This is not an AI summarizer or a generic accounting suite. Its core is **structured record reconciliation**: compare normalized fields, calculate differences deterministically, and explain why a candidate pair was matched or left unresolved.

AI may help map unfamiliar columns, suggest possible invoice pairs, summarize an exception, or draft a supplier query. It must not replace deterministic calculations or silently decide tax treatment.

Importantly, GSTN already provides an official offline matching tool. The opportunity must therefore be validated around workflow and usability advantages—such as arbitrary input mapping, multi-client CA workflow, evidence, follow-up tracking, history, and report quality—not a claim that invoice matching does not exist. See the source library in the project README.

## 4. MVP workflow

1. **Create client workspace:** record a client label, GSTIN(s), period, and authorized team members.
2. **Upload purchase register:** accept supported XLSX/CSV, preview sheets and rows, and map columns.
3. **Upload GSTR-2B:** accept supported GST portal downloads and identify the sheets/tables within the declared scope.
4. **Validate and normalize:** flag unsupported sheets, blank fields, ambiguous dates, invalid GSTIN formats, mismatched totals, and duplicate rows.
5. **Reconcile:** run deterministic exact matching followed by conservative candidate matching.
6. **Review dashboard:** filter exact matches, tax/value/date mismatches, books-only, 2B-only, duplicate candidates, amendment/credit-note records, and manual-review items.
7. **Investigate:** show row pairs side-by-side with field comparisons, source workbook/sheet/row, calculation, and prior-period context when available.
8. **Record disposition:** accept/reject a suggested pair, add notes, assign a task, or mark the issue as awaiting supplier/client response.
9. **Export report:** download detail and summary with data sources, rules/version, timestamp, totals, and reviewer status.
10. **Sign off:** a qualified reviewer decides the accounting/tax treatment through the firm's established process.

## 5. Core screens

### Upload and mapping
- File name, size, worksheet names, row counts, and detected formats.
- Preview rows and mappings for GSTIN, document type/number/date, taxable value, IGST, CGST, SGST/UTGST, cess, place of supply, reverse charge, and other available fields.
- Warnings for hidden rows/sheets, formula cells with missing cached values, duplicates, blank invoice numbers, unsupported document categories, or ambiguous parsing.
- Clear confirmation of the selected sheet/range being processed.

### Reconciliation summary
- Source rows read, invalid, skipped, and included.
- Exact/reviewed matches and candidate matches.
- Tax/value/date mismatches.
- Books-only and GSTR-2B-only records.
- Duplicate candidates in either source.
- Credit-note/debit-note/amendment records.
- Total differences by category and tax head.
- Data-quality warnings.

Counts and totals must be internally consistent. Do not count one invoice twice in incompatible categories. State whether a total is gross, net of credit/debit notes, or limited to a selected table/category.

### Exception workbench
For each exception show:
- Status, severity, and suggested action.
- Books row and source sheet/row.
- GSTR-2B row and source sheet/row, if present.
- GSTIN, invoice/document number, date, taxable value, and tax head-wise amounts.
- Field-by-field comparison and difference.
- Matching method and why a pair was suggested.
- Period and source-file metadata.
- Reviewer notes, owner, action, due date, and resolution state.

### Supplier / GSTIN view
Group issues by supplier GSTIN to answer: "Which suppliers account for the most unresolved differences?" Allow controlled export of only the necessary supplier-level data.

### Close-period report
Include client GSTIN, tax period, file names/checksums, imported row counts, result totals, open exceptions, reviewer/sign-off status, rule-set version, run timestamp, and a clear caveat: **a reconciliation match is not a conclusion that the invoice is eligible ITC.**

## 6. Status model

- `exact_match`: configured match fields agree within explicitly configured tolerances.
- `reviewed_match`: a human approved a candidate pair.
- `candidate_match`: plausible pair suggested by rules, awaiting review.
- `tax_mismatch`: paired record has a material tax difference.
- `value_mismatch`: taxable/total value differs beyond tolerance.
- `date_mismatch`: a candidate pair differs on document date.
- `document_number_mismatch`: likely related invoice, but document number differs.
- `books_only`: no match found in the supplied GSTR-2B records/period.
- `gstr2b_only`: no match found in the supplied purchase register.
- `duplicate_candidate_books` / `duplicate_candidate_2b`: same-side records may be duplicates.
- `credit_note_or_debit_note`: requires document-specific handling.
- `amendment_candidate`: possibly links to an amended record.
- `data_quality_issue`: source data is unreliable or not normalized sufficiently.
- `manual_review_required`: algorithm cannot choose safely.
- `resolved_with_note`: reviewer recorded a disposition.

"Books only" must not be rephrased as "supplier did not file" with certainty. The record might fall in another period/cutoff, be amended, be classified differently, be omitted from the uploaded file, or have failed parsing.

## 7. P0 functional requirements

- Authenticated multi-client workspace and strict client separation.
- XLSX/CSV upload, safe parsing, preview, and configurable field mapping.
- Preserve source-file/sheet/row references.
- Validate required columns, date formats, numeric precision, GSTIN/document fields, and file integrity.
- Normalize identifiers and values without destroying meaningful invoice-number detail.
- Exact matching using multiple fields.
- Conservative candidate matching with field-by-field reasons; uncertain matches remain candidates.
- Separate treatment for invoices, debit notes, credit notes, amendments, and special categories within the supported scope.
- Head-wise tax comparisons for IGST, CGST, SGST/UTGST, and cess where present.
- Duplicate-candidate detection on each side.
- Books-only and GSTR-2B-only classification.
- Exception review, note, owner, action, and status history.
- GSTIN-wise summary and downloadable report.
- Reproducible run metadata, validation warnings, and visible failure states.
- Export and deletion workflow for client data.

## 8. Explicitly out of scope for the MVP

- GST portal login, return filing, or direct GSTN/GSP API integration.
- Auto-filing GSTR-3B or submitting tax returns.
- A definitive instruction to claim/reverse a specific ITC amount as legal/tax advice.
- Automatically contacting suppliers.
- Full bookkeeping, invoicing, ERP, tax preparation, or practice management suite.
- Support for every import, ISD, reverse-charge, e-commerce, and amendment case before each is specified and tested.
- Assuming a mismatch is automatically a tax-law violation.

## 9. Acceptance criteria

1. Report source rows read, included, skipped, and invalid accurately.
2. Every result traces back to its source file, sheet, and row.
3. Every exact match explains which configured fields matched.
4. Candidate matches are never silently counted as exact.
5. Tax differences are calculated separately by tax head and overall.
6. The same supplier/invoice number with conflicting amounts becomes an exception, not a forced match.
7. Same-side duplicates are flagged instead of potentially double-counting credit.
8. Credit/debit notes, amendments, and reverse-charge records are not blindly treated as ordinary invoices.
9. Missing from supplied data is not represented as conclusive supplier non-compliance.
10. Data-quality warnings appear before totals are treated as reviewed.
11. Exported totals trace back to row IDs and calculation rules.
12. Tenant isolation and sensitive-file handling tests pass before real client files are processed.
13. Reviewers can accept/reject candidate pairs without overwriting the original automated result.
14. The app never labels all matched invoices "eligible ITC"; professional review remains necessary.

## 10. Discovery questions

- Is 50–500 GST clients the best initial segment?
- Which accounting software/export formats are common among interviewees?
- How much column mapping will users tolerate?
- Do firms prefer browser-local processing, private cloud processing, or a hybrid?
- Which report columns/formats are required for their working papers?
- How do they record vendor follow-ups and cross-period matches today?
- What audit trail does a CA partner expect before sign-off?
- Which monthly task consumes the most effort and what is the cost of getting it wrong?
- Which features of GSTN's official matching tool are insufficient for their workflow?
