'use client';
import Link from 'next/link';
import { useEffect, useState } from 'react';

const modules = [
  ['Threat Intelligence','Global threat landscape, actors, campaigns and IOCs','threat-intelligence'],
  ['Attack Surface','External exposure, domains, IPs and applications','attack-surface'],
  ['Vulnerability','CVE intelligence, exposure and remediation priority','vulnerabilities'],
  ['Security Posture','Infrastructure, server, cloud and network posture','security-posture'],
  ['Web Security','Authorized web and API security assessment','web-security'],
  ['Hardening','Firewall, network device and system hardening','network-hardening'],
  ['Compliance','ISO 27001, PCI DSS, DORA, SOC 2 and NIST CSF','compliance'],
  ['Cyber AI','AI-assisted analysis, correlation and reporting','ai-security'],
];

export default function CommandCenter() {
  const [health, setHealth] = useState('Checking control plane…');
  const [summary, setSummary] = useState(null);
  const base = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8100';
  useEffect(() => { fetch(base+'/health').then(r=>r.json()).then(d=>setHealth('Control plane '+d.status+' · Database '+d.database)).catch(()=>setHealth('Control plane unavailable')); fetch(base+'/api/v1/demo/summary').then(r=>r.json()).then(setSummary).catch(()=>{}); }, []);
  return <main><aside><div className="brand"><span className="mark">C</span><div><b>CYBEROS</b><small>GLOBAL SECURITY PLATFORM</small></div></div><nav><Link className="active" href="/command-center">Command Center</Link><Link href="/organization">Organization</Link><Link href="/operations">Operations</Link>{modules.map(([label,,slug])=><Link key={slug} href={'/module/'+slug}>{label}</Link>)}<Link href="/module/reports">Reports</Link></nav><div className="tenant"><small>CONTROL PLANE</small><strong>CyberOS Global</strong><span>● M1.1 Platform Kernel</span></div></aside><section className="content"><header><div><span className="eyebrow">SECURITY OPERATING PLATFORM</span><h1>Command Center</h1><p>One control plane for global cyber intelligence, exposure, posture, compliance and authorized security assessment.</p></div><Link className="primary" href="/module/attack-surface">Launch Demo →</Link></header><div className="status"><span className="dot"></span>{health}<span className="sep">|</span> Execution policy: <b>ENFORCED</b><span className="sep">|</span> Tenant isolation: <b>ACTIVE</b></div><div className="metrics"><Metric n={summary?.assets ?? '—'} l="Tracked assets" s="Demo database"/><Metric n={summary?.open_findings ?? '—'} l="Open findings" s="Normalized"/><Metric n="8" l="Security domains" s="Available"/><Metric n={summary?.frameworks ?? '—'} l="Compliance families" s="Catalog"/></div><section className="panel"><div className="panelhead"><div><span className="eyebrow">CYBEROS MODULES</span><h2>Unified security workspace</h2></div><span className="pill">M1.1 PLATFORM KERNEL</span></div><div className="grid">{modules.map((m,i)=><Link className="module-card" href={'/module/'+m[2]} key={m[0]}><span className="num">0{i+1}</span><h3>{m[0]}</h3><p>{m[1]}</p><span className="arrow">Open module →</span></Link>)}</div></section><section className="lower"><div className="panel architecture"><span className="eyebrow">OPERATING MODEL</span><h2>Policy-controlled execution</h2><div className="flow"><b>Web UI</b><i>→</i><b>Control Plane</b><i>→</i><b>Policy Engine</b><i>→</i><b>Worker / Connector</b></div><p>Kali Linux and other security engines will run as isolated execution environments beneath CyberOS. The platform owns authorization, scope, evidence, audit, risk and reporting.</p></div><div className="panel score"><span className="eyebrow">PLATFORM KERNEL</span><div className="ring">M1</div><h2>Tenant-scoped</h2><p>Organization and audit context are now visible in the live control plane.</p></div></section><footer>CYBEROS M1.1 · Web-first security operating platform · Portal 3100 / API 8100 / PostgreSQL 5433</footer></section></main> }
function Metric({n,l,s}) { return <div className="metric"><strong>{n}</strong><span>{l}</span><small>{s}</small></div> }
