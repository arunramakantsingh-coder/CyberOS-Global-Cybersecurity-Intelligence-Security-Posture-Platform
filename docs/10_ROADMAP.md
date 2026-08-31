# CyberOS Master Roadmap

**Roadmap principle:** architecture and security boundaries first; production active security execution later.

## Current Position

M0 foundation and M1.1 platform-kernel work are established. M2 public product experience is implemented and the approved public website is now frozen.

The next implementation focus is **M3 — Asset Intelligence + CyberOS Security Overview**, using isolated module development boundaries.

The complete capability expansion is defined in [`13_CYBEROS_COMPLETE_CAPABILITY_EXPANSION.md`](13_CYBEROS_COMPLETE_CAPABILITY_EXPANSION.md).

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

### M1.1 — Platform Context and Audit Kernel

Established foundation includes:

- organization/tenant context;
- operator context;
- authorization model foundation;
- audit/event model foundation;
- controlled operations lifecycle;
- policy-gated execution model; and
- command-center exposure of platform-kernel state.

**M1 full exit gate:** authenticated multi-tenant application with no cross-tenant data access in automated tests. Remaining identity/authentication depth is retained as a platform workstream and must not be bypassed by the public/demo experience.

## M2 — Public Website + Demo

### M2.1 — Public Product Experience — FROZEN

- Marketing website shell
- Product positioning
- Platform overview
- Module catalogue
- Industry solutions
- Compliance overview
- Assessment overview
- Trust/security information
- Pricing and packaging
- Contact/sales entry points
- Sign-in/sign-up entry points
- Fixed top navigation
- Responsive layout
- Vertical section flow
- Horizontal overflow protection

**Freeze baseline:** `81da2a1cface98479f6e92c8afea8830619ca618`

**Recovery snapshot:** `release/m2-public-website-frozen`

### M2.2 — Demo World

- Synthetic organization
- Synthetic assets/findings/evidence
- Demo dashboard
- Exposure and vulnerability views
- Threat intelligence views
- Security posture views
- Compliance views
- Remediation views
- Reports
- Safe demo boundaries
- No arbitrary target entry
- No outbound offensive execution
- Rate limiting/abuse controls

### M2.3 — Commercial Foundation

- Product catalogue model
- Plan model
- Add-on model
- Entitlement model
- Usage/limits model
- Subscription lifecycle model
- Payment-provider abstraction
- Safe test-mode checkout foundation
- Tenant provisioning contract

### M2.4 — Customer Entry Boundary

- Clear public/demo/customer routing
- Existing control-plane pages preserved
- Tenant context reused rather than duplicated
- Backend authorization remains authoritative

**M2 exit gate:** public experience and safe demo operate separately from production security execution, while consuming the same platform primitives for tenant, entitlement and product context.

## M3 — Asset Intelligence + Security Overview

### M3.1 — Organization / Asset Graph

- Organizations and business units
- Domains and subdomains
- IPs and networks
- Applications
- APIs
- Hosts/servers/endpoints
- Databases
- Cloud accounts/resources
- Containers/Kubernetes
- Network devices
- IoT/OT asset model
- Asset ownership and criticality
- Asset provenance
- Asset relationships

### M3.2 — External Exposure Intelligence

- Authorized domain discovery
- DNS intelligence
- Subdomain inventory
- IP/service inventory
- Technology fingerprinting
- TLS/security configuration observations
- Application/API exposure
- Internet exposure score

### M3.3 — Command Center Intelligence

- Organization security overview
- Asset distribution statistics
- Application/API coverage
- Exposure summary
- Security posture summary
- Finding summary
- Risk trend foundations
- Time-series analytics foundations
- Geographic/global security map foundations
- Cross-module drill-down contracts

**M3 exit gate:** normalized, provenance-aware asset graph and a real command-center overview driven by backend data rather than one generic placeholder page.

## M4 — Threat & Vulnerability Intelligence

- CVE/CWE/CVSS ingestion
- Known exploited vulnerability intelligence
- Vendor advisories
- Exploitability/activity signals
- Threat intelligence ingestion
- IOC normalization
- Threat actor/campaign model
- Malware/ransomware intelligence
- Geopolitical cyber intelligence
- Asset-to-vulnerability correlation
- Threat-to-exposure correlation
- Risk scoring v1
- Vulnerability trends
- Remediation prioritization

**Exit gate:** reproducible vulnerability and threat prioritization backed by evidence.

## M5 — Security Assessment Engines

### Web / Application / API

- Web assessment adapters
- API assessment
- OWASP-aligned testing
- Authentication/session assessment
- Injection detection, including authorized SQL injection testing
- TLS/security headers
- Dependency intelligence
- Authenticated scanning

### Network / Infrastructure

- Network assessment adapters
- Internal infrastructure assessment
- Network architecture assessment
- Segmentation assessment
- Server posture
- Endpoint posture
- Firewall/router/switch assessment

### Cloud / Container

- CSPM
- Cloud identity posture
- Cloud configuration assessment
- Container assessment
- Kubernetes/KSPM assessment
- IaC security

### Finding / Evidence

- Finding normalization
- Evidence collection
- Evidence provenance
- Assessment history

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
- Customer LAN/DC connectivity
- Hybrid connectivity

**Exit gate:** authorized internal assessment works without requiring public inbound management exposure.

## M7 — Hardening & Security Architecture

- Linux hardening
- Windows hardening
- Firewall posture
- Router/switch posture
- Database posture
- Kubernetes posture
- Cloud baseline posture
- Identity baseline posture
- Baseline policies
- Configuration drift
- Security architecture assessments
- Secure network architecture recommendations
- Custom policies
- Remediation recommendations

**Exit gate:** assessment-to-remediation workflow is complete and retestable.

## M8 — Compliance / GRC / Regulatory Intelligence

- Framework registry
- Control registry
- Versioned requirements
- Evidence mapping
- Gap analysis
- Control self-assessment
- Policy management
- Risk treatment
- Issue lifecycle
- Assessment workflow
- Evidence packages
- Compliance reporting
- Regulatory change tracking
- Privacy/security regulation mapping

Initial frameworks:

- ISO/IEC 27001
- PCI DSS
- DORA
- SOC 2
- NIST CSF

**Exit gate:** technical findings and evidence can be mapped to versioned controls without claiming formal certification.

## M9 — Authorized Security Testing / BAS

- Engagement management
- Rules of engagement
- Scope authorization
- Testing windows
- Tool permissions
- Execution controls
- Controlled penetration testing
- Benign breach-and-attack simulation
- MITRE ATT&CK-aligned validation
- Detection/response validation
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
- Application-security analyst
- Cloud-security analyst
- Compliance analyst
- Security architect
- Incident investigator
- Remediation advisor
- Report generator
- AI audit trail
- Human review

**Exit gate:** AI outputs are evidence-linked and AI cannot bypass security controls.

## M11 — Security Operations: SIEM / SOAR / Incident Response

- Real-time log/event ingestion
- Event normalization
- Correlation
- Detection/alert model
- Incident lifecycle
- Investigation workspace
- Timeline and evidence
- Forensic evidence integration
- SOAR playbooks
- Approval-gated response
- Endpoint/network containment integrations
- SOC dashboards

## M12 — Identity, PAM & Zero Trust

- SSO/OIDC/SAML
- Adaptive authentication
- MFA
- FIDO2/WebAuthn
- PAM integrations
- Privileged account monitoring
- Device/user trust context
- Continuous authorization
- Least-privilege analysis
- Zero-trust posture

## M13 — DevSecOps, Supply Chain & Data Security

### DevSecOps

- SAST/SCA integrations
- Dependency intelligence
- Secret detection integrations
- CI/CD security gates
- IaC security
- SBOM generation/ingestion
- Artifact provenance/signing

### Third-Party Risk

- Vendor inventory
- Vendor security questionnaires
- External security signals
- Vendor risk scoring
- Cyber-insurance evidence support

### Data Security

- Sensitive-data discovery
- PII/PHI classification
- Data-flow visibility
- DLP integrations
- Encryption posture
- Key-management posture
- Data access governance

## M14 — IoT / OT / ICS + Specialized Security

- IoT asset discovery
- ICS/SCADA/PLC inventory
- OT segmentation assessment
- Protocol-aware monitoring integrations
- Industrial asset criticality
- Safe non-disruptive assessment modes
- OT evidence and reporting

## M15 — Threat Sharing / VDP / Ecosystem

- STIX/TAXII ingestion/export
- ISAC integration where authorized
- Anonymous/aggregated intelligence exchange where lawful
- Vulnerability disclosure portal
- Researcher workflow
- Bug-bounty integrations
- Marketplace of vetted security integrations
- Partner/MSSP delegated administration
- Public APIs
- Webhooks
- Event-driven integrations

## M16 — Advanced Analytics / Digital Twin

- Security digital twin
- Attack-path modeling
- Blast-radius analysis
- Predictive risk
- What-if remediation simulation
- Peer benchmarking using privacy-preserving aggregation
- Control effectiveness analytics
- Global cyber trend analytics
- Geopolitical risk correlation

## M17 — Enterprise Resilience & Deployment

- Multi-region architecture
- Active/active or equivalent HA strategy
- Backup/restore
- RTO/RPO controls
- Data residency
- Customer-managed keys where supported
- Private cloud
- On-premises deployment
- Government edition
- Restricted deployment
- Offline/air-gapped operating model

## M18 — Personalization & Sustainability

- Role-based dashboards
- Custom widgets
- Saved views
- Personalized alert thresholds
- Guided onboarding
- Industry-specific experiences
- Carbon-footprint reporting
- Infrastructure/cloud efficiency recommendations

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
10. Regression verification of frozen surfaces

## Module Isolation Rule

The public M2 website is frozen. Internal work must be module-scoped.

A module change may modify its own page/components, data contracts and directly required backend services. It must not redesign unrelated modules or the global public website.

Before acceptance, verify:

- Command Center
- Organization
- Operations
- affected module
- public website
- responsive layout
- Git diff scope
- tenant/authorization boundaries
