'use client'
import Link from 'next/link'
import { useEffect, useState } from 'react'
import Shell from '../components/Shell'
import { api, auth, clearSession, getSession, setSession, disclaimer } from '../lib/client'

export default function Home() {
  const [session, setLocalSession] = useState(null)
  const [profile, setProfile] = useState(null)
  const [cases, setCases] = useState([])
  const [mode, setMode] = useState('login')
  const [form, setForm] = useState({ email: '', password: '', display_name: '', role: 'LAWYER' })
  const [error, setError] = useState('')
  const [notice, setNotice] = useState('')
  const [loading, setLoading] = useState(false)
  useEffect(() => { const s = getSession(); if (s) { setLocalSession(s); load() } }, [])
  async function load() {
    try {
      const p = await api('/profile')
      setProfile(p)
      if (p) setCases(await api('/cases'))
    } catch (e) { if (e.status === 401) setLocalSession(null); setError(e.message) }
  }
  async function submit(e) {
    e.preventDefault(); setError(''); setNotice(''); setLoading(true)
    try {
      let data
      if (mode === 'signup') {
        data = await auth('signup', { email: form.email, password: form.password, data: { display_name: form.display_name, role: form.role } })
        if (!data.access_token) {
          setMode('login')
          setNotice('Account created. Check your email for a confirmation link, then sign in.')
          return
        }
      } else data = await auth('token?grant_type=password', { email: form.email, password: form.password })
      setSession(data); setLocalSession(data)
      let p = await api('/profile')
      if (!p) p = await api('/profile', { method: 'POST', body: JSON.stringify({ role: data.user?.user_metadata?.role || form.role, display_name: data.user?.user_metadata?.display_name || form.display_name || form.email.split('@')[0] }) })
      setProfile(p); setCases(await api('/cases'))
    } catch (e) { if (e.status === 401) setLocalSession(null); setError(e.message) } finally { setLoading(false) }
  }
  if (!session) return <div className="auth-page"><div className="auth-intro"><div className="brand"><span className="brand-mark">C</span><span>CaseWise <em>AI</em></span></div><h1>Every detail of your case, in view.</h1><p>A focused workspace for legal matters, documents, evidence, and case-specific AI assistance.</p><div className="auth-note">{disclaimer}</div></div><div className="auth-card"><div className="eyebrow">WELCOME TO CASEWISE</div><h2>{mode === 'login' ? 'Sign in to continue' : 'Create your account'}</h2><p className="muted">Your legal workspace starts here.</p><form onSubmit={submit}>{mode === 'signup' && <><label>Name<input required value={form.display_name} onChange={e => setForm({ ...form, display_name: e.target.value })} /></label><label>Account type<select value={form.role} onChange={e => setForm({ ...form, role: e.target.value })}><option value="LAWYER">Lawyer</option><option value="CLIENT">Client</option></select></label></>}<label>Email<input type="email" required value={form.email} onChange={e => setForm({ ...form, email: e.target.value })} /></label><label>Password<input type="password" minLength="6" required value={form.password} onChange={e => setForm({ ...form, password: e.target.value })} /></label>{notice && <div className="notice">{notice}</div>}{error && <div className="error">{error}</div>}<button className="primary full" disabled={loading}>{loading ? 'Please wait…' : mode === 'login' ? 'Sign in' : 'Create account'}</button></form><button className="switch" onClick={() => { setError(''); setNotice(''); setMode(mode === 'login' ? 'signup' : 'login') }}>{mode === 'login' ? 'New to CaseWise? Create an account' : 'Already have an account? Sign in'}</button></div></div>
  if (!profile) return <div className="center-card"><h2>{error ? 'Could not load your profile' : 'Complete your profile'}</h2>{error ? <><div className="error">{error}</div><div className="actions"><button className="primary" onClick={() => { setError(''); load() }}>Try again</button><button onClick={() => { clearSession(); setLocalSession(null); setError('') }}>Sign out</button></div></> : <><p>Choose the workspace you need.</p><div className="actions"><button onClick={async () => { try { const p = await api('/profile', { method: 'POST', body: JSON.stringify({ role: 'LAWYER', display_name: 'Lawyer' }) }); setProfile(p) } catch (e) { setError(e.message) } }}>Lawyer</button><button onClick={async () => { try { const p = await api('/profile', { method: 'POST', body: JSON.stringify({ role: 'CLIENT', display_name: 'Client' }) }); setProfile(p) } catch (e) { setError(e.message) } }}>Client</button></div></>}</div>
  return <Shell title={profile.role === 'LAWYER' ? 'Good to see you.' : 'Your cases'} subtitle={profile.role === 'LAWYER' ? 'Your case workspace at a glance.' : 'Your matters and upcoming work.'} role={profile.role}><section className="stats"><div className="stat"><span>ACTIVE CASES</span><strong>{cases.filter(c => c.status === 'ACTIVE').length}</strong></div><div className="stat"><span>TOTAL CASES</span><strong>{cases.length}</strong></div><div className="stat"><span>YOUR ROLE</span><strong className="stat-word">{profile.role === 'LAWYER' ? 'Lawyer' : 'Client'}</strong></div></section><section className="panel"><div className="panel-head"><div><div className="eyebrow">YOUR WORKSPACE</div><h2>Cases</h2></div>{profile.role === 'LAWYER' && <Link className="primary" href="/register">+ Register new case</Link>}</div>{cases.length ? <div className="case-list">{cases.map(c => <Link key={c.id} href={`/cases/${c.id}`} className="case-row"><div className="case-icon">{c.title[0]}</div><div className="case-main"><strong>{c.title}</strong><span>{c.case_number || 'No case number'} · {c.court || 'Court not set'}</span></div><span className={`badge ${c.status.toLowerCase()}`}>{c.status}</span><span className="arrow">→</span></Link>)}</div> : <div className="empty"><h3>No cases yet</h3><p>{profile.role === 'LAWYER' ? 'Register a case to begin organizing documents and evidence.' : 'Your lawyer can invite you to a case.'}</p>{profile.role === 'LAWYER' && <Link href="/register" className="primary">Register first case</Link>}</div>}</section><p className="disclaimer">{disclaimer}</p></Shell>
}
