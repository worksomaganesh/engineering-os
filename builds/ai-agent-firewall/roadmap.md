# AI Agent Firewall — Roadmap and Competitive Landscape

## Product thesis

Developers want coding agents to complete real work, but the agent's available authority can exceed the task's intended scope. A local guardrail layer can make that authority more explicit, reduce the reachable attack surface, and make the session reviewable.

The product's value is not simply "log agent actions." It is the combination of **enforced isolation + narrowly scoped approval + evidence-based reporting + recovery-oriented workflow**.

## Phase 0 — Research and design
- Read the current security model of each supported agent.
- Compare existing local sandbox and agent-firewall projects.
- Choose a threat model and one OS/backend.
- Write explicit security claims and a test for each claim.
- Prototype policy schema and event format.
- Test a disposable workspace with no real secrets.

**Gate:** the project can clearly explain what it enforces, what it observes, and what it cannot guarantee.

## Phase 1 — Observe-only CLI
- CLI command and config validation.
- Session IDs and structured event log.
- Child-process start/exit status.
- Git baseline/final diff.
- JSON/Markdown report.
- Audit chain verifier.
- Coverage-gap reporting.

This phase is not a firewall and must be labelled accordingly.

## Phase 2 — First enforceable sandbox
- Support one Linux environment.
- Isolate a copy/worktree of the project.
- Restrict host filesystem visibility and writes.
- Remove host credentials and sensitive sockets.
- Apply process/resource restrictions.
- Add network deny-by-default or a tested allowlist.
- Fail closed if enforcement cannot be configured.
- Add escape-attempt regression tests.

**Gate:** every advertised restriction has repeatable negative tests showing prohibited actions fail.

## Phase 3 — Policy and approvals
- Strict policy schema and profile validation.
- Protected paths and high-risk operation policy.
- Approval broker with exact-action binding and expiry.
- Non-overridable deny rules.
- Safe command output redaction.
- Rule-level audit explanations.

**Gate:** approval scope cannot be broadened by target substitution, stale policy, or agent-controlled output.

## Phase 4 — Agent integration
- Start with one coding agent.
- Use official/supported hooks or protocols when available.
- Normalize tool requests into the event schema.
- Document which actions are hook-observed versus OS-enforced.
- Add agent-version compatibility tests.

**Gate:** integration adds useful observability without weakening the OS boundary.

## Phase 5 — Pilot and hardening
- Test with developers using disposable or non-sensitive repositories.
- Measure false positives, task completion, latency, approval burden, and enforcement outcomes.
- Conduct adversarial testing and independent review.
- Publish supported OS/backend/agent matrix.
- Document vulnerability reporting and release process.

**Gate:** no unexplained critical boundary bypass in the declared support matrix; all known limitations are public.

## Phase 6 — Extensions only when justified
Possible later features:
- macOS and Windows enforcement adapters.
- Team policy profiles and signed policy bundles.
- Optional remote audit sink.
- Pull-request workflow integration.
- Session replay from structured events.
- Additional agent adapters.
- Managed policy for enterprise teams.

Do not build a large dashboard before proving the local security boundary.

## Competitive landscape and differentiation

This space already has tools and platform-native controls. Research these before implementation:

| Project/product | Relevant overlap | What to investigate |
|---|---|---|
| [OpenAI Codex security practices](https://openai.com/index/running-codex-safely/) | Sandbox, approvals, telemetry, identity | Agent-specific safety controls and observability |
| [OpenAI Codex Windows sandbox](https://openai.com/index/building-codex-windows-sandbox/) | OS-level sandbox design | Platform-specific isolation and process boundaries |
| [Docker Sandboxes](https://docs.docker.com/ai/sandboxes/security/) | Isolated local agent runtime and network/filesystem policy | Whether to integrate a proven sandbox instead of reinventing one |
| [AgentWall](https://github.com/balyakin/agentwall) | Local agent command policy / firewall concepts | Rule model, integration points, supported agents |
| [Agent Firewall](https://github.com/asale-ai/agent-firewall) | Firewall/guardrail concept for agent actions | Enforcement boundaries and maintenance status |
| [Agent Quarantine](https://github.com/spacegiyou/agent-quarantine) | Isolated environment for agent work | Workspace isolation and recovery model |
| [OpenAgentLock](https://github.com/openagentlock/OpenAgentLock) | Local-first agent security controls | Policy and runtime architecture |
| [AgentGuard](https://github.com/Caua-ferraz/AgentGuard) | Similar name and adjacent agent-security concept | Existing features and naming collision |
| [Claude Code permissions and sandboxing](https://code.claude.com/docs/en/security) | Agent-native permissions and OS sandbox | Native capabilities, hooks, and gaps |

These links are starting points for research, not an endorsement or a complete feature comparison. Recheck repository activity, licenses, maintenance, and exact behavior before relying on any project. A similar name or feature does not establish that a tool is secure or actively maintained.

### Differentiation hypotheses to validate
- One report that separates agent requests, policy decisions, OS enforcement, and final Git state.
- A useful local-first workflow that does not require uploading source code.
- Fail-closed behavior when a required sandbox capability is missing.
- Easy review of a separate worktree instead of destructive cleanup in the original repository.
- Reproducible adversarial tests and a public support/coverage matrix.
- Agent-independent event schema without claiming universal compatibility.

Do not market it as the first AI-agent firewall. Prove that a specific workflow is easier to understand, safer to operate, or more auditable than the existing options.

## Risks and mitigations

| Risk | Mitigation |
|---|---|
| False sense of security | Publish exact guarantees, tests, and coverage gaps |
| OS sandbox escape | Unprivileged runtime, patched dependencies, adversarial tests, independent review |
| Tool-hook bypass | Enforce filesystem/process/network rules outside the model/tool hook |
| Existing user changes lost | Isolated copy/worktree; never auto-reset the source |
| Secrets passed into agent | Do not mount/pass secrets by default; use scoped credentials only if needed |
| Too many approval prompts | Narrow workspace and risk-based, one-time approvals |
| Audit log rewritten | Hash chaining, restricted writer, honest tamper-evidence language |
| Cross-platform complexity | One backend first; independent per-platform tests |
| Agent API changes | Versioned adapters and compatibility tests |
| Competitors already solve the basics | Compare real features; focus on evidence, UX, and verified guarantees |
| Unsafe default on setup failure | Fail closed; never silently run unguarded |

## Success metrics
- Blocked prohibited actions in the declared test suite.
- Number of unexplained false negatives (release blocker).
- Agent task completion rate under policy.
- False-positive blocks and approval prompts per task.
- Startup/runtime overhead.
- Percentage of sessions with complete report and verified audit chain.
- Coverage gaps disclosed correctly.
- Snapshot creation and recovery success.
- Developer ability to explain why an action was blocked.
- Independent security review findings.

## Decision log template
For each major decision, record:
- Date and author.
- Decision.
- Alternatives considered.
- Threat model and tradeoffs.
- Tests that validate the decision.
- Known limitations.
- Conditions that would trigger reconsideration.

## Research references
- [OpenAI — Running Codex safely at OpenAI](https://openai.com/index/running-codex-safely/)
- [OpenAI — Building a safe, effective sandbox to enable Codex on Windows](https://openai.com/index/building-codex-windows-sandbox/)
- [JetBrains — AI coding agent adoption trends, 2026](https://blog.jetbrains.com/research/2026/08/ai-coding-agent-adoption-2026/)
- [OWASP — Excessive Agency](https://genai.owasp.org/llmrisk/llm062025-excessive-agency/)
- [Docker Sandboxes security model](https://docs.docker.com/ai/sandboxes/security/)
- [Claude Code security documentation](https://code.claude.com/docs/en/security)
