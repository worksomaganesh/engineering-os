# Data Model and Evidence Schema

## Design rules
Every result is bound to repository, PR, exact SHA, and policy version. Store plan separately from execution, preserve raw output separately from AI summaries, use versioned enums, and record provenance. Logs, screenshots, traces, and diffs may be sensitive.

## Core entities
### PullRequestRun
`run_id`, installation/repository IDs, repository name, PR number, base/head SHA, webhook delivery ID, policy digest, planner version, status, timestamps, stale timestamp, report ID.

### ChangeItem
`change_item_id`, run ID, path, change type, diff reference, affected component, sensitive area, classification source/evidence, inference status.

### VerificationObligation
`obligation_id`, run ID, title, behavior at risk, severity, likelihood, evidence strength, source references, requiredness, planned check IDs, status, gap reason, policy decision.

### CheckDefinition
`check_id`, name, kind (unit, integration, static, security, contract, migration, browser, performance), trusted source, command-template ID, environment profile, timeout, network profile, requiredness, version.

### CheckExecution
`execution_id`, run ID, check ID, head SHA, attempt number, runner image digest, tool versions, start/end, exit code, status, parsed summary, raw log/report/coverage artifact IDs, environment digest.

### EvidenceItem
`evidence_id`, run ID, obligation ID, execution ID, type (test case, log, trace, screenshot, static finding, coverage, diff, config, human decision), source, artifact reference, content digest, timestamp, sensitivity, limitations.

### RiskFinding
`finding_id`, run ID, category, severity, likelihood, title, rationale, source references, related obligations, status, human decision.

### Report
`report_id`, run ID, schema version, generated time, required-check summary, obligation summary, risk summary, coverage gaps, final conclusion, conclusion-policy version, artifact references.

## Status vocabulary
`passed`, `failed`, `timed_out`, `cancelled`, `blocked`, `skipped`, `not_run`, `inconclusive`, `stale`, `review_required`. Not-run is not the same as skipped. Unknown or malformed output is not pass.

## Example evidence record
```json
{
  "schema_version": 1,
  "evidence_id": "ev-example-001",
  "run_id": "run-example-001",
  "obligation_id": "webhook-idempotency",
  "execution_id": "integration-007",
  "evidence_type": "test_report",
  "source": "junit-adapter",
  "artifact_id": "private-artifact-007",
  "content_digest": "sha256:example",
  "sensitivity": "private",
  "limitations": ["Synthetic webhook fixture; no live payment provider contacted"]
}
```

## Integrity and retention
Hash or otherwise identify artifacts; preserve raw output; keep parsed values traceable; restrict artifact access; expire links; redact tokens and personal data; avoid full source retention by default; record artifact upload failure instead of pretending evidence exists.
