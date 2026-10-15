# Product Requirements

## Objective
For every pull request, create a traceable report of changed behavior, likely risks, checks actually executed, their outcomes, and important scenarios still unverified. The system reports evidence, not confidence theater.

## Users
- **Developer:** wants to know whether an AI-authored change has meaningful test evidence.
- **Reviewer/tech lead:** wants to focus on risky behavior and missing checks.
- **Platform/security engineer:** needs controlled execution, least privilege, and audit records.

## Core user stories
- Inspect changed modules, public interfaces, schemas, auth boundaries, and user journeys.
- Distinguish tests proposed from tests that actually ran.
- Open logs, test reports, browser traces, and screenshots tied to the exact head SHA.
- Configure allowed checks, runner environments, timeouts, and required evidence.
- See failed, skipped, blocked, inconclusive, and unverified scenarios.
- Record human waivers with a reason and identity where policy permits.

## Functional requirements
1. **Webhook intake:** authenticate GitHub webhook events; handle duplicate deliveries idempotently; record repository, PR number, base/head SHA, delivery ID, and timestamps.
2. **Change understanding:** inspect bounded diff/context; classify code, API, database, dependency, auth, configuration, and UI changes; link claims to files/lines; label uncertain inferences.
3. **Verification planning:** create structured obligations with risk, reason, setup, expected result, proposed check, requiredness, and evidence needed.
4. **Safe execution:** run only approved checks in isolated ephemeral jobs; apply time/resource/output limits; record exact commit, environment, versions, command template, exit status, and artifacts.
5. **Browser checks:** optionally run Playwright with test-only config and synthetic data; capture results, screenshots/traces, console errors, and relevant failed requests.
6. **Evidence reconciliation:** compare planned obligations with checks actually run; missing evidence is not a pass.
7. **GitHub reporting:** publish a Check Run with risk summary, checks, failures, missing scenarios, artifact links, and limitations.
8. **Trusted policy:** security-sensitive policy must come from a trusted base branch or administrator-approved source, not an unreviewed PR's changed config.
9. **Human decisions:** record waivers and never let a model approve its own high-risk finding.
10. **Stale-run handling:** a force-push invalidates or marks prior results stale.

## Non-functional requirements
- Evidence bound to immutable SHA and policy digest.
- Least privilege and no production secrets by default.
- Reliable retries, idempotency, and explicit partial statuses.
- Privacy-conscious source/artifact retention.
- Versioned schemas and deterministic conclusion logic.
- Cost/rate limits and visible timeouts.
- Readable reports inside GitHub, without requiring a custom dashboard.

## MVP acceptance criteria
- A PR opened or updated triggers one idempotent run bound to the exact head SHA.
- Malicious PR code cannot access configured secrets or host credentials in the supported runner.
- Reports distinguish proposed, executed, passed, failed, skipped, blocked, not-run, and inconclusive checks.
- Required failures and missing high-risk evidence cannot silently produce success.
- A force-push makes old evidence stale.
- Artifacts identify runner/tool versions where available.
- Prompt injection in repository text cannot override policy or force a green conclusion.
- Report failure never produces a green check.
- No automatic merge or production deployment.

## Metrics
Track false-green rate, obligation recall/precision, evidence grounding, stale-result rate, time-to-report, test flakiness, useful findings, cost/run, and runner-isolation failures. Do not optimize only for more tests or green PRs.
