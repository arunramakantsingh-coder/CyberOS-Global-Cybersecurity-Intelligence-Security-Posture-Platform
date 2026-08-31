# CyberOS M0 — Operating Foundation

Status: FOUNDATION BASELINE
Branch: `foundation/m0-operating-platform`

## Objective

Establish the secure, modular foundation on which CyberOS will run as a web-first security operating platform. Kali Linux and other security tooling are execution environments, not the product identity.

## Core boundaries

1. Web UI never directly executes security commands.
2. Control Plane creates signed, auditable jobs.
3. Policy Engine validates tenant, authorization, scope, target, capability and time window before execution.
4. Tool Gateway permits only registered tool adapters.
5. Execution workers run in isolated, disposable environments with least privilege.
6. Customer LAN connectivity is provided by an outbound-oriented CyberOS Connector using established secure networking primitives.
7. Every security action produces audit metadata and evidence references.
8. AI may recommend, explain, correlate and prepare jobs, but cannot bypass authorization or policy controls.

## Initial modules

- Identity and RBAC
- Tenant management
- Asset inventory
- Findings and evidence
- Job orchestration
- Policy and authorization
- Audit logging
- Tool registry
- Connector registry
- AI gateway contract
- Reporting contract
- Compliance control catalog

## Initial repository layout

```text
apps/
  portal/                 # Web UI
  api/                    # Public/API control plane
services/
  identity/
  assets/
  findings/
  jobs/
  policy/
  audit/
  tools/
  connectors/
  intelligence/
  compliance/
  reporting/
  ai/
workers/
  execution/
  discovery/
  scanning/
connectors/
  cyberos-agent/
engines/
  vulnerability/
  websec/
  networksec/
  hardening/
  compliance/
os/
  base/
  images/
packages/
  contracts/
  security/
  observability/
infra/
  docker/
  terraform/
  kubernetes/
policies/
tests/
docs/
```

## M0 non-goals

M0 does not implement unrestricted penetration testing, autonomous exploitation, destructive testing, credential attacks, persistence, or arbitrary remote shell execution. Those capabilities require later milestones with explicit engagement authorization, technical scope enforcement, sandboxing, rate limits, evidence handling and kill-switch controls.

## Definition of done

- Repository structure established.
- Local development can run portal/API/worker components.
- Database schema supports tenants, identities, assets, jobs, findings, evidence and audit events.
- A job can move through `requested -> policy_checked -> queued -> running -> completed/failed/cancelled`.
- Tool adapters have a typed contract.
- Every execution is linked to tenant, actor, authorization context and scope.
- CI validates code quality, dependency/security checks and policy invariants.
- No secret, customer data or production target is embedded in source control.
