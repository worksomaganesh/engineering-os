# GeM Tender Copilot — Security, Privacy, and Procurement-Risk Controls

This product may handle company financial statements, tax registrations, certificates, contract values, signatures, employee or proprietor contact details, OEM letters, and other commercially sensitive information. Security and privacy must be architecture requirements from the beginning, not a final polishing task.

This document is engineering guidance, not legal advice or a determination that the product complies with every applicable law.

## 1. Assets to Protect

- Seller company profile and registration facts.
- GST/PAN/Udyam-related documents and identifiers.
- Audited financial statements and turnover information.
- Purchase/work orders, customer names, contract values, and completion records.
- OEM authorization letters, signed declarations, certificates, and signatures.
- Tender documents, strategy, proposed participation, and bid calendars.
- AI prompts and extracted records, job logs, analysis reports, and exports.
- Authentication credentials, model/API credentials, database credentials, and object-storage keys.
- Audit records and deletion/retention information.

Not every field has the same legal classification, but many are confidential business information and some documents may include personal data. Minimize data collection and protect the full document, not only the fields labelled sensitive.

## 2. Threat Model

| Threat | Example | Essential mitigations |
|---|---|---|
| Cross-tenant data exposure | Seller A reads Seller B's report | Server-side authorization on every object; test tenant isolation; database constraints/policies where appropriate |
| Malicious upload | A disguised or malformed file exploits a parser | Size/type validation, safe parsers, scanning, isolation, patched dependencies, resource limits |
| Secret leakage | Cloud/model keys committed to Git or browser bundle | Server-side secret storage, scoped credentials, secret scanning, rotation procedure |
| Prompt injection in tender | PDF text tells an AI to ignore rules or reveal data | Treat document content as untrusted; no instruction authority; structured extraction; no privileged tools in the extraction step |
| Hallucinated condition | Model invents a turnover threshold or clause | Require source quote/page; verify citation; unknown state; reviewer workflow |
| False green status | Incomplete proof shown as "meets" | Evidence-linked statuses; deterministic checks; release gates; critical human review |
| Stale amendment | Report uses original deadline after corrigendum | Immutable versions, diffing, report-stale flags, latest-known label |
| Insider/unintended sharing | Export sent to wrong person | Role-based access, deliberate export, short-lived links, audit events, user-visible recipients |
| Data retention surprise | Uploaded documents remain after user deletion | Published retention schedule, deletion jobs, backup expiration semantics, deletion tests |
| Provider retention/secondary use | Confidential tender content sent to a model provider under unknown terms | Review DPA/terms, retention, training, region and subprocessor settings before selection |
| Denial of service / cost abuse | User uploads thousands of long PDFs | Quotas, page/size caps, rate limits, concurrency limits, job budgets and cancellation |
| Misleading output | User treats preliminary analysis as a legal guarantee | UI caveat near conclusions, source visibility, expert review for unclear clauses |

## 3. Secure File Upload Design

Use the [OWASP File Upload Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/File_Upload_Cheat_Sheet.html) as a starting reference.

Recommended controls:
- Allow only required file extensions and formats; initially, PDF-only makes scope easier to control.
- Validate actual file signatures/content in addition to the filename extension and declared MIME type.
- Set maximum file size and page count before expensive processing.
- Generate storage keys/filenames in the application; never concatenate an untrusted filename into a filesystem path.
- Require authorization before upload and before every download/export.
- Store uploads in private object storage outside a public web root.
- Use short-lived signed URLs only when needed, with narrowly scoped access.
- Scan files where suitable; use maintained parsing/OCR dependencies.
- Run parsing in a worker with resource limits and restricted filesystem/network permissions.
- Reject or explicitly handle encrypted, corrupt, or unsupported PDFs.
- Rate-limit upload/job creation and limit parallel jobs.
- Log safe identifiers and status transitions, not the entire uploaded document or secrets.
- Clean up temporary files after processing and apply retention/deletion policy to stored originals, extracted text, outputs, caches, and backups.

Never accept a MIME type or file extension as proof that the file is safe.

## 4. Tenant Isolation and Authorization

- Associate every tender, document, extracted fact, requirement, review, export, and job with a workspace.
- Authorize the workspace relationship server-side for every read, write, job status check, download, and deletion.
- Do not rely on hiding a button or trusting a workspace ID sent by the browser.
- Test horizontal access: a user from Workspace A attempts to access every object type owned by Workspace B.
- Keep roles narrow: owner/admin, reviewer, contributor, and read-only can be a starting point.
- Apply least privilege to service accounts and background workers.
- Separate development, test, and production environments.
- Keep administrative actions and reviewer overrides auditable.
- Use short-lived access tokens and a mature authentication method; do not invent your own cryptography.

## 5. LLM and Prompt-Injection Boundaries

Tender PDFs and company documents are **untrusted input**. A document may contain malicious instructions in visible text, hidden text, annotations, or linked material.

Controls:
1. The extraction model's instruction must state that file content is data to analyze, not instructions to follow.
2. Never pass uploaded document content into a privileged agent that can submit bids, access other tenants, issue refunds, or retrieve arbitrary internal files.
3. Do not give the model unrestricted network or filesystem tools.
4. Restrict retrieval to authorized documents within the current workspace.
5. Ask for structured output with explicit fields and evidence quotations.
6. Validate returned output against a schema and the original extracted page text.
7. Check that claimed page numbers and citations exist in the analyzed document version.
8. Apply deterministic rules outside the model for numeric/date checks where feasible.
9. Treat all model-produced fields as untrusted until validated; escape/sanitize output in the UI and reports.
10. Log model/rule versions and safe diagnostic details without logging credentials or more document text than necessary.
11. Test indirect prompt injection and attempted cross-tenant data exfiltration in the evaluation suite.

A prompt saying "be accurate" is not a security boundary. Architecture, access control, constrained tools, validation, and testing are required.

## 6. Model and OCR Provider Selection

Before sending tender/company files to an external provider, evaluate:
- Whether data may be used for provider model training.
- Retention and deletion controls.
- Contractual data-processing terms and subprocessors.
- Processing region and data residency capabilities.
- Encryption and access-control posture.
- Support for the languages, tables, scans, and file sizes in the benchmark.
- Rate limits, quotas, service reliability, and total cost.
- What happens to uploaded files, extracted text, prompts, responses, logs, and cached results.
- Whether users have been clearly informed about this processing.

Keep OCR and LLM providers behind interfaces so a vendor can be replaced. Avoid vendor selection by demo quality alone; use the evaluation plan with representative documents.

## 7. Privacy and Indian Legal/Policy Review

The [Digital Personal Data Protection Act, 2023](https://www.indiacode.nic.in/indiacode/handle/123456789/22037?view_type=browse) and [Digital Personal Data Protection Rules, 2025](https://www.meity.gov.in/documents/act-and-policies/digital-personal-data-protection-rules-2025-gDOxUjMtQWa?pageTitle=Digital-Personal-Data-Protection-Rules-2025) are relevant sources to review when the system processes digital personal data. The Rules were notified with a phased commencement structure, so confirm the then-current commencement provisions and their application with qualified counsel before launch. Other legal, contractual, cybersecurity, and sector-specific requirements may also apply.

Engineering practices to consider:
- Document the purpose for collecting seller data and do not repurpose it without an appropriate basis.
- Give a clear privacy notice describing what data is processed, why, which providers receive it, and how it is retained/deleted.
- Collect only fields required for the bid-readiness use case.
- Provide a supported way to correct profile facts and request deletion where applicable.
- Maintain data-processing/vendor agreements as required.
- Define incident response, access reviews, and breach handling.
- Restrict access to documents and logs; record important access and administrative events.
- Avoid including personal/financial information in analytics, support tickets, or stack traces.
- Define retention for original files, extracted text, reports, snapshots, backups, and audit logs. Deleting only the source PDF while keeping all extracted text may not satisfy the product's intended deletion semantics.
- Review whether documents may include personal information belonging to owners, employees, references, or third parties.

This checklist is a design starting point, not a full legal compliance assessment.

## 8. Procurement Policy and Eligibility Guardrails

The product must not encode an assumption such as "all MSMEs are exempt from EMD" or "small sellers do not need experience." Public Procurement Policy benefits have eligibility and scope conditions; the official [MSME policy page](https://my.msme.gov.in/MyMsme/Reg/PPP_Home.aspx) describes policy provisions for MSE procurement and notes policy context/scope. The specific tender, applicable rules, supplier category, documentation, and current amendments must be checked.

Important distinctions:
- Eligibility, qualification, and evaluation criteria serve different purposes in official procurement guidance.
- A clause may be conditional, limited to a particular seller category, or subject to an exception elsewhere.
- A tender may define what proof counts and which financial periods or similar projects are accepted.
- Exemption claims need supporting evidence and must be checked against the actual tender and current applicable policy.
- Performance security is not the same obligation as bid security/EMD; identify the relevant clause and timing.
- A missing uploaded certificate means "not found among supplied files" unless the user has confirmed the evidence inventory complete.
- The product should not submit bids, sign declarations, or make certifications on a seller's behalf.

When a clause cannot be safely interpreted, state the source text and ask for human/procurement-professional review.

## 9. Secure Secrets and Infrastructure

- Store provider keys in a managed secret store or secured server-side environment; never hard-code them in the client bundle or Git.
- Use separate least-privileged identities for API, worker, storage, database, and deployment processes.
- Encrypt traffic and storage using maintained platform capabilities.
- Patch libraries for PDF parsing, OCR, web frameworks, and image decoding.
- Keep backups access-controlled and test restore procedures.
- Use per-environment secrets and data; do not copy customer production documents into development without approval and protection.
- Set quotas and cost alerts. An alert is not necessarily a hard spend cap.
- Verify a chosen hosting provider's region and contractual terms instead of assuming a specific compliance posture.

## 10. Pre-Pilot Security Checklist

- [ ] Authentication and recovery flows are tested.
- [ ] Tenant isolation is tested for every API/resource type.
- [ ] Upload type, size, page-count, and parser-failure paths are tested.
- [ ] Documents are private by default.
- [ ] Export links are authorized and expire as intended.
- [ ] Prompt-injection and unauthorized retrieval tests pass.
- [ ] API/model/storage secrets are not committed to source control.
- [ ] Model and OCR provider terms are reviewed.
- [ ] Retention and deletion behavior includes extracted text and backups.
- [ ] Privacy notice and user-facing limitations are reviewed.
- [ ] High-risk procurement conclusions require source evidence and appropriate human review.
- [ ] Incident, credential-rotation, backup, and deletion processes are documented.
- [ ] Qualified review of applicable privacy/procurement rules has happened before a commercial launch.

## References

- [OWASP File Upload Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/File_Upload_Cheat_Sheet.html)
- [Digital Personal Data Protection Act, 2023](https://www.indiacode.nic.in/indiacode/handle/123456789/22037?view_type=browse)
- [Digital Personal Data Protection Rules, 2025](https://www.meity.gov.in/documents/act-and-policies/digital-personal-data-protection-rules-2025-gDOxUjMtQWa?pageTitle=Digital-Personal-Data-Protection-Rules-2025)
- [MSME Public Procurement Policy](https://my.msme.gov.in/MyMsme/Reg/PPP_Home.aspx)
- [Department of Expenditure procurement manuals](https://doe.gov.in/en/manuals)
