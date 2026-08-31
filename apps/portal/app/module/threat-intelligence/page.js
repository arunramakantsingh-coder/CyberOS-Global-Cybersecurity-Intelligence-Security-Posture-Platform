'use client';

import Link from 'next/link';
import { useEffect, useState } from 'react';

const nav = [
  ['Command Center','/command-center'],
  ['Organization','/organization'],
  ['Operations','/operations'],
  ['Threat Intelligence','/module/threat-intelligence'],
  ['Attack Surface','/module/attack-surface'],
  ['Vulnerabilities','/module/vulnerabilities'],
  ['Security Posture','/module/security-posture'],
  ['Web Security','/module/web-security'],
  ['Network & Hardening','/module/network-hardening'],
  ['Compliance','/module/compliance'],
  ['AI Security','/module/ai-security'],
  ['Reports','/module/reports'],
];

const bars = [44,58,51,72,64,79,68,86,74,91,82,88];
const regions = [
  ['North America','Credential abuse','High','84'],
  ['Europe','Ransomware / APT','Critical','71'],
  ['APAC','Internet-edge exploitation','High','63'],
  ['Middle East','Targeted campaigns','Medium','42'],
  ['South America','Fraud infrastructure','Medium','31'],
];
const actors = [
  ['Actor cluster A','Energy / manufacturing','17 campaigns','High'],
  ['Actor cluster B','Financial services','11 campaigns','Critical'],
  ['Actor cluster C','SaaS / identity','8 campaigns','High'],
];

export default function ThreatIntelligence() {
  const [health, setHealth] = useState('Checking control plane…');
  const [summary, setSummary] = useState(null);
  const base = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8100';

  useEffect(() => {
    fetch(base + '/health')
      .then(r => r.json())
      .then(d => setHealth('Control plane ' + d.status + ' · Database ' + d.database))
      .catch(() => setHealth('Control plane unavailable'));
    fetch(base + '/api/v1/demo/summary')
      .then(r => r.json())
      .then(setSummary)
      .catch(() => {});
  }, [base]);

  return (
    <main className="ti-page">
      <style>{css}</style>
      <aside>
        <div className="brand"><span className="mark">C</span><div><b>CYBEROS</b><small>GLOBAL SECURITY PLATFORM</small></div></div>
        <nav>{nav.map(([label, href]) => <Link key={href} className={href.includes('threat-intelligence') ? 'active' : ''} href={href}>{label}</Link>)}</nav>
        <div className="tenant"><small>DEMO TENANT</small><strong>CyberOS Global</strong><span>● M2 PRODUCT EXPERIENCE</span></div>
      </aside>

      <section className="content">
        <header>
          <div>
            <span className="eyebrow">GLOBAL THREAT INTELLIGENCE</span>
            <h1>Threat Intelligence Center</h1>
            <p>Turn global threat signals into tenant-relevant intelligence by correlating actors, campaigns, malware, IOCs, vulnerabilities, exposure and geopolitical risk.</p>
          </div>
          <Link className="primary" href="/command-center">← Command Center</Link>
        </header>

        <div className="status"><span className="dot"></span>{health}<span className="sep">|</span>Feeds: <b>DEMO CONNECTED</b><span className="sep">|</span>Tenant isolation: <b>ACTIVE</b></div>

        <div className="metrics">
          <Metric n="312" label="Threat actors" sub="Tracked clusters" />
          <Metric n="84" label="Active campaigns" sub="Correlated" />
          <Metric n="1,842" label="IOCs" sub="Normalized" />
          <Metric n="27" label="High-risk regions" sub="Current signal" />
          <Metric n={summary?.open_findings ?? '—'} label="Linked findings" sub="Demo tenant" />
        </div>

        <section className="panel">
          <div className="panelhead"><div><span className="eyebrow">GLOBAL THREAT PULSE</span><h2>Threat activity and regional pressure</h2></div><span className="pill">LIVE ANALYTICS</span></div>
          <div className="analytics">
            <div className="card">
              <h3>Threat activity · 12 periods</h3>
              <div className="chart">{bars.map((v, i) => <span key={i} style={{height: v + '%'}} />)}</div>
              <div className="axis"><span>12 periods ago</span><b>Current pressure ↑</b><span>Now</span></div>
            </div>
            <div className="card">
              <h3>Global intelligence map</h3>
              <div className="map">
                <svg viewBox="0 0 600 280" aria-label="Global threat activity map">
                  <path d="M34 98l61-43 91 18 35 43-47 48-78-11-62-29zm222-48l71-34 99 17 43 56-50 43-92-5-67-39zm209 50l68-24 44 20 13 47-48 31-69-15-32-35zM155 196l75-22 68 30-34 39-89-4z" fill="none" stroke="currentColor" strokeOpacity=".2" strokeWidth="2"/>
                  {[['115','88','7'],['178','111','5'],['292','74','8'],['365','91','5'],['431','127','7'],['498','108','5'],['528','162','8'],['235','213','5'],['86','145','4']].map(([cx,cy,r],i)=><circle key={i} cx={cx} cy={cy} r={r} fill="currentColor" opacity={i%3===0?.95:.55}/>) }
                </svg>
              </div>
              <div className="legend"><span>● Threat activity</span><span>● Campaign concentration</span><span>● Risk overlap</span></div>
            </div>
          </div>
        </section>

        <section className="split">
          <div className="panel">
            <div className="panelhead"><div><span className="eyebrow">REGIONAL INTELLIGENCE</span><h2>Where pressure is building</h2></div><span className="pill">5 REGIONS</span></div>
            <div className="region-list">{regions.map(r => <div className="region" key={r[0]}><div><strong>{r[0]}</strong><small>{r[1]}</small></div><div className="region-bar"><i style={{width:r[3]+'%'}} /></div><b className={r[2].toLowerCase()}>{r[2]}</b></div>)}</div>
          </div>
          <div className="panel">
            <div className="panelhead"><div><span className="eyebrow">ACTOR INTELLIGENCE</span><h2>Priority clusters</h2></div><span className="pill">3 PRIORITIES</span></div>
            <div className="actor-list">{actors.map(a => <div className="actor" key={a[0]}><div><strong>{a[0]}</strong><small>{a[1]} · {a[2]}</small></div><b className={a[3].toLowerCase()}>{a[3]}</b></div>)}</div>
          </div>
        </section>

        <section className="panel">
          <div className="panelhead"><div><span className="eyebrow">INTELLIGENCE CORRELATION</span><h2>Signals that matter to the tenant</h2></div><span className="pill">EVIDENCE LINKED</span></div>
          <div className="table">
            <div className="row head"><span>Signal</span><span>Context</span><span>Priority</span><span>Action</span></div>
            {[
              ['APT activity','Eastern Europe / Energy','CRITICAL','Actor + campaign correlated'],
              ['Ransomware','Global / Manufacturing','HIGH','18 indicators linked'],
              ['Cloud credential abuse','North America / SaaS','HIGH','Identity telemetry'],
              ['Exploit campaign','APAC / Internet edge','HIGH','KEV + exposure overlap'],
            ].map((r,i)=><div className="row" key={i}><strong>{r[0]}</strong><span>{r[1]}</span><b className={r[2].toLowerCase()}>{r[2]}</b><small>{r[3]}</small></div>)}
          </div>
        </section>

        <section className="lower">
          <div className="panel"><span className="eyebrow">INTELLIGENCE PIPELINE</span><h2>From global signal to security decision</h2><div className="flow"><b>STIX / TAXII</b><i>→</i><b>Normalize</b><i>→</i><b>Correlate</b><i>→</i><b>Score</b><i>→</i><b>Tenant alert</b></div><p>Threat intelligence stays evidence-backed and tenant-scoped. Correlations can feed exposure, vulnerability, posture, operations, AI and reporting without bypassing authorization.</p></div>
          <div className="panel"><span className="eyebrow">CONTROLLED ACTION</span><h2>Analyst workflow</h2><div className="action-grid"><Link href="/module/vulnerabilities">Review linked vulnerabilities →</Link><Link href="/module/attack-surface">Check exposed assets →</Link><Link href="/module/ai-security">Ask Cyber AI to correlate →</Link><Link href="/module/reports">Generate intelligence brief →</Link></div></div>
        </section>

        <footer>CYBEROS M2 · Threat Intelligence workspace · Portal 3100 / API 8100 / PostgreSQL 5433</footer>
      </section>
    </main>
  );
}

function Metric({n,label,sub}) { return <div className="metric"><strong>{n}</strong><span>{label}</span><small>{sub}</small></div>; }

const css = `
.ti-page{min-height:100vh;background:#071016;color:#dce8ed;font-family:Inter,-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,sans-serif;display:flex;overflow-x:hidden}.ti-page *{box-sizing:border-box}.ti-page a{text-decoration:none;color:inherit}.ti-page aside{position:fixed;left:0;top:0;bottom:0;width:238px;background:#08141a;border-right:1px solid #193039;padding:20px 14px;display:flex;flex-direction:column;z-index:10}.ti-page .brand{display:flex;align-items:center;gap:10px;padding:4px 8px 22px}.ti-page .mark{width:34px;height:34px;border:2px solid #55d6c2;border-radius:9px;display:grid;place-items:center;color:#55d6c2;font-weight:800}.ti-page .brand b{display:block;font-size:13px;letter-spacing:2.5px}.ti-page .brand small{display:block;font-size:7px;color:#68828a;letter-spacing:1px}.ti-page nav{display:grid;gap:4px;overflow:auto}.ti-page nav a{padding:9px 10px;border-radius:6px;color:#78939b;font-size:11px;font-weight:500}.ti-page nav a:hover,.ti-page nav a.active{background:#10242b;color:#62dfca}.ti-page .tenant{margin-top:auto;border-top:1px solid #193039;padding:15px 9px 3px;display:grid;gap:5px}.ti-page .tenant small{font-size:8px;color:#4f727b;letter-spacing:1.5px}.ti-page .tenant strong{font-size:11px}.ti-page .tenant span{font-size:9px;color:#55b9ad}.ti-page .content{margin-left:238px;width:calc(100% - 238px);padding:38px 42px 28px;max-width:1700px}.ti-page header{display:flex;justify-content:space-between;gap:30px;align-items:flex-start;padding-bottom:24px;border-bottom:1px solid #193039}.ti-page .eyebrow{font-size:9px;letter-spacing:1.8px;color:#5d8c95;font-weight:700}.ti-page h1{font-size:32px;line-height:1.1;margin:9px 0}.ti-page header p{max-width:800px;color:#78939b;font-size:12px;line-height:1.7;margin:0}.ti-page .primary{background:#62dfca;color:#071016;border:0;border-radius:7px;padding:10px 15px;font-size:10px;font-weight:700;white-space:nowrap}.ti-page .status{margin:14px 0;padding:10px 12px;border:1px solid #17323a;background:#0b1a20;border-radius:7px;color:#68858c;font-size:9px}.ti-page .dot{display:inline-block;width:6px;height:6px;border-radius:50%;background:#55d6c2;margin-right:7px}.ti-page .sep{margin:0 9px;color:#29434a}.ti-page .metrics{display:grid;grid-template-columns:repeat(5,1fr);gap:9px;margin:14px 0}.ti-page .metric{border:1px solid #19323a;background:#09171d;border-radius:8px;padding:15px;min-width:0}.ti-page .metric strong{display:block;font-size:23px}.ti-page .metric span{display:block;color:#829da4;font-size:9px;margin-top:5px}.ti-page .metric small{display:block;color:#526f77;font-size:8px;margin-top:3px}.ti-page .panel{border:1px solid #19323a;background:#09171d;border-radius:9px;padding:18px;margin-top:14px;min-width:0}.ti-page .panelhead{display:flex;justify-content:space-between;align-items:flex-start;gap:15px}.ti-page h2{font-size:16px;margin:6px 0 0}.ti-page .pill{border:1px solid #285159;color:#6fa7a3;border-radius:20px;padding:5px 9px;font-size:8px;white-space:nowrap}.ti-page .analytics{display:grid;grid-template-columns:1.15fr .85fr;gap:12px;margin-top:16px}.ti-page .card{border:1px solid #172f37;background:#0b1a20;border-radius:8px;padding:15px}.ti-page .card h3{font-size:11px;margin:0 0 12px}.ti-page .chart{height:180px;display:flex;align-items:flex-end;gap:8px;padding:12px 8px 0;border-bottom:1px solid #1b343b}.ti-page .chart span{flex:1;max-width:38px;background:linear-gradient(to top,#24515a,#55d6c2);border-radius:4px 4px 0 0;opacity:.82}.ti-page .axis{display:flex;justify-content:space-between;margin-top:9px;color:#58757d;font-size:8px}.ti-page .axis b{color:#7bc7bb}.ti-page .map{height:180px;border:1px solid #132b32;border-radius:7px;display:grid;place-items:center;color:#55d6c2;background:radial-gradient(circle at center,rgba(44,107,111,.12),transparent 65%);overflow:hidden}.ti-page .map svg{width:100%;height:100%}.ti-page .legend{display:flex;gap:10px;flex-wrap:wrap;color:#59767e;font-size:8px;margin-top:8px}.ti-page .legend span:first-child{color:#79cfc1}.ti-page .split{display:grid;grid-template-columns:1fr 1fr;gap:14px}.ti-page .region-list,.ti-page .actor-list{display:grid;gap:8px;margin-top:15px}.ti-page .region{display:grid;grid-template-columns:1.25fr 1fr auto;gap:12px;align-items:center;border-bottom:1px solid #152c33;padding:9px 0}.ti-page .region:last-child,.ti-page .actor:last-child{border-bottom:0}.ti-page .region strong,.ti-page .actor strong{display:block;font-size:10px}.ti-page .region small,.ti-page .actor small{display:block;color:#58757d;font-size:8px;margin-top:3px}.ti-page .region-bar{height:5px;background:#142a31;border-radius:5px;overflow:hidden}.ti-page .region-bar i{display:block;height:100%;background:#55d6c2}.ti-page .region>b,.ti-page .actor>b,.ti-page .row>b{font-size:8px}.ti-page .critical{color:#e7a1a1}.ti-page .high{color:#e0bd7e}.ti-page .medium{color:#79b7a9}.ti-page .actor{display:flex;justify-content:space-between;gap:12px;align-items:center;padding:11px 0;border-bottom:1px solid #152c33}.ti-page .table{margin-top:14px}.ti-page .row{display:grid;grid-template-columns:1fr 1fr .6fr 1.2fr;gap:12px;align-items:center;padding:11px 4px;border-bottom:1px solid #152c33;font-size:9px}.ti-page .row:last-child{border-bottom:0}.ti-page .row.head{color:#58757d;font-size:8px;text-transform:uppercase;letter-spacing:.7px}.ti-page .row strong{font-size:10px}.ti-page .row span,.ti-page .row small{color:#6d888f}.ti-page .lower{display:grid;grid-template-columns:1.1fr .9fr;gap:14px}.ti-page .flow{display:flex;gap:7px;align-items:center;flex-wrap:wrap;margin:14px 0}.ti-page .flow b{border:1px solid #285159;background:#0d2229;padding:8px 9px;border-radius:6px;font-size:9px}.ti-page .flow i{font-style:normal;color:#55d6c2}.ti-page .panel p{color:#6f8991;font-size:10px;line-height:1.65;margin:0}.ti-page .action-grid{display:grid;grid-template-columns:1fr 1fr;gap:8px;margin-top:14px}.ti-page .action-grid a{border:1px solid #19323a;background:#0b1a20;border-radius:6px;padding:11px;color:#7fa0a7;font-size:9px}.ti-page .action-grid a:hover{border-color:#315a61;color:#62dfca}.ti-page footer{padding:20px 0 8px;color:#45636b;font-size:8px;text-align:center}@media(max-width:1100px){.ti-page .content{padding:28px}.ti-page .metrics{grid-template-columns:repeat(3,1fr)}.ti-page .analytics,.ti-page .split,.ti-page .lower{grid-template-columns:1fr}}@media(max-width:760px){.ti-page aside{position:relative;width:100%;height:auto;min-height:0;border-right:0;border-bottom:1px solid #193039}.ti-page{display:block}.ti-page nav{grid-template-columns:repeat(2,1fr);max-height:210px}.ti-page .tenant{display:none}.ti-page .content{margin-left:0;width:100%;padding:20px 14px}.ti-page header{display:block}.ti-page header .primary{display:inline-block;margin-top:15px}.ti-page .metrics{grid-template-columns:repeat(2,1fr)}.ti-page .row{grid-template-columns:1fr 1fr}.ti-page .row span:nth-child(2),.ti-page .row small{display:none}.ti-page .action-grid{grid-template-columns:1fr}.ti-page .region{grid-template-columns:1fr auto}.ti-page .region-bar{grid-column:1/-1}.ti-page h1{font-size:27px}}
`;
