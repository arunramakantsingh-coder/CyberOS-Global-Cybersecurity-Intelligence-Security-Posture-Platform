# CyberOS Compliance & Assurance Architecture

## 1. Purpose

CyberOS will provide a common evidence and control-management layer for cybersecurity compliance readiness and assurance programs.

It will not represent itself as a certification body or replace an independent auditor where independent certification/attestation is required.

## 2. Initial Frameworks

### ISO/IEC 27001

Support ISMS-oriented scope, control assessment, evidence, risk treatment, Statement of Applicability-related workflows, remediation and audit preparation.

### PCI DSS

Support requirements, evidence, technical assessment observations, segmentation considerations, remediation tracking and assessment preparation for organizations handling payment-card data.

### DORA

Support digital operational resilience requirements relevant to in-scope financial entities, including ICT risk management, resilience testing, incident-related evidence, third-party risk and related governance workflows.

### SOC 2

Support Trust Services Criteria-oriented evidence and control readiness workflows, with clear distinction between readiness tooling and formal attestation.

### NIST CSF

Support the CSF functions/categories/subcategories through risk and control mapping.

## 3. Framework Registry

Each framework is versioned:

```text
Framework
  id
  name
  jurisdiction
  publisher
  version
  effective_date
  status
```

## 4. Control Registry

```text
Control
  id
  framework_id
  parent_id
  title
  description
  assessment_objectives
  evidence_requirements
  applicable_assets
  applicable_industries
  version
```

## 5. Crosswalk Model

A finding/evidence item can map to multiple controls:

```text
Finding -> Evidence -> Control Mapping
                         |
             +-----------+-----------+
             |           |           |
          ISO27001    PCI DSS     NIST CSF
             |
           DORA
             |
           SOC 2
```

Mappings should be versioned and have provenance. No crosswalk should be treated as an automatic statement of legal equivalence.

## 6. Assessment States

Recommended control states:

- Not assessed
- Planned
- In progress
- Effective
- Partially effective
- Ineffective
- Not applicable
- Exception requested
- Exception approved
- Evidence expired

## 7. Evidence Lifecycle

```text
Requested
 -> Collected
 -> Validated
 -> Reviewed
 -> Mapped
 -> Accepted
 -> Expiring
 -> Expired / Revalidate
```

## 8. Audit Readiness

CyberOS should generate an evidence package containing:

- Control status
- Evidence references
- Assessment history
- Finding references
- Remediation status
- Owner
- Review timestamps
- Exceptions
- Supporting technical observations

## 9. Continuous Compliance

Compliance should not be a yearly spreadsheet exercise.

CyberOS will continuously connect technical posture to control readiness:

```text
Asset change
   -> Security observation
   -> Finding/evidence update
   -> Control impact
   -> Compliance status change
   -> Risk update
```

## 10. Legal/Assurance Language

Product UI and reports must distinguish:

- security observation
- automated assessment
- readiness status
- evidence collected
- management assertion
- independent audit/attestation
- formal certification

The platform must avoid claiming that an automated scan alone certifies compliance.

## 11. Framework Expansion

Future catalog candidates include sector-specific, cloud, privacy, resilience, national and customer-specific control frameworks.

New frameworks should be added as data/catalog packages wherever possible rather than requiring changes to the core compliance engine.
