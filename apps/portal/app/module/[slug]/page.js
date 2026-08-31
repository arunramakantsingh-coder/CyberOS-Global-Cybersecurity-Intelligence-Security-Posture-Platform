'use client';
import Link from 'next/link';
import { useParams } from 'next/navigation';
import { useEffect, useState } from 'react';

const catalog = {
  'threat-intelligence': ['Threat Intelligence','Global threat landscape, actors, campaigns, indicators and intelligence correlation.'],
  'attack-surface': ['Attack Surface','Authorized external exposure inventory for domains, IPs, applications and APIs.'],
  'vulnerabilities': ['Vulnerabilities','CVE intelligence, asset correlation, prioritization and remediation tracking.'],
  'security-posture': ['Security Posture','Unified infrastructure, server, cloud and network security posture.'],
  'web-security': ['Web Security','Controlled web and API security assessment workspace.'],
  'network-hardening': ['Network & Hardening','Firewall, network-device, server and system hardening posture.'],
  'compliance': ['Compliance','Control catalogs, evidence, gaps, remediation and readiness workflows.'],
  'ai-security': ['AI Security Analyst','Evidence-grounded AI analysis, correlation and reporting.'],
  'reports': ['Reports','Executive, technical, compliance and remediation reporting.'],
};

export default function ModulePage() {
  const { slug } = useParams();
  const [summary, setSummary] = useState(null);
  const [assets, setAssets] = useState([]);
  const [findings, setFindings] = useState([]);
  const [message, setMessage] = useState('Loading live control-plane data…');
  const [name, description] = catalog[slug] || ['Module','CyberOS module workspace'];
  useEffect(() => {
    const base = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8100';
    Promise.all([fetch(base+'/api/v1/demo/summary').then(r=>r.json()), fetch(base+'/api/v1/demo/assets').then(r=>r.json()), fetch(base+'/api/v1/demo/findings').then(r=>r.json())])
      .then(([s,a,f]) => { setSummary(s); setAssets(a); setFindings(f); setMessage('Live · Demo tenant · Policy engine enforced'); })
      .catch(() => setMessage('Control plane unavailable'));
  }, []);
  const relevant = slug === 'vulnerabilities' ? findings : assets;
  return <main className="module-page"><aside><div className="brand"><span className="mark">C</span><div><b>CYBEROS</b><small>GLOBAL SECURITY PLATFORM</small></div></div><nav><Link href="/">Command Center</Link>{Object.entries(catalog).map(([key,[label]])=><Link key={key} className={key===slug?'active':''} href={'/module/'+key}>{label}</Link>)}</nav><div className="tenant"><small>DEMO TENANT</small><strong>CyberOS Global</strong><span>● M0.1 Foundation</span></div></aside><section className="content"><header><div><span className="eyebrow">CYBEROS MODULE</span><h1>{name}</h1><p>{description}</p></div><Link className="primary" href="/">← Command Center</Link></header><div className="status"><span className="dot"></span>{message}</div><div className="metrics"><Metric n={summary?.assets ?? '—'} l="Tracked assets" s="Demo tenant"/><Metric n={summary?.open_findings ?? '—'} l="Open findings" s="Normalized"/><Metric n={summary?.online_connectors ?? '0'} l="Connectors online" s="Customer environments"/><Metric n={summary?.frameworks ?? '—'} l="Frameworks" s="Catalog"/></div><section className="panel"><div className="panelhead"><div><span className="eyebrow">LIVE DATA FOUNDATION</span><h2>{slug === 'vulnerabilities' ? 'Findings workspace' : 'Asset intelligence workspace'}</h2></div><span className="pill">READ-ONLY DEMO</span></div><div className="table">{relevant.length ? relevant.map(item => <div className="row" key={item.id}><div><strong>{item.name || item.title}</strong><small>{item.identifier || item.category || item.remediation}</small></div><span className={'severity '+(item.severity||item.criticality)}>{item.severity || item.criticality}</span><span>{item.type || item.status || item.exposure}</span></div>) : <div className="empty">No live records yet.</div>}</div></section><section className="lower"><div className="panel"><span className="eyebrow">NEXT CAPABILITY</span><h2>Policy-controlled execution</h2><p>Interactive execution controls will appear only after identity, authorization context, scope and policy checks are implemented. Demo mode remains synthetic-only.</p></div><div className="panel"><span className="eyebrow">PLATFORM STATE</span><h2>M0.1</h2><p>Database-backed tenant, asset, finding and compliance foundation is online.</p></div></section></section></main>
}
function Metric({n,l,s}) { return <div className="metric"><strong>{n}</strong><span>{l}</span><small>{s}</small></div> }
