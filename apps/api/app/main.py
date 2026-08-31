from datetime import datetime, timezone
import os
import psycopg
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI(title="CyberOS Control Plane", version="0.1.0-m0")
DB = os.environ.get("DATABASE_URL", "postgresql://cyberos:cyberos_dev_only@localhost:5433/cyberos")

class JobRequest(BaseModel):
    capability: str
    target: str
    authorized: bool = False

@app.get("/")
def root():
    return {"product": "CyberOS", "service": "control-plane", "milestone": "M0", "status": "online"}

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
        "version": "0.1.0-m0",
        "modules": ["Threat Intelligence", "Attack Surface", "Vulnerability", "Security Posture", "Compliance", "AI", "Reporting"],
        "execution": "policy-controlled",
        "api_port": 8000,
    }

@app.post("/api/v1/jobs/preview")
def preview_job(job: JobRequest):
    if not job.authorized:
        return {"status": "blocked", "reason": "explicit authorization required", "target": job.target}
    return {"status": "policy_review_required", "capability": job.capability, "target": job.target}
