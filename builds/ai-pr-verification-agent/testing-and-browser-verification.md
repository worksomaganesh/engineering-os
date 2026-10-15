# Test Strategy and Browser Verification

## Testing layers
1. **Deterministic checks:** formatting, lint, type checking, unit tests, build.
2. **Integration/contracts:** database/service boundaries, API schema, provider webhooks, migrations, retries, idempotency.
3. **Static/dependency security:** integrate existing SAST, code scanning, dependency and secret scanning; a clean scan is not proof of no vulnerabilities.
4. **Browser smoke tests:** Playwright or the repository's existing framework for changed critical user journeys.
5. **Targeted exploratory tests:** malformed inputs, permission boundaries, concurrency, migration compatibility, and degraded dependencies.

## Browser workflow
1. Build from exact PR head SHA.
2. Launch with test-only configuration.
3. Use synthetic fixtures/disposable database.
4. Wait for a health/readiness signal.
5. Run approved browser tests.
6. Collect JUnit/JSON/HTML reports, screenshots, and traces.
7. Record browser version, app SHA, runner image, command, timing, and setup/teardown.
8. Tear down resources and link artifacts to obligations.

Official guides: [Playwright introduction](https://playwright.dev/docs/intro), [CI guide](https://playwright.dev/docs/ci-intro), [test reports](https://playwright.dev/docs/test-reports).

## Example scenarios
**Authentication:** valid login, invalid credentials, protected route, logout/session refresh, OAuth callback errors, password reset if affected.

**Billing:** checkout in test mode, success/cancel URLs, webhook-driven state, duplicate webhook, cancellation and payment failure. Never use live payments.

**Data/CRUD:** permission boundaries, invalid inputs, empty states, cross-user resource access, migration on a representative prior schema.

**API contract:** validation, error responses, required/optional fields, auth behavior, pagination, and client handling.

## Evidence
Capture test name/status, command, Playwright/browser version, app SHA, runner image, trace/screenshot, console errors, relevant failed requests, assertions, setup/teardown, provider mocks, and limitations. Artifacts can contain tokens or personal data; use synthetic data, access controls, redaction, and retention limits.

## Coverage pitfalls
- Line coverage is not behavioral coverage.
- A passing happy path does not prove negative/security cases.
- Mocks may hide real provider problems.
- A flaky test that passes on retry remains flaky.
- Malformed reports are inconclusive.
- Tests added in the PR can share the implementation's incorrect assumptions.
- Generated tests must not delete/weaken existing assertions.
- Test environments do not prove production configuration/performance unless represented.

## Cost-aware selection
Run fast deterministic checks first. Select expensive suites by changed behavior and risk. Use safe immutable cache keys and bind evidence to SHA. Show checks omitted due to budget or environment limitations.
