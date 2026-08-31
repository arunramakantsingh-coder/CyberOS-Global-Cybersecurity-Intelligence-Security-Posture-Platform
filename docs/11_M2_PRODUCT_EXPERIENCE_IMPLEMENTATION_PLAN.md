# M2 Product Experience Implementation Plan

**Milestone:** M2 — Public Website + Demo  
**Branch:** `foundation/m2-product-platform`  
**Starting baseline:** M1.1 Platform Kernel (`f212233`)  
**Status:** Authorized to proceed; implementation in progress

## Objective

Turn the existing CyberOS control-plane foundation into the first coherent product experience while preserving tenant isolation, authorization, auditability and execution safety.

## Workstreams

### M2.1 Public Website Shell

Build a production-oriented public product surface covering:

- Home
- Platform
- Modules
- Industries
- Compliance
- Assessments
- Demo World
- Pricing
- Resources
- Trust/Security
- Contact/Sales
- Sign in / Sign up entry points

The public experience must clearly distinguish itself from the authenticated security operations workspace.

### M2.2 Product Catalogue

Create a normalized catalogue of CyberOS capabilities, including:

- module name;
- purpose;
- capabilities;
- target users;
- industry relevance;
- compliance relevance;
- plan/entitlement metadata; and
- demo availability.

### M2.3 Demo World

Provide a safe synthetic tenant with realistic but non-production data:

- assets;
- exposure;
- vulnerabilities;
- threat intelligence;
- posture;
- findings;
- compliance;
- evidence;
- remediation; and
- reports.

No arbitrary target entry or outbound offensive execution is permitted.

### M2.4 Commercial Funnel Foundation

Introduce the application model required for:

```text
Visitor
  ↓
Demo / Product discovery
  ↓
Plan selection
  ↓
Sign-up / Sales
  ↓
Subscription
  ↓
Entitlement
  ↓
Tenant provisioning
```

Payment gateway integration may initially be represented by a provider abstraction and safe test mode; production payment credentials must never be embedded in source code.

### M2.5 Customer Entry Boundary

Establish clear routing and UI boundaries between:

- public website;
- demo environment;
- authenticated customer portal; and
- security operations/control plane.

### M2.6 Platform Integration

The product shell must consume the existing M1.1 platform context instead of creating a second organization/tenant model.

## Acceptance Criteria

1. Public product experience is reachable without entering the security operations workspace.
2. Demo World uses synthetic data only.
3. Demo cannot initiate arbitrary external security testing.
4. Existing `/organization` and `/operations` control-plane pages remain functional.
5. Existing API health endpoint remains healthy.
6. Docker Compose remains operational.
7. Public product navigation is coherent and responsive.
8. Product catalogue reflects the complete CyberOS module vision.
9. Pricing/plan concepts are represented without hard-coded payment secrets.
10. Tenant and entitlement concepts are documented before production billing is enabled.
11. No UI-only security boundary is treated as authorization.
12. Documentation and verification evidence are updated before the M2 exit gate.

## Deferred from M2

The following remain later milestones unless required as platform primitives:

- real external vulnerability scanning;
- active penetration testing;
- internal network connector execution;
- production payment processing;
- full enterprise SSO;
- full compliance evidence automation;
- production Cyber AI;
- customer-side remediation automation.

## Verification Gate

M2 is complete only after implementation, tests, security checks, documentation and operational verification are recorded. The final gate must explicitly confirm that the public/demo experience cannot weaken the M1.1 authorization and tenant-isolation model.
