'use client';
import Link from 'next/link';
import { useEffect, useState } from 'react';

export default function OperationsPage() {
  const [audit, setAudit] = useState([]);
  const [jobs, setJobs] = useState([]);
  const [status, setStatus] = useState('Loading operational ledger…');
  const base = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8100';

  const load = () => Promise.all([
    fetch(base + '/api/v1/audit?limit=25').then(r => r.json()),
    fetch(base + '/api/v1/demo/jobs').then(r => r.json()),
  ]).then(([a,j]) => { setAudit(a); setJobs(j); setStatus('Live · tenant-scoped operational data'); });

  useEffect(() => { load().catch(() => setStatus('Control plane unavailable')); }, []);

  return <main className="module-page"><aside><div className="brand"><span className="mark">C</span><div><b>CYBEROS</b><small>GLOBAL SECURITY PLATFORM</small></div></div><nav><Link href="/">Command Center</Link><Link href="/organization">Organization</Link><Link className="active" href="/operations">Operations</Link><Link href="/module/attack-surface">Attack Surface</Link><Link href="/module/vulnerabilities">Vulnerabilities</Link><Link href="/module/security-posture">Security Posture</Link><Link href="/module/compliance">Compliance</Link><Link href="/module/ai-security">Cyber AI</Link><Link href="/module/reports">Reports</Link></nav><div className="tenant"><small>CONTROL PLANE</small><strong>CyberOS Global</strong><span>● M1.1 Platform Kernel</span></div></aside><section className="content"><header><div><span className="eyebrow">M1.1 PLATFORM KERNEL</span><h1>Operations</h1><p>Auditable view of security jobs and control-plane decisions. Active execution remains policy-controlled.</p></div><Link className="primary" href="/">← Command Center</Link></header><div className="status"><span className="dot"></span>{status}</div><div className="metrics"><Metric n={jobs.length} l="Recent jobs" s="Tenant scoped"/><Metric n={audit.length} l="Audit events" s="Latest 25"/><Metric n="ENFORCED" l="Execution policy" s="Deny by default"/><Metric n="ACTIVE" l="Tenant boundary" s="M1 kernel"/></div><section className="panel"><div className="panelhead"><div><span className="eyebrow">JOB LEDGER</span><h2>Security execution requests</h2></div><span className="pill">POLICY CONTROLLED</span></div><div className="table">{jobs.length ? jobs.map(j=><div className="row" key={j.id}><div><strong>{j.capability}</strong><small>{j.target} · {j.policy_reason || 'authorized synthetic request'}</small></div><span className="severity">{j.state}</span><span>{new Date(j.created_at).toLocaleString()}</span></div>) : <div className="empty">No jobs recorded.</div>}</div></section><section className="panel"><div className="panelhead"><div><span className="eyebrow">AUDIT LEDGER</span><h2>Control-plane events</h2></div><span className="pill">TENANT SCOPED</span></div><div className="table">{audit.length ? audit.map(e=><div className="row" key={e.id}><div><strong>{e.event_type}</strong><small>{e.actor || 'system'} · {e.resource_type || 'platform'} · {e.metadata ? JSON.stringify(e.metadata) : ''}</small></div><span className={'severity '+(e.decision === 'deny' ? 'high' : '')}>{e.decision || 'recorded'}</span><span>{new Date(e.created_at).toLocaleString()}</span></div>) : <div className="empty">No audit events recorded.</div>}</div></section></section></main>
}
function Metric({n,l,s}) { return <div className="metric"><strong>{n}</strong><span>{l}</span><small>{s}</small></div> }
