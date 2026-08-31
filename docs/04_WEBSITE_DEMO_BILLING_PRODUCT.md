# CyberOS Website, Demo, Subscription & Billing Product Specification

## 1. Public Website

Primary sections:

- Home
- Platform
- Modules
- Threat Intelligence
- Attack Surface
- Vulnerability Management
- Web/API Security
- Network & Infrastructure Security
- Hardening & Posture
- Authorized Pentesting
- Compliance
- Security Architecture
- AI Security Analyst
- Industries
- Pricing
- Demo
- Resources
- Trust & Security
- Contact Sales
- Sign In
- Get Started

## 2. Industry Solutions

Dedicated solution narratives should support:

- Financial services
- Government
- Manufacturing
- Healthcare
- Retail
- Technology/SaaS
- Telecom
- Critical infrastructure

Each industry page should explain common risks, relevant modules, compliance frameworks, deployment models and outcomes without making unsupported compliance guarantees.

## 3. Product Catalogue

Every module is a first-class product object with:

- Name
- Description
- Category
- Features
- Required capabilities
- Supported deployment models
- Supported industries
- Plan availability
- Usage metrics
- Add-ons
- Documentation

## 4. Pricing Model

The billing architecture should support multiple commercial models:

- Per organization
- Per asset
- Per endpoint
- Per domain/application
- Per connector
- Assessment credits
- AI usage
- Report/export limits
- Compliance framework add-ons
- Enterprise contracts
- Private deployment licensing

Do not hard-code a single pricing formula into the core platform.

## 5. Subscription Lifecycle

```text
Visitor
  -> Sign Up
  -> Organization Created
  -> Trial/Demo or Paid Plan
  -> Payment
  -> Subscription Active
  -> Entitlements Provisioned
  -> Usage Metering
  -> Renewal / Upgrade / Downgrade
  -> Cancellation / Grace Period
  -> Entitlements Updated
```

## 6. Payment Architecture

CyberOS should use a supported payment provider for payment processing and avoid storing raw card data.

The billing service should receive provider events such as:

- checkout completed
- payment succeeded
- payment failed
- subscription created
- subscription updated
- subscription canceled
- invoice created
- invoice paid
- refund issued

Webhook processing must be authenticated, idempotent and auditable.

## 7. Entitlement Service

Application modules query an entitlement service rather than embedding plan names.

Example:

```text
can_use(tenant, "internal_assessment")
can_use(tenant, "web_security")
can_use(tenant, "compliance:iso27001")
can_use(tenant, "ai:advanced")
```

## 8. Demo World

Demo must be intentionally safe and compelling.

Demo tenant contents:

- Synthetic company
- Synthetic users
- Synthetic domains
- Synthetic cloud assets
- Synthetic vulnerabilities
- Synthetic threat events
- Sample compliance gaps
- Sample reports
- AI analysis of synthetic data

Demo restrictions:

- No arbitrary internet targets
- No arbitrary IP input for active testing
- No customer-network connector
- No unrestricted shell
- No unrestricted pentesting
- Rate limits
- Data reset
- Clear demo watermark/label

## 9. Trial Environment

A future paid-trial environment may allow customer-owned assets after explicit onboarding and authorization controls. Trial capability must never be implemented by weakening the demo safety boundary.

## 10. Customer Onboarding

Recommended flow:

```text
Create account
 -> Verify identity/contact
 -> Create organization
 -> Select industry
 -> Select objectives
 -> Select compliance requirements
 -> Select deployment
 -> Configure subscription
 -> Invite team
 -> Connect first asset/connector
 -> Baseline assessment
 -> Security dashboard
```

## 11. Sales-to-Technical Handoff

Enterprise sales should be able to capture:

- Organization
- Industry
- Geography/data residency
- Asset scale
- Compliance requirements
- Deployment preference
- Security modules
- Assessment scope
- Required integrations
- Support tier

The information becomes an implementation/onboarding record rather than remaining trapped in sales notes.

## 12. Billing Security

Billing state must not itself grant security execution permissions. Entitlements and security authorization remain separate control layers.

## 13. Commercial Reporting

Internal commercial analytics should include:

- Active subscriptions
- Trial conversion
- Module adoption
- Usage
- Connector count
- Assessment volume
- AI usage
- Renewal status
- Customer health

Customer-facing billing should only expose that tenant's own billing data.
