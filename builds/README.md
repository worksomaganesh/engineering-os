# Builds and Experiments

Use this folder for prototypes, experiments, and product concepts that turn engineering knowledge into practical systems. A build may begin as a researched specification before code exists; each project must clearly state its current status.

## Projects

| Project | Purpose | Status |
|---|---|---|
| [GeM Tender Copilot](gem-tender-copilot/README.md) | Research-backed blueprint for an evidence-first tender PDF analysis and bid-readiness assistant for Indian MSME sellers | Concept / implementation blueprint |
| [WhatsApp Lead Rescue](whatsapp-lead-rescue/README.md) | Action-first assistant for finding unanswered WhatsApp enquiries and promised sales actions | Concept / implementation blueprint |
| [GST Reconciliation Copilot](gst-reconciliation-copilot/README.md) | Evidence-first purchase-register vs GSTR-2B reconciliation and discrepancy workbench for CA/finance teams | Concept / implementation blueprint |
| [AI Agent Firewall](ai-agent-firewall/README.md) | Local guardrails, scoped approvals, sandbox enforcement, audit events, and reports for AI coding-agent sessions | Concept / implementation blueprint |
| [AI PR Verification Agent](ai-pr-verification-agent/README.md) | GitHub App blueprint for change-specific test planning, safe check execution, browser smoke tests, and evidence-backed PR reports | Concept / implementation blueprint |

## What Each Project Should Document

Where applicable, a project folder should contain:
- `README.md` — project overview, problem, users, proposed solution, scope, and navigation.
- Product requirements and acceptance criteria.
- Architecture and end-to-end data flow.
- Data model and important interfaces.
- Evaluation, testing, and measurable quality gates.
- Security, privacy, and domain-specific risk controls.
- Roadmap, validation plan, risks, and open decisions.
- Source links for claims, platform behavior, and official guidance.

Not every small experiment needs all these files. Use enough documentation to make the problem, implementation, and limitations understandable.

## Engineering Principles

- Document what exists separately from what is proposed.
- Prefer a small working end-to-end slice over a large unvalidated feature list.
- Preserve source evidence and make important results reproducible.
- Test failures, edge cases, and security boundaries—not only the happy path.
- Measure performance, quality, and cost before making claims.
- Keep secrets and private data out of source control.
- Update the relevant project README and this index when adding a build.
