# CyberOS Security Execution & AI Guardrails

## Purpose

CyberOS combines security intelligence with authorized security testing. The platform therefore needs explicit controls that prevent accidental, unauthorized or over-broad execution.

## Execution Authorization Chain

```text
User / Service
   |
Authentication
   |
Tenant authorization
   |
Role/capability authorization
   |
Engagement authorization
   |
Target scope validation
   |
Exclusion validation
   |
Time-window validation
   |
Tool policy validation
   |
Resource/rate policy
   |
Execution sandbox
```

Any failed check stops the job.

## Scope Model

A scope must support:

- domains
- IP addresses/ranges
- applications
- APIs
- cloud accounts/resources
- internal networks
- individual assets
- explicit exclusions

Scope should be immutable after approval for an active engagement unless a new approval workflow is completed.

## AI Capability Model

AI receives typed capabilities rather than unrestricted operating-system access.

Examples:

- `get_asset_inventory`
- `get_finding_evidence`
- `query_threat_intel`
- `analyze_configuration`
- `map_control`
- `draft_remediation`
- `create_assessment_plan`
- `request_authorized_job`
- `generate_report`

Privileged capabilities require additional policy checks.

## Human Review

Human approval should be required for high-impact actions, including active testing categories defined by policy, scope changes, destructive-risk actions, and production-impacting remediation where the platform eventually supports automated remediation.

## Kill Switch

Every connector and execution worker should support immediate cancellation. The control plane should expose job cancellation and connector disablement to authorized operators.

## Evidence and Audit

Every execution records:

- tenant
- actor
- authorization source
- job ID
- engagement ID
- target scope
- tool
- version
- timestamps
- execution status
- output/evidence references
- policy decisions

## AI Auditability

For material AI decisions, retain:

- model identifier/version
- relevant retrieval references
- tool/capability calls
- policy decisions
- generated recommendation
- human approval where applicable

Do not retain sensitive prompts or customer data beyond the configured retention policy.

## Safety Boundary

CyberOS is designed for authorized defensive security operations. Product features, documentation, test fixtures and demos must reinforce customer-owned or explicitly authorized targets and must not encourage arbitrary unauthorized testing.
