'use client';
import Link from 'next/link';
import { useState } from 'react';

export default function LoginPage(){
 const [mode,setMode]=useState('signin');
 return <main className="module-page"><section className="content" style={{maxWidth:980,margin:'0 auto',minHeight:'100vh',padding:'56px 28px'}}>
  <header><div><span className="eyebrow">CYBEROS / CUSTOMER ACCESS</span><h1>{mode==='signin'?'Sign in to CyberOS':'Create your organization'}</h1><p>Secure tenant access for CISOs, security leaders, administrators and authorized security teams.</p></div><Link className="primary" href="/">← Public website</Link></header>
  <div className="status"><span className="dot"></span>Tenant-aware access · MFA / SSO ready architecture · No security execution from this page</div>
  <section className="panel" style={{maxWidth:620,margin:'18px auto'}}>
   <div className="panelhead"><div><span className="eyebrow">IDENTITY GATEWAY</span><h2>{mode==='signin'?'Customer sign-in':'Organization registration'}</h2></div><span className="pill">M2 UX</span></div>
   <div style={{display:'grid',gap:14}}>
    {mode==='signin'?<><label>Email or SSO identity<input aria-label="Email or SSO identity" placeholder="security.leader@company.com" style={input}/></label><label>Password / SSO<input aria-label="Password" type="password" placeholder="••••••••" style={input}/></label><button className="primary action" type="button" onClick={()=>location.href='/onboarding'}>Continue to tenant →</button></>:<><label>Organization name<input aria-label="Organization name" placeholder="Example Financial Services" style={input}/></label><label>Work email<input aria-label="Work email" placeholder="ciso@company.com" style={input}/></label><label>Industry<select aria-label="Industry" style={input}><option>Financial Services</option><option>Government</option><option>Manufacturing</option><option>Healthcare</option><option>Technology</option><option>Other</option></select></label><button className="primary action" type="button" onClick={()=>location.href='/onboarding'}>Begin secure onboarding →</button></>}
   </div>
   <p style={{marginTop:16,color:'#718b93',fontSize:11}}>Production identity will be backed by OIDC/SAML, MFA and server-side session/tenant authorization. This M2 screen is the customer journey shell; it does not claim production authentication.</p>
   <button className="secondary" style={{marginTop:10}} onClick={()=>setMode(mode==='signin'?'signup':'signin')}>{mode==='signin'?'New organization? Create one':'Already have an account? Sign in'}</button>
  </section>
 </section></main>
}
const input={width:'100%',marginTop:7,padding:'12px',background:'#08151b',border:'1px solid #24434b',borderRadius:7,color:'#dce8ed',fontSize:12};
