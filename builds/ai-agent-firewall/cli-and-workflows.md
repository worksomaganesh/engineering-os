# AI Agent Firewall — CLI and User Workflows

## 1. CLI design goals

- Every command should be understandable without reading implementation source.
- The active policy and security coverage must be visible before an agent starts.
- A failed guard must not silently fall back to unguarded execution.
- Machine-readable output should be stable and versioned.
- The CLI must distinguish observation from enforcement.

The command names below are proposed. They are not yet implemented.

## 2. Example command set

```bash
# Check runtime dependencies and available enforcement capabilities
agent-boundary doctor

# Validate a policy without running an agent
agent-boundary policy validate ./agent-policy.yaml

# Start a session with an explicit profile and agent command
agent-boundary run --profile balanced -- codex

# Produce a report for a completed session
agent-boundary report session-2026-10-15-001

# Verify the local audit event chain
agent-boundary audit verify session-2026-10-15-001

# List local snapshots/recovery points
agent-boundary snapshot list
```

Avoid implicit shell parsing for the agent command. Pass an explicit executable and argument array to reduce quoting ambiguity. The final implementation must clearly document how the agent process is started and which environment variables are inherited.

## 3. First-run experience

1. Run `agent-boundary doctor`.
2. The tool checks OS version, sandbox backend, required permissions, Git, storage, and network-enforcement capabilities.
3. It reports which guarantees are enforceable and which are unavailable.
4. The user selects or edits a policy profile.
5. The tool validates the policy and displays protected paths, writable workspace, network mode, process limits, and approval rules.
6. The tool identifies dirty/untracked files and explains how it will preserve them.
7. The user confirms the session launch.

If a required control is missing, the tool must stop with a clear explanation rather than present a weaker setup as equivalent.

## 4. Session launch screen

Example:

```text
AI AGENT BOUNDARY — PRE-FLIGHT

Workspace: /work/example-project
Agent: codex
Policy: balanced (sha256: 8a...example)
Sandbox: Linux backend X, capability check passed
Writable scope: isolated copy of project
Protected host paths: not mounted
Network: deny by default; allowlist: 1 host
Approval timeout: 120s, default deny
Baseline: created
Audit log: writable
Coverage: filesystem + process + configured network boundary
Not covered: actions outside this isolated session

Proceed? [yes/no]
```

Use real backend names and actual capability checks in the implementation. Do not print a generic "secure" badge when a check has not run.

## 5. Approval workflow

When a supported action requests elevated permission:

1. Pause the action at a reliable interception/enforcement point.
2. Normalize and display the exact action and target.
3. Explain the policy rule and potential side effect.
4. Offer allow-once or deny where the policy permits approval.
5. Deny on timeout, UI disconnect, or invalid approval.
6. Re-check target and policy before executing.
7. Record the result in the event log.

Example:

```text
APPROVAL REQUIRED — HIGH RISK
Action: write file
Target: deploy/production.yaml
Reason: path is protected from agent writes
Scope: one write operation
Policy rule: protected-production-config
Approval expires: 60 seconds

[Allow this operation once] [Deny]
```

If the path is prohibited by a non-overridable rule, show "Blocked by policy" rather than an approval button.

## 6. Final report

The report should contain the following sections:

### Session summary
- Session ID, start/end time, agent executable/version if available.
- Workspace and isolated worktree identifier.
- Policy profile, version, and digest.
- Exit state: success, failed, blocked, interrupted, or review required.

### Change summary
- Added, modified, deleted, and renamed files.
- Diff/statistics from the baseline comparison.
- Separate note for files changed and restored during the run if filesystem telemetry supports it.
- List of changes outside the workspace only if the backend actually collects that information.

### Process and test summary
- Commands/processes observed by the selected telemetry source.
- Exit code, timeout, and termination status.
- Test command and parser used.
- Test counts only when reliably parsed; otherwise show raw process exit status and output location.

### Security events
- Allowed, denied, and approval-required events.
- Rule ID, target, reason, source, and timestamp.
- Network activity by configured proxy/firewall.
- Protected-path access attempts.
- Coverage gaps and instrumentation failures.

### Recovery and review
- Snapshot status.
- Audit integrity verification result.
- Suggested next action: inspect diff, run tests, apply changes, discard isolated worktree, or investigate a policy event.

## 7. Exit codes

Proposed stable meanings:
- `0`: session completed and required checks passed.
- `1`: agent task or required test failed.
- `2`: invalid arguments or policy.
- `3`: enforcement/sandbox startup failure; agent was not launched.
- `4`: session interrupted or terminated.
- `5`: audit/report integrity problem.
- `6`: session completed but human review is required.

The implementation should document precedence when multiple conditions apply and should not reuse one exit code for unrelated outcomes.

## 8. Safe output handling
- Escape terminal control characters in paths and agent output.
- Escape HTML in generated reports.
- Redact tokens and secret-like command arguments.
- Limit event payload sizes.
- Avoid displaying file contents unless a user explicitly opens them.
- Treat all agent-generated text as untrusted.
- Keep raw logs private and provide a clear retention/deletion command.

## 9. Recovery workflow
The default should be: inspect changes in an isolated workspace, then explicitly apply them. Avoid destructive automatic rollback of the developer's original working tree.

A report may offer:
- Open diff.
- Run tests again inside the same sandbox.
- Export report.
- Apply selected changes.
- Preserve session for debugging.
- Delete session artifacts after confirmation.

Deleting the local snapshot does not reverse external side effects. Make this limitation visible.
