from datetime import datetime, timezone
import json
import os
import psycopg
from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from .threat_intelligence import router as threat_intelligence_router
from .tenant_workspace import router as tenant_workspace_router

app = FastAPI(title="CyberOS Control Plane", version="0.3.0-m2.3")
DB = os.environ.get("DATABASE_URL", "postgresql://cyberos:cyberos_dev_only@localhost:5433/cyberos")

app.add_middleware(CORSMiddleware, allow_origins=["http://localhost:3100"], allow_credentials=True, allow_methods=["GET", "POST", "PUT", "PATCH"], allow_headers=["*"])
app.include_router(threat_intelligence_router)
app.include_router(tenant_workspace_router)

MODULES = [("command-center", "Command Center"),("threat-intelligence", "Threat Intelligence"),("attack-surface", "Attack Surface"),("vulnerabilities", "Vulnerabilities"),("security-posture", "Security Posture"),("web-security", "Web & API Security"),("network-hardening", "Network & Hardening"),("compliance", "Compliance"),("ai-security", "Cyber AI"),("reports", "Reports")]
SAFE_CAPABILITIES = {"demo.asset_inventory", "demo.finding_fixture"}
AGENT_CAPABILITIES = {"authorized.network.discovery", "authorized.web.assessment", "authorized.vulnerability.assessment", "evidence.collection"}

class JobRequest(BaseModel):
    capability: str = Field(min_length=1, max_length=100)
    target: str = Field(min_length=1, max_length=500)
    authorized: bool = False
    connector_id: str | None = None
    parameters: dict = Field(default_factory=dict)

class ConnectorRequest(BaseModel):
    name: str = Field(min_length=2, max_length=120)
    connector_type: str = Field(default="customer_agent", max_length=50)
    environment: str = Field(default="hybrid", max_length=40)
    endpoint: str | None = Field(default=None, max_length=500)
    capabilities: list[str] = Field(default_factory=list)


def db_fetch(query, params=()):
    with psycopg.connect(DB, connect_timeout=3) as conn:
        with conn.cursor() as cur:
            cur.execute(query, params)
            return cur.fetchall()


def ensure_demo_control_plane():
    with psycopg.connect(DB, connect_timeout=3) as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT id FROM tenants WHERE slug='cyberos-demo'")
            tenant_row = cur.fetchone()
            if not tenant_row:
                raise RuntimeError("cyberos-demo tenant is not initialized")
            tenant_id = tenant_row[0]
            cur.execute("INSERT INTO identities (tenant_id,email,display_name,role) VALUES (%s,'operator@demo.cyberos.local','Demo Security Operator','security_operator') ON CONFLICT (tenant_id,email) DO UPDATE SET role=EXCLUDED.role RETURNING id", (tenant_id,))
            actor_id = cur.fetchone()[0]
            cur.execute("SELECT id FROM authorization_contexts WHERE tenant_id=%s AND engagement_name='CyberOS Synthetic Demo Authorization' ORDER BY created_at DESC LIMIT 1", (tenant_id,))
            existing = cur.fetchone()
            if existing:
                auth_id = existing[0]
            else:
                cur.execute("INSERT INTO authorization_contexts (tenant_id,engagement_name,authorized_by,scope,exclusions,allowed_capabilities,starts_at,ends_at,status) VALUES (%s,'CyberOS Synthetic Demo Authorization',%s,%s,%s,%s,now(),now()+interval '365 days','active') RETURNING id", (tenant_id, actor_id, json.dumps(["https://portal.demo.cyberos.local","api.demo.cyberos.local","demo-linux-01","demo-edge-fw"]), json.dumps([]), json.dumps(sorted(SAFE_CAPABILITIES))))
                auth_id = cur.fetchone()[0]
            conn.commit()
            return str(tenant_id), str(actor_id), str(auth_id)

@app.on_event("startup")
def startup():
    try: ensure_demo_control_plane()
    except Exception as exc: print(f"CyberOS startup control-plane initialization deferred: {exc}")

@app.get("/")
def root(): return {"product":"CyberOS","service":"control-plane","milestone":"M2.3","status":"online"}

@app.get("/health")
def health():
    db="healthy"
    try:
        with psycopg.connect(DB, connect_timeout=2) as conn: conn.execute("SELECT 1")
    except Exception: db="unavailable"
    return {"status":"healthy" if db=="healthy" else "degraded","database":db,"timestamp":datetime.now(timezone.utc).isoformat()}

@app.get("/api/v1/platform")
def platform(): return {"name":"CyberOS","version":"0.3.0-m2.3","milestone":"M2.3 Customer Security Workspace","modules":[name for _,name in MODULES],"execution":"policy-controlled","api_port":8000,"portal_port":3100,"network_execution":"customer-agent-only; authorization required"}

@app.get("/api/v1/context")
def context():
    tenant_id,actor_id,auth_id=ensure_demo_control_plane()
    tenant=db_fetch("SELECT id,name,slug,industry,region,subscription_tier,status,created_at FROM tenants WHERE id=%s",(tenant_id,))[0]
    identity=db_fetch("SELECT id,email,display_name,role,status,created_at FROM identities WHERE id=%s AND tenant_id=%s",(actor_id,tenant_id))[0]
    return {"tenant":{"id":str(tenant[0]),"name":tenant[1],"slug":tenant[2],"industry":tenant[3],"region":tenant[4],"subscription_tier":tenant[5],"status":tenant[6],"created_at":tenant[7].isoformat()},"identity":{"id":str(identity[0]),"email":identity[1],"display_name":identity[2],"role":identity[3],"status":identity[4],"created_at":identity[5].isoformat()},"authorization":{"id":auth_id,"mode":"synthetic-only","status":"active"},"isolation":"tenant-scoped"}

@app.get("/api/v1/organization")
def organization_workspace():
    tenant_id,actor_id,auth_id=ensure_demo_control_plane()
    tenant=db_fetch("SELECT id,name,slug,industry,region,subscription_tier,status FROM tenants WHERE id=%s",(tenant_id,))[0]
    modules=db_fetch("SELECT module_key,enabled,configuration FROM tenant_modules WHERE tenant_id=%s ORDER BY module_key",(tenant_id,))
    connectors=db_fetch("SELECT id,name,status,connector_type,environment,endpoint,last_seen,capabilities,authorization_id FROM connectors WHERE tenant_id=%s ORDER BY name",(tenant_id,))
    assets=db_fetch("SELECT id,name,asset_type,identifier,environment,criticality,exposure FROM assets WHERE tenant_id=%s ORDER BY name",(tenant_id,))
    return {"tenant":{"id":str(tenant[0]),"name":tenant[1],"slug":tenant[2],"industry":tenant[3],"region":tenant[4],"tier":tenant[5],"status":tenant[6]},"identity":{"id":actor_id,"role":"security_operator"},"authorization":{"id":auth_id,"status":"active","mode":"synthetic-only"},"modules":[{"key":r[0],"enabled":r[1],"configuration":r[2]} for r in modules],"connectors":[{"id":str(r[0]),"name":r[1],"status":r[2],"type":r[3],"environment":r[4],"endpoint":r[5],"last_seen":r[6].isoformat() if r[6] else None,"capabilities":r[7],"authorization_id":str(r[8]) if r[8] else None} for r in connectors],"assets":[{"id":str(r[0]),"name":r[1],"type":r[2],"identifier":r[3],"environment":r[4],"criticality":r[5],"exposure":r[6]} for r in assets]}

@app.get("/api/v1/modules")
def module_catalog():
    tenant_id,_,_=ensure_demo_control_plane(); rows=db_fetch("SELECT module_key,enabled,configuration FROM tenant_modules WHERE tenant_id=%s",(tenant_id,)); enabled={r[0]:{"enabled":r[1],"configuration":r[2]} for r in rows}; return [{"key":k,"name":n,**enabled.get(k,{"enabled":False,"configuration":{}})} for k,n in MODULES]

@app.patch("/api/v1/modules/{module_key}")
def set_module(module_key:str, enabled:bool=Query(...)):
    if module_key not in {k for k,_ in MODULES}: raise HTTPException(status_code=404,detail="Unknown module")
    tenant_id,actor_id,_=ensure_demo_control_plane()
    with psycopg.connect(DB,connect_timeout=3) as conn:
        with conn.cursor() as cur:
            cur.execute("INSERT INTO tenant_modules (tenant_id,module_key,enabled,updated_at) VALUES (%s,%s,%s,now()) ON CONFLICT (tenant_id,module_key) DO UPDATE SET enabled=EXCLUDED.enabled,updated_at=now()",(tenant_id,module_key,enabled))
            cur.execute("INSERT INTO audit_events (tenant_id,actor_id,event_type,resource_type,decision,metadata) VALUES (%s,%s,'tenant.module.changed','tenant_module','allow',%s)",(tenant_id,actor_id,json.dumps({"module":module_key,"enabled":enabled}))); conn.commit()
    return {"module":module_key,"enabled":enabled,"tenant_scoped":True}

@app.get("/api/v1/connectors")
def list_connectors():
    tenant_id,_,_=ensure_demo_control_plane(); rows=db_fetch("SELECT id,name,status,connector_type,environment,endpoint,last_seen,capabilities,authorization_id,metadata FROM connectors WHERE tenant_id=%s ORDER BY name",(tenant_id,)); return [{"id":str(r[0]),"name":r[1],"status":r[2],"type":r[3],"environment":r[4],"endpoint":r[5],"last_seen":r[6].isoformat() if r[6] else None,"capabilities":r[7],"authorization_id":str(r[8]) if r[8] else None,"metadata":r[9]} for r in rows]

@app.post("/api/v1/connectors")
def register_connector(req:ConnectorRequest):
    tenant_id,actor_id,auth_id=ensure_demo_control_plane(); allowed=set(req.capabilities).issubset(AGENT_CAPABILITIES); status="pending_authorization" if req.capabilities and not allowed else "pending"
    with psycopg.connect(DB,connect_timeout=3) as conn:
        with conn.cursor() as cur:
            cur.execute("INSERT INTO connectors (tenant_id,name,status,connector_type,environment,endpoint,capabilities,authorization_id,metadata) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s) RETURNING id,created_at",(tenant_id,req.name,status,req.connector_type,req.environment,req.endpoint,json.dumps(req.capabilities),auth_id,json.dumps({"registration_mode":"control-plane","network_access":"agent-side-only"}))); connector_id,created_at=cur.fetchone()
            cur.execute("INSERT INTO audit_events (tenant_id,actor_id,event_type,resource_type,resource_id,decision,metadata) VALUES (%s,%s,'connector.registered','connector',%s,%s,%s)",(tenant_id,actor_id,connector_id,"allow" if allowed else "review",json.dumps({"name":req.name,"capabilities":req.capabilities}))); conn.commit()
    return {"id":str(connector_id),"name":req.name,"status":status,"authorization_id":auth_id,"created_at":created_at.isoformat(),"network_execution":"not enabled until connector is approved/online"}

@app.get("/api/v1/assets")
def assets():
    tenant_id,_,_=ensure_demo_control_plane(); rows=db_fetch("SELECT id,name,asset_type,identifier,environment,criticality,exposure,metadata FROM assets WHERE tenant_id=%s ORDER BY name",(tenant_id,)); return [{"id":str(r[0]),"name":r[1],"type":r[2],"identifier":r[3],"environment":r[4],"criticality":r[5],"exposure":r[6],"metadata":r[7]} for r in rows]

@app.get("/api/v1/audit")
def audit(limit:int=Query(default=25,ge=1,le=100)):
    tenant_id,_,_=ensure_demo_control_plane(); rows=db_fetch("SELECT ae.id,ae.event_type,ae.resource_type,ae.resource_id,ae.decision,ae.metadata,ae.created_at,i.display_name FROM audit_events ae LEFT JOIN identities i ON i.id=ae.actor_id AND i.tenant_id=ae.tenant_id WHERE ae.tenant_id=%s ORDER BY ae.created_at DESC LIMIT %s",(tenant_id,limit)); return [{"id":str(r[0]),"event_type":r[1],"resource_type":r[2],"resource_id":str(r[3]) if r[3] else None,"decision":r[4],"metadata":r[5],"created_at":r[6].isoformat(),"actor":r[7]} for r in rows]

@app.get("/api/v1/tenants/current")
def current_tenant():
    tenant_id,_,_=ensure_demo_control_plane(); row=db_fetch("SELECT id,name,slug,industry,region,subscription_tier,status,created_at FROM tenants WHERE id=%s",(tenant_id,))[0]; return {"id":str(row[0]),"name":row[1],"slug":row[2],"industry":row[3],"region":row[4],"subscription_tier":row[5],"status":row[6],"created_at":row[7].isoformat()}

@app.get("/api/v1/identity/me")
def current_identity():
    _,actor_id,_=ensure_demo_control_plane(); row=db_fetch("SELECT id,email,display_name,role,status,created_at FROM identities WHERE id=%s",(actor_id,))[0]; return {"id":str(row[0]),"email":row[1],"display_name":row[2],"role":row[3],"status":row[4],"created_at":row[5].isoformat()}

@app.get("/api/v1/demo/summary")
def demo_summary():
    tenant=db_fetch("SELECT id,name,subscription_tier FROM tenants WHERE slug='cyberos-demo'")[0]; tenant_id=tenant[0]; assets=db_fetch("SELECT COUNT(*) FROM assets WHERE tenant_id=%s",(tenant_id,))[0][0]; findings=db_fetch("SELECT COUNT(*) FROM findings WHERE tenant_id=%s AND status='open'",(tenant_id,))[0][0]; connectors=db_fetch("SELECT COUNT(*) FROM connectors WHERE tenant_id=%s AND status='online'",(tenant_id,))[0][0]; frameworks=db_fetch("SELECT COUNT(*) FROM compliance_frameworks")[0][0]; jobs=db_fetch("SELECT COUNT(*) FROM jobs WHERE tenant_id=%s",(tenant_id,))[0][0]; return {"tenant":{"id":str(tenant[0]),"name":tenant[1],"tier":tenant[2]},"assets":assets,"open_findings":findings,"online_connectors":connectors,"frameworks":frameworks,"jobs":jobs,"execution_policy":"enforced"}

@app.get("/api/v1/demo/assets")
def demo_assets():
    tenant_id=db_fetch("SELECT id FROM tenants WHERE slug='cyberos-demo'")[0][0]; rows=db_fetch("SELECT id,name,asset_type,identifier,environment,criticality,exposure FROM assets WHERE tenant_id=%s ORDER BY name",(tenant_id,)); return [{"id":str(r[0]),"name":r[1],"type":r[2],"identifier":r[3],"environment":r[4],"criticality":r[5],"exposure":r[6]} for r in rows]

@app.get("/api/v1/demo/findings")
def demo_findings():
    tenant_id=db_fetch("SELECT id FROM tenants WHERE slug='cyberos-demo'")[0][0]; rows=db_fetch("SELECT id,title,severity,category,status,remediation FROM findings WHERE tenant_id=%s ORDER BY CASE severity WHEN 'critical' THEN 1 WHEN 'high' THEN 2 WHEN 'medium' THEN 3 ELSE 4 END,title",(tenant_id,)); return [{"id":str(r[0]),"title":r[1],"severity":r[2],"category":r[3],"status":r[4],"remediation":r[5]} for r in rows]

@app.get("/api/v1/demo/control-context")
def demo_control_context():
    tenant_id,actor_id,auth_id=ensure_demo_control_plane(); return {"tenant_id":tenant_id,"actor_id":actor_id,"authorization_id":auth_id,"mode":"synthetic-only","allowed_capabilities":sorted(SAFE_CAPABILITIES)}

@app.get("/api/v1/demo/jobs")
def demo_jobs():
    tenant_id=db_fetch("SELECT id FROM tenants WHERE slug='cyberos-demo'")[0][0]; rows=db_fetch("SELECT id,capability,target,state,policy_reason,created_at,updated_at FROM jobs WHERE tenant_id=%s ORDER BY created_at DESC LIMIT 25",(tenant_id,)); return [{"id":str(r[0]),"capability":r[1],"target":r[2],"state":r[3],"policy_reason":r[4],"created_at":r[5].isoformat(),"updated_at":r[6].isoformat()} for r in rows]

@app.post("/api/v1/demo/jobs")
def create_demo_job(job:JobRequest):
    tenant_id,actor_id,auth_id=ensure_demo_control_plane(); asset=db_fetch("SELECT id FROM assets WHERE tenant_id=%s AND identifier=%s",(tenant_id,job.target)); allowed=job.authorized and job.capability in SAFE_CAPABILITIES and bool(asset); reason=None if allowed else "policy denied: synthetic demo authorization, target allowlist, and capability are required"; state="queued" if allowed else "blocked"
    with psycopg.connect(DB,connect_timeout=3) as conn:
        with conn.cursor() as cur:
            cur.execute("INSERT INTO jobs (tenant_id,requested_by,authorization_id,capability,target,state,policy_reason,parameters) VALUES (%s,%s,%s,%s,%s,%s,%s,%s) RETURNING id,created_at,updated_at",(tenant_id,actor_id,auth_id,job.capability,job.target,state,reason,json.dumps({"mode":"synthetic-only",**job.parameters}))); job_id,created_at,updated_at=cur.fetchone(); cur.execute("INSERT INTO audit_events (tenant_id,actor_id,event_type,resource_type,resource_id,decision,metadata) VALUES (%s,%s,%s,'job',%s,%s,%s)",(tenant_id,actor_id,"job.requested",job_id,"allow" if allowed else "deny",json.dumps({"capability":job.capability,"target":job.target,"authorization_id":auth_id}))); conn.commit()
    return {"id":str(job_id),"state":state,"policy_reason":reason,"capability":job.capability,"target":job.target,"created_at":created_at.isoformat(),"updated_at":updated_at.isoformat()}

@app.post("/api/v1/jobs/preview")
def preview_job(job:JobRequest):
    if not job.authorized: return {"status":"blocked","reason":"explicit authorization required","target":job.target}
    if job.capability not in SAFE_CAPABILITIES and job.capability not in AGENT_CAPABILITIES: return {"status":"blocked","reason":"capability is not registered in CyberOS policy catalog","capability":job.capability}
    if job.capability in AGENT_CAPABILITIES: return {"status":"connector_required","reason":"customer-controlled connector must be approved and online before any network activity","capability":job.capability,"target":job.target}
    return {"status":"policy_review_required","capability":job.capability,"target":job.target}

@app.post("/api/v1/assessments/request")
def request_assessment(job:JobRequest):
    tenant_id,actor_id,auth_id=ensure_demo_control_plane()
    if not job.authorized: raise HTTPException(status_code=403,detail="Explicit customer authorization is required")
    if job.capability not in AGENT_CAPABILITIES: raise HTTPException(status_code=400,detail="Assessment capability is not registered")
    if not job.connector_id: raise HTTPException(status_code=400,detail="Approved customer connector is required")
    connector=db_fetch("SELECT id,status,authorization_id FROM connectors WHERE id=%s AND tenant_id=%s",(job.connector_id,tenant_id))
    if not connector: raise HTTPException(status_code=404,detail="Connector not found in current tenant")
    if connector[0][1] != "online": raise HTTPException(status_code=409,detail="Connector is not online")
    if connector[0][2] and str(connector[0][2]) != auth_id: raise HTTPException(status_code=403,detail="Connector authorization does not match current tenant authorization")
    with psycopg.connect(DB,connect_timeout=3) as conn:
        with conn.cursor() as cur:
            cur.execute("INSERT INTO jobs (tenant_id,requested_by,authorization_id,capability,target,state,policy_reason,parameters) VALUES (%s,%s,%s,%s,%s,'queued',%s,%s) RETURNING id,created_at,updated_at",(tenant_id,actor_id,auth_id,job.capability,job.target,"customer-agent execution; awaiting worker capability enablement",json.dumps({"connector_id":job.connector_id,**job.parameters}))); job_id,created_at,updated_at=cur.fetchone(); cur.execute("INSERT INTO audit_events (tenant_id,actor_id,event_type,resource_type,resource_id,decision,metadata) VALUES (%s,%s,'assessment.requested','job',%s,'review',%s)",(tenant_id,actor_id,job_id,json.dumps({"capability":job.capability,"target":job.target,"connector_id":job.connector_id,"authorization_id":auth_id}))); conn.commit()
    return {"id":str(job_id),"state":"queued","mode":"customer-agent","execution":"not yet enabled in worker","created_at":created_at.isoformat(),"updated_at":updated_at.isoformat()}
