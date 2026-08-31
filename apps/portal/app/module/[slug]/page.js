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
  const [jobs, setJobs] = useState([]);
  const [message, setMessage] = useState('Loading live control-plane data…');
  const [jobState, setJobState] = useState('');
  const [running, setRunning] = useState(false);
  const [name, description] = catalog[slug] || ['Module','CyberOS module workspace'];
  const base = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8100';

  const load = () => Promise.all([
    fetch(base+'/api/v1/demo/summary').then(r=>r.json()),
    fetch(base+'/api/v1/demo/assets').then(r=>r.json()),
    fetch(base+'/api/v1/demo/findings').then(r=>r.json()),
    fetch(base+'/api/v1/demo/jobs').then(r=>r.json()),
  ]).then(([s,a,f,j]) => { setSummary(s); setAssets(a); setFindings(f); setJobs(j); setMessage('Live · Demo tenant · Policy engine enforced'); });

  useEffect(() => { load().catch(() => setMessage('Control plane unavailable')); }, []);

  const launchSafeDemo = async () => {
    setRunning(true); setJobState('Submitting through authorization and policy checks…');
    try {
      const response = await fetch(base+'/api/v1/demo/jobs', { method:'POST', headers:{'Content-Type':'application/json'}, body:JSON.stringify({ capability:'demo.asset_inventory', target:'demo-edge-fw', authorized:true }) });
      const data = await response.json();
      setJobState(data.state === 'queued' ? 'Authorized → queued → worker execution' : 'Blocked → '+(data.policy_reason || 'policy denied'));
      await load();
    } catch { setJobState('Control plane unavailable'); }
    finally { setRunning(false); }
  };

  const relevant = slug === 'vulnerabilities' ? findings : assets;
  return <main className="module-page"><aside><div className="brand"><span className="mark">C</span><div><b>CYBEROS</b><small>GLOBAL SECURITY PLATFORM</small></div></div><nav><Link href="/command-center">Command Center</Link><Link href="/organization">Organization</Link><Link href="/operations">Operations</Link>{Object.entries(catalog).map(([key,[label]])=><Link key={key} className={key===slug?'active':''} href={'/module/'+key}>{label}</Link>)}</nav><div className="tenant"><small>DEMO TENANT</small><strong>CyberOS Global</strong><span>● M1.1 Platform Kernel</span></div></aside><section className="content"><header><div><span className="eyebrow">CYBEROS MODULE</span><h1>{name}</h1><p>{description}</p></div><Link className="primary" href="/command-center">← Command Center</Link></header><div className="status"><span className="dot"></span>{message}</div><div className="metrics"><Metric n={summary?.assets ?? '—'} l="Tracked assets" s="Demo tenant"/><Metric n={summary?.open_findings ?? '—'} l="Open findings" s="Normalized"/><Metric n={summary?.jobs ?? '0'} l="Security jobs" s="Policy controlled"/><Metric n={summary?.frameworks ?? '—'} l="Frameworks" s="Catalog"/></div><section className="panel"><div className="panelhead"><div><span className="eyebrow">LIVE DATA FOUNDATION</span><h2>{slug === 'vulnerabilities' ? 'Findings workspace' : 'Asset intelligence workspace'}</h2></div><span className="pill">DATABASE-BACKED</span></div><div className="table">{relevant.length ? relevant.map(item => <div className="row" key={item.id}><div><strong>{item.name || item.title}</strong><small>{item.identifier || item.category || item.remediation}</small></div><span className={'severity '+(item.severity||item.criticality)}>{item.severity || item.criticality}</span><span>{item.type || item.status || item.exposure}</span></div>) : <div className="empty">No live records yet.</div>}</div></section><section className="lower"><div className="panel"><span className="eyebrow">M0.2 CONTROLLED EXECUTION</span><h2>Run a safe synthetic assessment</h2><p>This button exercises the real authorization → policy → queue → worker path against a synthetic demo asset. No network access, shell execution or external target is permitted.</p><button className="primary action" onClick={launchSafeDemo} disabled={running}>{running ? 'Processing…' : 'Run synthetic job →'}</button>{jobState && <div className="status">{jobState}</div>}</div><div className="panel"><span className="eyebrow">RECENT JOBS</span><h2>Execution ledger</h2><div className="table">{jobs.length ? jobs.slice(0,5).map(j=><div className="row compact" key={j.id}><div><strong>{j.capability}</strong><small>{j.target}</small></div><span className="severity">{j.state}</span><span>{new Date(j.created_at).toLocaleTimeString()}</span></div>) : <div className="empty">No jobs submitted.</div>}</div></div></section></section></main>
}
function Metric({n,l,s}) { return <div className="metric"><strong>{n}</strong><span>{l}</span><small>{s}</small></div> }
