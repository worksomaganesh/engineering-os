# AI Agent Firewall — Technical Architecture

## 1. Architecture overview

The system is a local session orchestrator. The security boundary is the operating-system sandbox, not the CLI's user interface.

```text
Developer
   |
   v
CLI + policy validator
   |--- inspect workspace and Git baseline
   |--- resolve policy and display coverage
   v
Session orchestrator
   |--- create isolated workspace/snapshot
   |--- configure filesystem/process/network restrictions
   |--- start supported agent
   v
Enforcement boundary
   |--- filesystem restrictions
   |--- process/resource controls
   |--- network restrictions
   |--- optional agent tool hooks
   v
Event collector ---> append-only local event log
   |
   v
Finalizer
   |--- collect process/test outcomes
   |--- compare Git baseline to final state
   |--- verify event chain
   |--- generate JSON + Markdown/HTML report
```

## 2. Main modules

### CLI
Responsible for command parsing, policy selection, user interaction, output formatting, and exit codes. It should not implement security by parsing arbitrary shell strings alone.

Suggested commands:
- `agent-boundary run --profile balanced -- codex`
- `agent-boundary policy validate policy.yaml`
- `agent-boundary report <session-id>`
- `agent-boundary audit verify <session-id>`
- `agent-boundary snapshot list`
- `agent-boundary doctor`

### Policy loader and validator
- Parse a versioned policy schema.
- Reject unknown fields in security-critical sections.
- Normalize path/host/action rules.
- Explain effective policy before starting.
- Generate a stable policy digest and record it with the session.
- Ensure profile inheritance cannot silently broaden permissions.

### Workspace manager
- Detect repository root and canonical path.
- Record Git status before launch.
- Preserve dirty/untracked user changes.
- Create a baseline using a temporary worktree, filesystem snapshot, or a copied workspace, depending on the chosen design.
- Never use `git reset --hard`, `git clean -fdx`, or equivalent destructive cleanup as an automatic recovery mechanism.
- Make snapshot limitations visible.

### Sandbox adapter
The adapter maps product policy to the actual operating-system mechanism. Keep it behind a small interface so that different backends can be tested without pretending they provide equal guarantees.

Possible approaches to evaluate:
- Rootless container with restricted mounts and network.
- Linux namespaces plus seccomp and filesystem restrictions.
- Landlock for additional filesystem restrictions where supported.
- MicroVM-based isolation for stronger separation.
- A maintained sandbox product used as the underlying runtime.

A container is not automatically a perfect security boundary; configuration and kernel/runtime vulnerabilities matter. Choose a backend based on a documented threat model and test the actual restrictions.

### Agent adapter
- Starts the agent with an explicit executable and arguments.
- Captures structured tool events only when the agent offers a supported hook/protocol.
- Normalizes supported events into a common event schema.
- Declares which tool actions are intercepted and which are only inferred from process telemetry.
- Does not assume every agent supports the same hooks or permissions model.

### Policy engine
Input: normalized action + session context + policy version.

Output:
- `allow`
- `require_approval`
- `deny`

The decision must include the rule ID and explanation. If action classification is uncertain, the policy should fall back to a safe behavior appropriate to the action category.

The policy engine decides intent-level rules; the sandbox enforces hard boundaries. A tool hook can stop a tool call before it starts, but it cannot necessarily prevent a child process from bypassing the hook unless the OS boundary also restricts that process.

### Approval broker
- Displays the full target and requested operation.
- Uses a separate interactive terminal/UI channel from agent output.
- Does not accept approval text emitted by the agent.
- Binds approval to a specific action, target, and short expiry.
- Revalidates target and policy before executing.
- Records denied, expired, and approved requests.

### Event collector
Collects events from supported sources:
- Agent hooks/protocols.
- Process lifecycle/exit statuses.
- Sandbox decisions.
- Network proxy/firewall telemetry.
- Filesystem audit events, where available.
- Git baseline/final comparison.
- Test runner output adapters.

Every event records its source. "Observed through an agent hook" is not the same assurance as "blocked by the kernel." The report must preserve that distinction.

### Report generator
Builds output from saved structured records, not from a free-form LLM summary. An optional language model may summarize known facts, but it must not invent counts or conclusions and must not replace raw event evidence.

## 3. Recommended MVP implementation strategy

### Phase A — observe-only prototype
- CLI launches a harmless command in a test workspace.
- Capture session metadata, process exit status, Git diff, and JSONL event log.
- Label this as observe-only, not a firewall.
- Add test fixtures and a coverage report.

### Phase B — enforceable Linux sandbox
- Select one supported backend after evaluating filesystem, process, and network restrictions.
- Run the child agent only inside the backend.
- Restrict mounted paths to a dedicated workspace and required runtime resources.
- Keep host credentials and home-directory secrets out of the sandbox.
- Fail closed if restrictions cannot be established.
- Add adversarial tests before calling it an MVP.

### Phase C — approval integration
- Add tool-level approvals for supported actions and an enforcement-level control for operations that must be blocked.
- Verify exact-target binding and expiry.
- Avoid broad persistent approvals.

### Phase D — reports and developer ergonomics
- Markdown and JSON report.
- Test output adapters.
- Snapshot lifecycle and explicit cleanup.
- Policy linting and `doctor` diagnostics.

## 4. File-change accounting

Use a baseline/final comparison with clearly defined categories:
- Added tracked or untracked files.
- Modified tracked files.
- Deleted tracked files.
- Renamed files where Git can detect them.
- Ignored files, if collected by the implementation.
- Files outside the workspace: only claim visibility if the sandbox/audit backend provides it.

A Git diff does not show every filesystem operation. A file may be created and deleted before the final comparison, or modified and restored. Therefore:
- Git diff = final repository state difference.
- Filesystem/process telemetry = observed actions, subject to backend coverage.

Present these as separate data sources.

## 5. Snapshot and rollback model

A Git commit, Git worktree, filesystem copy, volume snapshot, or VM snapshot have different properties. Document which is used.

Recommended MVP behavior:
1. Detect existing changes.
2. Preserve them without mutation.
3. Create a separate isolated worktree/copy for the agent.
4. Run the agent only in that copy.
5. Review its diff.
6. Apply or cherry-pick reviewed changes back only after human action.

This is safer than trying to undo the agent's work in the user's active worktree. It still cannot roll back external effects like uploads, network requests, remote pushes, emails, or cloud API changes.

## 6. Failure handling
- Sandbox startup error: do not launch the agent.
- Policy parse error: stop before execution.
- Audit write failure: stop or pause according to explicit fail-closed policy.
- Approval UI disconnected: deny pending action.
- Agent timeout: terminate the contained process tree if the backend supports it; record whether termination was confirmed.
- Report generation error: preserve raw logs and show incomplete status.
- Snapshot unavailable: stop if the selected profile requires a recovery point.

## 7. Dependencies and build discipline
- Prefer small, maintained libraries with pinned versions.
- Use structured event schemas and version migrations.
- Keep policy and report generation deterministic.
- Minimize dependencies in the privileged/control-plane component.
- Avoid running the agent with elevated privileges.
- Keep secrets out of command arguments and logs.
- Include a reproducible test harness and sandbox capability checks.
- Do not add a new OS backend without an explicit security review and dedicated regression suite.
