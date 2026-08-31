# CyberOS Secure Execution Model

## Principle

CyberOS is an orchestration platform for authorized security work. Execution must be deterministic, scoped and auditable.

## Request path

```text
User/API/AI
   |
   v
Capability request
   |
   v
Authorization resolver
   |
   v
Scope resolver
   |
   v
Policy engine
   |
   v
Job signer
   |
   v
Queue
   |
   v
Isolated worker
   |
   v
Registered tool adapter
   |
   v
Normalized result/evidence
   |
   v
Finding + audit event
```

## Policy checks

Before execution, the policy engine verifies:

- authenticated actor
- tenant ownership
- subscription entitlement
- valid authorization
- engagement state
- target in scope
- target not excluded
- capability permitted
- execution time window
- worker trust state
- tool version/policy compatibility

Failure results in `blocked`; the worker is never invoked.

## Execution environments

The platform will support disposable execution environments:

- minimal CyberOS worker image
- security-tool containers
- Kali-based tool image where required
- specialized scanner images
- customer connector execution

Kali tooling is isolated behind adapters. The control plane must not depend on Kali-specific command-line behavior.

## Secrets

Secrets are injected at runtime from a secret-management system. They must never appear in job definitions, logs, prompts, source control or evidence unless explicitly classified and protected.

## AI guardrails

AI may:

- summarize findings
- correlate intelligence
- recommend remediation
- propose an assessment plan
- generate reports
- request a pre-defined capability

AI may not:

- invent authorization
- expand scope
- disable policy controls
- directly execute arbitrary shell commands
- retrieve another tenant's data
- silently alter an approved engagement

## Kill switch

Every worker and connector must support cancellation. Long-running operations must periodically check cancellation state.

## Evidence

Results are normalized and stored with provenance. Raw tool output should be retained according to tenant policy and data-retention requirements.

## Future active-testing milestone

Authorized active testing will require an engagement record, signed scope, explicit capabilities, target allowlists, exclusions, time windows, rate controls, worker isolation, audit trail and human approval for high-impact operations.
