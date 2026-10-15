# AI Agent Firewall — Product Requirements

## 1. Product goal

Help developers run AI coding agents inside a bounded development session with enforceable policies, explicit approvals, an audit trail, and a trustworthy summary of changes.

The primary user is a developer who wants to delegate multi-file tasks to an agent without granting the agent unrestricted access to the host machine, secrets, or network.

## 2. User stories

- As a developer, I can start a supported agent inside a known workspace and policy profile.
- As a developer, I can protect paths such as `.env`, private keys, cloud credentials, and production configuration.
- As a developer, I can restrict outbound network access to an explicit allowlist.
- As a developer, I can require approval before an agent performs a defined high-impact action.
- As a developer, I can see whether an action was requested, allowed, denied, or completed.
- As a reviewer, I can inspect the Git diff, new/deleted files, test outcomes, and policy events after a run.
- As a security-minded user, I can verify the audit log's integrity and understand its collection limitations.
- As a team, we can maintain policy files under version control and test them before use.

## 3. Personas and jobs to be done

### Individual developer
Wants a safe default for local coding agents without becoming a full-time security operator.

### Maintainer of a valuable repository
Wants an agent to fix issues while protecting secrets, release configuration, and unrelated work in progress.

### Team/security engineer
Wants consistent policy, testable guarantees, reviewable audit events, and documented exceptions.

The first MVP should optimize for the individual developer and a single local workspace. Team policy distribution and central dashboards come later.

## 4. Functional requirements

### FR-1: Session launch
- Launch a supported agent as a child process inside a configured boundary.
- Record agent command, version when available, working directory, policy profile/version, start time, and environment details that are safe to log.
- Never record environment variable values or credentials by default.
- Return the child process's exit status while distinguishing agent failure from firewall startup/enforcement failure.

### FR-2: Workspace preparation
- Resolve and display the canonical workspace path.
- Detect whether Git is available and whether the worktree has pre-existing changes.
- Do not silently overwrite, stash, discard, or reset a user's existing work.
- Create a baseline snapshot or clearly explain why snapshot creation failed.
- If a clean baseline is required by policy and cannot be obtained, stop before launching the agent.

### FR-3: Policy decisions
Every supported action decision must have:
- A stable action ID.
- Action type and normalized target.
- Rule ID and policy version.
- Decision: `allow`, `require_approval`, or `deny`.
- Human-readable reason.
- Timestamp and session ID.
- Enforcement status or coverage source.

Unknown or unsupported action types must not silently inherit a permissive policy.

### FR-4: Protected files
- Support explicit protected path patterns.
- Include safe starter patterns for common secret files but require users to review them.
- Enforce path restrictions using the sandbox or filesystem access control, not just string matching in the UI.
- Canonicalize paths and defend against symlinks, path traversal, hard links, and alternate access paths to the extent supported by the chosen backend.
- Test platform-specific path semantics.

### FR-5: Commands and processes
- Apply a declared process policy to child processes.
- Support block rules for known dangerous operations, while clearly stating that command-string rules alone cannot provide complete process security.
- Enforce resource/time limits where the selected runtime supports them.
- Record executable, safe-to-log arguments, exit code, start/end time, and timeout/termination outcome.
- Redact or omit command arguments that may contain secrets.

### FR-6: Network
- Start with network disabled or tightly allowlisted inside the enforcement boundary.
- If network access is enabled, record which enforcement point observed the request.
- Do not claim to monitor all network requests if only a proxy is instrumented.
- Avoid transparent TLS interception in the MVP; it adds trust, privacy, and certificate-management complexity.
- Explain that external network side effects cannot be undone by restoring a Git snapshot.

### FR-7: Approval
- Display the exact action, target, reason, and likely impact.
- Require an explicit user decision; default to deny on timeout or closed UI.
- Bind approval to one action or a narrowly scoped, expiring capability—not a vague "trust this agent" toggle.
- Re-check the action target immediately before execution to reduce time-of-check/time-of-use issues.
- Record approver identity as local user/session identity when available, decision, timestamp, scope, and expiry.
- Never let an agent approve its own request.

### FR-8: Run report
Include:
- Session metadata and policy version.
- Snapshot status and baseline reference.
- Files added/modified/deleted based on the chosen comparison.
- Commands/processes observed and exit outcomes.
- Network activity observed by configured enforcement points.
- Approval/deny events and risk classifications.
- Test commands and results, distinguishing parsed test counts from process exit status.
- Collection gaps and unsupported channels.
- Final status: success, failed, blocked, interrupted, or review required.

### FR-9: Audit integrity
- Write structured append-only events locally.
- Chain event hashes or use another documented tamper-evidence mechanism.
- Verify the chain on report generation.
- Make clear that a local administrator or compromised host may still alter or delete logs; hash chaining is not the same as remote immutable storage.
- Avoid sensitive payloads in logs.

### FR-10: Safe failure
- If the sandbox fails to start, do not silently fall back to unrestricted execution.
- If policy loading fails, use a documented fail-closed behavior for security-critical operations.
- If logging fails, either stop the agent or follow an explicit policy; never silently report full audit coverage.
- Clearly distinguish enforcement failures from agent failures.

## 5. Non-functional requirements

- **Security:** least privilege, sandbox-first, fail closed for protected operations.
- **Transparency:** show the active policy and coverage before execution.
- **Reliability:** stable session IDs, deterministic policy decisions, robust interruption handling.
- **Performance:** measure overhead on representative repositories before setting targets.
- **Usability:** safe defaults, readable explanations, low-friction approval for genuinely risky actions.
- **Portability:** state exactly which backend and OS version each guarantee supports.
- **Privacy:** local-first logs, minimal telemetry, secret redaction, configurable retention.
- **Maintainability:** versioned policy schema, modular enforcement adapters, regression suite.

## 6. Example policy profile

Illustrative YAML only; final field names must be defined by the implementation schema.

```yaml
version: 1
profile: balanced
workspace:
  writable_paths:
    - "./"
  protected_paths:
    - ".env"
    - ".env.*"
    - "**/*.pem"
    - "**/*credentials*"
network:
  mode: deny_by_default
  allow_hosts:
    - "registry.npmjs.org"
process:
  max_runtime_seconds: 1800
  require_approval_for:
    - "git push"
    - "terraform apply"
    - "docker push"
  deny:
    - "unrestricted host execution"
approval:
  timeout_seconds: 120
  timeout_decision: deny
logging:
  include_environment_values: false
```

This is a design example, not a functioning configuration. A production policy must be parsed by a strict schema, reject unknown security-sensitive fields, and map to actual controls in the selected sandbox backend. A string rule like `git push` is not enough to reliably intercept every possible push pathway.

## 7. Acceptance criteria

- A supported agent can be launched inside the declared sandbox.
- If the sandbox is unavailable, the tool fails closed instead of launching unrestricted.
- A harmless attempt to read a protected file is blocked by the actual enforcement backend and the test verifies that the contents were not returned.
- A denied network destination is unreachable from the sandbox in the tested configuration.
- Approval applies only to the intended action and expires as documented.
- All fixture events have correct allow/deny/approval outcomes and source coverage labels.
- Snapshot creation never destroys pre-existing user changes.
- A report's file counts match the baseline comparison and clearly define ignored/untracked files.
- Audit tampering is detected by the verifier.
- Tests cover symlink/path traversal, child process, timeout, logging failure, and interrupted-session cases.
- The report does not claim visibility into actions outside configured telemetry.
- No secrets are present in logs or test fixtures.

## 8. Product metrics

- Unsafe actions blocked in controlled tests.
- False-positive approval rate.
- False-negative rate for declared protected-action scenarios.
- Percentage of sessions with verified baseline and report.
- Agent task completion rate versus an unguarded test baseline.
- Added execution latency.
- User approval burden per session.
- Report completeness and audit verification success.
- Number of undisclosed coverage gaps (target: zero).
- Recovery success for file changes in the declared scope.

## 9. Open decisions
- Which Linux sandbox backend provides the first enforceable boundary?
- Does the first version use a container, bubblewrap/Landlock/seccomp, a microVM, or a combination?
- Which agent launch interface is supported first?
- Which network policy backend can be reliably enforced?
- Which test runner outputs are parsed, and how are unknown formats represented?
- How are snapshot size and cleanup managed?
- Which actions are always denied even if a user attempts to approve them?
- What is the exact security claim for the first release?
