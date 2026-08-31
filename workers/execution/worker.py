import json
import os
import time
from datetime import datetime, timezone
import psycopg

DB = os.environ.get("DATABASE_URL", "postgresql://cyberos:cyberos_dev_only@localhost:5433/cyberos")
SAFE_CAPABILITIES = {"demo.asset_inventory", "demo.finding_fixture"}

print("CyberOS execution worker: online")
print("Mode: policy-controlled / synthetic-only")


def run_once():
    with psycopg.connect(DB, connect_timeout=3) as conn:
        with conn.cursor() as cur:
            cur.execute("""
                SELECT id, tenant_id, capability, target
                FROM jobs
                WHERE state='queued'
                  AND capability = ANY(%s)
                ORDER BY created_at
                FOR UPDATE SKIP LOCKED
                LIMIT 1
            """, (list(SAFE_CAPABILITIES),))
            row = cur.fetchone()
            if not row:
                return False
            job_id, tenant_id, capability, target = row
            cur.execute("UPDATE jobs SET state='running', updated_at=now() WHERE id=%s", (job_id,))
            cur.execute("""
                INSERT INTO audit_events (tenant_id,event_type,resource_type,resource_id,decision,metadata)
                VALUES (%s,'job.started','job',%s,'allow',%s)
            """, (tenant_id, job_id, json.dumps({"capability": capability, "target": target, "mode": "synthetic-only"})))
            conn.commit()

    # This worker intentionally performs no network access and no shell execution.
    time.sleep(0.5)

    with psycopg.connect(DB, connect_timeout=3) as conn:
        with conn.cursor() as cur:
            cur.execute("UPDATE jobs SET state='completed', updated_at=now() WHERE id=%s AND state='running'", (job_id,))
            cur.execute("""
                INSERT INTO evidence (tenant_id,job_id,evidence_type,provenance,storage_ref)
                VALUES (%s,%s,'synthetic_fixture',%s,'inline://cyberos-m0.2')
            """, (tenant_id, job_id, json.dumps({"generated_at": datetime.now(timezone.utc).isoformat(), "executor": "cyberos-safe-fixture", "network_access": False})))
            cur.execute("""
                INSERT INTO audit_events (tenant_id,event_type,resource_type,resource_id,decision,metadata)
                VALUES (%s,'job.completed','job',%s,'allow',%s)
            """, (tenant_id, job_id, json.dumps({"capability": capability, "target": target, "mode": "synthetic-only"})))
            conn.commit()
    print(f"CyberOS worker completed synthetic job {job_id}")
    return True


while True:
    try:
        run_once()
    except Exception as exc:
        print(f"CyberOS worker loop error: {exc}")
    time.sleep(2)
