CREATE EXTENSION IF NOT EXISTS pgcrypto;

CREATE TABLE IF NOT EXISTS tenants (id UUID PRIMARY KEY DEFAULT gen_random_uuid(), name TEXT NOT NULL, slug TEXT NOT NULL UNIQUE, industry TEXT, region TEXT, subscription_tier TEXT NOT NULL DEFAULT 'demo', status TEXT NOT NULL DEFAULT 'active', created_at TIMESTAMPTZ NOT NULL DEFAULT now());
CREATE TABLE IF NOT EXISTS identities (id UUID PRIMARY KEY DEFAULT gen_random_uuid(), tenant_id UUID NOT NULL REFERENCES tenants(id) ON DELETE CASCADE, email TEXT NOT NULL, display_name TEXT, role TEXT NOT NULL DEFAULT 'viewer', status TEXT NOT NULL DEFAULT 'active', created_at TIMESTAMPTZ NOT NULL DEFAULT now(), UNIQUE (tenant_id, email));
CREATE TABLE IF NOT EXISTS assets (id UUID PRIMARY KEY DEFAULT gen_random_uuid(), tenant_id UUID NOT NULL REFERENCES tenants(id) ON DELETE CASCADE, name TEXT NOT NULL, asset_type TEXT NOT NULL, identifier TEXT NOT NULL, environment TEXT NOT NULL DEFAULT 'demo', criticality TEXT NOT NULL DEFAULT 'medium', exposure TEXT NOT NULL DEFAULT 'unknown', metadata JSONB NOT NULL DEFAULT '{}'::jsonb, created_at TIMESTAMPTZ NOT NULL DEFAULT now(), UNIQUE (tenant_id, identifier));
CREATE TABLE IF NOT EXISTS authorization_contexts (id UUID PRIMARY KEY DEFAULT gen_random_uuid(), tenant_id UUID NOT NULL REFERENCES tenants(id) ON DELETE CASCADE, engagement_name TEXT NOT NULL, authorized_by UUID REFERENCES identities(id), scope JSONB NOT NULL DEFAULT '[]'::jsonb, exclusions JSONB NOT NULL DEFAULT '[]'::jsonb, allowed_capabilities JSONB NOT NULL DEFAULT '[]'::jsonb, starts_at TIMESTAMPTZ, ends_at TIMESTAMPTZ, status TEXT NOT NULL DEFAULT 'draft', created_at TIMESTAMPTZ NOT NULL DEFAULT now());
CREATE TABLE IF NOT EXISTS jobs (id UUID PRIMARY KEY DEFAULT gen_random_uuid(), tenant_id UUID NOT NULL REFERENCES tenants(id) ON DELETE CASCADE, requested_by UUID REFERENCES identities(id), authorization_id UUID REFERENCES authorization_contexts(id), capability TEXT NOT NULL, target TEXT NOT NULL, state TEXT NOT NULL DEFAULT 'requested', policy_reason TEXT, parameters JSONB NOT NULL DEFAULT '{}'::jsonb, created_at TIMESTAMPTZ NOT NULL DEFAULT now(), updated_at TIMESTAMPTZ NOT NULL DEFAULT now());
CREATE TABLE IF NOT EXISTS findings (id UUID PRIMARY KEY DEFAULT gen_random_uuid(), tenant_id UUID NOT NULL REFERENCES tenants(id) ON DELETE CASCADE, asset_id UUID REFERENCES assets(id) ON DELETE SET NULL, title TEXT NOT NULL, severity TEXT NOT NULL DEFAULT 'info', confidence TEXT NOT NULL DEFAULT 'medium', category TEXT, description TEXT, remediation TEXT, status TEXT NOT NULL DEFAULT 'open', first_seen TIMESTAMPTZ NOT NULL DEFAULT now(), last_seen TIMESTAMPTZ NOT NULL DEFAULT now());
CREATE TABLE IF NOT EXISTS evidence (id UUID PRIMARY KEY DEFAULT gen_random_uuid(), tenant_id UUID NOT NULL REFERENCES tenants(id) ON DELETE CASCADE, finding_id UUID REFERENCES findings(id) ON DELETE CASCADE, job_id UUID REFERENCES jobs(id) ON DELETE CASCADE, evidence_type TEXT NOT NULL, content_hash TEXT, provenance JSONB NOT NULL DEFAULT '{}'::jsonb, storage_ref TEXT, created_at TIMESTAMPTZ NOT NULL DEFAULT now());
CREATE TABLE IF NOT EXISTS audit_events (id UUID PRIMARY KEY DEFAULT gen_random_uuid(), tenant_id UUID REFERENCES tenants(id) ON DELETE CASCADE, actor_id UUID REFERENCES identities(id) ON DELETE SET NULL, event_type TEXT NOT NULL, resource_type TEXT, resource_id UUID, decision TEXT, metadata JSONB NOT NULL DEFAULT '{}'::jsonb, created_at TIMESTAMPTZ NOT NULL DEFAULT now());
CREATE TABLE IF NOT EXISTS tool_registry (id UUID PRIMARY KEY DEFAULT gen_random_uuid(), name TEXT NOT NULL UNIQUE, version TEXT, capabilities JSONB NOT NULL DEFAULT '[]'::jsonb, safety_profile JSONB NOT NULL DEFAULT '{}'::jsonb, enabled BOOLEAN NOT NULL DEFAULT true, created_at TIMESTAMPTZ NOT NULL DEFAULT now());
CREATE TABLE IF NOT EXISTS connectors (id UUID PRIMARY KEY DEFAULT gen_random_uuid(), tenant_id UUID NOT NULL REFERENCES tenants(id) ON DELETE CASCADE, name TEXT NOT NULL, status TEXT NOT NULL DEFAULT 'pending', last_seen TIMESTAMPTZ, capabilities JSONB NOT NULL DEFAULT '[]'::jsonb, created_at TIMESTAMPTZ NOT NULL DEFAULT now());
CREATE TABLE IF NOT EXISTS compliance_frameworks (id UUID PRIMARY KEY DEFAULT gen_random_uuid(), code TEXT NOT NULL, version TEXT NOT NULL, name TEXT NOT NULL, status TEXT NOT NULL DEFAULT 'catalog', UNIQUE(code, version));

ALTER TABLE connectors ADD COLUMN IF NOT EXISTS connector_type TEXT NOT NULL DEFAULT 'customer_agent';
ALTER TABLE connectors ADD COLUMN IF NOT EXISTS environment TEXT NOT NULL DEFAULT 'hybrid';
ALTER TABLE connectors ADD COLUMN IF NOT EXISTS endpoint TEXT;
ALTER TABLE connectors ADD COLUMN IF NOT EXISTS authorization_id UUID REFERENCES authorization_contexts(id) ON DELETE SET NULL;
ALTER TABLE connectors ADD COLUMN IF NOT EXISTS metadata JSONB NOT NULL DEFAULT '{}'::jsonb;

CREATE TABLE IF NOT EXISTS tenant_modules (
  tenant_id UUID NOT NULL REFERENCES tenants(id) ON DELETE CASCADE,
  module_key TEXT NOT NULL,
  enabled BOOLEAN NOT NULL DEFAULT true,
  configuration JSONB NOT NULL DEFAULT '{}'::jsonb,
  updated_at TIMESTAMPTZ NOT NULL DEFAULT now(),
  PRIMARY KEY (tenant_id, module_key)
);

INSERT INTO tenants (name, slug, industry, region, subscription_tier) VALUES ('CyberOS Global Demo','cyberos-demo','Technology','Global','demo') ON CONFLICT (slug) DO NOTHING;
INSERT INTO compliance_frameworks (code,version,name) VALUES ('ISO27001','2022','ISO/IEC 27001'),('PCI-DSS','4.0.1','PCI DSS'),('DORA','1.0','Digital Operational Resilience Act'),('SOC2','TSC','SOC 2 Trust Services Criteria'),('NIST-CSF','2.0','NIST Cybersecurity Framework') ON CONFLICT (code,version) DO NOTHING;
INSERT INTO tool_registry (name,version,capabilities,safety_profile) VALUES ('cyberos-safe-fixture','0.1.0','["demo.asset_inventory","demo.finding_fixture"]','{"mode":"synthetic-only","network_access":false}') ON CONFLICT (name) DO NOTHING;
INSERT INTO tool_registry (name,version,capabilities,safety_profile) VALUES ('cyberos-kali-connector','0.1.0','["authorized.network.discovery","authorized.web.assessment","authorized.vulnerability.assessment","evidence.collection"]','{"mode":"customer-controlled-agent","network_access":"only-through-approved-scope","shell_execution":"agent-side-only","requires_authorization":true}') ON CONFLICT (name) DO NOTHING;

INSERT INTO assets (tenant_id,name,asset_type,identifier,environment,criticality,exposure) SELECT id,'Demo Customer Portal','web_application','https://portal.demo.cyberos.local','demo','high','internet' FROM tenants WHERE slug='cyberos-demo' ON CONFLICT DO NOTHING;
INSERT INTO assets (tenant_id,name,asset_type,identifier,environment,criticality,exposure) SELECT id,'Demo API Gateway','api','api.demo.cyberos.local','demo','critical','internet' FROM tenants WHERE slug='cyberos-demo' ON CONFLICT DO NOTHING;
INSERT INTO assets (tenant_id,name,asset_type,identifier,environment,criticality,exposure) SELECT id,'Demo Linux Server','server','demo-linux-01','demo','high','internal' FROM tenants WHERE slug='cyberos-demo' ON CONFLICT DO NOTHING;
INSERT INTO assets (tenant_id,name,asset_type,identifier,environment,criticality,exposure) SELECT id,'Demo Edge Firewall','firewall','demo-edge-fw','demo','critical','internet' FROM tenants WHERE slug='cyberos-demo' ON CONFLICT DO NOTHING;
INSERT INTO findings (tenant_id,asset_id,title,severity,confidence,category,description,remediation) SELECT t.id,a.id,'Demo API missing recommended security headers','medium','high','web-security','Synthetic fixture finding for the CyberOS demo environment.','Apply the approved security-header baseline and verify through a controlled retest.' FROM tenants t JOIN assets a ON a.tenant_id=t.id AND a.identifier='api.demo.cyberos.local' WHERE t.slug='cyberos-demo' AND NOT EXISTS (SELECT 1 FROM findings f WHERE f.tenant_id=t.id AND f.title='Demo API missing recommended security headers');
INSERT INTO findings (tenant_id,asset_id,title,severity,confidence,category,description,remediation) SELECT t.id,a.id,'Demo firewall management exposure requires review','high','medium','network-security','Synthetic fixture finding for demonstrating posture workflow.','Restrict management access to approved administrative networks and enforce strong authentication.' FROM tenants t JOIN assets a ON a.tenant_id=t.id AND a.identifier='demo-edge-fw' WHERE t.slug='cyberos-demo' AND NOT EXISTS (SELECT 1 FROM findings f WHERE f.tenant_id=t.id AND f.title='Demo firewall management exposure requires review');

INSERT INTO tenant_modules (tenant_id,module_key,enabled)
SELECT id, module_key, true FROM tenants CROSS JOIN (VALUES
('command-center'),('threat-intelligence'),('attack-surface'),('vulnerabilities'),('security-posture'),('web-security'),('network-hardening'),('compliance'),('ai-security'),('reports')
) AS modules(module_key) WHERE slug='cyberos-demo' ON CONFLICT DO NOTHING;
