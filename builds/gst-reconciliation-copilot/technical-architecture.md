# GST Reconciliation Copilot — Technical Architecture

## 1. Design principles

1. **Deterministic arithmetic:** tax and value differences are calculated by code using decimal arithmetic, never guessed by a language model.
2. **Evidence first:** every result retains source file, sheet, row, and the exact normalized fields used.
3. **Conservative matching:** exact matches, candidate pairs, and human-reviewed matches are distinct.
4. **Repeatability:** same input files + same rule-set version should produce the same match results.
5. **Tax professional remains responsible:** the software organizes evidence; it does not certify ITC eligibility or file returns.
6. **MVP without GST APIs:** begin with authorized file uploads; avoid portal login, filing, and integrations until the workflow is validated.

## 2. High-level architecture

~~~text
Web UI
  |
  | authenticated upload + mapping confirmation
  v
Application API + authorization
  |
  +--> private source-file storage
  |
  v
Import job / worker
  |
  +--> workbook inspection + format validation
  +--> column mapping + normalization
  +--> data-quality report
  |
  v
Reconciliation engine
  |
  +--> duplicate detection within each source
  +--> exact-match pass
  +--> candidate-match pass
  +--> deterministic difference calculation
  |
  v
Reconciliation run + match/exception records
  |
  +--> exception workbench and review history
  +--> summary dashboard
  +--> XLSX/CSV export
~~~

This is a proposed architecture, not a statement that the system is already implemented.

## 3. Component boundaries

### Frontend
- Client/GSTIN/period selector.
- Upload and column-mapping wizard.
- Source row preview and data-quality warnings.
- Summary dashboard and filters.
- Side-by-side exception workbench.
- Review, assign, note, resolve, and export actions.
- Display rule version and run status.

The frontend must not calculate authoritative tax totals or decide access control. It displays server-produced calculations and asks the API to perform authorized operations.

### API and access control
- Authenticate users and check their membership/role for every client resource.
- Validate upload size, supported format, number of sheets/rows, and processing limits.
- Create imports and reconciliation runs.
- Expose only authorized source rows, results, notes, and reports.
- Apply rate limits and audit important review actions.
- Use safe, non-sensitive error codes instead of returning raw stack traces or source contents.

### File ingestion
- Accept only declared formats in the MVP.
- Inspect file signatures/structure rather than trusting extension alone.
- Detect worksheets, hidden sheets/rows where supported, headers, blank rows, formulas, merged cells, and unexpected columns.
- Do not execute workbook macros.
- Warn if formula cells have no cached values or the workbook requires recalculation.
- Record which sheet/range was included.
- Reject files exceeding resource limits with a useful explanation.

### Normalization layer
Convert each source row into a canonical internal record while preserving original values.

Potential canonical fields:
- Client/workspace ID and GSTIN.
- Source type (purchase register / GSTR-2B).
- Original file ID, worksheet name, row number.
- Supplier GSTIN and recipient GSTIN, where available.
- Document type, original document number, normalized comparison key.
- Document date and original date text.
- Taxable value, IGST, CGST, SGST/UTGST, cess, invoice total.
- Place of supply, reverse-charge indicator, and source-specific fields when present.
- Financial/tax period and amendment/credit/debit-note references.
- Validation warnings.

Use decimal arithmetic for currency; binary floating-point can introduce rounding errors. Preserve original precision and define rounding/tolerance policy explicitly. Never silently strip meaningful characters from invoice numbers. Normalization rules should be versioned and visible.

### Reconciliation engine
Separate into passes:

1. **Data quality:** invalid/missing identifiers, duplicate rows, unsupported categories, invalid amounts/dates.
2. **Exact candidate keys:** normalized supplier GSTIN + document type + normalized invoice number, with date/value/tax checks.
3. **Exact-field validation:** compare document date, taxable value, tax heads, total, and applicable metadata.
4. **Candidate generation:** if identifiers are slightly different, produce a bounded set of plausible candidates with reasons; never silently auto-merge uncertain records.
5. **Duplicate analysis:** detect repeated or near-repeated records within each source separately.
6. **Unmatched classification:** records with no suitable counterpart become books-only or 2B-only for the selected files/period.
7. **Exception classification:** tax/value/date/document-number discrepancies, credit/debit notes, amendment candidates, or manual review.
8. **Summary calculation:** compute counts and totals from persisted match/exception records using a defined, non-overlapping category policy.

Candidate matching may use token normalization, date windows, amount tolerances, and a weighted score. Each signal should be explainable. The first release should favor precision over aggressive fuzzy matching. A human decision should be recorded separately from the original suggestion.

### Export service
Generate XLSX/CSV with:
- Summary and line-level result sheets.
- Original source references.
- Normalized comparison values and differences.
- Match method and rule-set version.
- Reviewer notes/status.
- Import and run timestamps.
- Clear scope limitations and disclaimer.

Prevent spreadsheet formula injection when exporting untrusted cell values: text beginning with formula-triggering characters must be safely encoded according to the chosen export library and format.

## 4. Matching logic and precedence

The exact rules need to be configurable and tested against real, authorized examples. A starting hierarchy:

1. Exclude or quarantine invalid rows from automated matching, while preserving them in the import report.
2. Detect same-side duplicate candidates before totals are finalized.
3. Match on a stable composite identity when available: supplier GSTIN + document type + normalized document number.
4. Compare date, taxable value, each tax head, and total separately.
5. If the key agrees but tax/value differs, classify as a mismatch, not an exact match.
6. If a likely identifier typo or amended number is present, create candidate pair(s) and explain the evidence.
7. If multiple candidates are similarly plausible, do not pick one automatically.
8. Unpaired rows become books-only or 2B-only relative to the supplied inputs.
9. Credit/debit notes and amendments follow separate supported rules.
10. All manual overrides require actor, timestamp, and rationale.

### Difference calculations
For a matched pair:
- taxable difference = books taxable value − GSTR-2B taxable value
- IGST difference = books IGST − GSTR-2B IGST
- CGST difference = books CGST − GSTR-2B CGST
- SGST/UTGST difference = books SGST/UTGST − GSTR-2B SGST/UTGST
- cess difference = books cess − GSTR-2B cess
- total tax difference = sum of applicable tax-head differences

Keep signs consistent and label the subtraction direction. Do not use an arbitrary universal tolerance. Define configurable absolute/relative tolerances, rounding behavior, and which fields can ever be tolerated. An invoice-number mismatch or GSTIN mismatch should not be ignored merely because the total amount matches.

## 5. Proposed data flow and states

### Import state
`uploaded → validating → needs_mapping → queued → processing → completed / completed_with_warnings / failed / cancelled`

### Reconciliation run state
`created → processing → needs_review → reviewed / failed / cancelled`

A successful import is not the same as a fully reviewed reconciliation. Surface that distinction.

### Exception state
`open → assigned → awaiting_supplier / awaiting_client / awaiting_internal_review → resolved_with_note`

Also support `dismissed_as_not_issue` with a reason and `reopened` if new data changes the result. Never delete the original automated result when a human overrides it.

## 6. Proposed API surface (illustrative, not implemented)

| Method | Path | Purpose |
|---|---|---|
| POST | `/api/clients` | Create client workspace |
| POST | `/api/imports` | Upload/create an import |
| GET | `/api/imports/{id}` | Read import status and warnings |
| POST | `/api/imports/{id}/mapping` | Save confirmed column mapping |
| POST | `/api/reconciliation-runs` | Start a run for selected imports/period |
| GET | `/api/reconciliation-runs/{id}` | Read run state and summary |
| GET | `/api/reconciliation-runs/{id}/exceptions` | Filter exceptions |
| POST | `/api/exceptions/{id}/review` | Accept/reject/resolve with rationale |
| POST | `/api/exceptions/{id}/assign` | Assign owner and action |
| GET | `/api/reconciliation-runs/{id}/export` | Request authorized report export |

Every endpoint needs resource-level authorization. Never trust client/workspace IDs from the browser without server-side membership checks.

## 7. Suggested stack

One practical option:
- **Frontend:** React + TypeScript.
- **Backend:** Python with FastAPI for workbook parsing and reconciliation.
- **Data:** PostgreSQL for clients, imports, row records, match groups, exceptions, reviews, and audit history.
- **File storage:** private object storage or private server-side storage for a small local prototype.
- **Worker:** durable background job for large workbooks.
- **Spreadsheet libraries:** a maintained XLSX reader and CSV parser with limits and formula handling documented.
- **Authentication:** established identity provider or framework rather than custom password handling.
- **Deployment:** managed app/database/storage with secrets management, backups, and access control.

This is a recommendation, not a requirement. A local-only prototype may start with Python, a simple UI, and in-memory/file-backed processing; do not introduce cloud infrastructure before the core matching tests work.

## 8. Security and operations
- Store original files privately and restrict downloads.
- Use least privilege for application, worker, database, and storage.
- Never put secrets in Git or frontend bundles.
- Encrypt transport and use appropriate storage/database protections.
- Avoid logging full GSTINs, invoice data, or source row values by default.
- Track job duration, row counts, parse warnings, candidate counts, exceptions, export failures, and cost.
- Make import/run operations idempotent where possible.
- Back up data and test restore/deletion.
- Apply retention and deletion across originals, normalized rows, exports, caches, and backups according to the firm's agreed policy.

## 9. Why no GST API in MVP?
A file-upload workflow is easier to scope, test, and validate. It avoids portal credential handling and integration approvals while proving whether the exception workbench is valuable. API integration may be considered later only after reviewing official GSTN/GSP availability, authorization, terms, technical documentation, and actual customer demand.

## 10. Official references
- [GSTN matching tool guide (PDF)](https://tutorial.gst.gov.in/downloads/matchingtool.pdf)
- [GST Portal — GSTR-2B FAQ](https://tutorial.gst.gov.in/userguide/returns/FAQ_gstr2b.htm)
- [GST Portal](https://www.gst.gov.in/)
- [E-Invoice System](https://einvoice.gst.gov.in/)
