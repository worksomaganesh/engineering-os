# Roadmap and Differentiation

## Phase 0 — validate the problem
Interview developers who review agent-authored PRs; compare existing code review, CI, static analysis, and test tools; choose one framework; build a benchmark of PRs with known missing tests; prototype the report; estimate GitHub API and runner costs.

**Gate:** target users confirm the report reveals meaningful gaps not already obvious in current CI.

## Phase 1 — advisory MVP
GitHub App webhook/idempotency, diff/context collection, risk hypotheses, structured verification obligations, existing CI ingestion, planned-vs-executed reconciliation, GitHub Check Run. Avoid arbitrary command execution initially.

**Gate:** grounded, useful reports and zero false-green in deterministic tests.

## Phase 2 — safe execution
Trusted policy, ephemeral runners, allowlisted commands, resource limits, structured test parsers, SHA binding, stale-run cancellation, no production secrets.

**Gate:** adversarial PRs cannot access host secrets or weaken policy in the supported environment.

## Phase 3 — browser smoke tests
Playwright adapter, one or two supported app templates, synthetic data, readiness/teardown, screenshots/traces, provider mocks.

**Gate:** reproducible browser evidence for bounded critical journeys.

## Phase 4 — risk-aware verification
Framework-specific change analyzers, API/migration checks, targeted security scenarios, risk-based test selection, review UI.

**Gate:** benchmark improves useful obligation recall without unacceptable noise/cost.

## Phase 5 — team adoption
Repository policy templates, organization controls, analytics, retention settings, optional enterprise runners, more language/framework adapters.

## Existing alternatives to investigate
- [GitHub CodeQL/code scanning](https://docs.github.com/en/code-security/concepts/code-scanning/code-scanning-alerts) — static security analysis.
- [GitHub Checks API](https://docs.github.com/en/rest/guides/using-the-rest-api-to-interact-with-checks) and [GitHub Actions](https://docs.github.com/en/actions) — status and CI execution.
- [Playwright](https://playwright.dev/) — browser automation.
- [Sonar](https://www.sonarsource.com/) — code quality/static analysis.
- [Qodo](https://www.qodo.ai/), [CodeRabbit](https://www.coderabbit.ai/), [Greptile](https://www.greptile.com/), and [Graphite](https://graphite.dev/) — adjacent code review/developer workflow products.

This is not a complete competitive matrix or endorsement. Verify current features and pricing before making differentiation claims.

## Differentiation hypotheses
1. Map each material change to concrete verification obligations.
2. Separate suggested, executed, passed, failed, and unverified.
3. Link evidence to exact SHA, runner, command, environment, and artifact.
4. Run browser checks only where a safe test environment exists.
5. Make high-risk missing evidence visible instead of generating a vague green score.
6. Integrate existing CI/security tools rather than rebuild them all.
7. Make privacy and runner safety first-class.

## Key risks
Crowded market; false confidence; unsafe execution; prompt injection; flaky tests; high latency/cost; incomplete repository context; data privacy; overclaiming. Mitigate with deterministic status rules, isolation, bounded context, transparent gaps, and measured pilots.

## Open decisions
First framework; Actions vs custom runner; mandatory vs advisory checks; trusted policy update process; model provider and data retention; artifact privacy; cost ceiling; treatment of PR-authored tests; evidence threshold for success/review-required.
