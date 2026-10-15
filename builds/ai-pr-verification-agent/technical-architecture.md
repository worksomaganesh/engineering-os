# Technical Architecture

## End-to-end flow
1. GitHub PR webhook arrives.
2. Receiver verifies signature and delivery ID.
3. Coordinator resolves the exact base/head SHA and trusted policy.
4. Diff/context collector identifies changed files, symbols, tests, schemas, migrations, and routes.
5. Change analyzer proposes evidence-backed risk hypotheses.
6. Planner converts hypotheses into concrete verification obligations.
7. Policy gate validates proposed checks and their permissions.
8. Isolated runner executes approved tests/static analysis/browser checks.
9. Result normalizer parses structured output and preserves raw artifacts.
10. Evidence reconciler compares planned obligations with actual results.
11. Report assembler publishes a GitHub Check Run and links to protected artifacts.

## Components
- **Webhook receiver:** signature validation, installation authorization, idempotency, durable queueing.
- **Run coordinator:** run IDs, SHA binding, concurrency limits, cancellation of stale runs, retry handling.
- **Context collector:** bounded diff and relevant repository files; avoid indiscriminate repository ingestion.
- **Change analyzer:** language-aware tools plus LLM hypotheses; every claim is marked observed, tool-derived, or inferred.
- **Verification planner:** creates scenarios, preconditions, expected outcomes, check type, requiredness, and evidence requirements.
- **Policy gate:** accepts only trusted command templates and policy; rejects privileged arbitrary commands and production side effects.
- **Runner adapter:** ephemeral isolated jobs with resource, time, filesystem, network, and output limits.
- **Browser adapter:** app test configuration, synthetic seed data, readiness check, Playwright execution, trace/screenshots, teardown.
- **Result normalizer:** translates JUnit/JSON/Playwright and tool-specific outputs; malformed output becomes inconclusive.
- **Evidence reconciler:** no planned test counts as evidence until executed; passing a suite does not prove every obligation was covered.
- **Report assembler:** deterministic conclusion logic and Check Run publishing.

## Suggested MVP storage
- PostgreSQL or SQLite for runs, obligations, policies, and results.
- Durable queue for asynchronous work if needed.
- Private object storage for larger artifacts with retention limits.
- GitHub Checks API as reviewer-facing status.
- Secret manager for GitHub App private key and webhook secret.

Store only required context; define retention/deletion rules. Consider orchestrating existing GitHub Actions first rather than immediately building a custom runner platform.

## Failure handling
- Duplicate webhook: acknowledge idempotently.
- Rate limit: bounded backoff.
- PR head changes: old run becomes stale.
- Runner loss/timeout: interrupted or inconclusive, never passed.
- Artifact upload failure: report missing evidence.
- Model unavailable: run deterministic checks and mark semantic planning incomplete.
- Invalid policy: stop unsafe execution.
- Report publication failure: do not emit success.
