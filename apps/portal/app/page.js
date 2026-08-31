'use client';
import { useEffect, useState } from 'react';
import './styles.css';

const modules = [
  ['Threat Intelligence','Global threat landscape, actors, campaigns and IOCs'],
  ['Attack Surface','External exposure, domains, IPs and applications'],
  ['Vulnerability','CVE intelligence, exposure and remediation priority'],
  ['Security Posture','Infrastructure, server, cloud and network posture'],
  ['Web Security','Authorized web and API security assessment'],
  ['Hardening','Firewall, network device and system hardening'],
  ['Compliance','ISO 27001, PCI DSS, DORA, SOC 2 and NIST CSF'],
  ['Cyber AI','AI-assisted analysis, correlation and reporting'],
];

export default function Home() {
  const [health, setHealth] = useState('Checking control plane…');
  useEffect(() => { fetch((process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8100') + '/health').then(r=>r.json()).then(d=>setHealth('Control plane ' + d.status + ' · Database ' + d.database)).catch(()=>setHealth('Control plane unavailable')); }, []);
  return <main>
    <aside><div className="brand"><span className="mark">C</span><div><b>CYBEROS</b><small>GLOBAL SECURITY PLATFORM</small></div></div>
      <nav><a className="active">Command Center</a><a>Threat Intelligence</a><a>Attack Surface</a><a>Vulnerabilities</a><a>Security Posture</a><a>Web Security</a><a>Network & Hardening</a><a>Compliance</a><a>AI Security Analyst</a><a>Reports</a></nav>
      <div className="tenant"><small>DEMO TENANT</small><strong>CyberOS Global</strong><span>● M0 Foundation</span></div>
    </aside>
    <section className="content"><header><div><span className="eyebrow">SECURITY OPERATING PLATFORM</span><h1>Command Center</h1><p>One control plane for global cyber intelligence, exposure, posture, compliance and authorized security assessment.</p></div><button>Launch Demo →</button></header>
      <div className="status"><span className="dot"></span>{health}<span className="sep">|</span> Execution policy: <b>ENFORCED</b><span className="sep">|</span> Tenant isolation: <b>ACTIVE</b></div>
      <div className="metrics"><Metric n="100" l="Platform readiness" s="M0 baseline"/><Metric n="0" l="Critical findings" s="Demo dataset"/><Metric n="8" l="Security domains" s="Available"/><Metric n="5" l="Compliance families" s="Catalog planned"/></div>
      <section className="panel"><div className="panelhead"><div><span className="eyebrow">CYBEROS MODULES</span><h2>Unified security workspace</h2></div><span className="pill">FOUNDATION</span></div><div className="grid">{modules.map((m,i)=><article key={m[0]}><span className="num">0{i+1}</span><h3>{m[0]}</h3><p>{m[1]}</p><span className="arrow">Explore module →</span></article>)}</div></section>
      <section className="lower"><div className="panel architecture"><span className="eyebrow">OPERATING MODEL</span><h2>Policy-controlled execution</h2><div className="flow"><b>Web UI</b><i>→</i><b>Control Plane</b><i>→</i><b>Policy Engine</b><i>→</i><b>Worker / Connector</b></div><p>Kali Linux and other security engines will run as isolated execution environments beneath CyberOS. The platform owns authorization, scope, evidence, audit, risk and reporting.</p></div><div className="panel score"><span className="eyebrow">SECURITY POSTURE</span><div className="ring">—</div><h2>Not assessed</h2><p>Connect an authorized environment to begin.</p></div></section>
      <footer>CYBEROS M0 · Web-first security operating platform · Local development ports: Portal 3100 / API 8100 / PostgreSQL 5433</footer>
    </section>
  </main>
}
function Metric({n,l,s}) { return <div className="metric"><strong>{n}</strong><span>{l}</span><small>{s}</small></div> }
