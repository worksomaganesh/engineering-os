# Security and Threat Model

## Objective
Run verification on potentially untrusted PRs without granting them unnecessary authority over the verifier, credentials, other jobs, or external systems.

## Assets
GitHub App private key, webhook secret, installation tokens, private source, runner host, caches, test credentials, artifacts, trusted policy, and integrity of published conclusions.

## Threats and controls
| Threat | Mitigation |
|---|---|
| Malicious PR reads environment | No secrets by default; isolated ephemeral runner |
| Prompt injection in README/comment | Treat repository text as data; deterministic policy gate |
| Command injection through path/branch | Argument arrays; avoid shell interpolation |
| Secret exfiltration | No credentials by default; restricted network |
| Cross-job compromise | Ephemeral workers; no shared privileged workspace |
| Cache poisoning | Separate trust domains and writable caches |
| Policy tampering in PR | Use trusted base-branch/admin policy |
| False-green summary | Structured results determine conclusion; raw records win |
| Stale SHA | Recheck current head before publish |
| Artifact leaks | Synthetic data, redaction, access controls, short retention |
| Spoofed/replayed webhook | Signature verification and idempotency |
| Dependency compromise | Lockfiles, pinned images, scanning, controlled network |
| Resource exhaustion | CPU/memory/time/disk/process/output limits |
| Test weakening | Highlight changed/deleted tests and enforce trusted policy |
| Live external side effect | Mock provider or test mode; block production endpoints |

## Prompt-injection boundary
Source code, comments, docs, PR descriptions, fixtures, and tool output are untrusted. They must not be allowed to change policy, request secrets, upload source, suppress failures, or set the final conclusion. Prompt wording is not a security boundary; permissions and runner controls must be enforced in code.

## Runner isolation
Use ephemeral unprivileged workers, minimal mounts, restricted network, no host Docker socket, bounded resources, and a separate control plane. Patch images and test isolation. Containers share the host kernel and are not sufficient for every threat model; document backend and remaining risk. Fail closed if required isolation is unavailable.

## Evidence integrity
Preserve raw results; record tool versions and SHA; hash artifacts; use deterministic conclusions; restrict policy edits; record human waivers; classify missing or contradictory output as inconclusive.

## Privacy
Minimize source snippets and full repository retention. Disclose external model processing. Redact credentials/personal data. Set artifact retention/deletion. Restrict access and provide an uninstall path.

## Incident response
Support disabling jobs/check publishing, rotating App credentials, revoking installations, preserving sanitized logs, notifying affected owners when exposure may have occurred, and responsibly disclosing vulnerabilities.
