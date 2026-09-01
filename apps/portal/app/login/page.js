'use client';

import Link from 'next/link';
import { useState } from 'react';
import { useRouter } from 'next/navigation';

const API = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8100';

export default function LoginPage() {
  const router = useRouter();
  const [email, setEmail] = useState('cro@demo.cyberos.local');
  const [message, setMessage] = useState('Demo identity boundary — authentication is simulated; tenant context is loaded from the control plane.');
  const [busy, setBusy] = useState(false);

  const enter = async (event) => {
    event.preventDefault();
    setBusy(true);
    setMessage('Authenticating identity and loading tenant policy…');
    try {
      const r = await fetch(API + '/api/v1/context');
      const data = await r.json();
      if (!r.ok) throw new Error(data.detail || 'Control plane authentication context unavailable');
      localStorage.setItem('cyberos.identity', JSON.stringify(data.identity));
      localStorage.setItem('cyberos.tenant', JSON.stringify(data.tenant));
      localStorage.setItem('cyberos.authorization', JSON.stringify(data.authorization));
      setMessage(`Authenticated → ${data.identity.display_name} → ${data.tenant.name} → tenant boundary active.`);
      setTimeout(() => router.push('/command-center'), 250);
    } catch (e) {
      setMessage(e.message + '. Start the CyberOS Docker stack and try again.');
    } finally { setBusy(false); }
  };

  return (
    <main className="login-shell">
      <section className="login-card">
        <Link href="/" className="login-brand"><span className="mark">C</span><span><b>CYBEROS</b><small>GLOBAL SECURITY PLATFORM</small></span></Link>
        <span className="eyebrow">CUSTOMER SECURITY PORTAL</span>
        <h1>Sign in to your security control plane.</h1>
        <p>A CRO, CISO or security operator signs into a tenant-aware workspace. CyberOS then loads organization entitlements, assets, connectors, authorization policy and security modules for that customer.</p>
        <form onSubmit={enter}>
          <label>Work email<input value={email} onChange={(e) => setEmail(e.target.value)} type="email" required /></label>
          <label>Password<input type="password" placeholder="Demo authentication" required /></label>
          <button className="primary" type="submit" disabled={busy}>{busy ? 'Loading tenant…' : 'Sign in →'}</button>
        </form>
        <div className="login-status"><span className="dot" />{message}</div>
        <div className="login-links"><Link href="/organization">Organization setup →</Link><Link href="/command-center">Enter Demo World →</Link></div>
      </section>
      <style>{`*{box-sizing:border-box}.login-shell{min-height:100vh;background:#071016;color:#dce8ed;display:grid;place-items:center;padding:40px 20px;font-family:Inter,ui-sans-serif,system-ui,sans-serif}.login-card{width:min(520px,100%);background:#09171d;border:1px solid #19323a;border-radius:12px;padding:38px;box-shadow:0 30px 90px rgba(0,0,0,.35)}.login-brand{display:flex;align-items:center;gap:11px;margin-bottom:42px}.mark{width:36px;height:36px;border:1px solid #55d6c2;border-radius:9px;display:grid;place-items:center;color:#55d6c2;font-weight:800}.login-brand b{display:block;letter-spacing:3px;font-size:14px}.login-brand small{display:block;color:#63818a;font-size:7px;letter-spacing:1.2px;margin-top:3px}.eyebrow{font-size:9px;letter-spacing:2px;color:#5d8c95}.login-card h1{font-size:34px;line-height:1.12;margin:14px 0}.login-card>p{color:#78939b;font-size:13px;line-height:1.7;margin-bottom:28px}.login-card form{display:grid;gap:16px}.login-card label{display:grid;gap:7px;color:#78939b;font-size:10px;letter-spacing:.7px;text-transform:uppercase}.login-card input{width:100%;background:#0b1b21;border:1px solid #19323a;border-radius:7px;padding:12px;color:#dce8ed;outline:none}.login-card input:focus{border-color:#55d6c2}.primary{border:0;background:#62dfca;color:#071016;border-radius:7px;padding:12px 17px;font-weight:800;font-size:12px;cursor:pointer}.primary:disabled{opacity:.55;cursor:wait}.login-status{margin-top:18px;border:1px solid #19373e;background:#0a1a20;border-radius:7px;padding:11px 13px;color:#78939b;font-size:10px;line-height:1.6}.dot{display:inline-block;width:7px;height:7px;background:#55d6c2;border-radius:50%;margin-right:8px}.login-links{display:flex;justify-content:space-between;gap:15px;margin-top:24px;font-size:10px;color:#67cdbf}@media(max-width:600px){.login-card{padding:26px}.login-card h1{font-size:28px}.login-links{flex-direction:column}}`}</style>
    </main>
  );
}
