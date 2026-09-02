-- M2.2 additive migration. Safe to run against an existing CyberOS development database.
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

INSERT INTO tool_registry (name,version,capabilities,safety_profile)
VALUES ('cyberos-kali-connector','0.1.0','["authorized.network.discovery","authorized.web.assessment","authorized.vulnerability.assessment","evidence.collection"]','{"mode":"customer-controlled-agent","network_access":"only-through-approved-scope","shell_execution":"agent-side-only","requires_authorization":true}')
ON CONFLICT (name) DO NOTHING;

INSERT INTO tenant_modules (tenant_id,module_key,enabled)
SELECT id, module_key, true FROM tenants CROSS JOIN (VALUES
('command-center'),('threat-intelligence'),('attack-surface'),('vulnerabilities'),('security-posture'),('web-security'),('network-hardening'),('compliance'),('ai-security'),('reports')
) AS modules(module_key) WHERE slug='cyberos-demo' ON CONFLICT DO NOTHING;
