# WhatsApp Lead Rescue — Product Requirements

## Product statement
For small businesses whose enquiries arrive in WhatsApp, find conversations needing action, explain the reason with message evidence, assign an owner, and remind that person before a lead goes cold.

## Personas
- **Owner/operator:** needs a short, trustworthy list of unresolved sales conversations.
- **Salesperson:** needs next actions, promises, and deadlines without manually maintaining a large CRM.
- **Team lead:** needs ownership, overdue tasks, and handoff visibility.
- **Consultant/agency:** may manage several client workspaces; strict tenant separation is mandatory.

## Jobs to be done
1. Tell me which conversation needs attention now.
2. Show the message that triggered the recommendation.
3. Extract what I promised to send, prepare, call about, or demonstrate.
4. Distinguish a customer waiting for us from us waiting for the customer.
5. Tell me who owns the next step and when it is due.
6. Let me accept, edit, snooze, complete, or dismiss a task quickly.
7. Respect stop-contact requests and avoid repetitive outreach.
8. Show whether follow-up discipline is improving.

## MVP requirements (P0)
- Authenticated private workspace.
- User-uploaded WhatsApp chat export text file.
- Supported-format instructions and safe upload limits.
- Parser for timestamps, sender labels, and message text.
- Participant mapping: user confirms which sender represents the business.
- Import quality report, malformed-line visibility, date span, and missing-media warning.
- Candidate detection for inbound questions, unanswered latest inbound messages, explicit promises, quotes/proposals, calls, and demos.
- Source-linked suggestions with message IDs, timestamps, and short excerpts.
- Human review before uncertain findings become priority tasks.
- Action queue filters: due now, overdue, due today, waiting for customer, unassigned, completed.
- Assign, edit, snooze, complete, dismiss, and mark not-a-lead actions.
- Task history and idempotent reminders.
- Data export and deletion flow.
- Synthetic examples only in public repository; never commit real customer conversations.

## Out of scope for the first MVP
- Scraping WhatsApp Web or silently reading a private inbox.
- Bulk outbound campaigns or automatic customer follow-up.
- Full contact management, invoices, forecasting, call-center software, or giant CRM feature set.
- Whole-account import without deliberate user action.
- Automatic bidirectional sync before demand is validated.
- Claims that the system guarantees sales improvement.
- Healthcare data processing before a separate privacy and policy review.

## Import flow
1. User exports a conversation.
2. User uploads the text file and confirms authorization to process it.
3. App parses messages while preserving source line and timestamp.
4. App asks the user to identify the business participant.
5. Extractor suggests lead intent, action, deadline, conversation state, and evidence.
6. UI presents source messages beside every proposed action.
7. User accepts, edits, or rejects the suggestions.
8. Confirmed actions appear in the dashboard and reminders are scheduled.

If the export excludes media, the product cannot claim it analyzed images, voice notes, or PDFs that are absent from the file. The app must not interpret "no later reply found in this export" as proof that no reply was sent in another channel.

## Keep separate state dimensions
### Lead stage
`new`, `qualified`, `quote_sent`, `waiting_for_customer`, `negotiation`, `won`, `lost`, `disqualified`, `unknown`.

### Conversation state
`inbound_waiting_for_business`, `business_replied`, `waiting_for_customer`, `ambiguous`, `not_a_lead`.

### Task state
`suggested`, `needs_review`, `open`, `snoozed`, `completed`, `dismissed`, `cancelled`.

### Priority
Explainable ordering based on confirmed overdue commitment, unanswered customer question, explicit customer deadline, age, unassigned owner, and user-configured importance. Priority is not a conversion probability.

## Task types
- Reply to question.
- Send pricing or brochure.
- Prepare/send quotation.
- Send technical proposal/datasheet.
- Schedule or conduct call/demo.
- Confirm appointment.
- Ask for missing information.
- Follow up after quote/demo/meeting.
- Escalate internally.
- Respect opt-out / stop contact.
- Review ambiguous promise.

Each task stores source messages, creator, owner, due-time origin (explicit or suggested), review status, and history.

## User stories and acceptance criteria

### Import a chat
As a salesperson, I want to know whether my chat export was understood.
- Unsupported/corrupt files fail with actionable messages.
- Parser reports recognized and unparsed lines.
- Every finding points to a source timestamp and line/message ID.
- Reimporting the same file does not silently duplicate tasks.
- Missing media is clearly disclosed.

### Find unanswered inbound
As an owner, I want to see a prospective customer's question that has no later business reply in the imported timeline.
- The item displays the latest relevant inbound message and time.
- Business participant mapping is confirmed.
- Ambiguous timestamps and incomplete exports are flagged.
- User can reply manually, assign, snooze, or dismiss.

### Extract a promise
As a salesperson, I want "I'll send the quotation by 6 PM" turned into a task.
- The exact commitment is shown in context.
- Explicit deadline is distinguished from suggested time.
- Ambiguous promises require user review.
- User can edit or reject the task.

### Assign and remind
- Every open team task is assigned or marked unassigned.
- Reassignment and snooze events are recorded.
- Repeated jobs do not create duplicate reminders.
- Completed/cancelled tasks do not trigger reminders.
- Notification text avoids unnecessary customer details.

## Non-functional requirements
- **Traceability:** every AI finding cites source messages.
- **Privacy:** minimize retained text; support deletion.
- **Reliability:** imports, retries, and reminders are idempotent.
- **Security:** tenant isolation, private storage, least privilege, secret management.
- **Explainability:** show why an action is due.
- **Versionability:** record parser/model/rule versions.
- **Cost control:** page/character limits, queue limits, and cost monitoring.
- **Accessibility:** readable labels, keyboard navigation, status not conveyed by color alone.
- **Graceful failure:** parser failure must not look like an empty but healthy dashboard.

## Acceptance gate
Do not call the MVP validated until held-out tests show acceptable detection quality, users confirm that the action queue reduces effort, and the pilot measures actual follow-up behavior against a baseline. Numeric release thresholds must be chosen before examining holdout results.

## Later official integration
After validating the export-based workflow:
- Onboard an authorized business through the documented WhatsApp Business Platform.
- Receive events through documented webhooks and send messages only through approved APIs.
- Deduplicate retries and tolerate out-of-order events.
- Follow current opt-in, opt-out, template, and customer-service-window requirements.
- Keep outbound automation off by default until separately reviewed.
- Verify current pricing and provider fees.
- Never rely on undocumented WhatsApp Web scraping.
- See the [official Developer Hub](https://whatsappbusiness.com/developers/developer-hub/) and [Meta Postman collection](https://www.postman.com/meta/whatsapp-business-platform/overview?sideView=agentMode).

## Open questions
- Which first vertical has the most repeated pain?
- Which export formats and locales must be supported?
- How should group chats and aliases be handled?
- How are voice notes and omitted media disclosed?
- What default follow-up interval can be suggested without inventing a promise?
- Which reminder channel is preferred?
- What retention period is acceptable?
- Which provider terms permit processing message content?
- Do real users request official API integration after testing the export prototype?
