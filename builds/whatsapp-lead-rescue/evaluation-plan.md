# WhatsApp Lead Rescue — Evaluation and Testing Plan

A fluent AI suggestion is not necessarily a correct one. Evaluate parsing, action detection, evidence grounding, task behavior, and actual workflow value separately.

## 1. Build a labelled benchmark
Begin with 30–50 permitted/synthetic conversation exports for an initial engineering benchmark. This is a practical starting suggestion, not proof of statistical sufficiency. Keep a separate holdout set that is not used to tune prompts.

Include:
- Different Android/iOS export formats and locale/date formats.
- Different time zones and ambiguous timestamps.
- Chats with long threads, multiple senders, group-chat messages, and aliases.
- Short messages, emojis, code-switching, abbreviations, and common typos.
- Business replies that occur outside the imported export.
- Questions that are not sales leads (personal, spam, existing customer support).
- A promise with an explicit deadline, no deadline, or ambiguous timing.
- A quote discussed but no quote attachment visible.
- Multiple promises in one message.
- Repeated questions and duplicate messages.
- Customer stop-contact requests.
- Media placeholders where the media itself is omitted.
- No action required and no lead present.
- Malformed lines and incomplete exports.

Use synthetic conversations for edge cases and remove real personal information from any permitted evaluation samples. Do not put real customer chats in GitHub.

### Annotation guide
For every message/thread, label:
- Participant identity and direction (business/contact/unknown).
- Is it a lead? Why?
- Intent and requirement.
- Does it need a business response?
- Is there a clear business commitment?
- Exact source messages supporting the label.
- Task type, owner if explicit, due-time text, and due-time origin.
- Conversation state and lead stage if known.
- Opt-out/stop-contact signal.
- Ambiguities or missing context.

Use two independent reviewers for the high-risk subset and adjudicate disagreements. The ground truth should not assume that every silence is a lost lead or that every quote mention means a quote was delivered.

## 2. Core metrics

| Metric | Definition | Why it matters |
|---|---|---|
| Import parse success | Files successfully parsed into a useful timeline | Basic product reliability |
| Message extraction accuracy | Correct timestamp, sender, and text mapping | Bad chronology ruins downstream logic |
| Action precision | Of created candidate actions, fraction that are genuinely useful | Prevents alert fatigue |
| Action recall | Of labelled actionable situations, fraction detected | Finds missed leads/promises |
| Unanswered-message precision/recall | Correct detection of inbound questions without a later business response in the supplied timeline | Core MVP feature |
| Promise extraction precision | Correct commitments found, with correct task type | Prevents invented promises |
| Deadline exact match | Correct explicit deadline and timezone when stated | Avoids incorrect reminders |
| Evidence grounding rate | Every claim links to valid supporting message(s) | Makes recommendations verifiable |
| Unsupported claim rate | Findings without sufficient evidence | Trust-critical measure |
| Opt-out suppression accuracy | Stop-contact cases correctly suppress outbound follow-up | Safety and policy concern |
| Duplicate task rate | Repeated/overlapping actions that create duplicate active tasks | Prevents noisy dashboards |
| Suggestion acceptance rate | Accepted without edit, interpreted alongside error review | Measures usefulness, not correctness alone |
| Task completion rate | Due tasks completed on time | Measures workflow behavior |
| First response time | Time from inbound enquiry to first human business response | Outcome metric |
| Time saved | Human review time with/without tool | Tests core value proposition |
| Cost per import | Parsing/model/storage/notification cost per conversation | Business economics |

Report results by export format, language style, message length, and scenario. A single average can hide failures on ambiguous dates or code-switched messages.

## 3. Provisional release gates
These are starting internal targets to validate, not measured product results or public claims:
- 100% of displayed suggestions link to message IDs that exist in the imported conversation.
- No suggestion claims a deadline is explicit unless the supporting text and parser establish it.
- No outbound follow-up is triggered by a dismissed task or a detected stop-contact state.
- Zero critical opt-out suppression failures in the release test suite; any failure blocks release until fixed and regression-tested.
- Initially aim for at least 90% action precision on the curated holdout before broadening the pilot, then raise the gate based on observed false-alert cost.
- Set separate recall goals for unanswered questions and promised actions based on risk and observed user needs.
- All import failure paths are visible; failed parsing must not be shown as a healthy empty dashboard.
- Authorization and tenant-isolation tests pass before real data is used.

A high score on a small benchmark is not a guarantee of real-world accuracy. Review severe errors and confidence calibration manually.

## 4. Test categories

### Import/parser
- Valid export, empty file, wrong extension, corrupt encoding, huge file, duplicate upload.
- Locale variations, 12/24-hour clock, ambiguous day/month order, missing year/timezone.
- Sender names with punctuation, changed display name, group chat, system messages.
- Wrapped messages, multiline text, emoji, newline characters, quoted content.
- Media placeholders and omitted attachments.
- Malformed/unrecognized lines and partial export.

### Action detection
- Clear pricing request.
- Customer question followed by a business answer.
- Customer question with no later business message in export.
- Promise with exact deadline.
- Promise without deadline.
- Ambiguous phrase like "will try to send it".
- Quote discussed but no proof it was attached.
- Customer says they will respond later.
- Follow-up date agreed by both parties.
- Existing conversation that is not a lead.
- Opt-out, complaint, spam, or unrelated personal conversation.
- Same commitment repeated across messages.
- Conversation closed or marked won/lost by the user.

### Task logic
- Accept/edit/reject candidate.
- Change due time or owner.
- Snooze, complete, reopen, cancel.
- Reimport identical file.
- Two users update the same task.
- Worker retries after timeout.
- Reminder delivery fails then retries.
- Completed task's reminder is cancelled.
- Workspace timezone changes.

### Security and privacy
- User tries to read another workspace's messages/task/export.
- Untrusted filename/path traversal.
- Oversized file or decompression/parser resource abuse.
- Prompt injection embedded in chat text.
- LLM response references a nonexistent message ID.
- HTML/script-like message content rendered in UI.
- Secret leakage into logs or frontend.
- Delete request includes originals, normalized messages, derived tasks, and caches.
- Opt-out message must not lead to an automatic outbound contact.

## 5. Pilot validation
Run a small closed pilot with consenting businesses. Observe the real workflow rather than only showing a mock dashboard.

Before the tool is used, record a baseline period:
- Number of leads handled.
- Median first response time.
- Number of overdue promised actions.
- Time spent reviewing chats.
- Current follow-up process.

During the pilot:
- Ask users to verify the action queue each day.
- Track accepted, edited, and dismissed suggestions.
- Record why false positives happen.
- Measure tasks completed by deadline.
- Compare first-response time and follow-up completion against baseline.
- Interview users about interruptions, trust, and missing features.
- Estimate real processing/support cost and willingness to pay.

Avoid attributing all sales changes to the tool: seasonality, lead quality, pricing, staff changes, and marketing also affect outcomes.

## 6. Regression process
For every parser, model, prompt, or rule change:
1. Run unit tests for date parsing, chronology, sender mapping, and deduplication.
2. Run the labelled benchmark.
3. Inspect opt-out, explicit-deadline, and false-unanswered cases manually.
4. Compare with previous version.
5. Investigate regressions rather than relying only on overall average.
6. Store parser/model/rule version and benchmark version with the evaluation.
7. Block release if a safety-critical regression remains.

## 7. Product experiments
- **Action queue test:** compare the generated queue with a human's manually prepared list.
- **Time saved test:** measure total review time, including corrections.
- **False-alert tolerance:** learn how many inaccurate reminders users tolerate before ignoring the product.
- **Follow-up discipline test:** compare task completion and response-time baselines during a pilot.
- **Retention test:** see whether users return to import more conversations after the first week.
- **Willingness-to-pay test:** test per-seat, per-workspace, or volume pricing only after measuring value and cost.

## 8. Claims to avoid
Do not claim:
- "We never miss a lead."
- "Guaranteed sales uplift."
- "AI knows which lead will convert."
- "All WhatsApp messages are synced" in an export-only MVP.
- "The quote was sent" when the export only shows a promise.
- "A lead is lost" because a customer did not reply.
- "100% accurate" based on a small benchmark.

A defensible claim is: "Import a supported chat export to generate a source-linked, reviewable list of possible unanswered enquiries and promised follow-ups."
