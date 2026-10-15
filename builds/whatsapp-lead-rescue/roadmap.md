# WhatsApp Lead Rescue — Roadmap and Business Validation

This roadmap is a sequence of evidence gates. The goal is not to ship the most features; it is to prove that a source-linked action queue reduces forgotten follow-ups and that businesses will repeatedly use it.

## Phase 0 — Discovery
- Interview owners, salespeople, and consultants in coaching, real estate, manufacturing, and B2B services.
- Ask them to walk through recent chats where a lead was forgotten or a promise was delayed.
- Observe their actual process, current spreadsheets/CRM, ownership, and reminders.
- Learn typical export formats, languages, and media use.
- Collect sample chats only with permission and a documented handling/deletion process.
- Review official WhatsApp policies and current pricing.
- Identify current alternatives and competitors; do not assume the market is empty.

**Gate:** one initial segment, repeated pain confirmed by observed workflows, permitted sample data, and clear baseline metrics.

## Phase 1 — Export parser proof of concept
Build:
- Supported text export upload.
- Format detection and robust parsing.
- Sender mapping and timeline view.
- Parse warnings and missing-media disclosure.
- Unit tests for timestamps, multiline messages, locale variants, and malformed lines.

**Gate:** supported exports are parsed accurately enough for reviewers to inspect the original timeline.

## Phase 2 — Action extraction
Build:
- Detection of unanswered inbound questions.
- Extraction of explicit commitments, quote/proposal mentions, calls, and demos.
- Source-message IDs and timestamps on every suggestion.
- Schema validation and evidence checks.
- Review UI for accept/edit/reject.
- Deterministic deduplication.

**Gate:** held-out benchmark meets predeclared precision/recall targets; no ungrounded deadlines; users can explain why each candidate appears.

## Phase 3 — Follow-up dashboard
Build:
- Due now/overdue/today filters.
- Task owner, due time, status, reason, and source.
- Snooze, complete, dismiss, and edit.
- Lead stage separated from conversation and task state.
- In-app reminder scheduling and audit history.

**Gate:** real users return to the dashboard and complete tasks; false alerts do not make users ignore it.

## Phase 4 — Closed pilot
- Use a small number of consenting businesses.
- Record a baseline for first-response time, overdue actions, and time spent reviewing chats.
- Measure suggestion acceptance, edits, false positives, and task completion.
- Track cost per import and support burden.
- Review security, provider terms, retention, and deletion before real data.
- Interview users after observing actual daily use.

**Gate:** measurable time/behavior improvement, repeat usage, manageable risk, and credible willingness-to-pay signal.

## Phase 5 — Reliability and workflow fit
Prioritize based on pilot evidence:
- Improve locale/date parsing and code-switched text handling.
- Improve action deduplication and task ownership.
- Add saved business rules for follow-up intervals.
- Add team roles and handoffs after tenant isolation is proven.
- Add import history and reusable lead/task corrections.
- Improve deletion/export controls and audit history.
- Add optional daily email digest and quiet hours.

## Phase 6 — Official WhatsApp integration (only after validation)
- Confirm customers genuinely need live synchronization.
- Use the official WhatsApp Business Platform/Cloud API.
- Complete business onboarding, permissions, webhook verification, and required setup.
- Handle webhook retries, duplicate/out-of-order events, and idempotency.
- Follow current opt-in, opt-out, template, customer-service-window, and quality requirements.
- Verify current per-message pricing and any business-solution-provider fees.
- Start with inbound event ingestion; keep outbound sending human-approved.
- Build suppression rules, audit history, quotas, and a stop mechanism before any automation.

Do not start with scraping the inbox, auto-sending bulk follow-ups, or automated bidirectional control of WhatsApp Web.

## Suggested build sequence
1. Problem interviews and permitted sample conversations.
2. Text export parser and timeline.
3. Evaluation harness and source evidence.
4. Action extraction with review.
5. Task queue and reminder service.
6. Security review and pilot.
7. Iterate based on errors and observed behavior.
8. Consider official API integration only if users demand it.

A solo prototype may take weeks; a reliable multi-tenant service and official messaging integration can take considerably longer. Estimate timing only after format discovery and benchmark results.

## Validation experiments
### A. Action queue accuracy
Give the tool a conversation a salesperson has already reviewed. Compare its action list to the person's list and ask them to explain every false positive and missed action.

### B. Time saved
Measure the full workflow, including import, corrections, review, and follow-up—not just model response time.

### C. False-alert tolerance
Determine how many incorrect reminders cause a user to stop trusting the queue. This informs precision targets and review design.

### D. Follow-up discipline
Compare task completion and first-response time with the business's baseline. Treat this as observational evidence, not proof that the tool alone caused every improvement.

### E. Repeat use
See whether users import more conversations after the first week and whether they prefer the export workflow or request official integration.

### F. Willingness to pay
Test pricing hypotheses after measuring value and cost. Possible models:
- Per conversation/import for occasional use.
- Monthly plan per business workspace.
- Per-seat plan for sales teams.
- Consultant plan with multiple client workspaces.

These are hypotheses, not final pricing. Estimate OCR/LLM, storage, reminder, support, and official messaging costs before choosing a model.

## Risks and mitigations

| Risk | Mitigation |
|---|---|
| Too many false alerts | Source evidence, review queue, precision benchmark, user correction |
| Missed lead | Recall tests, export limitations visible, manual review |
| Incomplete export | Warn that only supplied history is analyzed |
| Wrong date/time | Preserve raw timestamp; ask user when ambiguous |
| AI invents promise | Validate message IDs/quotes and require review |
| Users ignore another dashboard | Keep one action-first screen and test repeated use |
| Sensitive chats exposed | Private storage, tenant isolation, retention/deletion |
| Platform policy changes | Re-check official docs before integration and launch |
| Messaging costs exceed margin | Keep outbound messaging out of MVP; meter usage |
| Scope becomes giant CRM | Keep focus on conversations needing action |
| Users won't pay | Validate willingness to pay before scaling |
| Low conversion attribution | Compare baselines and avoid causal claims from observational data |

## Decision log
Record dated decisions for:
- Initial industry/segment.
- Supported export formats and languages.
- File/message limits.
- Default follow-up policy.
- Reminder channel.
- AI provider and data terms.
- Retention/deletion policy.
- Accuracy release gates.
- Pricing hypothesis.
- Whether official integration is justified by real user demand.

Every material change to action-detection or reminder logic should include a regression test.
