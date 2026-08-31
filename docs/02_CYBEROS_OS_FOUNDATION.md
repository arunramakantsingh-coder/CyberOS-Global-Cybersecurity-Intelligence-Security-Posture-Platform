# CyberOS Security Operating Platform Foundation

## 1. Objective

CyberOS needs an execution foundation capable of running security assessment workloads in cloud, VM, appliance and customer-network environments while presenting a web-native operator experience.

The OS should be treated as a secure platform component, not as the customer-facing product UI.

## 2. Recommended Direction

Build a **minimal, hardened Linux-based CyberOS Base** and run specialized security tooling in isolated execution environments.

Kali Linux is valuable as a source of mature security tooling and as an execution environment, but CyberOS should not become a customized Kali desktop.

## 3. Layered Model

```text
CyberOS Web UI / API
        |
CyberOS Control Plane
        |
Policy / Authorization / Scope Engine
        |
CyberOS Agent + Job Runtime
        |
Sandbox / Container / VM Boundary
        |
+-------------------------------+
| Kali Tool Environment         |
| Web Security Environment      |
| Network Assessment Environment |
| Config/Hardening Environment   |
| CyberOS Native Engines        |
+-------------------------------+
        |
Linux / Kernel / Networking
```

## 4. Base OS Requirements

The eventual base should support:

- Minimal package footprint
- Secure boot where deployment permits
- Signed/verified artifacts
- Immutable or controlled-update model
- Automatic security updates or controlled enterprise update channels
- Disk encryption where appropriate
- Strong service isolation
- Least privilege
- Systemd hardening or equivalent
- Mandatory access control where practical
- Firewall defaults
- Secure logging
- Remote attestation options for future editions
- Reproducible build goals
- SBOM generation
- Vulnerability scanning of the OS image

## 5. Execution Environments

Tooling should be packaged independently from the base OS.

Example classes:

- `network-assessment`
- `web-security`
- `vulnerability-assessment`
- `configuration-audit`
- `cloud-security`
- `container-security`
- `forensics`
- `compliance-evidence`

The platform should pin versions and record tool provenance for every job.

## 6. Job Runtime

Every execution follows:

```text
Job Requested
    |
Validate Tenant
    |
Validate User/Service Identity
    |
Validate Authorization
    |
Validate Target Scope
    |
Validate Time Window
    |
Validate Tool Permission
    |
Apply Resource Limits
    |
Create Isolated Runtime
    |
Execute
    |
Collect Evidence
    |
Destroy/Reset Runtime
    |
Normalize Results
```

## 7. No Unrestricted AI Shell

The AI layer must never receive a general-purpose root shell as its normal operating interface.

Instead it calls typed CyberOS capabilities such as:

```text
create_assessment_job
request_asset_inventory
analyze_configuration
run_authorized_web_assessment
query_threat_intelligence
map_finding_to_controls
create_remediation_plan
```

The capability gateway enforces authorization and scope.

## 8. Cloud Deployment

The same execution model should run in:

- Kubernetes
- VM-based cloud deployment
- dedicated security worker nodes
- customer-hosted appliance
- private cloud

The base OS should therefore avoid assumptions about a single cloud provider.

## 9. Customer Connector

The connector is a hardened CyberOS agent/appliance deployed inside an authorized customer environment.

Responsibilities:

- Secure enrollment
- Device identity
- Health reporting
- Approved route management
- Internal asset discovery
- Authorized assessment execution
- Configuration collection
- Evidence transfer
- Policy enforcement
- Local emergency stop

## 10. Connectivity

Use established secure overlay technology and well-reviewed cryptographic primitives. Do not implement custom encryption or a custom VPN protocol merely to resemble an existing product.

The architecture should support WireGuard-based or equivalent mature secure transport, with CyberOS providing the control plane, identity, routing policy, tenant association and job authorization.

## 11. Connector Trust Model

```text
CyberOS Tenant
     |
Connector Identity
     |
Approved Environment
     |
Approved Route
     |
Approved Job
     |
Approved Tool
```

A valid connector credential alone must not authorize arbitrary scanning.

## 12. Build Pipeline

The OS build pipeline will eventually produce:

```text
Source
 -> Dependency Lock
 -> Build
 -> SBOM
 -> Vulnerability Scan
 -> Security Tests
 -> Image Signing
 -> Artifact Repository
 -> Release Manifest
```

Updates should be atomic and rollback-capable where the deployment platform permits.

## 13. Initial Implementation Strategy

Do not build a new Linux distribution kernel ecosystem in the first milestone.

Start with a minimal supported Linux base plus containers/VMs and establish:

1. CyberOS agent
2. secure job runner
3. execution policy
4. tool adapter interface
5. evidence pipeline
6. update mechanism
7. connector packaging

Only after the execution model is stable should the project invest in deeper OS customization.

## 14. Future OS Editions

- CyberOS Cloud Worker
- CyberOS Connector
- CyberOS Security Appliance
- CyberOS Enterprise Private Node
- CyberOS Restricted Deployment
- CyberOS Offline/Air-Gapped Edition
