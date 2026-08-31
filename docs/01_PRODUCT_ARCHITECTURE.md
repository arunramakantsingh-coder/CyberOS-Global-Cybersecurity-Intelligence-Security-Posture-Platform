# CyberOS Product Architecture

## 1. Experience Architecture

CyberOS consists of four major experience zones.

### Public / Commercial

- Marketing website
- Product/module pages
- Industry pages
- Compliance pages
- Pricing
- Demo
- Documentation
- Contact/sales
- Sign-up/sign-in
- Checkout
- Billing portal

### Customer Security Portal

- Organization overview
- Security score
- Asset inventory
- Threat intelligence
- Vulnerabilities
- Attack surface
- Security assessments
- Pentest engagements
- Compliance
- Remediation
- Reports
- AI assistant
- Administration

### Security Operations

- Jobs
- Scans
- Findings
- Evidence
- Investigations
- Connector status
- Execution logs
- Retesting
- Security posture

### Executive / Governance

- Business risk
- Risk trend
- Control maturity
- Compliance readiness
- Major incidents/exposures
- Remediation progress
- Board reporting

## 2. Logical Architecture

```text
Browser
  |
Web / BFF
  |
API Gateway
  |
+----------------------+-------------------------+
| Identity & Tenant    | Product/Billing         |
| RBAC / SSO / Audit   | Plans/Entitlements      |
+----------------------+-------------------------+
| Core Domain Platform                           |
| Assets | Findings | Risk | Evidence | Reports |
+------------------------------------------------+
| Security Intelligence & Assessment             |
| CTI | ASM | Vuln | Web | Network | Hardening  |
| Cloud | Config | Pentest | Compliance          |
+------------------------------------------------+
| Orchestration / Policy / Tool Gateway          |
+------------------------------------------------+
| Workers / Connectors / Sandboxes / Tool Runtimes|
+------------------------------------------------+
| Data: PostgreSQL | Object Store | Search | Cache|
+------------------------------------------------+
```

## 3. Control Plane vs Data Plane

### Control Plane

Owns:

- Tenants
- Users
- Roles
- Policies
- Scopes
- Jobs
- Tool permissions
- Connector enrollment
- Findings
- Evidence metadata
- Reports
- Billing entitlements
- Audit events

### Data / Execution Plane

Owns:

- Security scans
- Network observations
- Configuration collection
- Tool execution
- Evidence generation
- Connector-local operations

The control plane authorizes the execution plane; execution results return as structured evidence.

## 4. Tool Adapter Architecture

Every security tool is wrapped behind a stable CyberOS engine interface.

```text
CyberOS Job
   |
Policy + Scope Validation
   |
Tool Adapter
   |
Execution Sandbox
   |
Tool
   |
Normalized Result
   |
Evidence / Finding Pipeline
```

A tool adapter must declare:

- Name/version
- Supported job types
- Input schema
- Scope requirements
- Network requirements
- Privileges
- Resource limits
- Output schema
- Evidence mapping
- Failure states

## 5. Security Testing Guardrails

Active testing requires explicit authorization. The platform must enforce:

- Scope allowlist
- Scope exclusions
- Time window
- Job approval state
- Tenant authorization
- Connector authorization
- Tool permission
- Rate/resource limit
- Emergency stop

A UI-only authorization check is insufficient.

## 6. Evidence Architecture

Evidence is a first-class object.

```text
Evidence
├── source
├── collection timestamp
├── tenant
├── asset
├── job
├── tool
├── tool version
├── cryptographic integrity metadata
├── raw/normalized artifact reference
├── parser version
└── retention classification
```

Findings reference evidence rather than storing unverifiable claims.

## 7. Finding Lifecycle

```text
Observed
  -> Normalized
  -> Deduplicated
  -> Correlated
  -> Risk scored
  -> Reviewed
  -> Accepted / Remediating / Resolved
  -> Retested
  -> Closed
```

## 8. Multi-Tenant Architecture

Tenant context must be carried through API, database queries, queues, object storage paths, search indexes, AI context, connector identity and reports.

High-value data access should use defense-in-depth:

- Application authorization
- Database tenant isolation strategy
- Object-store isolation
- Search filtering
- Queue/job ownership checks
- Connector identity checks

## 9. AI Architecture Boundary

AI can:

- summarize
- correlate
- classify
- explain
- prioritize
- recommend
- draft remediation
- create reports
- query approved knowledge
- propose an authorized assessment job

AI cannot independently bypass authorization, expand target scope, retrieve another tenant's data, disable audit logging, or directly execute unrestricted commands.

## 10. Compliance Architecture

The compliance engine consumes the same underlying evidence and findings as security operations.

```text
Technical Observation
        |
     Evidence
        |
 Control Mapping Engine
    /       |       \
 ISO27001  PCI DSS  NIST CSF
    |       DORA      SOC2
        |
 Control Status
        |
 Gap / Remediation
        |
 Evidence Pack / Report
```

## 11. Subscription Architecture

```text
Product Catalogue
      |
Plans + Add-ons
      |
Entitlements
      |
Tenant Subscription
      |
Usage Metering
      |
Billing Provider
      |
Invoice / Payment State
```

Access decisions are made by entitlements, not hard-coded plan checks scattered throughout the application.

## 12. Website and Demo Isolation

The public website and demo world must be logically and operationally separated from production customer security execution.

The demo environment must never provide an arbitrary target-testing capability.

## 13. Reporting Pipeline

```text
Assets + Findings + Evidence + Controls + Risk
                         |
                   Report Model
                         |
          +--------------+--------------+
          |              |              |
      Executive       Technical      Compliance
          |              |              |
       PDF/Web        PDF/Web        PDF/Web
```

Reports should be reproducible from versioned data and report templates.
