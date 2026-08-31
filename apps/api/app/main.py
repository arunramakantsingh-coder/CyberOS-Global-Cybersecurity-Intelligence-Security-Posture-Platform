from datetime import datetime, timezone, timedelta
import json
import os
import psycopg
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

app = FastAPI(title="CyberOS Control Plane", version="0.2.0-m0.2")
DB = os.environ.get("DATABASE_URL", "postgresql://cyberos:cyberos_dev_only@localhost:5433/cyberos")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3100"],
    allow_credentials=True,
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)

SAFE_CAPABILITIES = {"demo.asset_inventory", "demo.finding_fixture"}

class JobRequest(BaseModel):
    capability: str = Field(min_length=1, max_length=100)
    target: str = Field(min_length=1, max_length=500)
    authorized: bool = False


def db_fetch(query, params=()):
    with psycopg.connect(DB, connect_timeout=3) as conn:
        with conn.cursor() as cur:
            cur.execute(query, params)
            return cur.fetchall()


def ensure_demo_control_plane():
    with psycopg.connect(DB, connect_timeout=3) as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT id FROM tenants WHERE slug='cyberos-demo'")
            tenant_id = cur.fetchone()[0]
            cur.execute("""
                INSERT INTO identities (tenant_id,email,display_name,role)
                VALUES (%s,'operator@demo.cyberos.local','Demo Security Operator','security_operator')
                ON CONFLICT (tenant_id,email) DO UPDATE SET role=EXCLUDED.role
                RETURNING id
            """, (tenant_id,))
            actor_id = cur.fetchone()[0]
            cur.execute("""
                SELECT id FROM authorization_contexts
                WHERE tenant_id=%s AND engagement_name='CyberOS Synthetic Demo Authorization'
                ORDER BY created_at DESC LIMIT 1
            """, (tenant_id,))
            existing = cur.fetchone()
            if existing:
                auth_id = existing[0]
            else:
                cur.execute("""
                    INSERT INTO authorization_contexts
                    (tenant_id,engagement_name,authorized_by,scope,exclusions,allowed_capabilities,starts_at,ends_at,status)
                    VALUES (%s,'CyberOS Synthetic Demo Authorization',%s,%s,%s,%s,now(),now()+interval '365 days','active')
                    RETURNING id
                """, (tenant_id, actor_id, json.dumps(["https://portal.demo.cyberos.local","api.demo.cyberos.local","demo-linux-01","demo-edge-fw"]), json.dumps([]), json.dumps(sorted(SAFE_CAPABILITIES))))
                auth_id = cur.fetchone()[0]
            conn.commit()
            return str(tenant_id), str(actor_id), str(auth_id)


@app.on_event("startup")
def startup():
    try:
        ensure_demo_control_plane()
    except Exception as exc:
        print(f"CyberOS startup control-plane initialization deferred: {exc}")


@app.get("/")
def root():
    return {"product": "CyberOS", "service": "control-plane", "milestone": "M0.2", "status": "online"}

@app.get("/health")
def health():
    db = "healthy"
    try:
        with psycopg.connect(DB, connect_timeout=2) as conn:
            conn.execute("SELECT 1")
    except Exception:
        db = "unavailable"
    return {"status": "healthy" if db == "healthy" else "degraded", "database": db, "timestamp": datetime.now(timezone.utc).isoformat()}

@app.get("/api/v1/platform")
def platform():
    return {
        "name": "CyberOS",
        "version": "0.2.0-m0.2",
        "modules": ["Threat Intelligence", "Attack Surface", "Vulnerability", "Security Posture", "Web Security", "Network & Hardening", "Compliance", "AI", "Reporting"],
        "execution": "policy-controlled",
        "api_port": 8000,
    }

@app.get("/api/v1/demo/summary")
def demo_summary():
    tenant = db_fetch("SELECT id, name, subscription_tier FROM tenants WHERE slug='cyberos-demo'")[0]
    tenant_id = tenant[0]
    assets = db_fetch("SELECT COUNT(*) FROM assets WHERE tenant_id=%s", (tenant_id,))[0][0]
    findings = db_fetch("SELECT COUNT(*) FROM findings WHERE tenant_id=%s AND status='open'", (tenant_id,))[0][0]
    connectors = db_fetch("SELECT COUNT(*) FROM connectors WHERE tenant_id=%s AND status='online'", (tenant_id,))[0][0]
    frameworks = db_fetch("SELECT COUNT(*) FROM compliance_frameworks")[0][0]
    jobs = db_fetch("SELECT COUNT(*) FROM jobs WHERE tenant_id=%s", (tenant_id,))[0][0]
    return {"tenant": {"id": str(tenant[0]), "name": tenant[1], "tier": tenant[2]}, "assets": assets, "open_findings": findings, "online_connectors": connectors, "frameworks": frameworks, "jobs": jobs, "execution_policy": "enforced"}

@app.get("/api/v1/demo/assets")
def demo_assets():
    tenant_id = db_fetch("SELECT id FROM tenants WHERE slug='cyberos-demo'")[0][0]
    rows = db_fetch("SELECT id,name,asset_type,identifier,environment,criticality,exposure FROM assets WHERE tenant_id=%s ORDER BY name", (tenant_id,))
    return [{"id": str(r[0]), "name": r[1], "type": r[2], "identifier": r[3], "environment": r[4], "criticality": r[5], "exposure": r[6]} for r in rows]

@app.get("/api/v1/demo/findings")
def demo_findings():
    tenant_id = db_fetch("SELECT id FROM tenants WHERE slug='cyberos-demo'")[0][0]
    rows = db_fetch("SELECT id,title,severity,category,status,remediation FROM findings WHERE tenant_id=%s ORDER BY CASE severity WHEN 'critical' THEN 1 WHEN 'high' THEN 2 WHEN 'medium' THEN 3 ELSE 4 END, title", (tenant_id,))
    return [{"id": str(r[0]), "title": r[1], "severity": r[2], "category": r[3], "status": r[4], "remediation": r[5]} for r in rows]

@app.get("/api/v1/demo/control-context")
def demo_control_context():
    tenant_id, actor_id, auth_id = ensure_demo_control_plane()
    return {"tenant_id": tenant_id, "actor_id": actor_id, "authorization_id": auth_id, "mode": "synthetic-only", "allowed_capabilities": sorted(SAFE_CAPABILITIES)}

@app.get("/api/v1/demo/jobs")
def demo_jobs():
    tenant_id = db_fetch("SELECT id FROM tenants WHERE slug='cyberos-demo'")[0][0]
    rows = db_fetch("SELECT id,capability,target,state,policy_reason,created_at,updated_at FROM jobs WHERE tenant_id=%s ORDER BY created_at DESC LIMIT 25", (tenant_id,))
    return [{"id": str(r[0]), "capability": r[1], "target": r[2], "state": r[3], "policy_reason": r[4], "created_at": r[5].isoformat(), "updated_at": r[6].isoformat()} for r in rows]

@app.post("/api/v1/demo/jobs")
def create_demo_job(job: JobRequest):
    tenant_id, actor_id, auth_id = ensure_demo_control_plane()
    asset = db_fetch("SELECT id FROM assets WHERE tenant_id=%s AND identifier=%s", (tenant_id, job.target))
    allowed = job.authorized and job.capability in SAFE_CAPABILITIES and bool(asset)
    reason = None if allowed else "policy denied: synthetic demo authorization, target allowlist, and capability are required"
    state = "queued" if allowed else "blocked"
    with psycopg.connect(DB, connect_timeout=3) as conn:
        with conn.cursor() as cur:
            cur.execute("""
                INSERT INTO jobs (tenant_id,requested_by,authorization_id,capability,target,state,policy_reason,parameters)
                VALUES (%s,%s,%s,%s,%s,%s,%s,%s) RETURNING id,created_at,updated_at
            """, (tenant_id, actor_id, auth_id, job.capability, job.target, state, reason, json.dumps({"mode": "synthetic-only"})))
            job_id, created_at, updated_at = cur.fetchone()
            cur.execute("""
                INSERT INTO audit_events (tenant_id,actor_id,event_type,resource_type,resource_id,decision,metadata)
                VALUES (%s,%s,%s,'job',%s,%s,%s)
            """, (tenant_id, actor_id, "job.requested", job_id, "allow" if allowed else "deny", json.dumps({"capability": job.capability, "target": job.target, "authorization_id": auth_id})))
            conn.commit()
    return {"id": str(job_id), "state": state, "policy_reason": reason, "capability": job.capability, "target": job.target, "created_at": created_at.isoformat(), "updated_at": updated_at.isoformat()}

@app.post("/api/v1/jobs/preview")
def preview_job(job: JobRequest):
    if not job.authorized:
        return {"status": "blocked", "reason": "explicit authorization required", "target": job.target}
    if job.capability not in SAFE_CAPABILITIES:
        return {"status": "blocked", "reason": "capability is not enabled for M0.2 demo execution", "capability": job.capability}
    return {"status": "policy_review_required", "capability": job.capability, "target": job.target}
