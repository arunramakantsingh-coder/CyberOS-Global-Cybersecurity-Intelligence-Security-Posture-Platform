# CyberOS M2.2 — Customer Assessment Agent Contract

## Purpose

CyberOS uses a customer-controlled assessment agent for authorized network, web/API and vulnerability assessment. The cloud/control plane never receives an unrestricted route into a customer's private network.

## Deployment model

```text
CRO / CISO login
      |
      v
CyberOS Tenant Control Plane
      |
      | tenant_id + authorization_id + policy
      v
Assessment Job Queue
      |
      v
Customer Assessment Agent
(Kali-based runtime / hardened Linux agent)
      |
      +--> approved network scope
      +--> approved web/API scope
      +--> approved vulnerability scope
      |
      v
Evidence + normalized findings
      |
      v
Tenant-scoped Command Center / Threat Correlation / Posture / Reports
```

## Agent responsibilities

- Maintain an outbound authenticated connection to CyberOS.
- Poll only for jobs assigned to its tenant and authorized connector.
- Verify job authorization, target scope and exclusions before execution.
- Execute only the capability explicitly granted to the job.
- Never accept arbitrary shell commands from the control plane.
- Return structured evidence, tool versions, timestamps, target identifiers and hashes.
- Keep customer secrets and raw credentials local to the customer environment.
- Support a disconnected/offline evidence export mode for restricted data centers.

## Initial capability contract

| Capability | Purpose | Execution state |
|---|---|---|
| `authorized.network.discovery` | Asset/service discovery inside approved CIDR/ranges | Gateway registered; worker execution pending |
| `authorized.web.assessment` | Authorized web/API assessment | Gateway registered; worker execution pending |
| `authorized.vulnerability.assessment` | Vulnerability discovery/prioritization | Gateway registered; worker execution pending |
| `evidence.collection` | Package normalized evidence and provenance | Gateway registered; worker execution pending |

## Kali integration

Kali Linux is the reference assessment runtime, not the control plane. CyberOS should invoke a small allowlisted tool adapter on the customer agent rather than transmitting arbitrary commands. The adapter maps a CyberOS capability to a versioned assessment profile and produces normalized JSON evidence.

Examples of future adapters include approved network discovery, HTTP/TLS inspection, authenticated application testing and vulnerability assessment. Each adapter must declare its safety profile, required privileges, supported target types and evidence schema.

## Authorization requirements

Before active execution, all of the following must be true:

1. Tenant identity is authenticated.
2. An active authorization context exists.
3. The target is inside the approved scope.
4. The target is not in exclusions.
5. The requested capability is allowed by the engagement.
6. The customer connector is online and bound to the same tenant/authorization context.
7. The job is recorded in the audit ledger.

A failed check results in `blocked` or `review_required`; it must never silently execute.

## Evidence model

Every assessment result should preserve:

- tenant ID
- authorization ID
- connector ID
- job ID
- target
- capability
- tool and version
- start/end timestamps
- result status
- evidence hash
- provenance
- finding IDs created or updated

This evidence becomes the common input to vulnerabilities, security posture, web/API security, network hardening, compliance, threat correlation, AI and reporting.

## Implementation boundary

M2.2 establishes the tenant connector registry, authorization-aware assessment gateway, module entitlements and UI. Actual customer-side network execution is intentionally a subsequent implementation step so that the agent protocol, allowlists, audit trail and evidence format are established before any active scanning capability is enabled.
