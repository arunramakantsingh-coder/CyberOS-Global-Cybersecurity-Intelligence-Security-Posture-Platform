# CyberOS Platform Data Model

## Purpose

This document defines the first stable domain vocabulary for the CyberOS control plane.

## Tenant

The hard security boundary for a customer organization.

Key fields:

- tenant_id
- legal_name
- industry
- region/data residency
- subscription_tier
- status

All tenant-owned records must carry a tenant identity directly or through an immutable ownership relationship.

## Identity

A human, service account or controlled agent operating within a tenant.

Roles are capability-based and must follow least privilege.

## Asset

A security-relevant object such as domain, IP, URL, application, API, server, endpoint, cloud resource, database, firewall, router, switch, container or Kubernetes object.

An asset has:

- ownership
- environment
- criticality
- exposure
- technology metadata
- discovery source
- lifecycle state

## Authorization Context

An explicit record describing why an assessment is allowed.

Required concepts:

- authorization_id
- tenant_id
- engagement_id
- authorized_by
- scope
- excluded_targets
- allowed_capabilities
- start/end time
- emergency stop state
- evidence of approval

## Job

A requested unit of work. Examples include passive asset discovery, vulnerability assessment, configuration evaluation or an authorized security test.

Lifecycle:

`requested -> policy_checked -> queued -> running -> completed`

Alternative terminal states:

`failed`, `cancelled`, `expired`, `blocked`

## Finding

A normalized security observation independent of any particular scanner.

Fields include:

- finding_id
- tenant_id
- asset_id
- severity
- confidence
- category
- title
- description
- evidence references
- remediation
- status
- first_seen
- last_seen

## Evidence

Immutable or content-addressed supporting material for a finding or assessment. Examples: scanner output, configuration snapshot, HTTP response metadata, screenshot reference, command result or compliance evidence.

Evidence must have provenance and access controls.

## Tool Adapter

A controlled integration between CyberOS and an external security engine. An adapter exposes metadata, capabilities, input schema, safety constraints and output normalization. Tools never receive raw user prompts.

## Compliance Control

A versioned control from a framework/catalog such as ISO/IEC 27001, PCI DSS, DORA, SOC 2 or NIST CSF. A control maps to evidence requirements, tests, findings and remediation guidance.

## AI Run

An auditable AI operation with:

- model/provider
- prompt/context policy
- retrieved evidence
- requested capability
- authorization context
- output
- human approval where required

AI context must be tenant-isolated.
