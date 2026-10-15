# WhatsApp Lead Rescue — Data Model

This is a proposed relational model for the export-based MVP. It deliberately separates a conversation, a lead, a detected action, and the task that a human accepts.

## 1. Entity relationship overview
```text
Workspace
 ├── Members
 ├── Imports
 │    └── Conversations
 │          └── Messages
 ├── Leads
 │    ├── Conversation links
 │    └── Evidence documents/notes (future)
 ├── Suggestions
 │    └── Source message references
 ├── Tasks
 │    ├── Task evidence
 │    ├── Task events
 │    └── Reminder jobs
 └── Audit events
```

All customer-owned entities must carry a workspace association directly or through a relation that can be checked securely. Never trust a client-provided workspace identifier as authorization.

## 2. Tables

### workspaces
- `id` UUID primary key
- `name`
- `timezone`
- `created_at`
- `retention_policy_id`

### workspace_members
- `workspace_id`
- `user_id`
- `role` (owner/admin/member/read-only)
- `created_at`
- Unique constraint on workspace/user.

### imports
- `id`
- `workspace_id`
- `uploaded_by_user_id`
- `original_filename` (display-only, never used as storage path)
- `storage_key` (private)
- `content_hash`
- `status` (queued/processing/needs_review/completed/failed/cancelled)
- `source_format`
- `message_count`
- `unparsed_line_count`
- `media_omitted`
- `started_at`, `completed_at`
- `parser_version`, `extractor_version`
- `error_code` (safe, not raw confidential content)

### conversations
- `id`
- `workspace_id`
- `import_id`
- `source_conversation_key` (if identifiable)
- `display_label`
- `business_participant_id`
- `start_at`, `end_at`
- `parse_quality`
- `state`
- `created_at`

A WhatsApp text export may represent only one conversation, not a complete live inbox. Do not pretend imported data is a real-time sync.

### participants
- `id`
- `workspace_id`
- `conversation_id`
- `display_name`
- `participant_type` (business/contact/unknown)
- `user_confirmed_type`
- `created_at`

### messages
- `id`
- `workspace_id`
- `conversation_id`
- `source_line_number`
- `source_timestamp_text`
- `timestamp_utc` nullable if timezone is unknown
- `sender_participant_id`
- `message_text` encrypted/controlled per policy
- `message_kind` (text/system/media-placeholder/unknown)
- `parse_confidence`
- `created_at`

Store the raw timestamp string and parsed timestamp separately. Do not silently invent a timezone for exports that lack one.

### leads
- `id`
- `workspace_id`
- `display_name`
- `contact_identifier` (optional, minimized/protected)
- `source` (import/manual/future-api)
- `stage` (new/qualified/quote_sent/waiting_for_customer/negotiation/won/lost/disqualified/unknown)
- `owner_user_id` nullable
- `status_confirmed_by_user`
- `created_at`, `updated_at`

### conversation_leads
- `conversation_id`
- `lead_id`
- `relationship_type`
- Unique constraint where appropriate to prevent duplicate links.

### suggestions
- `id`
- `workspace_id`
- `conversation_id`
- `lead_id` nullable
- `suggestion_type`
- `structured_payload` validated JSON
- `suggested_due_at` nullable
- `due_time_origin` (explicit/inferred/unknown)
- `confidence` nullable; calibrated only after evaluation
- `review_state` (needs_review/accepted/edited/rejected)
- `extractor_version`
- `created_at`, `reviewed_by`, `reviewed_at`

### suggestion_evidence
- `suggestion_id`
- `message_id`
- `evidence_role` (trigger/context/contradiction)
- `quoted_span` (optional; avoid unnecessary duplicate storage)
- Composite uniqueness to prevent duplicate evidence links.

### tasks
- `id`
- `workspace_id`
- `lead_id` nullable
- `conversation_id`
- `source_suggestion_id` nullable
- `task_type`
- `title`
- `description`
- `owner_user_id` nullable
- `due_at` nullable
- `due_time_origin` (explicit/user-set/suggested/unknown)
- `state` (open/snoozed/completed/dismissed/cancelled)
- `priority` and `priority_reason`
- `idempotency_key`
- `created_by`, `created_at`, `updated_at`, `completed_at`

### task_events
- `id`
- `workspace_id`
- `task_id`
- `actor_user_id`
- `event_type` (created/edited/assigned/snoozed/completed/dismissed/reopened)
- `previous_value`, `new_value` (structured and minimized)
- `reason`
- `created_at`

### reminder_jobs
- `id`
- `workspace_id`
- `task_id`
- `scheduled_for`
- `channel` (in-app/email)
- `status` (scheduled/sent/failed/cancelled)
- `deduplication_key`
- `attempt_count`
- `last_error_code`
- `created_at`, `sent_at`

### audit_events
- `id`
- `workspace_id`
- `actor_user_id`
- `event_type`
- `resource_type`, `resource_id`
- `timestamp`
- `safe_metadata` JSON

Avoid putting entire messages, access tokens, or sensitive documents into audit metadata.

## 3. Important invariants
- Every message belongs to a conversation and workspace.
- Every source evidence reference points to a message that exists in the same authorized workspace.
- A suggestion cannot become a confirmed task without an allowed review path.
- Due-time origin is always explicit, user-set, suggested, or unknown.
- A suggested date is never displayed as a definite promise made by a salesperson.
- One source action should not create multiple active duplicate tasks.
- Completing/cancelling a task cancels pending reminders.
- An opt-out/stop-contact flag suppresses outbound follow-up recommendations.
- Deletion must include originals, parsed text, suggestions, tasks that contain customer data, cached results, and defined backup-expiry behavior.

## 4. Example extraction payload
Illustrative schema payload (not an actual model response):

~~~json
{
  "suggestion_type": "send_quote",
  "action_title": "Confirm and send quotation",
  "due_time_origin": "suggested",
  "due_at": null,
  "review_required": true,
  "evidence": [
    {
      "message_id": "msg_123",
      "role": "commitment",
      "quote": "I'll send the quotation shortly."
    }
  ],
  "reason": "A quotation was promised, but no confirmed completion is present in this export."
}
~~~

The API must validate payload types, allowed enum values, message IDs, workspace access, and quote grounding. Treat model output as untrusted input.

## 5. Indexes and constraints
- Index `tasks(workspace_id, state, due_at)` for the action queue.
- Index `messages(conversation_id, timestamp_utc, source_line_number)`.
- Unique `imports(workspace_id, content_hash)` if the product treats identical files as one import; otherwise track duplicate imports explicitly.
- Unique reminder deduplication key.
- Foreign keys for workspace and task/message relations.
- Consider row-level security as defense in depth, not a replacement for correct server authorization.
