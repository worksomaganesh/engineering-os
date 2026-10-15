# AI Agent Firewall — Local Guardrails, Approvals, and Evidence for AI Coding Agents

> **Product promise:** Let coding agents do useful work inside clear boundaries, while showing you what they attempted, what was allowed or blocked, what changed, and whether the result passed your checks.

**Project status:** Researched product concept and implementation blueprint. The repository contains documentation, not a working firewall implementation.

## 1. The Problem

AI coding agents can do far more than suggest a line of code. Depending on the agent, configuration, and permissions, they may read repositories, edit or delete files, start processes, run tests, access network services, call tools, and create development artifacts such as branches or pull requests.

This changes the security question from "Did the AI generate a bad suggestion?" to:

**"What actions did the agent attempt, which actions was it actually permitted to perform, what evidence do we have, and can we recover safely?"**

A developer may ask an agent to fix one bug but give it a shell, network access, repository write access, and the user's local permissions. A bug, mistaken plan, malicious instruction hidden in repository content, or compromised tool could cause it to read a secret, delete files, install an untrusted package, upload private code, change a Git remote, or run an unexpected command.

## 2. Why This Problem Matters

Research and first-party security guidance support the need for boundaries and observability:

- OpenAI's **8 May 2026** article *Running Codex safely at OpenAI* describes sandbox boundaries, human approvals, network policies, identity controls, and agent-aware telemetry as complementary controls—not one magic permission prompt. [OpenAI source](https://openai.com/index/running-codex-safely/)
- JetBrains' **August 2026** report, based on its Developer Ecosystem Survey of more than 15,000 professional developers, says that in May–July 2026, 90% of surveyed developers used AI coding agents at work at least weekly and 68% used them daily. These are survey findings about respondents, not a universal census of all developers. [JetBrains research](https://blog.jetbrains.com/research/2026/08/ai-coding-agent-adoption-2026/)
- OWASP identifies **excessive agency**—excessive tool functionality, permissions, or autonomy—as a risk that can turn mistaken or manipulated agent behavior into damaging actions. Its mitigations include least privilege, granular tools, human approval, downstream authorization, and monitoring. [OWASP Excessive Agency](https://genai.owasp.org/llmrisk/llm062025-excessive-agency/)
- Docker's documentation describes local agent sandboxes that combine microVM isolation, workspace controls, network policies, and credential isolation. This is evidence that the area already has serious product activity, not an open field without alternatives. [Docker Sandboxes security model](https://docs.docker.com/ai/sandboxes/security/)

## 3. What We Want to Build

A local CLI that launches a supported AI coding agent inside a controlled session, applies policy to risky actions, records decisions and results, and produces a readable end-of-run report.

The idea starts with a command shaped like:

```bash
agent-boundary run --profile balanced -- codex
```

**Working CLI name:** `agent-boundary`. The original `agentguard` name is only a concept placeholder. Research found existing similarly named projects (including AgentGuard, AgentWall, Agent Firewall, Agent Quarantine, and OpenAgentLock), so do not assume a product or command name is available. See [competitive landscape](roadmap.md#competitive-landscape-and-differentiation).

The tool should orchestrate a safe development session:

1. Identify the repository and capture a baseline/snapshot.
2. Start the agent with a constrained filesystem and process environment.
3. Apply policy at actual enforcement boundaries, not only by asking the model to behave.
4. Require approval for configured risky operations and block forbidden ones.
5. Record what the monitor can actually observe, including coverage limitations.
6. Capture resulting file changes, executed test commands, exit statuses, and Git diff.
7. Produce a reviewable report and preserve a recovery point.

## 4. Example User Experience

### Example A — secret access attempt

```text
AGENT ACTION ATTEMPT
Operation: read protected file
Target: .env
Policy: deny protected secret paths
Risk: HIGH

DECISION: BLOCKED
Reason: This path is protected by the active policy.
Evidence: policy event + enforcement backend event
```

The report must distinguish an agent/tool request, an observed process attempt, and a blocked OS-level access. If the implementation cannot observe a particular pathway, it must not imply it can.

### Example B — destructive command

```text
AGENT ACTION ATTEMPT
Operation: delete files
Scope estimate: 42,381 paths
Risk: CRITICAL

DECISION: BLOCKED
Required next step: inspect target scope and create an isolated snapshot.
```

A confirmation button by itself is not protection. The command must remain stopped until a valid, scoped approval is recorded; certain actions may be policy-blocked even if the user is tempted to approve them.

### Example C — end-of-run report

```text
AGENT RUN REPORT
Session: session-2026-10-15-001
Agent: codex
Workspace: ./my-project

Files changed: 83
Files created: 12
Files deleted: 4
Commands observed: 31
Network requests via configured proxy: 17
Secret-path attempts observed: 0
Coverage gaps: direct network outside proxy is blocked by sandbox policy

Tests observed:
  127 passed
  3 failed

Policy events:
  2 medium
  0 critical

Snapshot: created
Final status: review required
```

These numbers are fictional examples. The product must report **observed and verified counts**, disclose the scope of instrumentation, and avoid inventing coverage. "No secret access observed" is not the same as "the agent could not access any secret" unless the enforcement and telemetry actually guarantee that for the configured environment.

## 5. Core Product Principle: Policy Must Be Enforced Outside the Model

Do not ask the AI agent to decide whether its own action is safe and then trust the answer.

Use separate layers:
- **Policy engine:** deterministic allow / require-approval / deny decision.
- **Operating-system sandbox:** enforces filesystem, process, and network boundaries wherever supported.
- **Agent/tool integration:** captures structured tool requests and can gate calls when the particular agent exposes a reliable hook or protocol boundary.
- **Audit/telemetry:** records decisions, observed actions, tool results, process outcomes, and collection coverage.
- **Recovery/review:** preserves the starting state and presents the final changes for human approval.

A wrapper that merely reads shell command strings is not a complete firewall. An agent can use another interpreter, a script, a subprocess, a runtime file API, or a direct network library. Real enforcement requires an appropriate OS sandbox or equivalent boundary; event interception and OS-level controls have different coverage and must be described separately.

## 6. MVP Scope

### In scope
- One operating-system target first (recommended: Linux), one or two supported coding-agent launch paths, and a narrow documented set of guarantees.
- Local CLI with `run`, `policy`, `report`, `snapshot`, and audit-log verification commands.
- Explicit workspace boundary and least-privilege defaults.
- Protected-path rules and dangerous-command policy.
- Deny-by-default or allowlist-based network control through an enforced boundary.
- One-time, exact-action approval for selected high-risk operations.
- Session-level file-change report from a Git baseline.
- Command/test process results with exit codes.
- Structured local JSONL audit log with tamper-evidence checks.
- A coverage report that states what is and is not observed.
- Safe demo mode and a test harness with harmless attack-shaped examples.

### Out of scope initially
- A guarantee that every action from every AI agent on every OS can be observed.
- A cross-platform kernel security product on the first release.
- Automatic production deployment, credential use, financial actions, or irreversible external changes.
- A hosted central management console or mandatory cloud logging.
- Preventing every possible exploit, zero-day, or kernel compromise.
- Treating Git snapshots as rollback for external side effects such as network uploads, database changes, emails, or cloud deployments.
- A claim that AI Agent Firewall is the first tool of its kind; public prior art already exists.

## 7. Documentation Pack

- [Product requirements and acceptance criteria](product-requirements.md)
- [Technical architecture and enforcement layers](technical-architecture.md)
- [Threat model and policy model](threat-model-and-policy.md)
- [CLI workflows and report design](cli-and-workflows.md)
- [Data model and audit events](data-model.md)
- [Evaluation and security test plan](evaluation-plan.md)
- [Security limitations and operating-system boundaries](security-and-limitations.md)
- [Roadmap and competitive landscape](roadmap.md)

## 8. What Success Looks Like

The first successful version is not one that prints scary risk labels. It should demonstrate that:
- Protected paths and forbidden operations are blocked by an actual enforcement mechanism in the supported environment.
- Low-risk tasks remain practical without repetitive approvals.
- High-risk actions pause with the exact target and consequences visible.
- Reports distinguish attempted, allowed, blocked, and completed operations.
- File changes and test outcomes are reproducible and reviewable.
- Incomplete monitoring is disclosed instead of disguised as certainty.
- The tool's security guarantees survive adversarial tests in the declared scope.

## 9. Research Sources

- [OpenAI — Running Codex safely at OpenAI (8 May 2026)](https://openai.com/index/running-codex-safely/)
- [OpenAI — Building a safe, effective sandbox to enable Codex on Windows (13 May 2026)](https://openai.com/index/building-codex-windows-sandbox/)
- [OpenAI — Codex Security research preview (6 March 2026)](https://openai.com/index/codex-security-now-in-research-preview/)
- [JetBrains — AI Coding Agents: Adoption Trends (August 2026)](https://blog.jetbrains.com/research/2026/08/ai-coding-agent-adoption-2026/)
- [OWASP — LLM06:2025 Excessive Agency](https://genai.owasp.org/llmrisk/llm062025-excessive-agency/)
- [Docker — Sandboxes security model](https://docs.docker.com/ai/sandboxes/security/)
- [Docker — isolation layers](https://docs.docker.com/ai/sandboxes/security/isolation)
- [OWASP — Agentic Security Initiative](https://genai.owasp.org/2024/12/15/announcing-the-owasp-llm-and-gen-ai-security-project-initiative-for-securing-agentic-applications/)
- [AgentWall](https://github.com/balyakin/agentwall)
- [Agent Firewall](https://github.com/asale-ai/agent-firewall)
- [Agent Quarantine](https://github.com/spacegiyou/agent-quarantine)
- [OpenAgentLock](https://github.com/openagentlock/OpenAgentLock)
- [AgentGuard](https://github.com/Caua-ferraz/AgentGuard)

**Status reminder:** a strong project blueprint is not a working security control. Before any use on valuable work, implement the enforcement backend, test its actual boundaries, document limitations, and treat every claim about blocking/monitoring as a testable security property.
