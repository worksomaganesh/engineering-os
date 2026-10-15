# WhatsApp Lead Rescue — Technical Architecture

## 1. Architecture principle
Start with an import-and-review pipeline, not a live messaging integration. Keep parsing, AI extraction, business rules, task management, and reminders as separate components. AI suggests; validated application logic and a human reviewer decide what becomes an active task.

## 2. High-level flow
```text
Browser / web UI
   |
   | authenticated upload
   v
API + authorization
   |
   +--> private object storage (original export, restricted access)
   |
   v
Import job queue
   |
   v
Format detector + parser
   |
   +--> normalized messages + parse warnings
   |
   v
Candidate extractor (rules + LLM behind an interface)
   |
   v
Schema validation + evidence checks
   |
   v
Candidate actions needing human review
   |
   v
User review + deterministic task rules
   |
   v
Follow-up dashboard + task database
   |
   v
Reminder scheduler --> in-app/email reminder
```

The diagram is the proposed architecture, not an assertion that these components already exist.

## 3. Component responsibilities

### Web UI
- Upload and explain export limitations.
- Ask the user to map sender identities.
- Display import progress and parse-quality warnings.
- Show source message context beside each candidate action.
- Support accept/edit/reject, assign, snooze, complete, and delete.
- Make the reason for priority visible.

### API and authorization
- Authenticate the user.
- Authorize access to every workspace, file, message, task, export, and job.
- Enforce file-size, text-length, rate, and job concurrency limits.
- Issue short-lived download links only after authorization.
- Never trust a workspace ID or owner ID supplied by the browser without server-side checks.

### File storage
- Store exports privately, not in a public web directory.
- Generate internal storage keys; don't use raw filenames as paths.
- Keep originals only as long as needed by the declared retention policy.
- Delete derived text, embeddings if any, cached content, and reports according to the same data lifecycle.

### Import parser
- Identify supported export format and probable locale/time format.
- Parse sender, timestamp, and message content while preserving original line number and order.
- Recognize common system messages and media placeholders.
- Return warnings for unknown lines, malformed timestamps, unsupported encodings, and missing media.
- Avoid silently converting ambiguous dates.
- Use deterministic parsers for known formats and a fallback review path for unknown formats.

### Candidate extractor
Use a hybrid approach:
1. Deterministic parsing identifies messages and chronology.
2. Rules identify obvious patterns such as questions and explicit "I'll send/call" commitments.
3. An LLM may classify intent and extract structured candidate actions from bounded context.
4. Output is validated against a strict schema.
5. Evidence message IDs must exist in the imported conversation.
6. Any unsupported inference is labelled suggested/uncertain.
7. Human review promotes candidates into active tasks.

Do not send the entire conversation to an LLM if a small relevant window is enough. Avoid sending confidential messages to a provider until its retention, training, regional processing, and contractual terms are reviewed.

### Rule engine
- Determine whether an inbound message has a later reply from the confirmed business participant in the imported timeline.
- Check whether an explicit promise has a due time and whether the due time passed.
- Distinguish a detected promise from proof that the promised attachment was actually sent.
- Suppress follow-up recommendations after an opt-out/stop-contact state.
- Avoid duplicate tasks for the same evidence/action.
- Keep lead stage, conversation state, task state, and priority separate.

### Task service
- Create, edit, assign, snooze, complete, cancel, and dismiss actions.
- Record actor, timestamp, prior/new state, and reason for important changes.
- Use idempotency keys for imports and reminder jobs.
- Cancel/reschedule pending reminders when a task changes.

### Reminder scheduler
- Use a durable queue or scheduled-job system rather than relying on a browser tab being open.
- Store the user's timezone and quiet hours.
- Deduplicate retries and track delivery/failure.
- Start with in-app or email reminders. WhatsApp outbound reminders require a separate official integration and policy review.

## 4. Proposed API surface
Illustrative endpoints only; not implemented.

| Method | Path | Purpose |
|---|---|---|
| POST | `/api/imports` | Create an authorized import job |
| GET | `/api/imports/{id}` | Check import and parse status |
| GET | `/api/conversations/{id}/messages` | Read authorized normalized messages |
| GET | `/api/conversations/{id}/suggestions` | Get source-linked candidate actions |
| POST | `/api/suggestions/{id}/review` | Accept/edit/reject a suggestion |
| GET | `/api/tasks?state=open` | Query the action queue |
| PATCH | `/api/tasks/{id}` | Update owner, due time, or task state |
| POST | `/api/tasks/{id}/snooze` | Snooze a task |
| GET | `/api/audit-events` | Read authorized workspace activity |

Every endpoint must enforce authorization at the resource level. Avoid placing message text or secrets in URLs and routine request logs.

## 5. Suggested technology choices

Choose technologies based on what the builder can maintain; this product does not require a custom AI model.

- **Frontend:** React + TypeScript, or another familiar web framework.
- **Backend:** Python/FastAPI or TypeScript/Node. Python is convenient for text parsing and ML evaluation; TypeScript can simplify a single-language web stack.
- **Database:** PostgreSQL for workspaces, tasks, normalized messages, review history, and relations.
- **Object storage:** private S3-compatible or cloud object storage for uploaded exports.
- **Job queue:** a managed queue or durable worker system for imports and reminders.
- **AI:** provider-neutral extraction interface with a deterministic fallback for basic patterns.
- **Observability:** structured logs, job-stage metrics, error reporting, and cost tracking.
- **Deployment:** a managed app platform with private storage, secrets management, backups, and access controls.

These are options, not a mandatory stack. Start with a monolith plus background worker if the usage is small; microservices add operational complexity without proven need.

## 6. Import lifecycle and idempotency
1. Validate file and workspace access.
2. Compute a content hash for duplicate detection.
3. Create import record and enqueue one job.
4. Parse and persist normalized messages.
5. Generate candidate suggestions with model/rule versions.
6. Validate references and store suggestions.
7. Mark job completed or failed with a safe, user-readable error.
8. Allow controlled retry without duplicating messages or tasks.

A job should have explicit states such as `queued`, `processing`, `needs_review`, `completed`, `failed`, and `cancelled`.

## 7. Future official WhatsApp integration
When real users demonstrate demand:
- Use the official WhatsApp Business Platform/Cloud API, not browser scraping.
- Verify current onboarding, business permissions, webhook verification, and supported endpoints.
- Receive webhook events through a public HTTPS endpoint; verify authenticity as documented.
- Acknowledge events quickly and enqueue processing rather than running long model calls inside webhook requests.
- Handle retries, duplicates, and out-of-order events.
- Store event IDs and idempotency keys.
- Follow the current customer-service window, message-template, opt-in, opt-out, and quality rules.
- Keep inbound ingestion separate from outbound send authorization.
- Apply per-workspace quotas and messaging cost controls.
- Keep a human escalation path and an audit record for every outbound message.

Use the [official WhatsApp Business Developer Hub](https://whatsappbusiness.com/developers/developer-hub/) and [Meta's official Cloud API Postman collection](https://www.postman.com/meta/whatsapp-business-platform/overview?sideView=agentMode) to verify current details before implementation.

## 8. Operational visibility
Track:
- Import jobs by stage and failure type.
- Parser success and unparsed-line rates.
- AI calls, latency, and cost per import.
- Suggestions accepted, edited, and rejected.
- Tasks created per conversation and duplicate suppression.
- Reminder scheduling/delivery/failure.
- Workspace authorization failures and suspicious upload patterns.
- Retention/deletion job completion.

Do not log full customer messages by default. Prefer IDs, counts, stage, error class, and redacted diagnostic information.
