# CyberOS Module Development Boundaries

**Status:** Active engineering rule
**Baseline:** M2 public website freeze

## Rule 1 — Frozen Surface

The approved public website is treated as immutable during internal module development.

## Rule 2 — One Module at a Time

Every implementation task must declare its target module before code changes begin.

Allowed examples:

- Command Center only
- Threat Intelligence only
- Vulnerabilities only
- Security Posture only
- Web/Application/API Security only
- Network & Hardening only
- Compliance/GRC only
- Cyber AI only
- Reports only
- Organization/Operations platform work only

## Rule 3 — Shared Contracts Are Controlled

A module may consume shared services, but may not silently redesign the global shell, routing, tenant model, authorization model or data contracts.

If a shared contract genuinely must change, the change must be documented and regression-tested separately.

## Rule 4 — Purpose-Built Workspaces

Specialist modules must not all render the same generic page. Each module gets domain-specific information architecture and visualizations.

Examples:

- Threat Intelligence: global threat map, campaigns, actors, IOCs, trends and customer relevance.
- Vulnerabilities: severity/exploitability analytics, asset correlation, KEV exposure, remediation queues and trend charts.
- Security Posture: infrastructure/cloud/network posture, control coverage, drift and trend analytics.
- Web/Application/API Security: application inventory, API inventory, OWASP findings, authentication/session/API risks and authorized test results.
- Network & Hardening: topology, segmentation, firewall/device posture, baselines and remediation.
- Compliance: framework posture, control coverage, evidence, gaps, risk treatment and audit packages.
- Cyber AI: evidence-grounded analysis, investigation and recommendations.
- Reports: report catalogue, generation, evidence lineage and executive/technical views.

## Rule 5 — Global Context, Local Depth

The command center owns cross-domain visibility. Specialist modules own deep domain workflows. Organization and Operations remain platform-kernel surfaces.

## Rule 6 — Security Boundaries

All active security capabilities must preserve:

- tenant isolation;
- authorization;
- scope enforcement;
- policy enforcement;
- evidence provenance;
- auditability;
- safe execution;
- rate/resource controls;
- kill/disable controls where execution exists.

## Rule 7 — Regression Gate

Before accepting a module change:

1. run the module-specific tests;
2. run affected shared-contract tests;
3. verify the command center;
4. verify Organization and Operations;
5. verify public website navigation and layout;
6. verify no unexpected route or CSS regression;
7. verify Git diff contains only intended files.

## Rule 8 — No Generic Placeholder Expansion

Do not add fake charts or arbitrary statistics merely to make a page look complete. Synthetic/demo analytics must have clearly defined semantics and be replaceable by real backend data.

## Rule 9 — Architecture Before Tooling

Security engines are replaceable implementations behind CyberOS contracts. CyberOS remains the product and control plane; third-party tools are execution/intelligence providers rather than the product itself.
