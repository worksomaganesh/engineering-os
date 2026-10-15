# Evaluation Plan and Release Gates

## Evaluation question
Does the system find meaningful verification gaps and accurately report evidence without false-green outcomes, unsafe execution, or excessive noise?

## Benchmark corpus
Use licensed/synthetic PRs covering bug fixes, multi-file features, auth changes, migrations, provider integrations, API contracts, dependency upgrades, UI changes, performance-sensitive code, vulnerable patches, weakened tests, malicious prompt-injection text, missing critical tests, and force-push races.

For each PR, maintain expert-reviewed ground truth: changed behavior, risk categories, required obligations, available checks, known gaps, and expected outcomes. Have reviewers independently label a subset and resolve disagreements.

## Metrics
- Obligation recall and precision.
- Evidence grounding: claims linked to evidence or labelled inference.
- False-green rate for missing/failed required checks.
- Stale-result rate.
- Test-selection value per runtime/cost.
- Test-output parser accuracy.
- Prompt-injection resistance.
- Runner isolation success.
- Reviewer usefulness and time saved.
- Latency, cost/run, flake rate.

## Proposed release gates
- Zero false-green outcomes in deterministic result/policy tests.
- Every result identifies exact head SHA and policy digest.
- Old results never appear current after force-push.
- Malformed output cannot become pass.
- Prompt-injection fixtures cannot change policy/conclusion.
- Runner tests verify prohibited resources are inaccessible.
- Webhook signature/replay/idempotency tests pass.
- No production credentials in test environments by default.
- Artifact access/retention tests pass.
- Security review of runner isolation and GitHub permissions completed.

These are proposed internal gates, not a claim of universal security.

## Failure injection
Test duplicate/out-of-order webhooks, API rate limits, force-push during execution, runner loss/timeouts, artifact-store outage, model outage, malformed reports, missing artifacts, contradictory model summary, PR-modified policy, fork secret access, and browser attempts to contact production endpoints.

## Human pilot
Start in advisory mode on a non-critical repository. Measure baseline review time and CI; ask reviewers to rate useful/noisy/missing findings; compare plans to actual tests and later bugs; measure latency and cost. Do not claim bug reduction from anecdotes alone.

## Launch checklist
- [ ] GitHub App permissions reviewed.
- [ ] Threat model/data flow documented.
- [ ] Supported languages/runners documented.
- [ ] Parsers tested with fixtures.
- [ ] False-green and stale-SHA tests pass.
- [ ] Prompt-injection and untrusted-code tests pass.
- [ ] Retention/deletion verified.
- [ ] Cost and rate limits monitored.
- [ ] Uninstall/disable path works.
- [ ] Human-review fallback is clear.
- [ ] Claims match measured evidence.
