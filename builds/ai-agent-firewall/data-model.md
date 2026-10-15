# AI Agent Firewall — Data Model and Audit Events

## 1. Design principles
- Use structured, versioned events rather than relying on free-form text logs.
- Store only what is needed for security investigation and reproducibility.
- Never store secret values or full environment variables by default.
- Every event identifies its source and coverage level.
- Keep "requested action", "policy decision", "enforcement result", and "final state" distinct.
- Use UTC timestamps in machine records; render local time only in the UI.

## 2. Core entities

### Session
Represents one guarded agent run.

Fields:
- `session_id`: random, unique identifier.
- `schema_version`: event/report schema version.
- `started_at`, `ended_at`: UTC timestamps.
- `agent_name`, `agent_version`: when reliably available.
- `agent_command_redacted`: safe representation of the launch command.
- `workspace_id`: opaque local identifier.
- `baseline_id`: baseline/snapshot reference.
- `policy_id`, `policy_version`, `policy_digest`.
- `sandbox_backend`, `backend_version`.
- `status`: starting, running, succeeded, failed, blocked, interrupted, review_required.
- `coverage_summary`: enabled, disabled, and unavailable sensors/enforcement controls.
- `exit_code`: nullable integer.
- `report_digest`: nullable hash.

### Policy
- `policy_id`
- `schema_version`
- `profile_name`
- `version`
- `content_digest`
- `created_at`
- `effective_rules`
- `validation_result`
- `backend_mapping_version`

Do not store an API key or credential inside the policy file. Policy should describe whether secrets are accessible, not contain the secrets themselves.

### Action event
A normalized record of an agent/tool/process/filesystem/network event.

Suggested fields:
- `event_id`
- `session_id`
- `sequence_number`
- `timestamp_utc`
- `event_type`
- `action_id`
- `actor` (agent hook, child process, sandbox, network boundary, Git collector, user)
- `source`
- `coverage_level`
- `operation` (read, write, delete, execute, connect, publish, approve, deny, etc.)
- `target_redacted`
- `rule_id`
- `policy_digest`
- `decision` (allow, require_approval, deny, not_applicable)
- `enforcement_result` (blocked, allowed, failed, unknown)
- `reason_code`
- `safe_metadata`
- `previous_event_hash`
- `event_hash`

Use an enum for event types and reason codes. Do not allow arbitrary agent-provided fields to overwrite trusted event metadata.

### Approval
- `approval_id`
- `session_id`
- `action_id`
- `normalized_action_digest`
- `target_digest`
- `requested_at`
- `expires_at`
- `decision`
- `approver_kind`
- `policy_version`
- `enforcement_result`

Do not store authentication tokens or unnecessary personal information. Bind approval to exact normalized action/target, policy version, and expiry.

### Baseline/snapshot
- `baseline_id`
- `session_id`
- `method` (worktree, copy, filesystem snapshot, VM snapshot)
- `location` (private local path or opaque identifier)
- `created_at`
- `verified`
- `git_head`
- `preexisting_dirty_state_digest`
- `limitations`
- `cleanup_status`

A snapshot can contain sensitive source code; protect it like the repository itself.

### Report
- `report_id`
- `session_id`
- `generated_at`
- `report_schema_version`
- `source_event_count`
- `audit_chain_verified`
- `coverage_gaps`
- `file_change_summary`
- `process_summary`
- `network_summary`
- `policy_summary`
- `test_summary`
- `final_status`

## 3. Event taxonomy

| Event | Example | Trust/coverage note |
|---|---|---|
| `session.started` | Preflight passed and sandbox launched | Trusted controller event |
| `session.blocked` | Required sandbox capability missing | Trusted controller event |
| `policy.loaded` | Policy digest selected | Trusted controller event |
| `action.requested` | Agent hook requests file write | Agent/tool integration; only if supported |
| `policy.decided` | Rule says deny | Policy engine decision, not proof of enforcement |
| `enforcement.blocked` | OS backend denies filesystem access | Backend event; strongest evidence if correctly configured |
| `process.started` | Child process created | Process telemetry source |
| `process.exited` | Exit code and duration | Process telemetry source |
| `network.connection` | Connection via controlled egress point | Does not imply all host traffic observed |
| `approval.requested` | Specific action paused | Approval broker event |
| `approval.decided` | User approves/denies | Controller event |
| `workspace.diff` | Final Git diff summary | Final state, not every file operation |
| `test.result` | Parsed test output | Parser-specific reliability |
| `audit.integrity_failed` | Hash chain mismatch | Local log verification event |
| `coverage.gap` | A sensor/backend unavailable | Explicit limitation |
| `session.ended` | Session finalized | Controller event |

## 4. Example JSONL event

Illustrative only:

```json
{
  "schema_version": 1,
  "event_id": "evt-000042",
  "session_id": "session-example",
  "sequence_number": 42,
  "timestamp_utc": "2026-10-15T10:00:00Z",
  "event_type": "policy.decided",
  "action_id": "act-0009",
  "actor": "policy-engine",
  "source": "agent-tool-hook",
  "coverage_level": "tool-request-observed",
  "operation": "read",
  "target_redacted": ".env",
  "rule_id": "protected-secret-paths",
  "decision": "deny",
  "enforcement_result": "pending",
  "reason_code": "PROTECTED_PATH",
  "previous_event_hash": "example-previous-hash",
  "event_hash": "example-event-hash"
}
```

Notice that a policy decision is not yet proof that the OS denied access. A subsequent event should record the enforcement outcome, or the report should say it is unknown.

## 5. Hash chaining and integrity
A simple event chain can compute each event hash from a canonical serialization of the event excluding its own hash, plus the previous event hash. The verifier recomputes each hash and checks sequence numbers and links.

Requirements:
- Specify the canonical serialization and hash algorithm.
- Include schema version in the hashed payload.
- Prevent event fields from being reordered or ambiguously serialized.
- Detect missing, reordered, and modified events.
- Record verifier result in the report.

Limitations:
- A local attacker with control over the program and storage may be able to rewrite the entire chain.
- Hash chaining does not prove the event is truthful; it proves only that the saved chain is internally consistent under the scheme.
- Stronger tamper resistance requires a separate trust boundary (for example, a remote append-only service), which is not in the local-first MVP.

## 6. Privacy and retention
- Do not log environment variable values.
- Redact tokens in URLs, command arguments, and error output.
- Avoid storing file contents unless necessary for a clear security purpose.
- Protect logs and snapshots with restrictive file permissions.
- Set a retention policy and provide a safe deletion mechanism.
- Explain that logs may still reveal file names, directory structure, repository names, and development activity.
- Make report exports opt-in and clearly label their sensitivity.
