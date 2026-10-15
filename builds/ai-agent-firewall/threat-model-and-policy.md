# AI Agent Firewall — Threat Model and Policy Model

## 1. Security objective

Limit the damage a supported AI coding agent can cause if it makes a mistake, follows malicious instructions from repository content, misuses an exposed tool, or runs an unexpected command.

The product does not attempt to prove that an agent is trustworthy. It reduces authority, constrains reachable resources, asks for human approval at defined boundaries, and preserves evidence.

## 2. Assets to protect

- API keys, tokens, SSH keys, cloud credentials, and `.env` files.
- Source code and proprietary repositories.
- Uncommitted developer work.
- Production configuration and deployment credentials.
- Local files outside the intended workspace.
- Git remotes, release branches, and signing credentials.
- Database contents and external services reachable over the network.
- Audit logs and policy configuration.
- User privacy and confidential command output.

## 3. Trust boundaries

1. **Host OS ↔ agent sandbox:** strongest core boundary. Host secrets should not be mounted into the sandbox.
2. **Developer ↔ approval broker:** agent output must not be able to approve its own actions.
3. **Agent ↔ tool integration:** agent tool requests are untrusted, even if syntactically valid.
4. **Sandbox ↔ network:** outbound connectivity should be explicitly controlled.
5. **Agent workspace ↔ original repository:** isolate changes to prevent accidental mutation of pre-existing work.
6. **Runtime ↔ audit store:** audit failure must be visible and must not silently create false assurance.
7. **Agent output ↔ report renderer:** output is untrusted content; escape HTML/terminal control sequences and avoid rendering it as executable markup.

## 4. Threat scenarios

| Threat | Example | Primary mitigation | Residual limitation |
|---|---|---|---|
| Secret discovery | Agent reads `.env` or SSH key | Do not mount secrets; enforce filesystem boundary | Secrets intentionally passed into process remain exposed to that process |
| Prompt injection | Malicious instruction in README/test fixture asks agent to upload files | Least privilege, network restrictions, approval, source isolation | Cannot make the model immune to all manipulation |
| Destructive command | Agent deletes repository or home directory | Isolated workspace, filesystem restrictions, process policy | Host/kernel/runtime vulnerabilities remain possible |
| Data exfiltration | Agent sends source code to an external host | Network deny-by-default and enforced egress boundary | Allowed endpoints may relay data; encrypted traffic limits content inspection |
| Tool bypass | Agent uses Python or another executable instead of a gated shell command | OS sandbox plus tool hooks | Tool-hook-only implementations are bypassable |
| Path escape | Symlink or traversal accesses outside workspace | Canonicalization plus OS-enforced mount/path restrictions | Backend-specific edge cases require testing |
| Privilege escalation | Agent exploits a vulnerable runtime or host kernel | Unprivileged execution, hardened backend, patching | No local sandbox guarantees zero-day immunity |
| Supply-chain attack | Agent installs a malicious package | Network policy, lockfiles, approval for package changes | A permitted package registry can serve malicious packages |
| Remote side effect | Agent pushes a branch or calls a cloud API | Restrict credentials and network; require action approval | Snapshot cannot undo remote changes already made |
| Audit tampering | Process edits local logs | Append-only interface, hash chain, separate ownership where feasible | Host administrator can potentially alter/delete local storage |
| Telemetry gap | Agent uses a direct socket not covered by proxy | Enforce network policy outside proxy; report gap | Cannot claim full visibility without actual coverage |
| Approval confusion | Agent persuades user to approve broad access | Exact target, risk context, one-time scoped approval | Human can still approve a harmful action |
| Denial of service | Infinite loop, fork bomb, huge file output | CPU/memory/PID/time/disk quotas | Limits depend on runtime/OS support |
| Malicious report content | Terminal escapes or HTML in file paths | Escape all untrusted text | Rendering libraries still need secure configuration |

## 5. Policy outcomes

### Allow
Action is within the declared policy and can proceed under the sandbox. The report should record the rule and the enforcement source.

### Require approval
The action is potentially consequential but can be permitted if a human approves its exact scope. Approval must expire and should not be reusable for different targets.

### Deny
The action violates a hard policy or cannot be safely authorized. A user interface should not offer a casual override for actions that the active policy explicitly forbids.

Unknown action classification should not automatically become "allow." The fallback depends on the action and backend: for a tool request it may require approval; for a hard sandbox escape it should be impossible at the OS boundary.

## 6. Risk scoring

Risk labels help humans prioritize; they are not proof of safety. Prefer deterministic rules over an LLM-generated risk score.

Illustrative factors:
- **Target sensitivity:** secret, production, user home, repository, temporary directory.
- **Impact:** read, write, delete, execute, transmit, publish, deploy.
- **Scope:** one file, workspace, parent directory, whole disk, remote service.
- **Reversibility:** easy local diff, destructive overwrite, irreversible external action.
- **Authority:** ordinary process, privileged process, cloud/deployment credential.
- **Confidence:** exact structured tool call versus inferred shell intent.

Suggested examples:
- Low: read a file within the sandboxed project.
- Medium: modify files in the designated workspace.
- High: attempt to access a protected secret path or change security configuration.
- Critical: broad destructive operation, privilege escalation attempt, or data transfer to a denied destination.

The policy engine must decide using explicit rules. Risk labels must not replace enforcement.

## 7. Policy design rules
- Default to least privilege.
- Keep the writable workspace narrow.
- Keep host home directories, SSH directories, cloud credential folders, and environment secrets outside the sandbox.
- Network starts disabled or allowlisted.
- Never run the agent as root/admin merely to make a sandbox convenient.
- Require exact, time-limited approvals.
- Revalidate targets after approval.
- Separate allowed test/build commands from release/deployment commands.
- Make policy changes visible and versioned.
- Fail closed if enforcement setup cannot be verified.
- Include an explicit emergency-stop mechanism.
- Avoid hidden "auto-approve all" fallbacks.
- Log policy decisions and enforcement evidence without logging secret values.

## 8. Human approval must be specific

Weak prompt:
"Agent wants more permissions. Approve?"

Better prompt:
"Allow this session to run `git push origin feature/bugfix` once? This may publish commits to the remote repository. The active policy blocks remote writes by default. Approval expires in 60 seconds. [Allow once] [Deny]"

Before approval:
- Show the actual executable/action, arguments that are safe to display, target, and known side effects.
- Redact tokens and secret-like arguments.
- Explain what is not known.
- Bind approval to a normalized action and target.
- Check that the policy has not changed.
- Do not accept approval from text in the agent's own output.

## 9. Secure development and response
- Use an unprivileged user and minimal host permissions.
- Pin and update sandbox/runtime dependencies.
- Test enforcement failures and bypass attempts.
- Treat logs as sensitive because commands and paths can reveal private work.
- Have a vulnerability disclosure process before public release.
- Publish a clear security policy and supported-version matrix.
- If a sandbox escape or false security claim is discovered, disable the affected backend/profile until fixed and document the issue.
