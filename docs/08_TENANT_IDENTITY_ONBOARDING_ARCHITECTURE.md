# CyberOS Tenant Identity & Onboarding Architecture

**Status:** M2 design baseline  
**Branch:** `foundation/m2-tenant-experience`

## Purpose

CyberOS is a multi-tenant security operating platform. A customer executive must not enter the product as a generic demo operator. A CRO/CISO/security administrator signs in, establishes or selects an organization tenant, chooses entitled capabilities, configures the security environment, enrolls connectivity, and only then requests authorized assessments.

## Customer journey

```text
Public Website
  ↓
Sign in / Create organization
  ↓
Identity verification + MFA
  ↓
Tenant provisioning
  ↓
Organization profile
  ↓
Plan / modules / entitlements
  ↓
Users + roles
  ↓
Cloud / on-prem / hybrid connectivity
  ↓
Asset discovery
  ↓
Assessment scope + exclusions
  ↓
Authorized job request
  ↓
Execution policy checks
  ↓
Evidence + findings
  ↓
Risk / remediation / reporting
```

## Tenant boundary

Every authenticated request must resolve an active tenant context on the server. Tenant ID must never be accepted as a trusted client-side authorization value.

Core hierarchy:

```text
Identity
  └── Organization
       └── Tenant
            ├── Subscription
            ├── Entitlements
            ├── Users / Roles
            ├── Assets
            ├── Connectors
            ├── Engagements / Scopes
            ├── Findings
            ├── Evidence
            ├── Jobs
            └── Audit events
```

Backend authorization independently enforces tenant isolation, role permissions, entitlement checks, scope authorization and execution policy. The UI is not a security boundary.

## Executive login

Initial product UX should provide `/login` as the customer entry point. Production identity should support OIDC/SAML SSO, MFA, session management, device/context checks and future FIDO2/WebAuthn. Passwords must not be stored by the portal in plain text.

Suggested roles:

- Organization Owner
- CISO / Security Executive
- Security Administrator
- SOC / Security Analyst
- Vulnerability Manager
- Compliance / GRC Manager
- Security Architect
- Auditor / Read-only
- MSSP / delegated operator

## Organization setup

The first organization administrator completes:

1. Organization name, industry and operating regions.
2. Security objectives and risk profile.
3. Regulatory/compliance obligations.
4. Purchased modules and add-ons.
5. User invitations and roles.
6. Data retention/residency preferences where supported.
7. Notification and alert preferences.

The resulting configuration becomes tenant policy and feeds module availability.

## Module selection

The customer can select capabilities that are included in the subscription. Examples:

- Threat Intelligence
- Attack Surface
- Vulnerability Intelligence
- Security Posture
- Web & API Security
- Network & Hardening
- Compliance / GRC
- Cyber AI
- Reports
- future SIEM/SOAR, CSPM/KSPM, DevSecOps, BAS, IoT/OT, data security and other engines

Module visibility is UX only. The API must enforce entitlements for every protected capability.

## Secure connectivity

For customer networks, the preferred model is an outbound-initiated customer connector:

```text
CyberOS Control Plane
       ⇅ encrypted channel
Customer Connector
       ⇅ least-privilege access
Customer Cloud / DC / Hybrid Network
```

Connector enrollment requires a device identity and approval. Customers should be able to disable a connector immediately. Each assessment request still carries an explicit target scope, exclusions and time window.

Supported onboarding categories should include:

- AWS / Azure / GCP
- on-premise data center
- network devices
- servers/endpoints
- web applications/APIs
- Kubernetes/containers
- SIEM/EDR/security tools

## Assessment lifecycle

No customer asset is scanned merely because it was connected. The safe lifecycle remains:

```text
Discover
  ↓
Inventory
  ↓
Define scope
  ↓
Authorize
  ↓
Policy validation
  ↓
Execute approved engine
  ↓
Collect evidence
  ↓
Normalize findings
  ↓
Correlate threat + exposure + asset criticality
  ↓
Remediate
  ↓
Retest / verify
```

The execution chain remains:

```text
Authentication
→ Tenant authorization
→ Role/capability authorization
→ Engagement authorization
→ Target scope validation
→ Exclusion validation
→ Time-window validation
→ Tool policy validation
→ Resource/rate policy
→ Execution sandbox
```

Any failed check stops execution.

## Tenant-relevant threat intelligence

Global threat intelligence is not automatically treated as a customer incident. CyberOS first maintains global intelligence, then correlates it against the tenant's security graph.

```text
Global intelligence
  ├── actors
  ├── campaigns
  ├── malware
  ├── IOCs
  ├── vulnerabilities / KEV
  └── geopolitical signals
          ↓
Tenant security graph
  ├── assets
  ├── technologies
  ├── locations
  ├── applications/APIs
  ├── vulnerabilities
  └── controls
          ↓
Correlation engine
          ↓
Tenant relevance score
          ↓
Alert / investigation / executive brief
```

Relevance should consider asset exposure, technology fingerprints, vulnerability state, known exploitation, business criticality, geography, sector and observed tenant telemetry. Global intelligence remains globally reusable; customer-specific telemetry and findings remain tenant-isolated.

## M2 implementation boundary

M2 should establish the customer-facing login and onboarding experience without pretending that a production identity provider, payment processor or offensive execution engine already exists. Backend identity, tenant persistence and connector enrollment are subsequent platform-kernel work and must use the same contracts defined here.

The public website is frozen. Future changes must be isolated to the requested module or to explicitly versioned platform primitives.
