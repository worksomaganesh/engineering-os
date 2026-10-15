# AI Agent Firewall — Security Boundaries and Limitations

## 1. This is a security product, so precision matters

A product that says "blocked" when it merely printed a warning can make users less safe than before. Every guarantee must identify:
- The action it covers.
- The mechanism that enforces it.
- The supported OS/runtime and configuration.
- The test demonstrating that the action is blocked.
- The known bypasses or coverage gaps.

This document defines design constraints for the proposed project. It does not certify a working implementation.

## 2. Monitoring is not enforcement

There are several different evidence levels:

1. **Agent request observed:** an agent hook reports a proposed tool call.
2. **Policy decision recorded:** the local policy engine decides allow/deny.
3. **Process event observed:** the operating system reports process lifecycle or related metadata.
4. **Enforcement denial observed:** the sandbox/OS boundary denies the operation.
5. **Result verified:** a test confirms the protected resource or operation was not accessible/completed.

These levels must not be merged. For example, an agent hook may see a request to read `.env`, but a different process pathway may bypass that hook. A policy engine can decide "deny", but only the enforcement boundary can prevent the operation. A successful test in one configuration does not prove all configurations are safe.

## 3. Host secrets

Best defense: do not put secrets inside the agent's accessible environment.

- Do not mount the host home directory into the sandbox.
- Do not pass host cloud credentials, SSH agent sockets, Git credential helpers, browser profiles, or production environment variables unless a narrowly defined task genuinely requires them.
- Use a separate temporary identity with minimum permissions if a task needs authentication.
- Never log environment variable values.
- Avoid exposing a host Docker socket; access to it can grant powerful control over the host.
- Do not allow an agent to modify the firewall's own executable, policy, or audit store from inside the session.
- Remember that a secret deliberately supplied to the agent may be read, copied, or transmitted by it.

A filename denylist alone is not sufficient. Secrets may be copied, renamed, embedded in config files, exposed through environment variables, or obtained through helper processes.

## 4. Filesystem and process boundaries

A string filter around commands is insufficient. A command can invoke a script, an interpreter, another binary, a file API, or a child process. Path rules must consider symlinks, traversal, mounts, and platform semantics.

Use an OS-enforced isolation backend that restricts:
- Which filesystem paths are mounted/readable/writable.
- Which process privileges are available.
- Which syscalls/capabilities are allowed where supported.
- CPU, memory, process count, disk, and execution time where supported.
- Access to host sockets and sensitive devices.
- Network egress and access to sensitive local endpoints.

Run unprivileged. Keep the sandbox runtime and host patched. A container shares the host kernel; depending on threat model, a microVM or another stronger boundary may be appropriate. The chosen mechanism must be justified and tested rather than selected for convenience alone.

## 5. Network controls

A proxy log is not a complete network monitor if direct connections are possible. A robust profile must route or restrict outbound traffic at an enforced boundary and test direct sockets, DNS, IPv4/IPv6, redirects, and proxy bypasses.

Even with an allowlist:
- An allowed host can receive sensitive content.
- A permitted package registry can serve a malicious package.
- Encrypted traffic limits what a network observer can inspect without TLS interception.
- Localhost and cloud metadata endpoints may be sensitive.
- DNS and IP changes may affect the meaning of a host allowlist.
- Network denial cannot undo data already transmitted.

The MVP should prefer deny-by-default networking and clearly documented allowed endpoints.

## 6. Human approval limitations

Approval is a safety control, not a substitute for isolation. Users may misunderstand a prompt, and agent output can manipulate the human.

- Show exact action and target.
- Explain possible irreversible effects.
- Default to deny.
- Use one-time approvals.
- Do not permit approvals for actions forbidden by a hard policy.
- Revalidate the target immediately before execution.
- Redact secrets in the prompt.
- Do not let the agent control the approval interface.

Do not make the user approve dozens of low-risk file operations individually. Use a narrow workspace and pre-approved low-risk operations; reserve prompts for meaningful boundaries.

## 7. Snapshots and rollback

A Git diff or snapshot protects only the state represented by that snapshot. It cannot automatically undo:
- A network upload or data leak.
- A remote Git push.
- An email or message.
- A database write.
- A cloud deployment or resource deletion.
- A package installed globally outside the isolated environment.
- Changes made through a credential or socket available to the agent.

Prefer an isolated worktree/copy/VM and apply changes after review. Do not automatically reset the user's original working tree. Snapshot cleanup must be explicit and must not delete pre-existing work.

## 8. Audit log limitations

A local append-only file and hash chain are useful for detecting accidental or unsophisticated tampering, but they are not magically immutable. A sufficiently privileged process may rewrite logs or the entire chain.

To improve integrity:
- Keep the audit writer outside the agent sandbox.
- Restrict permissions.
- Chain hashes with canonical serialization.
- Verify the chain before reporting.
- Separate raw events from rendered summaries.
- Consider a remote append-only sink later, with privacy and data residency reviewed.

The local-first MVP should call its logs "tamper-evident", not "tamper-proof."

## 9. Platform-specific scope

The first version should support one platform and backend combination. Every release should publish a matrix:
- OS version.
- Sandbox backend and version.
- Filesystem restrictions supported.
- Process/resource restrictions supported.
- Network restrictions supported.
- Agent integration and version.
- Known gaps.
- Tests run.

A macOS or Windows version needs its own backend design and tests; do not label it supported merely because the CLI compiles.

## 10. Operational safety
- Require explicit opt-in before network telemetry leaves the machine.
- Make logs/snapshots private by default.
- Document retention and cleanup.
- Use dependency pinning and timely updates.
- Provide a safe emergency stop.
- Do not execute untrusted code in privileged components.
- Separate the controller from the contained agent.
- Fail closed if a required guard is unavailable.
- Have a responsible disclosure path before public release.
