# CyberOS M1.1 — Platform Kernel

## Purpose

M1.1 turns the M0 control-plane foundation into a tenant-scoped platform kernel. The web portal remains the primary operator surface; security engines remain subordinate execution environments.

## Implemented in M1.1

- Versioned platform identity: `0.3.0-m1.1`
- Current tenant context API
- Current operator identity API
- Tenant-scoped audit event API
- Explicit tenant/identity/authorization context returned by the control plane
- Existing job, finding, evidence and connector records remain tenant-keyed
- Existing synthetic execution policy remains enforced

## Control-Plane APIs

- `GET /api/v1/platform`
- `GET /api/v1/context`
- `GET /api/v1/tenants/current`
- `GET /api/v1/identity/me`
- `GET /api/v1/audit?limit=25`
- Existing demo asset/finding/job APIs

## Security Model

Every customer-owned resource is associated with a tenant. The production implementation must derive tenant identity from authenticated session credentials rather than from client-supplied identifiers.

M1.1 therefore treats the current demo operator as a controlled bootstrap identity. It is **not production authentication** and must not be presented as SSO, password authentication, or enterprise identity proofing.

## Next M1 increments

### M1.2 — Authentication boundary

- Session/JWT design
- Passwordless or enterprise IdP path
- Token rotation and expiry
- Authentication audit events
- CSRF/session protections where applicable

### M1.3 — Authorization

- RBAC permissions
- Resource/action authorization matrix
- Tenant boundary middleware
- Deny-by-default API policy
- Authorization tests

### M1.4 — Operational records

- Finding lifecycle
- Evidence metadata and integrity fields
- Report lifecycle
- Job lifecycle and worker acknowledgements
- Immutable audit strategy

## Exit criteria for M1

M1 is complete only when an authenticated multi-tenant application can demonstrate, through automated tests, that one tenant cannot read or mutate another tenant's resources and that all security-sensitive operations generate auditable events.
