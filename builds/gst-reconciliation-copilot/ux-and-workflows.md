# GST Reconciliation Copilot — UX and Reconciliation Workflows

## 1. The central experience

The product should feel like a controlled reconciliation workbench, not a chatbot. The main question it answers is: **"What needs my attention, and what is the evidence?"**

### Dashboard example (fictional)

| Category | Count | What it means |
|---|---:|---|
| Exact matches | 1,204 | All configured exact-match fields passed |
| Candidate matches | 19 | Plausible pairs awaiting review |
| Tax mismatches | 8 | One or more tax-head values differ |
| Books only | 27 | No corresponding row in the supplied GSTR-2B data |
| GSTR-2B only | 13 | No corresponding row in the supplied purchase register |
| Duplicate candidates | 4 | Same-side rows may represent duplicate records |
| Data quality issues | 6 | Input needs correction or manual interpretation |

These numbers are illustrative, not real product performance. Counts should be disjoint or clearly explain overlap. Summary tax amounts must use a documented inclusion policy.

## 2. Workflow A — upload and map files

### Step 1: choose client and period
Show the client label, target GSTIN, selected tax period, and who has access. Warn if the two files appear to relate to different GSTINs or periods.

### Step 2: upload source files
- Purchase register (XLSX/CSV).
- GSTR-2B download in a supported format.
- Display size and format limits.
- State that the MVP processes uploaded files only and does not connect to the GST portal.

### Step 3: map columns
Show the original column name, sample values, and mapped canonical field. Require confirmation for ambiguous fields like "Tax", "Invoice Value", or "GST Amount".

For example:
- `Supplier GSTIN` → `supplier_gstin`
- `Bill No` → `document_number`
- `Bill Date` → `document_date`
- `Taxable Amt` → `taxable_value`
- `IGST Amt` → `igst`

Never assume a generic "Tax" column is IGST or combined GST without an explicit mapping. Allow optional fields to remain unmapped, but explain what matching/reporting becomes less reliable.

### Step 4: validate before matching
Display invalid rows, duplicate candidates, unsupported document categories, date parsing warnings, blank invoice numbers, and source totals. Users should be able to download a validation report or fix the source file and re-upload.

## 3. Workflow B — summary dashboard

Recommended filters:
- Exact match / reviewed match.
- Candidate match.
- Taxable-value mismatch.
- IGST / CGST / SGST / cess mismatch.
- Books only / GSTR-2B only.
- Duplicate candidates.
- Credit note / debit note / amendment.
- Invalid or unsupported data.
- Assigned to me / unassigned / awaiting supplier / resolved.

Show source row counts and reconciliation status. Make it obvious that a candidate match needs review and that an exact match is only a match under the configured fields—not a legal ITC eligibility conclusion.

## 4. Workflow C — exception workbench

The reviewer opens a discrepancy and sees both sides side by side.

### Example: tax mismatch (fictional)
- Supplier GSTIN: fictional masked value.
- Invoice: `INV-871`.
- Books GST: ₹18,400.
- GSTR-2B GST: ₹16,400.
- Difference (books − GSTR-2B): ₹2,000.

| Field | Purchase register | GSTR-2B | Difference / result |
|---|---:|---:|---|
| Document number | INV-871 | INV-871 | Same normalized key |
| Taxable value | ₹1,02,222.22 | ₹1,02,222.22 | ₹0.00 |
| IGST | ₹18,400.00 | ₹16,400.00 | ₹2,000.00 |
| CGST | — | — | Not supplied |
| SGST | — | — | Not supplied |

All amounts are illustrative. The UI must distinguish "not supplied" from zero. The system should display the exact source sheet and row for each side.

### Required evidence panel
- Source file, worksheet, row, and tax period.
- Original and normalized invoice identifiers.
- Raw and parsed date.
- Taxable amount and tax-head amounts.
- Matching rule and version.
- Exact fields that matched and differed.
- Duplicate/credit-note/amendment relationships if detected.
- Reviewer note, owner, and resolution history.

The AI may summarize the discrepancy in plain language, but that summary must be generated from the calculated comparison and be subordinate to the underlying fields.

## 5. Workflow D — duplicate review

Show possible duplicate rows within the purchase register separately from duplicates within GSTR-2B. Include original row references and explain why the pair was flagged (same GSTIN/document number/date/value, or near-duplicate signals).

Actions:
- Confirm duplicate.
- Mark legitimate repeated reference with explanation.
- Ignore suggestion with reason.
- Keep both source rows visible.

Never delete duplicate-looking source records automatically. Similar amounts can be valid separate invoices; the product must show evidence and ask for review.

## 6. Workflow E — missing from one side

### Books-only
Display "Not found in the supplied GSTR-2B records for this run." Do not assert "supplier failed to report" without further verification. Offer checks:
- Correct GSTIN and tax period?
- Invoice in another month or later statement?
- Amended or differently classified document?
- Source export complete?
- Parsing/mapping issue?
- Supplier follow-up needed?

### GSTR-2B-only
Display "Not found in the supplied purchase register." Offer checks:
- Was the invoice booked in a different period?
- Is the purchase register complete?
- Is this an expense/purchase that belongs to another accounting workflow?
- Is the supplier/document correctly mapped?
- Is a manual entry or correction required?

Do not automatically label either category as an ITC claim/reversal instruction.

## 7. Workflow F — credit notes, debit notes, amendments, reverse charge

These categories can have different semantics from ordinary invoices. The product must either:
1. support a specifically tested rule for that category, or
2. label it unsupported/manual review and exclude it from misleading aggregate conclusions.

Show links to original documents when those references exist. Do not blindly net all credit notes against all invoices without a defined matching and reporting rule. Reverse-charge flags should be preserved and surfaced for professional review, not inferred from tax amounts alone.

## 8. Reviewer actions and status lifecycle

Suggested workflow:

~~~text
Detected issue
     |
Evidence + comparison shown
     |
     +--> accept candidate match
     +--> reject candidate pair
     +--> assign to colleague
     +--> request supplier/client clarification
     +--> add explanatory note
     +--> resolve with reason
     +--> reopen if new evidence arrives
~~~

Keep the automated finding and human disposition as separate records. The audit timeline should show who changed the state, when, and why.

## 9. Export experience

Provide:
- **Summary sheet:** counts, totals, period, client GSTIN, source filenames, run time, rule version, warnings.
- **Matched sheet:** record identifiers and fields used to match.
- **Mismatches sheet:** field-by-field values and differences.
- **Books-only sheet.**
- **GSTR-2B-only sheet.**
- **Duplicate candidates sheet.**
- **Data-quality sheet.**
- **Review history sheet** where appropriate.

Keep tax-head calculations transparent. Protect exports from spreadsheet formula injection. Include the scope limitation and avoid presenting the workbook as an official GST filing.

## 10. Accessibility and usability
- Do not rely only on red/green to communicate status.
- Use clear labels, keyboard navigation, visible focus, and readable table headers.
- Support large registers with pagination/virtualization and server-side filtering.
- Allow users to save column mappings by source format/client if security policy permits.
- Make failures actionable: "Column not mapped" is more useful than "AI failed."
- Confirm before destructive actions and provide reversible review states.

## 11. What not to build
- A chat screen as the primary interface.
- A generic dashboard full of vanity metrics.
- One opaque "AI match score" without reasons.
- Auto-removal of duplicates.
- An "ITC eligible" green badge solely because two rows match.
- Automatic supplier emails or tax filing in the MVP.
