# Verification Workflow and Risk Taxonomy

## Verification obligation
A concrete behavior that should be tested because of a change. Each obligation includes a title, behavior at risk, reason/evidence references, severity, expected outcome, proposed check, requiredness, execution state, and limitations.

Example: "If a Stripe webhook is delivered twice with the same event ID, subscription state must not be applied twice." Evidence points to the changed webhook handler and persistence logic; verification replays a synthetic event twice and checks one effective state transition.

## Workflow
1. **Establish identity:** repository, PR, base/head SHA, policy digest, run ID.
2. **Understand the diff:** identify API/schema, database, auth, external integration, UI, dependency, and configuration changes.
3. **Derive risk hypotheses:** regression, access-control bypass, data migration, idempotency/concurrency, contract break, external failure handling, performance, unsafe logging.
4. **Plan checks:** fast existing checks first; then targeted unit/integration, static/security, contract/migration, browser smoke tests, and justified adversarial tests.
5. **Apply policy:** reject production deploys, live payments, real customer messaging, host-secret access, and uncontrolled network access.
6. **Execute:** record command/template, SHA, runner image, tool versions, timing, exit status, parsed test results, artifacts, retries, and limitations.
7. **Reconcile:** compare obligations against actual runs.
8. **Publish:** create a commit-bound report; mark old runs stale after force-push.

## Obligation statuses
- **Verified by configured test:** relevant check ran and passed under its defined conditions.
- **Failed:** check ran and failed.
- **Partially verified:** only some conditions were exercised.
- **Not run:** no execution occurred.
- **Blocked:** policy/environment prevented execution.
- **Inconclusive:** output was missing, malformed, or contradictory.
- **Human review required:** test evidence cannot settle a design or semantic question.

"Verified" is scoped to test conditions; it does not mean universally correct.

## Risk dimensions
Use separate dimensions: severity, likelihood, evidence strength, verification gap, exposure, and reversibility. Categories include security, regression, database/data, API contract, external integration, UI/browser, performance/reliability, and build/deployment.

## Example subscription verification matrix
| Obligation | Useful check | Evidence | Common gap |
|---|---|---|---|
| Checkout succeeds | Integration test in provider test mode | State/result assertions | UI renders but request fails |
| Duplicate webhook | Replay same event twice | One effective state transition | Only one delivery tested |
| Invalid signature | Negative fixture | Rejected without mutation | Only happy path |
| Payment failure | Provider test event/fixture | Expected state/access behavior | Failure state missing |
| Cancellation | Service and browser flow | DB and UI agree | Only DB method tested |
| Authorization | User A requests User B resource | Denied, no leak | Only authenticated happy path |
| Migration | Apply on empty and representative prior schema | Schema/data invariants | Migration never executed |
| Browser checkout | Playwright in isolated test environment | Trace and assertions | Live provider/customer used |

## Test-generation guardrails
Generated tests are proposals until run. Prefer repository conventions; assert business invariants; include negative cases; never weaken assertions or skip failures silently. Record whether tests pre-existed, came from the PR, or were proposed by the verifier.
