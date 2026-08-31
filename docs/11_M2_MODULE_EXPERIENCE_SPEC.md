# CyberOS M2 — Module Experience Specification

## Purpose

M2 must not present every security capability as the same generic page. The public website shell is treated as a frozen visual foundation; internal product modules are developed independently on top of the shared CyberOS control plane.

## Frozen boundary

The following foundation is not to be casually changed while module work is underway:

- public website orientation, fixed top navigation and responsive behavior;
- public website visual language and core layout;
- tenant/control-plane boundaries;
- Organization and Operations routes;
- authorization/policy-controlled execution model;
- evidence and audit concepts.

A module change must remain localized to the module route/components and its explicitly required data contract. Do not refactor unrelated pages as part of a module implementation.

## Global internal navigation invariant

Every internal security module must keep these destinations visible:

1. Command Center
2. Organization
3. Operations
4. Threat Intelligence
5. Attack Surface
6. Vulnerabilities
7. Security Posture
8. Web Security
9. Network & Hardening
10. Compliance
11. AI Security
12. Reports

Organization and Operations are platform-kernel destinations, not children that disappear when another module is selected.

## Module experience model

Every module should contain, where applicable:

- module-specific executive KPIs;
- module-specific operational statistics;
- trend or time-series visualization;
- global/regional analytics where geography is meaningful;
- prioritized observations/findings;
- asset/application/network context;
- controlled workflow or assessment lifecycle;
- evidence/audit relationship;
- recent execution/activity ledger;
- cloud, on-premise and hybrid context where relevant;
- a clear path back to Command Center.

### Threat Intelligence

- actors, campaigns, malware and IOCs;
- STIX/TAXII-ready intelligence ingestion model;
- geopolitical and regional threat context;
- threat-to-asset correlation;
- campaign and indicator prioritization;
- global threat map and trend analytics.

### Attack Surface

- domains, IPs, applications, APIs, certificates and services;
- external exposure discovery and change tracking;
- internet-facing asset risk;
- cloud/on-premise/hybrid exposure;
- business context and ownership;
- exposure trend and remediation prioritization.

### Vulnerabilities

- CVE/CWE/CVSS/KEV intelligence;
- vendor advisories;
- asset and business-context correlation;
- exploitability and exposure prioritization;
- remediation aging and verification;
- risk trend analytics.

### Security Posture

- cloud security posture (CSPM direction);
- on-premise data-center posture;
- hybrid connectivity and identity posture;
- server, endpoint and infrastructure posture;
- configuration baselines and control coverage;
- posture score and trend analytics.

### Web Security / Application Security

This is an application-security workspace, not a generic vulnerability table. It must grow toward:

- web applications and API inventory;
- authorized DAST/SAST/IAST integration points;
- API security;
- authentication and authorization testing;
- injection testing including SQL injection;
- XSS, SSRF and security-header/configuration coverage;
- secrets and dependency/supply-chain signals;
- SBOM/SCA/CI-CD integration direction;
- evidence, retest and remediation lifecycle.

All active testing remains subject to the CyberOS authorization and controlled-execution model. The UI must never imply arbitrary-target or unrestricted offensive execution.

### Network & Hardening

- network topology and trust zones;
- firewalls, routers, switches and security appliances;
- segmentation and east/west traffic context;
- remote access / VPN / ZTNA direction;
- secure network architecture assessment;
- CIS-style configuration baselines;
- hardening recommendations and verification;
- cloud, data-center and hybrid network coverage.

### Compliance

Compliance is evidence-driven rather than a static checklist:

`Framework → Control → Asset → Evidence → Finding → Risk → Remediation → Verification → Report`

Initial framework families include ISO/IEC 27001, PCI DSS, DORA, SOC 2 and NIST CSF, with an extensible framework catalog.

### AI Security

- evidence-grounded AI analyst workflows;
- threat, vulnerability and architecture analysis;
- cross-module correlation;
- predictive/what-if analysis direction;
- report generation;
- human approval for consequential actions;
- AI guardrails and auditability.

### Reports

- executive risk briefs;
- technical security reports;
- vulnerability/remediation reports;
- compliance evidence packs;
- assessment/pentest reports;
- scheduled reporting;
- evidence provenance and source traceability.

## Future capability coverage

The product vision also reserves architecture space for advanced identity governance/PAM/MFA, SIEM/SOAR and incident management, CSPM/KSPM, DevSecOps/SCA/SBOM, third-party risk, breach-and-attack simulation, IoT/OT, threat-intelligence sharing, data security/DLP, vulnerability disclosure, benchmarking/predictive analytics, endpoint/MDM/EDR integrations, geopolitical/regulatory intelligence, automated remediation, GRC workflows, API-first integrations, resilience/multi-region, personalization, marketplace/MSSP workflows and sustainability reporting.

These capabilities should be introduced through explicit milestones rather than by overloading M2 with production execution.

## Development safety rules

1. Work on one module at a time.
2. Prefer module-local configuration/components over global refactors.
3. Preserve Organization and Operations navigation on every internal module.
4. Do not modify the public website shell during module implementation unless a separately approved foundation defect is found.
5. Use synthetic/demo data for M2 visual experiences; do not introduce arbitrary outbound scanning or offensive execution.
6. Real security execution must continue to flow through authorization, scope, policy, worker/connector, evidence and audit controls.
7. Before closing a module task, verify the target route plus Command Center, Organization and Operations routes.
8. Keep each commit narrowly scoped and reversible.
9. Do not claim a capability is production-active when the UI is only a demo/contract representation.

## M2 completion definition

M2 module experience is complete when each module has a distinct information architecture, meaningful analytics, module-specific workflows, preserved platform navigation, demo-safe execution boundaries and no regression to the frozen public experience.
