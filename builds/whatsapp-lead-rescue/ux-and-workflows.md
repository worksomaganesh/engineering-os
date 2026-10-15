# WhatsApp Lead Rescue — UX and Workflows

## 1. Home screen: Follow-Ups Due Now
The central screen is an ordered action queue, not a generic analytics dashboard.

Example fictional data:

| Priority | Lead | What happened | Why it appears | Next action |
|---|---|---|---|---|
| High | Rahul | Asked for ₹80k package | No later business reply detected in this export | Reply with package details |
| High | ABC Industries | Asked for technical proposal | A promise appears in the messages; completion isn't confirmed | Confirm proposal status |
| Medium | Priya | Quote discussed yesterday | Export doesn't prove quote attachment was sent | Verify, then schedule follow-up |
| Medium | Karthik | Requested demo | No owner or next step recorded | Assign owner and propose times |

Each row should show contact label, last relevant message/time, lead stage, conversation state, priority reason, suggested action, owner, due time, source evidence, review state, and quick actions.

Do not label a lead as "lost revenue" just because a response is late. The system generally cannot know the outcome unless a user records it.

## 2. Keep four concepts separate
- **Lead stage:** where the opportunity sits in the sales process.
- **Conversation state:** whether the next response is expected from the business, customer, or is ambiguous.
- **Task state:** whether the internal action is open, snoozed, completed, or dismissed.
- **Priority:** how soon the action should be handled, with an explainable reason.

Do not overload all four into one AI-generated status.

## 3. Import screen
Suggested copy:
- "Upload a WhatsApp chat export (.txt)."
- "This imports the exported conversation for follow-up analysis."
- "If you exported without media, omitted images, voice notes, PDFs, and attachments won't be analyzed."
- "This import does not connect to your live inbox or send a customer message."
- "Only upload conversations you are authorized to process."

After import show file name/size, recognized message count, unparsed lines, date span, participant list, selected business sender, missing-media warning, analysis status, and retry option.

## 4. Review a suggestion
Example:

**Candidate action:** Send quotation  
**Evidence:** "I'll send you the quotation by this evening."  
**Timestamp:** 14 October, 11:20  
**Due time:** Suggested for 14 October, 18:00 — confirm or change  
**Why:** This message contains a first-person commitment and a time phrase.  
**Actions:** Accept · Edit · Reject

The UI must distinguish:
- Explicit promise with a clear deadline.
- Explicit promise without a clear deadline.
- Inferred follow-up opportunity.
- Customer request with no detected answer.
- Ambiguous language requiring review.

A suggested action must not be presented as proof that the salesperson definitely made that promise.

## 5. Explainable detection rules
### Unanswered inbound
If a prospective customer asks a question and there is no later message from the confirmed business participant in the imported timeline, create a candidate reply-needed task. Consider incorrect sender mapping, replies outside the export, closed conversations, non-lead chats, and bad timestamps.

### Explicit promise
If the business writes "I'll share the brochure by 6 PM", create a candidate task linked to that message. Use the explicit deadline only when unambiguous; otherwise ask the user to choose a time.

### Quote/proposal
"Selling/sending the quote now" is evidence of a promise, not proof that an attachment was actually sent. If the export doesn't prove it, show "verify whether sent".

### Waiting for customer
A follow-up may be suggested based on the business's policy, but the suggested time must be editable. Silence alone must not trigger automatic customer messages.

### Opt-out
A request to stop contact suppresses follow-up recommendations that would cause outbound contact. If ambiguous, ask a human to review.

## 6. Prioritization
Use explainable factors:
- Confirmed overdue commitment.
- Explicit customer question with no later business reply.
- Time since the inbound message.
- Customer's stated deadline or callback time.
- Confidence in the extraction, based on measured performance.
- Unassigned owner.
- Existing overdue task.
- User-defined importance.

Show a human-readable reason. Do not claim a conversion probability without validated outcome data. Deduplicate overlapping actions from the same message.

## 7. Task lifecycle
~~~text
AI suggests action
       |
Human reviews source context
       |
       +---- reject / not a lead ----> dismissed
       |
       v
Accept or edit
       |
Assign owner + due time
       |
Open task in action queue
       |
       +---- snooze ----> update due time, keep history
       +---- complete --> completion record
       +---- cancel ----> record reason
~~~

Reminder jobs must be idempotent. Repeated worker execution should not create notification spam. Changes to a task should reschedule or cancel pending reminders.

## 8. Notifications
Start with in-app reminders or email digests. Provide quiet hours, timezone, digest/individual preference, suppression after completion, and escalation settings. Avoid unnecessary customer information in notification previews.

Do not send outbound WhatsApp messages automatically in the MVP. If added later, use the official API and comply with current opt-in, opt-out, template, customer-service-window, and messaging policy requirements.

## 9. Team view (later)
- Open/overdue tasks by owner.
- Unassigned leads.
- Leads without next action.
- Median first-response time.
- Promised actions completed on time.
- Lead stages and age.
- Import and parse-quality warnings.

Avoid raw message volume as an employee productivity metric; it rewards unnecessary messaging and lacks context.

## 10. Empty and error states
Design for: no import, no recognized messages, no actions detected, everything up to date, malformed lines, provider unavailable, analysis running, conflicting task edits, unassigned owner, ambiguous deadline, omitted media, unauthorized workspace access, and deletion request.

Status must not rely only on red/green colors. Support keyboard navigation and visible focus states.

## 11. Example user session
1. A coaching institute owner exports three recent conversations.
2. The app asks them to identify the business sender.
3. It detects one unanswered pricing question, one promise to send a brochure, and one quote whose attachment isn't confirmed by the export.
4. The owner checks each source, accepts two suggestions, edits one, and dismisses a personal chat.
5. The dashboard shows two tasks with owners and due times.
6. Salespeople reply manually in WhatsApp and mark tasks complete.
7. At week's end, the owner compares task completion and first-response time with baseline.

The MVP succeeds if this small workflow reliably saves effort. Live integration comes only after users repeatedly request it.
