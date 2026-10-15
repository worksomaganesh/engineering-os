# GitHub App Integration and Permissions

## Integration model
Use a GitHub App with installation-scoped permissions and webhooks rather than a personal access token copied into repository secrets.

Official starting points:
- [GitHub Apps quickstart](https://docs.github.com/en/apps/creating-github-apps/writing-code-for-a-github-app/quickstart)
- [Checks API guide](https://docs.github.com/en/rest/guides/using-the-rest-api-to-interact-with-checks)
- [List PR files](https://docs.github.com/en/rest/pulls/pulls#list-pull-requests-files)
- [Webhook events](https://docs.github.com/en/webhooks/webhook-events-and-payloads)

Confirm endpoint permission requirements at implementation time because GitHub APIs evolve.

## Least-privilege permission starting point
- Metadata: read.
- Pull requests: read.
- Checks: write to publish the app's own Check Runs.
- Contents: read only if repository files/config must be fetched.
- Actions: read only if workflow-run integration is needed.
- Commit statuses: write only if statuses are used instead of or alongside Checks.

Avoid contents write, merge, deployment, and administration permissions in MVP. Final permissions must be validated against actual endpoints.

## Webhook handling
Verify signatures; validate installation/repository; use delivery IDs for idempotency; persist event before acknowledging; enqueue expensive work; handle uninstall/permission changes; re-fetch head SHA before publishing.

## Check Runs
Include stable name, head SHA, timestamps, status/conclusion, summary, annotations where supported, and secure artifact links. Never publish success for stale SHA, missing required evidence, or incomplete report.

## GitHub Actions vs custom runner
Use existing Actions when it already provides safe CI and established scripts. Consider a custom ephemeral runner only when stronger isolation or more precise resource/network controls are required. Do not run untrusted PRs on privileged self-hosted runners.

## Secrets and forks
No secrets by default. Use scoped test credentials only when necessary. Keep App private key/webhook secret in a secret manager. Never log or send secrets to a model. Treat PR text, branch names, file names, code, fixtures, and tool output as untrusted. Do not interpolate them into shell commands.

## Rate limits and privacy
Respect rate-limit headers; use bounded backoff; cancel stale runs; cap concurrency; keep artifacts private with expiry. Before installation, disclose what content is read, where it is processed, external model-provider use, retention, and deletion/uninstall behavior.
