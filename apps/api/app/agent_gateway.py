import hashlib
import json
import os
import secrets
from datetime import datetime, timezone

import psycopg
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

router = APIRouter(prefix="/api/v1/agent", tags=["Customer Agent Gateway"])
DB = os.environ.get("DATABASE_URL", "postgresql://cyberos:cyberos_dev_only@localhost:5433/cyberos")

class Heartbeat(BaseModel):
    connector_id: str
    enrollment_token: str = Field(min_length=16, max_length=200)
    agent_version: str = "0.1.0"
    capabilities: list[str] = Field(default_factory=list)

class Result(BaseModel):
    connector_id: str
    enrollment_token: str = Field(min_length=16, max_length=200)
    job_id: str
    state: str
    result: dict = Field(default_factory=dict)


def db(): return psycopg.connect(DB, connect_timeout=3)
def token_hash(token): return hashlib.sha256(token.encode()).hexdigest()

def auth_connector(cur, connector_id, token):
    cur.execute("SELECT id,tenant_id,status,metadata,authorization_id FROM connectors WHERE id=%s", (connector_id,))
    row=cur.fetchone()
    if not row: raise HTTPException(status_code=404, detail="Connector not found")
    metadata=row[3] or {}
    if metadata.get("enrollment_token_hash") != token_hash(token): raise HTTPException(status_code=401, detail="Invalid enrollment token")
    if row[4]:
        cur.execute("SELECT id,status FROM authorization_contexts WHERE id=%s AND tenant_id=%s",(row[4],row[1])); auth=cur.fetchone()
        if not auth or auth[1] != "active": raise HTTPException(status_code=403, detail="Connector authorization is not active")
    return row

@router.post("/enroll")
def enroll(connector_id: str):
    token=secrets.token_urlsafe(32)
    with db() as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT id,status FROM connectors WHERE id=%s",(connector_id,)); row=cur.fetchone()
            if not row: raise HTTPException(status_code=404,detail="Connector not found")
            cur.execute("UPDATE connectors SET metadata=COALESCE(metadata,'{}'::jsonb) || %s::jsonb WHERE id=%s",(json.dumps({"enrollment_token_hash":token_hash(token),"enrollment_issued_at":datetime.now(timezone.utc).isoformat()}),connector_id))
            conn.commit()
    return {"connector_id":connector_id,"enrollment_token":token,"warning":"Store this token securely. It is shown once and is required for the customer-side agent heartbeat."}

@router.post("/heartbeat")
def heartbeat(req: Heartbeat):
    with db() as conn:
        with conn.cursor() as cur:
            row=auth_connector(cur,req.connector_id,req.enrollment_token)
            cur.execute("UPDATE connectors SET status='online',last_seen=now(),capabilities=%s,metadata=COALESCE(metadata,'{}'::jsonb)||%s::jsonb WHERE id=%s",(json.dumps(req.capabilities),json.dumps({"agent_version":req.agent_version}),req.connector_id))
            conn.commit()
    return {"status":"online","connector_id":req.connector_id,"tenant_id":str(row[1]),"allowed":"authorized jobs only"}

@router.get("/jobs/{connector_id}")
def next_job(connector_id: str, enrollment_token: str):
    with db() as conn:
        with conn.cursor() as cur:
            row=auth_connector(cur,connector_id,enrollment_token)
            if row[2] != "online": raise HTTPException(status_code=409,detail="Connector heartbeat required")
            cur.execute("SELECT id,capability,target,parameters,authorization_id FROM jobs WHERE tenant_id=%s AND state='queued' AND authorization_id=%s ORDER BY created_at LIMIT 1",(row[1],row[4]))
            job=cur.fetchone()
            if not job: return {"job":None}
            cur.execute("UPDATE jobs SET state='running',updated_at=now() WHERE id=%s",(job[0],)); conn.commit()
    return {"job":{"id":str(job[0]),"capability":job[1],"target":job[2],"parameters":job[3],"authorization_id":str(job[4])}}

@router.post("/result")
def result(req: Result):
    with db() as conn:
        with conn.cursor() as cur:
            row=auth_connector(cur,req.connector_id,req.enrollment_token)
            cur.execute("SELECT id FROM jobs WHERE id=%s AND tenant_id=%s",(req.job_id,row[1])); job=cur.fetchone()
            if not job: raise HTTPException(status_code=404,detail="Job not found in connector tenant")
            state=req.state if req.state in {"completed","failed","blocked"} else "failed"
            cur.execute("UPDATE jobs SET state=%s,updated_at=now(),parameters=COALESCE(parameters,'{}'::jsonb)||%s::jsonb WHERE id=%s",(state,json.dumps({"agent_result":req.result,"connector_id":req.connector_id}),req.job_id))
            cur.execute("INSERT INTO audit_events (tenant_id,event_type,resource_type,resource_id,decision,metadata) VALUES (%s,'agent.job.result','job',%s,%s,%s)",(row[1],req.job_id,"allow" if state=="completed" else "review",json.dumps({"connector_id":req.connector_id,"state":state}))); conn.commit()
    return {"job_id":req.job_id,"state":state}
