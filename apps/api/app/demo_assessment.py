import json
import os
from datetime import datetime, timezone

import psycopg
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

router = APIRouter(prefix="/api/v1/demo-assessment", tags=["Demo Assessment"])
DB = os.environ.get("DATABASE_URL", "postgresql://cyberos:cyberos_dev_only@localhost:5433/cyberos")

PROFILES = {
    "general-hardening": {
        "name": "General Security Hardening",
        "capability": "demo.finding_fixture",
        "standards": ["CIS-style baseline", "NIST CSF 2.0"],
        "description": "Configuration, management-plane, encryption, logging and access-control posture checks.",
    },
    "vulnerability": {
        "name": "Vulnerability & Exposure Review",
        "capability": "demo.finding_fixture",
        "standards": ["CVE/CVSS context", "NIST CSF 2.0"],
        "description": "Synthetic vulnerability, exposure and remediation-priority review for the selected demo asset.",
    },
    "pci-dss": {
        "name": "PCI DSS Readiness",
        "capability": "demo.finding_fixture",
        "standards": ["PCI DSS 4.0.1"],
        "description": "Limited technical readiness checks mapped to PCI DSS security themes; not a certification audit.",
    },
    "iso-27001": {
        "name": "ISO/IEC 27001 Technical Readiness",
        "capability": "demo.finding_fixture",
        "standards": ["ISO/IEC 27001:2022"],
        "description": "Technical evidence and control-readiness view that supports, but does not replace, an ISMS audit.",
    },
    "nist-csf": {
        "name": "NIST CSF Security Posture",
        "capability": "demo.finding_fixture",
        "standards": ["NIST CSF 2.0"],
        "description": "Synthetic posture checks organized around Govern, Identify, Protect, Detect, Respond and Recover.",
    },
}

ASSET_CHECKS = {
    "firewall": [
        ("Management-plane exposure", "high", "Restrict administrative access to approved management networks and strong authentication."),
        ("Rulebase review", "medium", "Remove stale or overly broad rules and document business justification."),
        ("Security logging", "medium", "Forward security and administrative events to centralized monitoring."),
    ],
    "router": [
        ("Administrative service hardening", "high", "Disable unnecessary management services and restrict administrative source networks."),
        ("Routing control protection", "medium", "Protect routing adjacencies and validate route-control policy."),
        ("Configuration backup", "low", "Maintain versioned, access-controlled configuration backups."),
    ],
    "switch": [
        ("Layer-2 protection baseline", "medium", "Apply approved edge-port and control-plane protections."),
        ("Unused access ports", "medium", "Disable or quarantine unused ports and document exceptions."),
        ("Management network separation", "high", "Separate device administration from general user traffic."),
    ],
    "server": [
        ("Patch posture", "high", "Apply approved security updates and verify remediation."),
        ("Privileged access", "high", "Limit administrative access, use MFA/PAM where applicable and review privileged groups."),
        ("Host logging", "medium", "Collect security logs and verify retention and monitoring."),
    ],
    "web_application": [
        ("Application security headers", "medium", "Apply the approved security-header baseline and verify with a controlled retest."),
        ("Authentication configuration", "high", "Review session, MFA and account-recovery controls."),
        ("Input validation", "high", "Use parameterized queries and server-side validation; verify through authorized testing."),
    ],
    "api": [
        ("API authorization", "high", "Enforce object- and function-level authorization on every sensitive endpoint."),
        ("Input validation", "high", "Validate and constrain request data and use safe database access patterns."),
        ("API logging", "medium", "Capture security-relevant API activity without exposing secrets."),
    ],
}

FRAMEWORK_MAP = {
    "pci-dss": ["Req. 2 Secure configurations", "Req. 6 Secure systems/software", "Req. 7 Restrict access", "Req. 10 Log and monitor"],
    "iso-27001": ["A.5 Organizational controls", "A.8 Technological controls", "Risk treatment evidence"],
    "nist-csf": ["GV Govern", "ID Identify", "PR Protect", "DE Detect", "RS Respond", "RC Recover"],
    "general-hardening": ["Secure configuration", "Least privilege", "Logging/monitoring", "Encryption", "Attack-surface reduction"],
    "vulnerability": ["Asset context", "Exposure", "Exploitability", "Remediation priority", "Verification"],
}

class DemoAssessmentRequest(BaseModel):
    asset_id: str = Field(min_length=1, max_length=100)
    profile: str = Field(min_length=1, max_length=50)
    authorized: bool = False


def fetch_rows(query, params=()):
    with psycopg.connect(DB, connect_timeout=3) as conn:
        with conn.cursor() as cur:
            cur.execute(query, params)
            return cur.fetchall()


def demo_tenant():
    rows = fetch_rows("SELECT id,name,industry,region FROM tenants WHERE slug='cyberos-demo' LIMIT 1")
    if not rows:
        raise HTTPException(status_code=404, detail="Demo tenant is not initialized")
    return rows[0]


@router.get("/catalog")
def catalog():
    tenant = demo_tenant()
    assets = fetch_rows(
        "SELECT id,name,asset_type,identifier,environment,criticality,exposure FROM assets WHERE tenant_id=%s AND asset_type IN ('firewall','router','switch','server','web_application','api') ORDER BY asset_type,name",
        (tenant[0],),
    )
    return {
        "mode": "limited-demo",
        "tenant": {"id": str(tenant[0]), "name": tenant[1], "industry": tenant[2], "region": tenant[3]},
        "assets": [
            {"id": str(r[0]), "name": r[1], "type": r[2], "identifier": r[3], "environment": r[4], "criticality": r[5], "exposure": r[6]}
            for r in assets
        ],
        "profiles": [{"key": key, **value} for key, value in PROFILES.items()],
        "safety": {
            "network_access": False,
            "description": "This demo produces synthetic assessment evidence only. Real customer infrastructure requires an approved customer-side connector and explicit authorization.",
        },
    }


@router.post("/run")
def run_demo_assessment(req: DemoAssessmentRequest):
    if not req.authorized:
        raise HTTPException(status_code=403, detail="Explicit authorization acknowledgement is required")
    if req.profile not in PROFILES:
        raise HTTPException(status_code=400, detail="Unknown assessment profile")

    tenant = demo_tenant()
    rows = fetch_rows(
        "SELECT id,name,asset_type,identifier,environment,criticality,exposure FROM assets WHERE id=%s AND tenant_id=%s",
        (req.asset_id, tenant[0]),
    )
    if not rows:
        raise HTTPException(status_code=404, detail="Asset is outside the current tenant demo scope")
    asset = rows[0]
    checks = ASSET_CHECKS.get(asset[2], ASSET_CHECKS["server"])
    severity_weight = {"critical": 30, "high": 20, "medium": 10, "low": 4}
    deductions = sum(severity_weight.get(sev, 5) for _, sev, _ in checks)
    score = max(0, 100 - deductions)
    now = datetime.now(timezone.utc)

    findings = [
        {
            "title": title,
            "severity": severity,
            "status": "review",
            "evidence": "Synthetic evidence generated by CyberOS limited demo",
            "remediation": remediation,
        }
        for title, severity, remediation in checks
    ]
    report = {
        "report_id": f"DEMO-{now.strftime('%Y%m%d%H%M%S')}",
        "generated_at": now.isoformat(),
        "tenant": tenant[1],
        "asset": {"id": str(asset[0]), "name": asset[1], "type": asset[2], "identifier": asset[3], "environment": asset[4], "criticality": asset[5], "exposure": asset[6]},
        "assessment": PROFILES[req.profile],
        "score": score,
        "risk_rating": "high" if score < 55 else "medium" if score < 80 else "low",
        "controls_reviewed": FRAMEWORK_MAP[req.profile],
        "findings": findings,
        "disclaimer": "CyberOS limited demo report. Synthetic evidence only; not a certification, attestation or production penetration-test report.",
    }

    with psycopg.connect(DB, connect_timeout=3) as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT id FROM identities WHERE tenant_id=%s ORDER BY created_at LIMIT 1", (tenant[0],))
            actor = cur.fetchone()
            actor_id = actor[0] if actor else None
            cur.execute("SELECT id FROM authorization_contexts WHERE tenant_id=%s AND status='active' ORDER BY created_at DESC LIMIT 1", (tenant[0],))
            auth = cur.fetchone()
            auth_id = auth[0] if auth else None
            cur.execute(
                "INSERT INTO jobs (tenant_id,requested_by,authorization_id,capability,target,state,policy_reason,parameters) VALUES (%s,%s,%s,'demo.finding_fixture',%s,'completed',NULL,%s) RETURNING id",
                (tenant[0], actor_id, auth_id, asset[3], json.dumps({"demo_assessment": True, "profile": req.profile, "report_id": report["report_id"], "score": score})),
            )
            job_id = cur.fetchone()[0]
            cur.execute(
                "INSERT INTO audit_events (tenant_id,actor_id,event_type,resource_type,resource_id,decision,metadata) VALUES (%s,%s,'demo.assessment.completed','job',%s,'allow',%s)",
                (tenant[0], actor_id, job_id, json.dumps({"asset_id": str(asset[0]), "profile": req.profile, "report_id": report["report_id"], "synthetic_only": True})),
            )
            conn.commit()
    report["job_id"] = str(job_id)
    return report
