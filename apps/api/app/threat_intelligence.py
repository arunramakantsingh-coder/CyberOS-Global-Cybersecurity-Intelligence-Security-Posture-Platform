import os
from fastapi import APIRouter, HTTPException
import psycopg

router = APIRouter(prefix="/api/v1/threat-intelligence", tags=["Threat Intelligence"])
DB = os.environ.get("DATABASE_URL", "postgresql://cyberos:cyberos_dev_only@localhost:5433/cyberos")

GLOBAL_INTELLIGENCE = [
    {
        "id": "TI-APT-VPN-001",
        "type": "campaign",
        "title": "Credential-theft campaign targeting exposed remote access infrastructure",
        "severity": "critical",
        "sectors": ["manufacturing", "financial services", "technology"],
        "regions": ["APAC", "EMEA", "North America"],
        "technologies": ["vpn", "remote-access", "identity"],
        "ttps": ["T1133", "T1078", "T1556"],
        "related_cves": [],
        "description": "Synthetic intelligence object used to demonstrate tenant relevance correlation.",
    },
    {
        "id": "TI-CVE-REMOTE-001",
        "type": "vulnerability",
        "title": "Exploited remote-access appliance vulnerability",
        "severity": "high",
        "sectors": ["all"],
        "regions": ["all"],
        "technologies": ["vpn", "firewall", "gateway"],
        "ttps": ["T1190"],
        "related_cves": ["CVE-DEMO-2026-001"],
        "description": "Synthetic CVE intelligence object for correlation testing.",
    },
    {
        "id": "TI-RANSOMWARE-002",
        "type": "campaign",
        "title": "Ransomware campaign with lateral-movement and backup targeting",
        "severity": "high",
        "sectors": ["manufacturing", "healthcare", "government"],
        "regions": ["APAC", "EMEA"],
        "technologies": ["windows", "identity", "backup", "network"],
        "ttps": ["T1486", "T1021", "T1562"],
        "related_cves": [],
        "description": "Synthetic campaign object for tenant-risk modeling.",
    },
    {
        "id": "TI-IOC-EDGE-003",
        "type": "indicator",
        "title": "Suspicious edge infrastructure indicator",
        "severity": "medium",
        "sectors": ["all"],
        "regions": ["all"],
        "technologies": ["internet-facing", "gateway", "web"],
        "ttps": ["T1583", "T1595"],
        "related_cves": [],
        "description": "Synthetic indicator used to demonstrate asset-exposure correlation.",
    },
]


def fetch_rows(query, params=()):
    with psycopg.connect(DB, connect_timeout=3) as conn:
        with conn.cursor() as cur:
            cur.execute(query, params)
            return cur.fetchall()


def current_tenant():
    row = fetch_rows(
        "SELECT id,name,slug,industry,region,subscription_tier,status FROM tenants WHERE slug='cyberos-demo' LIMIT 1"
    )
    if not row:
        raise HTTPException(status_code=404, detail="Current tenant is not initialized")
    return row[0]


def normalize(value):
    return (value or "").strip().lower()


def tenant_intelligence_profile(tenant_id):
    tenant = fetch_rows(
        "SELECT id,name,slug,industry,region,subscription_tier,status FROM tenants WHERE id=%s",
        (tenant_id,),
    )[0]
    assets = fetch_rows(
        "SELECT id,name,asset_type,identifier,environment,criticality,exposure FROM assets WHERE tenant_id=%s ORDER BY name",
        (tenant_id,),
    )
    findings = fetch_rows(
        "SELECT id,title,severity,category,status,remediation FROM findings WHERE tenant_id=%s ORDER BY id",
        (tenant_id,),
    )
    technologies = set()
    exposures = set()
    asset_summaries = []
    for row in assets:
        asset_type = normalize(row[2])
        identifier = normalize(row[3])
        exposure = normalize(row[6])
        technologies.add(asset_type)
        if exposure:
            exposures.add(exposure)
        asset_summaries.append({
            "id": str(row[0]),
            "name": row[1],
            "type": row[2],
            "identifier": row[3],
            "environment": row[4],
            "criticality": row[5],
            "exposure": row[6],
        })
        if "vpn" in identifier or "vpn" in normalize(row[1]):
            technologies.add("vpn")
        if any(token in identifier or token in normalize(row[1]) for token in ("web", "api", "portal")):
            technologies.add("web")
        if any(token in identifier or token in normalize(row[1]) for token in ("firewall", "gateway", "edge")):
            technologies.add("gateway")
    return {
        "tenant": {
            "id": str(tenant[0]),
            "name": tenant[1],
            "slug": tenant[2],
            "industry": tenant[3],
            "region": tenant[4],
            "subscription_tier": tenant[5],
            "status": tenant[6],
        },
        "technologies": sorted(technologies),
        "exposures": sorted(exposures),
        "asset_count": len(assets),
        "open_finding_count": sum(1 for row in findings if normalize(row[4]) == "open"),
        "assets": asset_summaries,
        "findings": [
            {"id": str(r[0]), "title": r[1], "severity": r[2], "category": r[3], "status": r[4], "remediation": r[5]}
            for r in findings
        ],
    }


def correlate(profile, intel):
    tenant = profile["tenant"]
    industry = normalize(tenant["industry"])
    region = normalize(tenant["region"])
    technologies = {normalize(x) for x in profile["technologies"]}
    exposures = {normalize(x) for x in profile["exposures"]}
    findings_text = " ".join(normalize(f["title"]) + " " + normalize(f["category"]) for f in profile["findings"])

    reasons = []
    matched_assets = []
    score = 0

    if "all" in intel["sectors"] or industry in {normalize(x) for x in intel["sectors"]}:
        score += 25
        reasons.append("tenant sector matches intelligence targeting")
    if "all" in intel["regions"] or region in {normalize(x) for x in intel["regions"]}:
        score += 15
        reasons.append("tenant region matches intelligence geography")
    tech_matches = sorted(technologies.intersection({normalize(x) for x in intel["technologies"]}))
    if tech_matches:
        score += min(25, len(tech_matches) * 10)
        reasons.append("tenant technology footprint matches: " + ", ".join(tech_matches))
    if exposures and ({"internet-facing", "external", "public"} & exposures) and any(t in technologies for t in ("vpn", "gateway", "web")):
        score += 20
        reasons.append("internet-facing technology increases exposure relevance")
    if intel["related_cves"] and any(cve.lower() in findings_text for cve in intel["related_cves"]):
        score += 15
        reasons.append("tenant findings contain a related CVE")
    if intel["type"] == "campaign" and any(term in findings_text for term in ("ransomware", "remote", "identity", "credential")):
        score += 10
        reasons.append("existing tenant findings contain campaign-relevant signals")

    for asset in profile["assets"]:
        haystack = f"{normalize(asset['name'])} {normalize(asset['identifier'])} {normalize(asset['type'])}"
        if any(normalize(t) in haystack for t in intel["technologies"]):
            matched_assets.append({"id": asset["id"], "name": asset["name"], "reason": "technology match"})

    score = min(score, 100)
    if score >= 75:
        priority = "critical"
    elif score >= 50:
        priority = "high"
    elif score >= 25:
        priority = "medium"
    else:
        priority = "monitor"

    return {
        "intelligence_id": intel["id"],
        "title": intel["title"],
        "type": intel["type"],
        "severity": intel["severity"],
        "tenant_id": tenant["id"],
        "tenant_name": tenant["name"],
        "relevance_score": score,
        "priority": priority,
        "confidence": "high" if score >= 75 else "medium" if score >= 40 else "low",
        "reasons": reasons,
        "matched_assets": matched_assets,
        "ttps": intel["ttps"],
        "related_cves": intel["related_cves"],
        "source_scope": "global-intelligence",
        "tenant_scope": "tenant-derived correlation",
    }


@router.get("/profile")
def intelligence_profile():
    tenant = current_tenant()
    return tenant_intelligence_profile(tenant[0])


@router.get("/global")
def global_intelligence():
    return {"scope": "global", "objects": GLOBAL_INTELLIGENCE, "source_model": "STIX-compatible normalized intelligence"}


@router.get("/correlations")
def tenant_correlations():
    tenant = current_tenant()
    profile = tenant_intelligence_profile(tenant[0])
    correlations = [correlate(profile, intel) for intel in GLOBAL_INTELLIGENCE]
    correlations.sort(key=lambda item: item["relevance_score"], reverse=True)
    return {
        "scope": "tenant",
        "tenant": profile["tenant"],
        "model": "global intelligence -> tenant context -> relevance score -> actionable correlation",
        "correlations": correlations,
    }
