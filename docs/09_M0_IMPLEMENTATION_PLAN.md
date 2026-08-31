# M0 Implementation Plan

## M0.1 Repository and engineering foundation

- [ ] monorepo directory skeleton
- [ ] Python backend baseline
- [ ] Next.js/React portal baseline
- [ ] shared contracts package
- [ ] environment configuration
- [ ] local Docker Compose
- [ ] CI pipeline

## M0.2 Identity and tenancy

- [ ] tenant entity
- [ ] user identity entity
- [ ] role/permission model
- [ ] API authentication
- [ ] tenant isolation tests
- [ ] audit events

## M0.3 Security domain model

- [ ] assets
- [ ] findings
- [ ] evidence
- [ ] engagements
- [ ] authorization contexts
- [ ] jobs
- [ ] tools
- [ ] connectors

## M0.4 Execution control plane

- [ ] capability registry
- [ ] authorization resolver
- [ ] scope resolver
- [ ] policy engine
- [ ] job signing
- [ ] queue abstraction
- [ ] worker abstraction
- [ ] cancellation

## M0.5 Tool adapter boundary

Create a stable adapter interface so scanners can be replaced without changing the control plane.

First safe adapters should support non-destructive/passive capabilities and fixture-based tests. Active testing remains a later milestone.

## M0.6 Connector foundation

Define the CyberOS Connector protocol before implementing production networking. The connector must authenticate to the control plane, receive only authorized jobs, report health and support cancellation.

## M0.7 AI boundary

Implement an AI gateway interface, not a direct shell/tool interface. AI requests become structured capability requests and pass through the same policy engine as human/API requests.

## M0.8 Verification gate

M0 is complete only when:

- all core services start locally
- migrations are reproducible
- authentication works
- tenant isolation tests pass
- job lifecycle tests pass
- policy-denial tests pass
- audit records are generated
- CI is green
- no secrets are committed
- documentation matches implementation

No M1 scanner development should be treated as complete until this gate passes.
