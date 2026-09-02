import os
import re
import json
from datetime import datetime, timezone

import psycopg
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

router = APIRouter(prefix="/api/v1/customer", tags=["Customer Workspace"])
DB = os.environ.get("DATABASE_URL", "postgresql://cyberos:cyberos_dev_only@localhost:5433/cyberos")

MODULE_KEYS = [
    "command-center", "threat-intelligence", "attack-surface", "vulnerabilities",
    "security-posture", "web-security", "network-hardening", "compliance", "ai-security", "reports"
]
ALLOWED_ASSET_TYPES = {"firewall", "router", "switch", "server", "web_application", "api"}
ALLOWED_CAPABILITIES = {
    "authorized.network.discovery", "authorized.web.assessment",
    "authorized.vulnerability.assessment", "evidence.collection"
}

class RegistrationRequest(BaseModel):
    company_name: str = Field(min_length=2, max_length=160)
    admin_name: str = Field(min_length=2, max_length=120)
    admin_email: str = Field(min_length=5, max_length=240)
    industry: str = Field(min_length=2, max_length=100)
    region: str = Field(min_length=2, max_length=80)
    environments: list[str] = Field(default_factory=list)
    modules: list[str] = Field(default_factory=list)

class AssetRequest(BaseModel):
    tenant_id: str
    name: str = Field(min_length=2, max_length=160)
    asset_type: str
    identifier: str = Field(min_length=1, max_length=500)
    environment: str = "on-premise"
    criticality: str = "medium"
    exposure: str = "internal"

class ConnectorRequest(BaseModel):
    tenant_id: str
    name: str = Field(min_length=2, max_length=160)
    connector_type: str = "kali_agent"
    environment: str = "hybrid"
    endpoint: str | None = Field(default=None, max_length=500)
    capabilities: list[str] = Field(default_factory=list)

class ScanRequest(BaseModel):
    tenant_id: str
    asset_id: str
    profile: str
    authorized: bool = False


def conn():
    return psycopg.connect(DB, connect_timeout=3)


def slugify(value: str) -> str:
    slug = re.sub(r"[^a-z0-9]+", "-", value.lower()).strip("-")
    return slug[:70] or "customer"


def ensure_tenant(tenant_id: str):
    with conn() as db:
        with db.cursor() as cur:
            cur.execute("SELECT id,name,slug,industry,region,subscription_tier,status FROM tenants WHERE id=%s", (tenant_id,))
            row = cur.fetchone()
    if not row:
        raise HTTPException(status_code=404, detail="Tenant not found")
    return row


@router.post("/register")
def register(req: RegistrationRequest):
    requested = [m for m in req.modules if m in MODULE_KEYS]
    enabled = requested or MODULE_KEYS
    base_slug = slugify(req.company_name)
    with conn() as db:
        with db.cursor() as cur:
            slug = base_slug
            suffix = 2
            while True:
                cur.execute("SELECT 1 FROM tenants WHERE slug=%s", (slug,))
                if not cur.fetchone():
                    break
                slug = f"{base_slug}-{suffix}"
                suffix += 1
            cur.execute(
                "INSERT INTO tenants (name,slug,industry,region,subscription_tier,status) VALUES (%s,%s,%s,%s,'trial','active') RETURNING id,created_at",
                (req.company_name, slug, req.industry, req.region),
            )
            tenant_id, created_at = cur.fetchone()
            cur.execute(
                "INSERT INTO identities (tenant_id,email,display_name,role) VALUES (%s,%s,%s,'ciso_admin') RETURNING id",
                (tenant_id, req.admin_email.lower(), req.admin_name),
            )
            identity_id = cur.fetchone()[0]
            scope = {"environments": req.environments, "assets": [], "network_access": "customer-side-only"}
            capabilities = sorted(ALLOWED_CAPABILITIES)
            cur.execute(
                "INSERT INTO authorization_contexts (tenant_id,engagement_name,authorized_by,scope,exclusions,allowed_capabilities,starts_at,ends_at,status) VALUES (%s,%s,%s,%s,'[]',%s,now(),now()+interval '30 days','active') RETURNING id",
                (tenant_id, "Customer security workspace initial authorization", identity_id, json.dumps(scope), json.dumps(capabilities)),
            )
            auth_id = cur.fetchone()[0]
            for key in enabled:
                cur.execute("INSERT INTO tenant_modules (tenant_id,module_key,enabled,configuration) VALUES (%s,%s,true,%s) ON CONFLICT DO NOTHING", (tenant_id, key, json.dumps({"source": "customer-registration"})))
            cur.execute("INSERT INTO audit_events (tenant_id,actor_id,event_type,resource_type,decision,metadata) VALUES (%s,%s,'tenant.registered','tenant','allow',%s)", (tenant_id, identity_id, json.dumps({"company": req.company_name, "modules": enabled, "environments": req.environments})))
            db.commit()
    return {"tenant": {"id": str(tenant_id), "name": req.company_name, "slug": slug, "industry": req.industry, "region": req.region, "tier": "trial"}, "identity": {"id": str(identity_id), "name": req.admin_name, "email": req.admin_email.lower(), "role": "ciso_admin"}, "authorization": {"id": str(auth_id), "status": "active", "mode": "customer-scoped"}, "modules": enabled, "created_at": created_at.isoformat()}


@router.get("/workspace/{tenant_id}")
def workspace(tenant_id: str):
    tenant = ensure_tenant(tenant_id)
    with conn() as db:
        with db.cursor() as cur:
            cur.execute("SELECT id,email,display_name,role,status FROM identities WHERE tenant_id=%s ORDER BY created_at LIMIT 1", (tenant_id,))
            identity = cur.fetchone()
            cur.execute("SELECT id,engagement_name,status,scope,allowed_capabilities FROM authorization_contexts WHERE tenant_id=%s ORDER BY created_at DESC LIMIT 1", (tenant_id,))
            auth = cur.fetchone()
            cur.execute("SELECT module_key,enabled,configuration FROM tenant_modules WHERE tenant_id=%s ORDER BY module_key", (tenant_id,))
            modules = cur.fetchall()
            cur.execute("SELECT id,name,asset_type,identifier,environment,criticality,exposure,metadata FROM assets WHERE tenant_id=%s ORDER BY name", (tenant_id,))
            assets = cur.fetchall()
            cur.execute("SELECT id,name,status,connector_type,environment,endpoint,last_seen,capabilities FROM connectors WHERE tenant_id=%s ORDER BY name", (tenant_id,))
            connectors = cur.fetchall()
    return {
        "tenant": {"id": str(tenant[0]), "name": tenant[1], "slug": tenant[2], "industry": tenant[3], "region": tenant[4], "tier": tenant[5], "status": tenant[6]},
        "identity": {"id": str(identity[0]), "email": identity[1], "display_name": identity[2], "role": identity[3], "status": identity[4]} if identity else None,
        "authorization": {"id": str(auth[0]), "engagement": auth[1], "status": auth[2], "scope": auth[3], "allowed_capabilities": auth[4]} if auth else None,
        "modules": [{"key": r[0], "enabled": r[1], "configuration": r[2]} for r in modules],
        "assets": [{"id": str(r[0]), "name": r[1], "type": r[2], "identifier": r[3], "environment": r[4], "criticality": r[5], "exposure": r[6], "metadata": r[7]} for r in assets],
        "connectors": [{"id": str(r[0]), "name": r[1], "status": r[2], "type": r[3], "environment": r[4], "endpoint": r[5], "last_seen": r[6].isoformat() if r[6] else None, "capabilities": r[7]} for r in connectors],
    }


@router.post("/assets")
def add_asset(req: AssetRequest):
    ensure_tenant(req.tenant_id)
    if req.asset_type not in ALLOWED_ASSET_TYPES:
        raise HTTPException(status_code=400, detail="Unsupported asset type")
    with conn() as db:
        with db.cursor() as cur:
            cur.execute("INSERT INTO assets (tenant_id,name,asset_type,identifier,environment,criticality,exposure,metadata) VALUES (%s,%s,%s,%s,%s,%s,%s,%s) ON CONFLICT (tenant_id,identifier) DO UPDATE SET name=EXCLUDED.name,environment=EXCLUDED.environment,criticality=EXCLUDED.criticality,exposure=EXCLUDED.exposure RETURNING id", (req.tenant_id, req.name, req.asset_type, req.identifier, req.environment, req.criticality, req.exposure, json.dumps({"source": "customer-mapped"})))
            asset_id = cur.fetchone()[0]
            db.commit()
    return {"id": str(asset_id), "tenant_id": req.tenant_id, "status": "mapped", "execution": "not started"}


@router.post("/connectors")
def add_connector(req: ConnectorRequest):
    ensure_tenant(req.tenant_id)
    unknown = sorted(set(req.capabilities) - ALLOWED_CAPABILITIES)
    if unknown:
        raise HTTPException(status_code=400, detail=f"Unsupported capabilities: {', '.join(unknown)}")
    with conn() as db:
        with db.cursor() as cur:
            cur.execute("SELECT id FROM authorization_contexts WHERE tenant_id=%s AND status='active' ORDER BY created_at DESC LIMIT 1", (req.tenant_id,))
            auth = cur.fetchone()
            if not auth:
                raise HTTPException(status_code=403, detail="No active authorization context")
            cur.execute("INSERT INTO connectors (tenant_id,name,status,connector_type,environment,endpoint,capabilities,authorization_id,metadata) VALUES (%s,%s,'pending',%s,%s,%s,%s,%s,%s) RETURNING id", (req.tenant_id, req.name, req.connector_type, req.environment, req.endpoint, json.dumps(req.capabilities), auth[0], json.dumps({"execution_boundary": "customer-side", "agent": "Kali-compatible"})))
            connector_id = cur.fetchone()[0]
            db.commit()
    return {"id": str(connector_id), "status": "pending", "authorization_id": str(auth[0]), "next": "install customer-side agent, validate heartbeat, then approve scoped execution"}


@router.post("/scan/plan")
def scan_plan(req: ScanRequest):
    if not req.authorized:
        raise HTTPException(status_code=403, detail="Explicit authorization acknowledgement is required")
    ensure_tenant(req.tenant_id)
    with conn() as db:
        with db.cursor() as cur:
            cur.execute("SELECT id,name,asset_type,identifier,environment,criticality,exposure FROM assets WHERE id=%s AND tenant_id=%s", (req.asset_id, req.tenant_id))
            asset = cur.fetchone()
            if not asset:
                raise HTTPException(status_code=404, detail="Asset is outside this tenant")
            cur.execute("SELECT id FROM connectors WHERE tenant_id=%s AND status IN ('online','approved') ORDER BY last_seen DESC NULLS LAST LIMIT 1", (req.tenant_id,))
            connector = cur.fetchone()
            cur.execute("SELECT id FROM authorization_contexts WHERE tenant_id=%s AND status='active' ORDER BY created_at DESC LIMIT 1", (req.tenant_id,))
            auth = cur.fetchone()
    return {"status": "planned" if connector else "blocked", "tenant_id": req.tenant_id, "asset": {"id": str(asset[0]), "name": asset[1], "type": asset[2], "identifier": asset[3], "environment": asset[4], "criticality": asset[5], "exposure": asset[6]}, "connector_id": str(connector[0]) if connector else None, "authorization_id": str(auth[0]) if auth else None, "execution": "customer-agent-only", "message": "Execution remains gated until an approved/online customer-side connector is present." if not connector else "Authorized scan plan ready for customer-side agent execution."}
