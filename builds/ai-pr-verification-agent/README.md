# AI PR Verification Agent — Evidence That a Pull Request Was Actually Tested

> **Product promise:** Don't just review the code an AI agent wrote. Build an evidence-backed report of what changed, what could break, which checks ran, which critical behaviors were actually exercised, and what remains unverified.

**Status:** Researched product concept and implementation blueprint. This folder documents a proposed product, not an already-built GitHub App. The idea is narrower than generic AI code review: **verification for changes produced by AI coding agents**, using the same disciplined workflow that should also be usable for any pull request.

## 1. The Exact Problem

A developer asks a coding agent to implement Stripe subscriptions. The agent modifies 17 files, runs the tests it knows about, and opens a pull request. The existing test suite passes. The PR looks plausible.

But the developer still has to ask:
- Did the tests exercise the new subscription path, or did only unrelated unit tests pass?
- Were checkout, webhook processing, idempotency, cancellation, failed payments, and access-control boundaries considered?
- Was the database migration applied to a representative database?
- Does the OAuth/session flow still work?
- Did the change introduce a security weakness, broken API contract, or production configuration issue?
- What ran, in which environment, against which commit, and what did it actually prove?
- Which important behavior remains untested?

The painful gap is between **code generation** and **verified behavior**.

A code review can explain a change. A verification system should assemble evidence from tests and tools that run against the exact proposed revision, state the limits of that evidence, and make missing critical checks visible.

## 2. Why This Is Timely — Evidence and Caveats

Recent developer surveys point to a verification bottleneck:
- Sonar's January 2026 *State of Code Developer Survey*, based on more than 1,100 professional developers, reported that 96% did not fully trust AI-generated code, 38% said review took more effort than reviewing human-written code, and only 48% said they always verify AI-generated code before committing. This is vendor-sponsored survey research; it describes respondents' reported experience, not every developer or a direct measurement of this product's potential. [Sonar research](https://www.sonarsource.com/blog/state-of-code-developer-survey-report-the-current-reality-of-ai-coding/)
- Black Duck's June 2026 research release reported that nearly 90% of surveyed teams encountered AI-generated-code issues, with manual review (52%), security testing (51%), and rework (48%) prominent bottlenecks. It is also vendor research and should be read with its methodology and framing in mind. [Black Duck study release](https://news.blackduck.com/2026-06-09-AI-Coding-Hits-97-Enterprise-Adoption-New-Black-Duck-Study-Shows-Governance-Is-the-ROI-Multiplier)
- JetBrains' August 2026 report, based on its Developer Ecosystem Survey of more than 15,000 professional developers, reported that 90% of respondents used AI coding agents at work at least weekly and 68% daily during May–July 2026. That is a survey result, not a universal census. [JetBrains research](https://blog.jetbrains.com/research/2026/08/ai-coding-agent-adoption-2026/)

Together, these reports support investigating the workflow. They do **not** prove that an AI PR verifier automatically improves software quality, nor that the market is empty.

There are mature existing tools for code review, static analysis, dependency scanning, CI, and browser automation. The differentiation must be the **verification plan, traceable evidence, and honest coverage report**, not simply adding an LLM comment to a pull request.

## 3. Product Definition

AI PR Verification Agent is a GitHub App that runs a bounded verification workflow when a pull request opens or changes.

It will:
1. Identify the exact base and head commit.
2. Read the diff and relevant repository context.
3. Classify changed behavior and map it to potential failure modes.
4. Propose a targeted verification plan.
5. Select and run permitted checks in an isolated CI environment.
6. Collect test results, coverage data where available, static-analysis/security outputs, and browser smoke-test evidence.
7. Compare planned critical behaviors against the checks that actually executed.
8. Publish a risk-and-evidence report on GitHub, including what was not verified.
9. Request additional checks or human review when evidence is insufficient.

It should never say "the PR is safe" just because a model gave a confident explanation or a test command exited with zero.

## 4. The Key Difference: A Verification Report, Not Just an AI Review

An AI code-review tool commonly answers: "What might be wrong in this diff?"

This project should answer four connected questions:

1. **What changed?** Identify touched components, public APIs, data models, authorization boundaries, and user-visible flows.
2. **What could break?** Build a change-specific list of plausible regressions and risks, supported by repository context.
3. **What was tested?** Record the actual command/workflow, environment, commit SHA, exit code, test report, and relevant evidence.
4. **What remains unverified?** Show missing high-value checks, failed checks, skipped tests, unavailable dependencies, and coverage limitations.

Example:

| Area | Verification status | Evidence |
|---|---|---|
| Subscription unit tests | Passed | Test run for exact PR head SHA |
| Webhook signature validation | Passed | Security test case plus CI artifact |
| Database migration | Passed in ephemeral PostgreSQL | Migration job output and schema check |
| Browser checkout flow | Passed | Playwright trace and screenshot |
| Cancellation after failed payment | Not tested | Scenario mapped from change; no matching test found |
| Production Stripe live-mode behavior | Not tested | No live financial operations are executed in this environment |

The last row is essential: tests can establish behavior only within their defined inputs and environment. A sandbox test cannot prove every real production integration works.

## 5. Example Risk Report

The following is fictional UI content, not the output of a real product run.

```text
AI PR VERIFICATION REPORT
Pull request: #142
Head commit: 91ab...example
Run ID: verify-2026-10-15-001

CHANGE UNDERSTANDING
- Subscription creation and cancellation paths modified
- Database schema and webhook handler changed
- Authentication/session logic touched

RISK FINDINGS
- REGRESSION: HIGH
  Cancellation after payment failure needs a targeted test.
- SECURITY: MEDIUM
  Webhook signature validation changed; required negative tests passed.
- DATABASE: MEDIUM
  Migration passed against the supported PostgreSQL test version.
- API CONTRACT: LOW
  No public request/response schema change detected by configured checks.

VERIFICATION EVIDENCE
- Unit tests: 127 passed, 3 failed
- Integration tests: passed
- Browser checkout smoke test: passed
- Password reset flow: not run
- Static analysis: 2 findings requiring review

CONCLUSION
Status: REVIEW REQUIRED
Reason: 3 test failures and one high-risk scenario remain unresolved.
```

The report must display the exact check source and output. An LLM may summarize known evidence, but may not invent test counts or turn missing evidence into a pass.

## 6. MVP Scope

### First release
- One GitHub App installed on explicitly selected repositories.
- Subscribe to pull-request events such as opened, synchronized, and reopened.
- Read PR metadata, diff, and relevant repository files using least-privilege permissions.
- Create a structured change-impact/verification plan.
- Run existing safe CI checks or a small configurable check catalog in an isolated runner.
- Support one browser-test adapter such as Playwright for projects that already provide a local test environment.
- Collect artifacts and commit-specific check results.
- Publish a GitHub Check Run with detailed steps/annotations where supported.
- Produce a report separating passed, failed, skipped, not run, inconclusive, and blocked.
- Keep human approval for dangerous or environment-sensitive test actions.
- Never auto-merge or deploy in the MVP.

### Not in the first release
- A guarantee of bug-free code or complete security.
- Running untrusted PR code with production credentials or privileged self-hosted runners.
- Executing migrations or browser tests against production data.
- Inventing tests that simply confirm the new code's current behavior without checking requirements.
- Replacing human code review, CI, CodeQL/SAST, dependency scanning, or domain-specific test design.
- Automatic merging solely based on an AI verdict.
- Testing every possible state, browser, database, concurrency condition, or external provider response.

## 7. Recommended Reading Order

- [Product requirements](product-requirements.md) — use cases, users, MVP, states, acceptance criteria.
- [Technical architecture](technical-architecture.md) — GitHub event ingestion, verification planning, runner isolation, results, reporting.
- [Verification workflow and risk taxonomy](verification-workflow.md) — how changed code becomes a test plan and an evidence-based status.
- [Data model and evidence schema](data-model.md) — commits, plans, executions, results, artifacts, and report facts.
- [Test strategy and browser automation](testing-and-browser-verification.md) — unit/integration/security/E2E strategy, Playwright, coverage caveats.
- [GitHub App permissions and integration](github-app-and-permissions.md) — webhooks, Checks API, permissions, and safe installation.
- [Security and threat model](security-and-threat-model.md) — untrusted PR code, prompt injection, secrets, isolation, supply-chain risk.
- [Evaluation and release gates](evaluation-plan.md) — benchmark, metrics, false claims, acceptance thresholds.
- [Roadmap and differentiation](roadmap.md) — milestones, experiments, existing alternatives, risks, and open decisions.

## 8. Existing Ecosystem and Differentiation

This is a crowded adjacent space. GitHub Apps can publish rich check runs and annotations; GitHub Actions runs CI workflows; CodeQL/code scanning finds supported classes of security issues; Playwright automates browser tests; Sonar and other vendors provide code analysis and AI-oriented verification features.

Useful references:
- [GitHub Checks API](https://docs.github.com/en/rest/guides/using-the-rest-api-to-interact-with-checks)
- [GitHub pull request files API](https://docs.github.com/en/rest/pulls/pulls#list-pull-requests-files)
- [GitHub code-scanning alerts](https://docs.github.com/en/code-security/concepts/code-scanning/code-scanning-alerts)
- [Playwright test reports](https://playwright.dev/docs/test-reports)
- [OWASP Secure Coding with AI Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Secure_Coding_with_AI_Cheat_Sheet.html)
- [Sonar AI code verification and quality](https://www.sonarsource.com/blog/state-of-code-developer-survey-report-the-current-reality-of-ai-coding/)

Potential differentiation to test:
- Map changed behavior to specific verification obligations.
- Track a verification plan separately from results actually executed.
- Make evidence clickable and bound to the exact commit and environment.
- Call out untested high-risk scenarios instead of publishing a vague "AI approved" badge.
- Start browser-level smoke checks only when a safe, reproducible app/test environment exists.
- Show a useful negative conclusion: "not verified" can be more valuable than an ungrounded green check.

## 9. Research and Official References

- [Sonar — State of Code Developer Survey, 8 January 2026](https://www.sonarsource.com/blog/state-of-code-developer-survey-report-the-current-reality-of-ai-coding/)
- [Black Duck — 2026 AI coding study release, 9 June 2026](https://news.blackduck.com/2026-06-09-AI-Coding-Hits-97-Enterprise-Adoption-New-Black-Duck-Study-Shows-Governance-Is-the-ROI-Multiplier)
- [JetBrains — AI Coding Agents: Adoption Trends, August 2026](https://blog.jetbrains.com/research/2026/08/ai-coding-agent-adoption-2026/)
- [GitHub Apps quickstart](https://docs.github.com/en/apps/creating-github-apps/writing-code-for-a-github-app/quickstart)
- [GitHub Checks REST API guide](https://docs.github.com/en/rest/guides/using-the-rest-api-to-interact-with-checks)
- [GitHub pull request files API](https://docs.github.com/en/rest/pulls/pulls#list-pull-requests-files)
- [GitHub code-scanning alerts](https://docs.github.com/en/code-security/concepts/code-scanning/code-scanning-alerts)
- [Playwright Test introduction](https://playwright.dev/docs/intro)
- [Playwright CI guidance](https://playwright.dev/docs/ci-intro)
- [OWASP Secure Coding with AI Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Secure_Coding_with_AI_Cheat_Sheet.html)

**Boundary:** this is a proposed product blueprint, not a claim that an implementation exists or that a particular AI-generated code change is correct. The system must tie every result to observable evidence and the exact source revision.
