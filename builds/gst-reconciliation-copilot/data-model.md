# GST Reconciliation Copilot — Data Model

This is a proposed data model for the file-based MVP. It separates imported source data, normalized records, machine-generated suggestions, human decisions, and exported reports so the work remains auditable.

## 1. Relationship overview

~~~text
Workspace
 ├── Members
 ├── Client GST profiles
 ├── Imports
 │    └── Source rows
 │         └── Normalized records
 ├── Reconciliation runs
 │    ├── Match groups / candidate pairs
 │    ├── Exceptions
 │    ├── Exception evidence
 │    ├── Review events
 │    └── Exports
 └── Audit events
~~~

Every client-related resource must be scoped to an authorized workspace/client. A user-supplied client ID is not authorization.

## 2. Suggested entities

### workspaces
- `id` UUID primary key.
- `name`, `created_at`.
- `retention_policy_id`.
- Plan/usage fields only if billing is introduced.

### workspace_members
- `workspace_id`, `user_id`.
- `role`: owner, admin, preparer, reviewer, read-only.
- `created_at`.
- Unique constraint on workspace/user.

### clients
- `id`, `workspace_id`.
- `display_name`.
- Client GSTINs stored in a related table where multiple registrations are supported.
- `created_at`, `updated_at`.
- Avoid collecting unrelated client personal data.

### client_gst_registrations
- `id`, `client_id`, `gstin`.
- State/registration metadata only when needed.
- Effective dates/status if required by the workflow.
- Access controls and retention policy apply to this data.

### imports
- `id`, `workspace_id`, `client_id`, `uploaded_by_user_id`.
- `source_type`: purchase_register / gstr2b.
- `original_filename` (display-only; never use as storage path).
- `private_storage_key`.
- `content_hash`, `file_size_bytes`, `file_format`.
- `tax_period`, `target_gstin`.
- `status`, `warning_count`, `error_count`.
- `sheet_manifest` and confirmed mapping version.
- `created_at`, `completed_at`.
- `parser_version`, `normalization_version`.

### source_rows
- `id`, `workspace_id`, `import_id`.
- `sheet_name`, `row_number`.
- `raw_values` JSON or protected raw-row reference.
- `row_hash`.
- `validation_status`, `validation_messages`.
- Unique constraint on import/sheet/row.
- Avoid duplicating confidential data in routine logs.

### normalized_records
- `id`, `workspace_id`, `import_id`, `source_row_id`.
- `source_type`, `record_category`.
- `supplier_gstin`, `recipient_gstin` where available.
- `document_type`, `document_number_original`, `document_number_key`.
- `document_date`, `document_date_raw`.
- `taxable_value_decimal`.
- `igst_decimal`, `cgst_decimal`, `sgst_utgst_decimal`, `cess_decimal`.
- `invoice_total_decimal`.
- `place_of_supply`, `reverse_charge_indicator`.
- `financial_period`, `amendment_reference`, `original_document_reference`.
- `normalization_warnings`.
- Currency amounts should use fixed-precision decimal database types, not binary floating-point.

Only include fields actually available in a given source. A null means "not supplied/known"; it is not the same as numeric zero.

### reconciliation_runs
- `id`, `workspace_id`, `client_id`.
- `purchase_import_id`, `gstr2b_import_id`.
- `tax_period`, `target_gstin`.
- `status`: created, processing, needs_review, reviewed, failed, cancelled.
- `rule_set_version`, `normalization_version`, `matching_engine_version`.
- `configuration_snapshot` (tolerances and selected categories).
- `source_row_counts`, `summary_totals`.
- `started_at`, `completed_at`, `created_by`.
- A run should be reproducible from immutable source imports and its rule/configuration snapshot.

### match_groups
- `id`, `workspace_id`, `run_id`.
- `match_status`: exact_match, candidate_match, reviewed_match, mismatch.
- `matching_method`, `rule_version`.
- `candidate_score` nullable and only meaningful if calibrated.
- `review_status`, `created_at`.
- A group may relate one record on each side for ordinary invoice matching; more complex amendment relationships should be represented explicitly rather than forced into a one-to-one model.

### match_group_records
- `match_group_id`, `normalized_record_id`, `side` (books / gstr2b).
- Constraints prevent a record from being assigned to conflicting active match groups within the same run unless a documented many-to-one rule applies.

### exceptions
- `id`, `workspace_id`, `run_id`, `match_group_id` nullable.
- `exception_type`, `severity`, `status`.
- `taxable_difference_decimal`, `igst_difference_decimal`, `cgst_difference_decimal`, `sgst_utgst_difference_decimal`, `cess_difference_decimal`.
- `explanation_code`, `suggested_action`.
- `assigned_user_id`, `due_at`.
- `created_at`, `updated_at`, `resolved_at`.
- Difference sign convention must be documented (for example, books minus GSTR-2B).

### exception_evidence
- `id`, `workspace_id`, `exception_id`.
- `normalized_record_id`, `source_row_id`.
- `evidence_role`: books_side, gstr2b_side, duplicate_candidate, amendment_link, reviewer_attachment.
- `field_name`, `observed_value`, `comparison_value`.
- Evidence should refer back to source rows; don't rely solely on an AI-written paragraph.

### review_events
- `id`, `workspace_id`, `exception_id`, `actor_user_id`.
- `event_type`: accepted_match, rejected_match, note_added, assigned, status_changed, resolved, reopened.
- `previous_state`, `new_state`, `reason`, `created_at`.
- Preserve original machine result when a reviewer makes a decision.

### exports
- `id`, `workspace_id`, `run_id`, `requested_by`.
- `format`, `private_storage_key`, `status`, `created_at`, `expires_at`.
- Only authorized workspace members may download.
- Expire/delete exports under the retention policy.

### audit_events
- `id`, `workspace_id`, `actor_user_id`.
- `event_type`, `resource_type`, `resource_id`, `timestamp`.
- `safe_metadata` JSON.
- Do not put full invoice rows, passwords, or secrets in audit metadata.

## 3. Important invariants

- Every normalized record traces to exactly one source row.
- Every match group belongs to one reconciliation run and authorized workspace.
- No record may silently match two unrelated counterpart records.
- A candidate pair is not an exact match until the defined rules prove it or a reviewer confirms it.
- Missing tax-head data is not treated as zero unless the source format/rule explicitly establishes that interpretation.
- All differences use fixed-precision arithmetic and one documented sign convention.
- Duplicate candidates remain visible; they are not silently removed from the source.
- Manual decisions are append-only events or versioned changes, not destructive overwrites.
- A run records exact input imports and rule versions.
- Deleted client data must be removed from source files, normalized rows, exports, caches, and other derived artifacts according to policy.

## 4. Example normalized record

Illustrative only; not an actual GST record:

~~~json
{
  "source_type": "purchase_register",
  "record_category": "invoice",
  "supplier_gstin": "29ABCDE1234F1Z5",
  "document_type": "invoice",
  "document_number_original": "INV-1042",
  "document_number_key": "INV1042",
  "document_date": "2026-09-12",
  "taxable_value_decimal": "82000.00",
  "igst_decimal": "14760.00",
  "cgst_decimal": null,
  "sgst_utgst_decimal": null,
  "cess_decimal": null,
  "source_reference": {
    "file": "purchase_register.xlsx",
    "sheet": "September",
    "row": 18
  }
}
~~~

The GSTIN and figures above are fictional examples for schema illustration. Validation rules must not use a sample GSTIN as a real client identity.

## 5. Indexes and constraints

Potential indexes:
- `normalized_records(import_id, supplier_gstin, document_number_key)`.
- `normalized_records(import_id, document_date)`.
- `exceptions(run_id, status, exception_type)`.
- `exceptions(workspace_id, assigned_user_id, due_at)`.
- `source_rows(import_id, sheet_name, row_number)`.
- Unique content hash per workspace/import only if duplicate upload policy says identical files should be treated as one.
- Foreign keys on workspace, client, import, run, source row, and review-event relationships.
- Unique event/job IDs for idempotent processing.

Consider row-level security as defense in depth; it does not replace correct server-side authorization.
