import Link from 'next/link';

const modules = [
  ['Threat Intelligence', 'Global threats, actors, campaigns and IOCs.'],
  ['Attack Surface', 'Discover external exposure across domains, IPs and applications.'],
  ['Vulnerability', 'Prioritize vulnerabilities using exposure, context and risk.'],
  ['Security Posture', 'Understand infrastructure, cloud, server and network posture.'],
  ['Web & API Security', 'Assess authorized applications and APIs.'],
  ['Hardening', 'Measure configuration and security-baseline compliance.'],
  ['Compliance', 'Build evidence-driven readiness across major frameworks.'],
  ['Cyber AI', 'Correlate security context and accelerate analysis and reporting.'],
];

const frameworks = ['ISO/IEC 27001', 'PCI DSS', 'DORA', 'SOC 2', 'NIST CSF'];

export default function PublicWebsite() {
  return (
    <div className="site-shell">
      <header className="site-nav">
        <Link href="/website" className="site-brand"><span className="site-mark">C</span><span><b>CYBEROS</b><small>GLOBAL SECURITY PLATFORM</small></span></Link>
        <nav className="site-links">
          <a href="#platform">Platform</a><a href="#modules">Modules</a><a href="#compliance">Compliance</a><a href="#pricing">Pricing</a><a href="#trust">Trust</a>
        </nav>
        <div className="site-actions"><Link href="/" className="site-secondary">Command Center</Link><a href="#demo" className="site-primary">Explore Demo →</a></div>
      </header>

      <main>
        <section className="hero" id="platform">
          <div className="hero-copy">
            <span className="site-eyebrow">CYBERSECURITY OPERATING PLATFORM</span>
            <h1>One control plane for your entire security program.</h1>
            <p>CyberOS brings threat intelligence, attack surface, vulnerabilities, security posture, compliance, authorized assessments, evidence, remediation and Cyber AI into one tenant-aware security operating platform.</p>
            <div className="hero-actions"><a href="#demo" className="site-primary large">Enter Demo World →</a><a href="#modules" className="site-secondary large">Explore the platform</a></div>
            <div className="hero-note"><span className="pulse"></span>Built around authorization, evidence, tenant isolation and auditable security operations.</div>
          </div>
          <div className="hero-console">
            <div className="console-top"><span>CYBEROS / SECURITY CONTROL PLANE</span><span className="console-status">● OPERATIONAL</span></div>
            <div className="console-score"><span>ORGANIZATION SECURITY VIEW</span><strong>Unified</strong><small>Threat · Exposure · Posture · Compliance</small></div>
            <div className="console-grid"><div><b>Assets</b><strong>360°</strong><small>security context</small></div><div><b>Findings</b><strong>Prioritized</strong><small>risk-aware</small></div><div><b>Evidence</b><strong>Linked</strong><small>audit-ready</small></div><div><b>Execution</b><strong>Gated</strong><small>policy-controlled</small></div></div>
            <div className="console-flow"><span>Discover</span><i>→</i><span>Analyze</span><i>→</i><span>Assess</span><i>→</i><span>Remediate</span><i>→</i><span>Prove</span></div>
          </div>
        </section>

        <section className="trust-strip"><span>Designed for modern security teams</span><b>FINANCIAL SERVICES</b><b>GOVERNMENT</b><b>MANUFACTURING</b><b>HEALTHCARE</b><b>TECHNOLOGY</b>
        </section>

        <section className="section" id="modules"><div className="section-heading"><span className="site-eyebrow">THE CYBEROS PLATFORM</span><h2>Security capabilities that work together.</h2><p>CyberOS is designed as one operating model rather than a collection of disconnected security products.</p></div><div className="public-module-grid">{modules.map(([title, desc], i) => <article className="public-card" key={title}><span>0{i + 1}</span><h3>{title}</h3><p>{desc}</p><a href="#demo">Explore capability →</a></article>)}</div></section>

        <section className="split-section" id="compliance"><div><span className="site-eyebrow">EVIDENCE-DRIVEN ASSURANCE</span><h2>Turn technical security work into compliance evidence.</h2><p>Map findings, assessments and evidence to versioned controls so one technical observation can support multiple assurance workflows.</p><div className="frameworks">{frameworks.map(f => <span key={f}>{f}</span>)}</div><a href="#demo" className="site-primary">Explore compliance →</a></div><div className="evidence-card"><div className="evidence-row"><span>Control</span><b>Access Control</b><em>Mapped</em></div><div className="evidence-row"><span>Evidence</span><b>Identity configuration</b><em>Verified</em></div><div className="evidence-row"><span>Finding</span><b>Privileged access gap</b><em>High</em></div><div className="evidence-row"><span>Remediation</span><b>Owner + due date</b><em>Tracked</em></div><div className="evidence-row"><span>Report</span><b>Executive evidence package</b><em>Ready</em></div></div></section>

        <section className="demo-section" id="demo"><div><span className="site-eyebrow">DEMO WORLD</span><h2>See the operating model before you connect anything.</h2><p>Explore a synthetic organization with realistic assets, findings, posture, compliance evidence and reports. Demo World is isolated from customer environments and cannot launch arbitrary security testing.</p><a href="/" className="site-primary large">Launch limited demo →</a></div><div className="demo-list"><div><b>01</b><span>Explore a synthetic organization</span></div><div><b>02</b><span>Review exposure and findings</span></div><div><b>03</b><span>Trace evidence and controls</span></div><div><b>04</b><span>See reports and remediation</span></div></div></section>

        <section className="section pricing-section" id="pricing"><div className="section-heading"><span className="site-eyebrow">COMMERCIAL PLATFORM</span><h2>Start with the capabilities you need. Expand as your security program grows.</h2><p>CyberOS will use plans, modules, add-ons, usage and entitlements to control access across the platform.</p></div><div className="pricing-grid"><div className="price-card"><span>FOUNDATION</span><h3>Core visibility</h3><p>Organization, assets, exposure, posture and foundational reporting.</p><a href="#demo">Talk to sales →</a></div><div className="price-card featured"><span>SECURITY OPERATIONS</span><h3>Unified security</h3><p>Threat, vulnerability, assessments, compliance and operational workflows.</p><a href="#demo">Explore package →</a></div><div className="price-card"><span>ENTERPRISE</span><h3>Scale & control</h3><p>Enterprise identity, private deployment, integrations and advanced controls.</p><a href="#demo">Contact enterprise →</a></div></div></section>

        <section className="trust-section" id="trust"><span className="site-eyebrow">SECURITY BY DESIGN</span><h2>Powerful security capabilities behind explicit control boundaries.</h2><div className="trust-points"><span>Tenant isolation</span><span>RBAC & authorization</span><span>Evidence provenance</span><span>Auditable execution</span><span>Safe demo isolation</span><span>AI guardrails</span></div></section>
      </main>

      <footer className="site-footer"><div><b>CYBEROS</b><p>Global Cybersecurity Intelligence & Security Posture Platform.</p></div><div><span>Platform</span><span>Modules</span><span>Compliance</span><span>Pricing</span></div><div><span>Trust & Security</span><span>Resources</span><span>Contact</span><span>Sign in</span></div><small>CyberOS product experience · M2 foundation</small></footer>
    </div>
  );
}
