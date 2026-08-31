# CyberOS Master Roadmap

**Roadmap principle:** architecture and security boundaries first; production active security execution later.

## M0 — Repository & Governance Foundation

- Master specification
- Product architecture
- OS foundation decision record
- Compliance architecture
- Website/demo/billing specification
- Security boundaries
- Repository structure
- ADR process
- CI baseline
- Dependency/security scanning
- Documentation index

**Exit gate:** architecture reviewed and implementation boundaries frozen.

## M1 — CyberOS Platform Kernel

- Backend foundation
- Web application shell
- PostgreSQL schema foundation
- Identity
- Tenant model
- RBAC
- Audit event model
- API conventions
- Job model
- Evidence model
- Finding model
- Report model
- Basic observability

**Exit gate:** authenticated multi-tenant application with no cross-tenant data access in automated tests.

## M2 — Public Website + Demo

- Marketing website
- Product/module catalogue
- Industry pages
- Pricing pages
- Demo tenant
- Demo dashboard
- Sign-up/sign-in
- Commercial funnel
- Demo isolation controls

**Exit gate:** public experience and safe demo operate separately from production security execution.

## M3 — Asset Intelligence

- Organizations
- Domains
- IPs
- Applications
- APIs
- Hosts
- Cloud resources
- Network devices
- Asset relationships
- External attack-surface inventory

**Exit gate:** normalized asset inventory with provenance.

## M4 — Threat & Vulnerability Intelligence

- CVE ingestion
- Vulnerability metadata
- Exploitability/activity signals
- Threat intelligence ingestion
- IOC normalization
- Threat actor/campaign model
- Asset-to-vulnerability correlation
- Risk scoring v1

**Exit gate:** reproducible vulnerability prioritization backed by evidence.

## M5 — Security Assessment Engines

- Network assessment adapters
- Web assessment adapters
- API assessment
- TLS assessment
- Configuration assessment
- Server posture
- Cloud posture
- Container posture
- Finding normalization
- Evidence collection

**Exit gate:** controlled jobs produce normalized, auditable findings.

## M6 — CyberOS Connector

- Connector identity
- Secure enrollment
- Outbound secure transport
- Route policy
- Internal asset discovery
- Internal assessment jobs
- Health telemetry
- Local kill switch
- Connector audit

**Exit gate:** authorized internal assessment works without requiring public inbound management exposure.

## M7 — Hardening & Security Architecture

- Linux hardening
- Windows hardening
- Firewall posture
- Router/switch posture
- Database posture
- Kubernetes posture
- Baseline policies
- Security architecture questionnaires
- Custom policies
- Remediation recommendations

**Exit gate:** assessment-to-remediation workflow is complete and retestable.

## M8 — Compliance Readiness

- Framework registry
- Control registry
- Evidence mapping
- Gap analysis
- Risk treatment
- Assessment workflow
- Evidence packages
- Reporting

Initial frameworks:

- ISO/IEC 27001
- PCI DSS
- DORA
- SOC 2
- NIST CSF

**Exit gate:** technical findings and evidence can be mapped to versioned controls without claiming formal certification.

## M9 — Authorized Penetration Testing

- Engagement management
- Rules of engagement
- Scope authorization
- Testing windows
- Tool permissions
- Execution controls
- Evidence chain
- Finding validation
- Retest
- Final reporting

**Exit gate:** no active execution can bypass authorization/scope controls.

## M10 — Cyber AI

- AI gateway
- Model abstraction
- RAG
- Cyber knowledge base
- Threat analyst
- Vulnerability analyst
- Compliance analyst
- Security architect
- Report generator
- AI audit trail
- Human review

**Exit gate:** AI outputs are evidence-linked and AI cannot bypass security controls.

## M11 — Enterprise Platform

- SSO/OIDC/SAML
- Advanced RBAC/ABAC
- Enterprise audit
- SIEM integration
- SOAR integration
- Ticketing integrations
- Data residency
- High availability
- Private deployment
- Customer-managed keys where supported

## M12 — CyberOS Security Operating Platform

- Minimal hardened base image
- Secure build pipeline
- Signed releases
- SBOM
- Tool runtime manager
- Sandboxed execution
- CyberOS appliance
- Cloud worker image
- Private node

## M13 — Advanced Intelligence

- Security digital twin
- Attack-path risk modeling
- Threat-to-exposure correlation
- Continuous control monitoring
- Predictive risk indicators
- Industry intelligence
- Global security trends

## M14 — Restricted / Government / Offline

- Private deployment
- Restricted networks
- Offline intelligence import
- Air-gapped operating model
- Dedicated key management
- Enhanced audit
- Controlled update packages

## Release Discipline

No milestone is considered complete because code exists. Each milestone requires:

1. Implementation
2. Unit tests
3. Integration tests
4. Security tests
5. Documentation
6. Operational verification
7. Auditability
8. Rollback/recovery consideration
9. Explicit exit-gate approval

## Initial Recommendation

Begin with **M0** and establish the architecture and repository skeleton before implementing active scanners or penetration-testing capabilities.
