# GeM Tender Copilot — Data Model and Evidence Schemas

The most important data-model decision is to keep **source documents, extracted facts, requirements, evidence links, rule evaluations, and human review decisions separate**. If an AI output is stored as a single summary paragraph, it becomes hard to audit or correct.

## 1. Entities and Relationships

```text
User
  |
  +-- WorkspaceMembership --> Workspace / SellerCompany
                                  |
                                  +-- SellerProfile
                                  +-- EvidenceDocument --> EvidenceVersion
                                  |                         |
                                  |                         +-- ExtractedFact(s)
                                  |
                                  +-- TenderReview
                                         |
                                         +-- TenderDocument --> DocumentVersion
                                         |                       |
                                         |                       +-- PageText / LayoutBlock
                                         |                       +-- CorrigendumVersion
                                         |
                                         +-- Requirement(s)
                                         |       |
                                         |       +-- RequirementEvidenceLink --> EvidenceFact
                                         |       +-- RuleEvaluation(s)
                                         |       +-- HumanReview(s)
                                         |
                                         +-- AnalysisRun(s)
                                         +-- Deadline(s)
                                         +-- ReportExport(s)
                                         +-- AuditEvent(s)
```

Use UUIDs or another non-guessable identifier for records exposed through APIs. Every tenant-owned record should carry a workspace/tenant reference or be securely reachable only through an authorized parent. Enforce isolation in application code and, where suitable, database policies.

## 2. Core Tables

### Workspace / SellerCompany
- `id`
- `name`
- `company_type`
- `business_categories`
- `created_at`
- `updated_at`

### WorkspaceMembership
- `workspace_id`
- `user_id`
- `role` (owner, reviewer, contributor, read-only)
- `created_at`

### SellerProfile
- `workspace_id`
- `legal_name`
- `registration_facts` (structured, source-linked facts rather than unreviewed free text)
- `product_and_service_categories`
- `claimed_statuses` (for example, MSE/startup/OEM relationship; each claim requires evidence and applicable conditions)
- `reviewed_at`
- `created_at`
- `updated_at`

### Document
- `id`
- `workspace_id`
- `parent_tender_id` (nullable for reusable company evidence)
- `document_kind` (tender, corrigendum, company evidence, output)
- `original_filename` (display only; never use it as a storage path)
- `storage_key` (private object identifier)
- `sha256`
- `mime_type_detected`
- `file_size_bytes`
- `page_count`
- `status`
- `uploaded_by`
- `created_at`
- `deleted_at`

### DocumentVersion
- `id`
- `document_id`
- `version_number`
- `published_date` (nullable)
- `uploaded_at`
- `supersedes_version_id` (nullable)
- `source_type` (original tender, amendment, seller evidence revision)
- `checksum`
- `is_latest_known`
- `extraction_version`

Do not overwrite a tender PDF when the user uploads a corrigendum. Store each version and explicitly connect it to the prior version.

### PageText / LayoutBlock
- `id`
- `document_version_id`
- `page_number` (1-based for display)
- `block_id`
- `block_type` (paragraph, heading, table_cell, footer, form_field, etc.)
- `text`
- `bounding_box` (optional page coordinates)
- `extraction_method` (native text, OCR, provider)
- `ocr_confidence` (nullable)
- `reading_order`
- `quality_flags`

Preserve tables and the headings/units that explain their values. Text position and page number are part of the evidence, not cosmetic metadata.

### Requirement
- `id`
- `tender_review_id`
- `document_version_id`
- `category`
- `requirement_type`
- `title`
- `normalized_statement`
- `source_quote`
- `source_page_start`
- `source_page_end`
- `clause_number` (nullable)
- `condition_text` (nullable)
- `operator` (>=, <=, equals, contains, requires-document, semantic-review, etc.)
- `threshold_value` (typed/normalized when possible)
- `unit` (nullable)
- `currency` (nullable)
- `period` (nullable, e.g. financial year)
- `required_evidence_types`
- `severity`
- `extraction_confidence`
- `review_status`
- `created_in_analysis_run_id`
- `superseded_by_requirement_id` (nullable)

The original clause quote must remain available even when an analyst edits the normalized statement.

### EvidenceFact
- `id`
- `document_version_id`
- `fact_type`
- `normalized_value` (typed or structured)
- `original_value`
- `unit` and `currency` (nullable)
- `period_start` / `period_end` (nullable)
- `issuer` / `entity_name` (nullable)
- `issue_date` / `expiry_date` (nullable)
- `source_page_start` / `source_page_end`
- `source_quote`
- `extraction_confidence`
- `human_verification_status`
- `verified_by` / `verified_at` (nullable)

Presence of an uploaded file is not equivalent to verifying its authenticity, validity, or legal acceptability.

### RequirementEvidenceLink
- `id`
- `requirement_id`
- `evidence_fact_id`
- `match_type` (exact, deterministic, semantic-suggested, user-selected)
- `match_explanation`
- `match_confidence`
- `review_status`
- `created_at`

### RuleEvaluation
- `id`
- `requirement_id`
- `analysis_run_id`
- `rule_id`
- `rule_version`
- `result_status`
- `inputs_snapshot`
- `explanation`
- `evidence_ids`
- `evaluated_at`

### Deadline
- `id`
- `tender_review_id`
- `document_version_id`
- `deadline_type`
- `raw_date_text`
- `normalized_datetime` (nullable)
- `timezone` (nullable)
- `source_page`
- `confidence`
- `confirmation_status`
- `supersedes_deadline_id` (nullable)
- `reminder_settings`

Never create a normalised deadline if the date or time is ambiguous. Retain the raw source text and request confirmation.

### AnalysisRun
- `id`
- `tender_review_id`
- `tender_version_ids`
- `seller_evidence_version_ids`
- `prompt_or_schema_version`
- `model_provider_and_version`
- `ruleset_version`
- `status`
- `started_at` / `completed_at`
- `failure_stage` (nullable)
- `token_or_page_usage` (where available)
- `estimated_or_reported_cost` (nullable)

### HumanReview
- `id`
- `requirement_id` or `rule_evaluation_id`
- `reviewer_id`
- `previous_status`
- `new_status`
- `decision_reason`
- `created_at`

### AuditEvent
- `id`
- `workspace_id`
- `actor_id`
- `action`
- `target_type`
- `target_id`
- `timestamp`
- `metadata` (redacted; avoid copying secret or whole document contents into logs)

## 3. Stable Requirement Statuses

Suggested normalized statuses:
- `supported`
- `missing_evidence`
- `potential_mismatch`
- `not_established`
- `conflicting_evidence`
- `not_applicable_reviewable`
- `human_verification_required`
- `rule_failed_pending_review`

Presentation labels can be friendlier, but do not merge missing evidence and confirmed failure into one status.

A rule evaluation should also retain why its result was assigned. For example, "Turnover threshold not demonstrated" is different from "Verified turnover is below required threshold."

## 4. Example Extracted Requirement Object

This is illustrative JSON for a fictional tender clause, not a statement about any current tender:

```json
{
  "requirement_id": "req-example-001",
  "category": "financial_capacity",
  "requirement_type": "numeric_threshold",
  "normalized_statement": "Average annual turnover must be at least INR 5000000 for the three specified financial years.",
  "source": {
    "document_version_id": "docver-example-tender-v1",
    "page_start": 18,
    "page_end": 18,
    "clause_number": "4.2",
    "quote": "Illustrative clause text: average annual turnover shall be not less than INR 50 lakh for the last three financial years."
  },
  "comparison": {
    "operator": ">=",
    "threshold": 5000000,
    "currency": "INR",
    "period": "three financial years specified in the tender"
  },
  "required_evidence_types": [
    "audited_financial_statements",
    "turnover_certificate"
  ],
  "severity_candidate": "high",
  "extraction_confidence": 0.92,
  "review_status": "not_reviewed"
}
```

The product must never replace the illustrative quote with a made-up citation. In real analysis, store the actual source quote extracted from that uploaded document.

## 5. Example Rule Result

```json
{
  "requirement_id": "req-example-001",
  "result_status": "not_established",
  "explanation": "A turnover certificate was uploaded, but it covers only two of the three financial years requested. The available evidence is insufficient to establish the requirement.",
  "inputs": [
    {
      "evidence_fact_id": "fact-example-006",
      "period": "FY-1",
      "value": 4200000,
      "source_page": 2
    },
    {
      "evidence_fact_id": "fact-example-007",
      "period": "FY-2",
      "value": 5300000,
      "source_page": 3
    }
  ],
  "missing_or_unresolved": [
    "Required third financial year"
  ],
  "requires_human_review": true
}
```

This avoids pretending that incomplete evidence proves the seller's actual turnover was insufficient.

## 6. Versioning and Traceability

- Store the original uploaded binary immutably, subject to user deletion and retention rules.
- Store normalized text with the document version and page number.
- Associate every extraction and evaluation with an `AnalysisRun`.
- Do not mutate prior analysis results in place after a corrigendum or company evidence update; create a new run and compare outputs.
- Human corrections should be stored as review records or explicit overrides, with the actor and reason.
- The report should identify the version it analyzed and whether a newer version is known to the workspace.
- If a requirement is removed or changed by a corrigendum, preserve its prior state and map the newer requirement to the superseded one where possible.

## 7. Data Quality and Integrity Rules

1. Display page numbers consistently as human-readable 1-based pages, even if the parser uses a zero-based index internally.
2. Validate that each cited page exists in the exact referenced file version.
3. Keep units and currencies attached to numeric values; never compare ₹50 lakh with an unnormalised string such as "50" alone.
4. Preserve financial periods; turnover for one year cannot silently substitute for an average across several years.
5. Record if the evidence belongs to a parent, subsidiary, OEM, partner, or a different legal entity.
6. Treat date formats as ambiguous until normalized with an explicit interpretation.
7. Keep extracted and human-verified values distinguishable.
8. Do not store an opaque overall score as a replacement for per-requirement evidence and explanation.
