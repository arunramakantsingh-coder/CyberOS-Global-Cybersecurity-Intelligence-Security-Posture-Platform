# CyberOS Repository Architecture

```text
CyberOS-Global-Cybersecurity-Intelligence-Security-Posture-Platform/
│
├── apps/
│   ├── web/                    # Main customer web portal
│   ├── marketing/              # Public product website
│   ├── demo/                   # Safe demo experience
│   └── admin/                  # Platform administration
│
├── services/
│   ├── api/                    # API/BFF
│   ├── identity/               # Identity and access domain
│   ├── tenancy/                # Tenant lifecycle and isolation
│   ├── assets/                 # Asset intelligence
│   ├── findings/               # Findings/evidence
│   ├── risk/                   # Risk engine
│   ├── intelligence/           # CTI/vulnerability intelligence
│   ├── compliance/             # Control and framework engine
│   ├── billing/                # Subscription/entitlement domain
│   ├── reporting/              # Reports
│   ├── ai/                     # AI gateway/orchestration
│   └── connectors/             # Connector control plane
│
├── workers/
│   ├── ingestion/
│   ├── assessment/
│   ├── normalization/
│   ├── reporting/
│   └── ai/
│
├── connectors/
│   └── cyberos-connector/      # Customer environment agent/appliance
│
├── engines/
│   ├── common/                 # Engine contracts
│   ├── network/
│   ├── web/
│   ├── vulnerability/
│   ├── configuration/
│   ├── hardening/
│   ├── cloud/
│   └── compliance/
│
├── os/
│   ├── base/                   # CyberOS base image
│   ├── build/                  # OS image build pipeline
│   ├── runtime/                # Runtime policies
│   └── tool-images/            # Isolated tool environments
│
├── packages/
│   ├── schemas/
│   ├── sdk/
│   ├── auth/
│   └── observability/
│
├── compliance/
│   ├── frameworks/
│   ├── controls/
│   └── mappings/
│
├── infra/
│   ├── docker/
│   ├── kubernetes/
│   ├── terraform/
│   └── environments/
│
├── policies/
│   ├── security/
│   ├── assessment/
│   ├── ai/
│   └── data-retention/
│
├── scripts/
├── tests/
│   ├── unit/
│   ├── integration/
│   ├── security/
│   ├── e2e/
│   └── tenancy/
│
├── docs/
└── .github/
    └── workflows/
```

## Design Rule

Domain ownership should remain explicit. A future microservice split should follow domain boundaries rather than creating services merely because a component sounds independent.

## Initial Implementation Recommendation

Use a modular backend with background workers first. Introduce independent deployment units when one of the following requires it:

- security isolation
- independent scaling
- independent release cadence
- customer deployment boundary
- compliance boundary
- failure isolation

This keeps the first release understandable while preserving the long-term architecture.
