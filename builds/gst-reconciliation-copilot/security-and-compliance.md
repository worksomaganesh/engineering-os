# GST Reconciliation Copilot — Security, Privacy, and Compliance Guardrails

This product may process supplier identities, GSTINs, invoice numbers, commercial values, tax details, client records, and working papers. Treat uploaded files and derived reports as confidential by default. This document is engineering guidance, not legal or tax advice.

## 1. Data to protect
- Original purchase registers and GSTR-2B downloads.
- GSTINs, supplier names, invoice identifiers, values, tax heads, and client labels.
- Normalized rows, match suggestions, exceptions, notes, and reviewer decisions.
- Downloadable reports, temporary files, cached data, logs, and backups.
- User credentials, session tokens, database credentials, and model-provider keys.

Collect only the information needed for reconciliation. Do not use client files as demo data or training data without appropriate authorization.

## 2. Threat model

| Threat | Example | Mitigation |
|---|---|---|
| Cross-client exposure | One CA client can access another client's invoice register | Server-side authorization on every request and tenant-isolation tests |
| Malicious workbook | Crafted XLSX exhausts worker memory or abuses parser | File/row/sheet limits, safe libraries, worker resource caps |
| Formula injection | Exported invoice text becomes an executable spreadsheet formula | Escape/sanitize untrusted cells in generated exports |
| False match | Wrong invoice pair is shown as exact | Conservative deterministic rules, evidence, regression tests |
| Duplicate credit risk | Duplicate-looking row silently removed or double-counted | Preserve source rows; show candidate and require review |
| Secret leakage | Cloud/database key committed to Git | Secret manager, least privilege, rotation |
| Confidential log leak | Full invoice row copied into error logs | Redacted structured logs, access controls, retention limits |
| Unauthorized download | Stale report URL remains accessible | Short-lived authorized links, expiry, server checks |
| AI prompt injection | Workbook text instructs model to ignore safeguards | Treat source text as untrusted data; no privileged tools |
| Cost/availability abuse | Huge file or repeated upload triggers resource exhaustion | Quotas, rate limits, idempotency, file/row limits |

## 3. File upload controls
Use the [OWASP File Upload Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/File_Upload_Cheat_Sheet.html) as a baseline.

- Accept only declared supported formats and validate actual file structure.
- Enforce byte size, sheet count, row count, column count, cell length, and processing-time limits.
- Store uploads privately and use internally generated storage keys.
- Never execute macros; do not trust filenames or declared MIME types.
- Use patched parsers and isolate heavy parsing in a bounded worker.
- Treat formula cells carefully; never assume a workbook's cached formula value is current.
- Do not run arbitrary formulas from user uploads.
- Make malformed and unsupported files fail visibly.
- Avoid putting source cell values in logs or error reports.
- Scan files where appropriate to the deployment environment and risk model.

## 4. Client and workspace isolation
- Every client, GST registration, import, source row, normalized record, run, exception, note, and export must belong to an authorized workspace.
- Enforce access checks on the server, not only by hiding UI elements.
- Do not trust workspace/client IDs from the browser.
- Use least-privilege roles for preparers, reviewers, and read-only members.
- Test attempts to fetch another tenant's IDs and report URLs.
- Separate test, staging, and production data.
- Audit sensitive operations without duplicating invoice details in audit metadata.

## 5. AI guardrails
The reconciliation engine does not need a language model for arithmetic or exact matching. If AI is used for column mapping or natural-language explanations:

- Treat workbook contents and cell text as untrusted input, not instructions.
- Do not give the model access to secrets, database tools, file systems, or unrestricted actions.
- Keep calculations and matching results outside the model as trusted structured inputs.
- Validate any model output against a strict schema and source fields.
- Never let a model invent a tax amount, source row, GSTIN, or legal conclusion.
- Require a human to approve uncertain mappings and candidate matches.
- Avoid sending confidential client data to an external provider until retention, training, region, subprocessors, contract, and deletion terms are reviewed.
- Keep model provider, prompt, and version behind an interface; log versions, not unnecessary raw client text.

Prompt instructions are not a security boundary. The model must not be authoritative for tax calculations or ITC eligibility.

## 6. Privacy, retention, and client authorization
- Establish the firm's authority to upload/process the records and provide clear notices to authorized users.
- Define retention for source files, normalized rows, reports, caches, audit records, and backups.
- Implement deletion across original and derived data, including expired exports.
- Document backup expiry and deletion timelines.
- Minimize logs and telemetry; avoid full GSTINs and invoice values unless operationally essential.
- Encrypt transport and use appropriate managed storage/database protections.
- Restrict staff access and review permissions periodically.
- Maintain an incident-response and credential-rotation procedure.
- Do not reuse client data to improve a model unless appropriate authorization and contractual terms permit it.

For an India launch, have qualified counsel review applicable data-protection, confidentiality, tax-practice, and contractual obligations. The product's precise role and obligations depend on how it is deployed and who determines processing purposes.

## 7. GST-specific product guardrails
Official GST guidance says GSTR-2B is an auto-drafted ITC statement and advises taxpayers to reconcile it with their own records/books. It also warns against taking credit twice and explains that supplier-filed documents may reflect in a later open GSTR-2B depending on cut-off timing. See:
- [GST Portal GSTR-2B FAQ](https://tutorial.gst.gov.in/userguide/returns/FAQ_gstr2b.htm)
- [CBIC — Input Tax Credit](https://cbic-gst.gov.in/input-tax-credit-rules.html)

Therefore:
- "Not found in this supplied GSTR-2B file" is not proof that a supplier never reported the invoice.
- A match is not a determination of ITC eligibility.
- A mismatch is not automatically a violation or a direction to reverse credit.
- Preserve GSTR-2B table/category and period context.
- Treat credit notes, debit notes, amendments, reverse-charge records, ISD, imports, and other special categories according to tested rules or manual review.
- Never submit returns or make portal changes in the MVP.
- Require a qualified professional to review tax treatment and filing decisions.

## 8. E-invoice reporting rule — how to document it safely
The official e-invoice portal has published a revised reporting time limit for taxpayers with aggregate annual turnover of ₹10 crore and above. Because applicability and operational details may change, do not hard-code a general tax conclusion into the matching engine. Verify the current official advisory at implementation and retain its effective date/source in product documentation:
- [Official e-Invoice System advisory](https://einvoice6.gst.gov.in/content/revised-time-limit-for-e-invoice-reporting-for-businesses-with-aato-of-%E2%82%B910-crores-above/)

The reconciliation product may surface a date-related review warning if the required source fields and policy rules are explicitly implemented. It should not claim to decide whether an invoice is legally reportable based only on a spreadsheet.

## 9. Secrets and deployment
- Keep credentials in a server-side secret manager or protected environment configuration.
- Never commit secrets to Git or bundle them into browser JavaScript.
- Use separate least-privileged identities for web app, worker, database, and object storage.
- Configure cost/resource alerts; an alert is not necessarily a hard spending limit.
- Patch dependencies and back up the database securely.
- Test recovery, access revocation, and deletion.

## 10. Pre-pilot checklist
- [ ] Supported file types, size limits, and parsing boundaries documented.
- [ ] Uploads private by default.
- [ ] Tenant isolation tested across all resources.
- [ ] Formula-injection tests pass for exports.
- [ ] No macros or arbitrary workbook formulas are executed.
- [ ] Source rows and calculations are traceable.
- [ ] No silent exact match for ambiguous records.
- [ ] Credit-note/amendment/special-category behavior reviewed.
- [ ] AI provider data terms reviewed if AI is used.
- [ ] Deletion covers originals, normalized rows, exports, caches, and backup expiry.
- [ ] Secrets absent from source control and client bundles.
- [ ] Qualified professional reviews disclaimers and supported tax workflows.
- [ ] Existing CA review/sign-off process remains in place during pilot.

## References
- [OWASP File Upload Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/File_Upload_Cheat_Sheet.html)
- [GST Portal — GSTR-2B FAQ](https://tutorial.gst.gov.in/userguide/returns/FAQ_gstr2b.htm)
- [CBIC — Input Tax Credit](https://cbic-gst.gov.in/input-tax-credit-rules.html)
- [Official e-Invoice System](https://einvoice6.gst.gov.in/)
