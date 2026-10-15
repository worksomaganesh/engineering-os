# GeM Tender Copilot — Evidence-First Bid Readiness for Indian MSMEs

> **Product promise:** Upload a tender and your company's supporting documents. Get an evidence-backed view of what appears to be satisfied, what is missing, what needs verification, and what could put the bid at risk—before investing time and money in a submission.

**Status:** Research-backed product concept and implementation blueprint. This folder documents the intended product; it does not imply that a working app has already been built.

## 1. The Problem

A public tender can spread important obligations across the main bid document, technical specifications, annexures, declarations, financial conditions, schedules, and later corrigenda. A seller must work out whether the company qualifies, which proof is acceptable, which forms need signing, and what deadlines or changes matter.

The difficult question is not simply "What does this PDF say?" It is:

**"Given this exact tender version and the evidence my company can provide, what is satisfied, what is not established, what is missing, and what needs a human decision before we bid?"**

Errors can be costly. The [Department of Expenditure's Manual for Procurement of Goods, Second Edition (2024)](https://doe.gov.in/files/circulars_document/Manual_Goods_2024.pdf) distinguishes eligibility criteria, qualification criteria, and evaluation criteria. They are related but not interchangeable; a tool must preserve the actual clause language and context instead of flattening every condition into a generic checklist.

## 2. Why This Is a Worthwhile Problem to Explore

Official Government of India releases provide scale signals:
- A PIB release dated **7 August 2026** reported GeM cumulative gross merchandise value (GMV) above **₹20 lakh crore** and more than **3.78 crore orders** since inception. [Source](https://www.pib.gov.in/PressReleasePage.aspx?PRID=2296138&lang=1&reg=48)
- A PIB release dated **11 August 2026** reported MSME procurement through GeM of about **₹2.37 lakh crore in FY 2025–26**, and **11,75,001 MSMEs registered as of 30 July 2026**. [Source](https://www.pib.gov.in/PressReleasePage.aspx?PRID=2297820&lang=1&reg=48)

These figures support the relevance of investigating the problem; they do **not** prove customer demand, willingness to pay, or product-market fit. Validate those with sellers and procurement professionals before committing to a business.

GeM also publishes a seller learning path including **Bid and RA Participation**, and its bid listing explicitly surfaces corrigenda and warns that published changes may modify technical specifications, terms, and schedules. [GeM seller learning portal](https://elearning.gem.gov.in/course/index.php?categoryid=2) · [GeM bid listing](https://bidplus-global.gem.gov.in/).

## 3. Who It Is For

**Primary user:** an Indian micro, small, or medium enterprise (MSME) seller evaluating a tender and preparing a compliant bid.

**Other users:** a tender consultant serving multiple sellers; a bid manager; a finance or compliance team member gathering evidence; a technical employee verifying specifications.

The first release should focus on one seller and one tender at a time. Avoid turning the first version into a generic tender search engine, a marketplace, or a fully autonomous bid-submission robot.

## 4. What the Product Produces

1. **Bid-readiness summary:** an evidence-backed status for each important requirement.
2. **Eligibility and qualification matrix:** what the tender asks for, the exact source passage, the seller evidence, and the remaining gap.
3. **Mandatory-document checklist:** required proof, evidence found, document/page reference, expiry/validity where relevant, and next action.
4. **Disqualification-risk register:** material conditions that appear unmet, lack proof, conflict with other documents, or require expert verification.
5. **Technical compliance matrix:** specification → seller product/service evidence → match, mismatch, or unresolved detail.
6. **Deadline calendar:** bid close, clarification deadline, pre-bid meeting, opening dates when specified, and a warning that dates must be checked against the latest official notice.
7. **Corrigendum impact report:** which dates, thresholds, clauses, and deliverables changed between manually supplied document versions.
8. **Evidence-linked export:** a PDF or spreadsheet report with source page numbers, quoted clauses, analysis version, and review status.

The product should use nuanced states such as **Evidence found**, **Likely matches**, **Missing evidence**, **Possible mismatch**, **Conflicting evidence**, **Needs human verification**, and **Not applicable with explanation**. A missing document is not always proof that the company is ineligible.

## 5. Non-Negotiable Product Principle

**Every material conclusion must be traceable to source text and evidence.** If the system cannot show the tender clause and the supporting or missing evidence, it must show uncertainty instead of inventing an answer.

The Copilot is an analysis and preparation assistant—not the buyer, the GeM portal, a legal adviser, or the final authority on eligibility. Sellers must verify the latest official tender and amendments and make the final bid/no-bid and submission decisions themselves.

## 6. Proposed MVP

### In scope
- User uploads one tender PDF.
- User can manually upload one or more corrigenda/addenda as separate versions.
- User creates a simple seller profile and uploads company evidence documents.
- Pipeline extracts native PDF text and uses OCR when needed.
- System extracts requirements into a structured schema, each with clause/page evidence.
- Deterministic checks compare numeric/date/boolean conditions; AI assists with classification and semantic matching.
- User sees a readiness report, missing-evidence checklist, risk register, deadlines, and a source-linked compliance matrix.
- Human review/edit/confirm actions are recorded.
- Export a report for internal review.

### Explicitly out of scope at first
- Scraping the entire GeM portal or maintaining a live tender crawler.
- Assuming undocumented GeM APIs or bypassing access controls.
- Automated login, digital signing, price submission, or bid submission on the user's behalf.
- Guaranteeing eligibility, legal compliance, bid acceptance, or winning a tender.
- Applying a general MSE/Startup/other exemption without verifying the current rule and exact tender conditions.
- Building an exhaustive rule engine for every government procurement category at launch.

## 7. Architecture at a Glance

```text
Web UI
  -> authenticated upload API
  -> private object storage
  -> background document-processing job
  -> text extraction / OCR / layout parsing
  -> tender clause and requirement extraction
  -> schema validation + evidence/page verification
  -> deterministic rules + semantic evidence matching
  -> human review
  -> readiness dashboard, calendar, matrix, and export
```

A sensible first-stack proposal is React + TypeScript for the UI, Python + FastAPI for the API/processing services, PostgreSQL for structured records, private object storage for files, and a job queue for long-running PDF/OCR/LLM processing. These are recommendations to validate, not mandatory technology choices.

## 8. Documentation Pack

- [Product requirements and user experience](product-requirements.md)
- [Technical architecture and processing pipeline](technical-architecture.md)
- [Data model and evidence schemas](data-model.md)
- [Evaluation, test strategy, and release gates](evaluation-plan.md)
- [Security, privacy, and procurement-risk controls](security-and-compliance.md)
- [Roadmap, validation plan, and open decisions](roadmap.md)

## 9. Research Notes and Sources

- [PIB: GeM crosses ₹20 lakh crore cumulative GMV, 7 August 2026](https://www.pib.gov.in/PressReleasePage.aspx?PRID=2296138&lang=1&reg=48)
- [PIB: MSME procurement through GeM reaches ₹2.37 lakh crore in FY 2025–26, 11 August 2026](https://www.pib.gov.in/PressReleasePage.aspx?PRID=2297820&lang=1&reg=48)
- [GeM official bid listing](https://bidplus-global.gem.gov.in/)
- [GeM Interactive LMS — Seller Journey, including Bid and RA Participation](https://elearning.gem.gov.in/course/index.php?categoryid=2)
- [Department of Expenditure: Manual for Procurement of Goods, Second Edition, 2024](https://doe.gov.in/files/circulars_document/Manual_Goods_2024.pdf)
- [Department of Expenditure: official procurement manuals index](https://doe.gov.in/en/manuals)
- [MSME Ministry: Public Procurement Policy for MSEs](https://my.msme.gov.in/MyMsme/Reg/PPP_Home.aspx)
- [Google Cloud Document AI: overview of document extraction and OCR concepts](https://docs.cloud.google.com/document-ai/docs/overview)
- [Google Cloud Document AI: supported files and quality notes](https://docs.cloud.google.com/document-ai/docs/file-types)
- [OWASP File Upload Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/File_Upload_Cheat_Sheet.html)
- [Digital Personal Data Protection Act, 2023 — India Code](https://www.indiacode.nic.in/indiacode/handle/123456789/22037?view_type=browse)
- [Digital Personal Data Protection Rules, 2025 — MeitY](https://www.meity.gov.in/documents/act-and-policies/digital-personal-data-protection-rules-2025-gDOxUjMtQWa?pageTitle=Digital-Personal-Data-Protection-Rules-2025)

**Legal and policy caution:** procurement manuals are guidance, and the actual tender, applicable procurement rules, policies, amendments, and bidder-specific facts govern the decision. Policy applicability and enforcement timelines can vary. Obtain qualified procurement/legal review before representing any result as an eligibility determination.
