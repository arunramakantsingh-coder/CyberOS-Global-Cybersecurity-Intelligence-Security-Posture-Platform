from datetime import datetime, timezone
import os
import psycopg
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

app = FastAPI(title="CyberOS Control Plane", version="0.1.0-m0.1")
DB = os.environ.get("DATABASE_URL", "postgresql://cyberos:cyberos_dev_only@localhost:5433/cyberos")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3100"],
    allow_credentials=True,
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)

class JobRequest(BaseModel):
    capability: str
    target: str
    authorized: bool = False


def db_fetch(query, params=()):
    with psycopg.connect(DB, connect_timeout=3) as conn:
        with conn.cursor() as cur:
            cur.execute(query, params)
            return cur.fetchall()

@app.get("/")
def root():
    return {"product": "CyberOS", "service": "control-plane", "milestone": "M0.1", "status": "online"}

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
        "version": "0.1.0-m0.1",
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
    return {"tenant": {"id": str(tenant[0]), "name": tenant[1], "tier": tenant[2]}, "assets": assets, "open_findings": findings, "online_connectors": connectors, "frameworks": frameworks, "execution_policy": "enforced"}

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

@app.post("/api/v1/jobs/preview")
def preview_job(job: JobRequest):
    if not job.authorized:
        return {"status": "blocked", "reason": "explicit authorization required", "target": job.target}
    return {"status": "policy_review_required", "capability": job.capability, "target": job.target}
