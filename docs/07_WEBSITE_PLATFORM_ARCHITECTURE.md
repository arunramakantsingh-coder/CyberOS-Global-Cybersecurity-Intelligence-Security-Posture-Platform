# CyberOS Website and Commercial Platform Architecture

CyberOS has two connected but separately secured surfaces.

## Public website

Purpose:

- product positioning
- module catalogue
- industry solutions
- compliance capabilities
- pricing
- documentation
- security/trust center
- demo environment
- contact/sales
- customer onboarding

Suggested routes:

```text
/
/product
/modules
/solutions
/compliance
/pricing
/demo
/security
/resources
/docs
/contact
/login
/signup
```

## Customer control plane

Authenticated routes include:

```text
/dashboard
/assets
/exposure
/vulnerabilities
/threat-intelligence
/security-posture
/web-security
/network-security
/hardening
/compliance
/engagements
/connectors
/reports
/ai
/settings
/billing
/audit
```

## Demo world

A separate synthetic tenant containing intentionally safe, non-production sample assets and findings. It must not provide a bridge to real Internet targets or arbitrary customer networks.

Demo restrictions include:

- synthetic data
- read-only or simulated actions where possible
- fixed tool capabilities
- strict rate/compute limits
- no arbitrary target input
- no customer data
- automatic reset

## Subscription platform

Commercial services should support:

- plans
- monthly/annual billing
- entitlements
- usage meters
- seats
- assets/scanning limits
- connectors
- compliance modules
- invoices
- payment provider integration
- tax handling
- trials
- upgrades/downgrades
- cancellation
- enterprise contracts

Payment processing must use a reputable payment provider and avoid storing raw card data in CyberOS.

## Commercial isolation

Billing data and security-tenant data have separate authorization boundaries. A payment event may change entitlements but cannot directly grant security execution capability without policy evaluation.
