# CyberOS Kali-Compatible Customer Agent

This agent is designed to run **inside the customer's authorized network**. The CyberOS control plane does not open an unrestricted inbound tunnel.

## Flow

1. Register the company in CyberOS.
2. Map a small allowlisted set of customer resources.
3. Register the Kali-compatible connector in Organization.
4. Enroll the connector once and store the returned token securely.
5. Run this agent from the customer-side Kali host.
6. The agent sends a heartbeat and polls only for jobs belonging to its tenant authorization context.
7. The control plane creates jobs only for assets already mapped to that tenant.
8. The agent executes limited, non-destructive discovery/service enumeration and returns evidence.

## Local Kali example

After the connector is registered, enroll it through the API using its connector ID. Then run:

```bash
export CYBEROS_CONTROL_PLANE=http://<cyberos-control-plane>:8100
export CYBEROS_CONNECTOR_ID=<connector-id>
export CYBEROS_ENROLLMENT_TOKEN=<one-time-token>
python3 tools/cyberos-kali-agent/agent.py
```

The initial network execution profile uses Nmap TCP connect scanning with service/version detection against the top 100 ports. Nmap supports `-sT` for TCP connect scanning and `--top-ports` for a bounded port set. See the official Nmap documentation for the scan semantics.

The agent deliberately does **not** accept arbitrary CLI targets. Targets come from CyberOS jobs created against tenant-mapped assets and an active authorization context.

Production hardening still requires mTLS/device identity, signed jobs, short-lived enrollment credentials, certificate rotation, stronger policy enforcement, and a dedicated evidence store.
