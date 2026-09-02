INSERT INTO assets (tenant_id,name,asset_type,identifier,environment,criticality,exposure)
SELECT id,'Demo Branch Router','router','demo-router-01','demo','high','internal'
FROM tenants WHERE slug='cyberos-demo' ON CONFLICT DO NOTHING;

INSERT INTO assets (tenant_id,name,asset_type,identifier,environment,criticality,exposure)
SELECT id,'Demo Access Switch','switch','demo-switch-01','demo','medium','internal'
FROM tenants WHERE slug='cyberos-demo' ON CONFLICT DO NOTHING;
