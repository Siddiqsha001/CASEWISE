'use client'
import Link from 'next/link'
import { useRouter } from 'next/navigation'
import { clearSession } from '../lib/client'
export default function Shell({ children, title, subtitle, role }) {
  const router = useRouter()
  return <div className="shell"><aside className="sidebar"><Link href="/" className="brand"><span className="brand-mark">C</span><span>CaseWise <em>AI</em></span></Link><div className="nav-label">WORKSPACE</div><nav><Link href="/">Overview</Link>{role === 'LAWYER' && <Link href="/register">Register new case</Link>}</nav><div className="sidebar-bottom"><div className="small">{role === 'LAWYER' ? 'Lawyer workspace' : 'Client workspace'}</div><button className="text-button" onClick={() => { clearSession(); router.push('/') }}>Sign out</button></div></aside><main className="main"><header className="topbar"><div><h1>{title}</h1>{subtitle && <p>{subtitle}</p>}</div><div className="avatar">CW</div></header>{children}</main></div>
}
