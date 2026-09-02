import re
import json
import psycopg
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from .main import DB, MODULES

router = APIRouter(prefix="/api/v1/organizations", tags=["Organization Registration"])

class OrganizationRegistration(BaseModel):
    name: str = Field(min_length=2, max_length=160)
    industry: str = Field(min_length=2, max_length=100)
    region: str = Field(min_length=2, max_length=100)
    admin_name: str = Field(min_length=2, max_length=120)
    admin_email: str = Field(min_length=5, max_length=200)
    modules: list[str] = Field(default_factory=lambda: ["command-center", "threat-intelligence", "attack-surface", "vulnerabilities", "security-posture", "web-security", "network-hardening", "compliance", "ai-security", "reports"])


def slugify(value: str) -> str:
    slug = re.sub(r"[^a-z0-9]+", "-", value.lower()).strip("-")
    return slug[:70] or "organization"

@router.post("")
def register_organization(req: OrganizationRegistration):
    modules = [m for m in req.modules if m in {k for k, _ in MODULES}]
    if not modules:
        raise HTTPException(status_code=400, detail="Select at least one valid CyberOS module")
    email = req.admin_email.strip().lower()
    base_slug = slugify(req.name)
    with psycopg.connect(DB, connect_timeout=3) as conn:
        with conn.cursor() as cur:
            slug = base_slug
            for i in range(1, 100):
                cur.execute("SELECT 1 FROM tenants WHERE slug=%s", (slug,))
                if not cur.fetchone():
                    break
                slug = f"{base_slug}-{i+1}"
            else:
                raise HTTPException(status_code=409, detail="Unable to allocate a unique organization identifier")
            cur.execute("INSERT INTO tenants (name,slug,industry,region,subscription_tier,status) VALUES (%s,%s,%s,%s,'evaluation','active') RETURNING id,name,slug,industry,region,status,created_at", (req.name.strip(), slug, req.industry.strip(), req.region.strip()))
            tenant = cur.fetchone()
            tenant_id = tenant[0]
            cur.execute("INSERT INTO identities (tenant_id,email,display_name,role,status) VALUES (%s,%s,%s,'organization_admin','active') RETURNING id", (tenant_id, email, req.admin_name.strip()))
            actor_id = cur.fetchone()[0]
            for key, _ in MODULES:
                cur.execute("INSERT INTO tenant_modules (tenant_id,module_key,enabled,configuration) VALUES (%s,%s,%s,'{}'::jsonb)", (tenant_id, key, key in modules))
            cur.execute("INSERT INTO authorization_contexts (tenant_id,engagement_name,authorized_by,scope,exclusions,allowed_capabilities,status) VALUES (%s,'Organization onboarding - pending security scope',%s,%s,%s,%s,'draft') RETURNING id", (tenant_id, actor_id, json.dumps([]), json.dumps([]), json.dumps([])))
            auth_id = cur.fetchone()[0]
            cur.execute("INSERT INTO audit_events (tenant_id,actor_id,event_type,resource_type,decision,metadata) VALUES (%s,%s,'organization.registered','tenant','allow',%s)", (tenant_id, actor_id, json.dumps({"modules": modules, "subscription_tier": "evaluation"})))
            conn.commit()
    return {"organization": {"id": str(tenant[0]), "name": tenant[1], "slug": tenant[2], "industry": tenant[3], "region": tenant[4], "status": tenant[5]}, "admin": {"id": str(actor_id), "email": email, "name": req.admin_name.strip(), "role": "organization_admin"}, "authorization": {"id": str(auth_id), "status": "draft", "mode": "customer-controlled"}, "enabled_modules": modules, "next": "/onboarding"}

@router.get("/{tenant_id}")
def organization_by_id(tenant_id: str):
    with psycopg.connect(DB, connect_timeout=3) as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT id,name,slug,industry,region,subscription_tier,status,created_at FROM tenants WHERE id=%s", (tenant_id,))
            tenant = cur.fetchone()
            if not tenant:
                raise HTTPException(status_code=404, detail="Organization not found")
            cur.execute("SELECT id,email,display_name,role,status FROM identities WHERE tenant_id=%s ORDER BY created_at LIMIT 1", (tenant_id,))
            identity = cur.fetchone()
            cur.execute("SELECT module_key,enabled,configuration FROM tenant_modules WHERE tenant_id=%s ORDER BY module_key", (tenant_id,))
            modules = cur.fetchall()
            cur.execute("SELECT id,engagement_name,status,scope,exclusions,allowed_capabilities FROM authorization_contexts WHERE tenant_id=%s ORDER BY created_at DESC LIMIT 1", (tenant_id,))
            auth = cur.fetchone()
    return {"tenant": {"id": str(tenant[0]), "name": tenant[1], "slug": tenant[2], "industry": tenant[3], "region": tenant[4], "subscription_tier": tenant[5], "status": tenant[6], "created_at": tenant[7].isoformat()}, "identity": ({"id": str(identity[0]), "email": identity[1], "display_name": identity[2], "role": identity[3], "status": identity[4]} if identity else None), "modules": [{"key": r[0], "enabled": r[1], "configuration": r[2]} for r in modules], "authorization": ({"id": str(auth[0]), "engagement_name": auth[1], "status": auth[2], "scope": auth[3], "exclusions": auth[4], "allowed_capabilities": auth[5]} if auth else None)}
