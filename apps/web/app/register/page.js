'use client'
import { useEffect, useState } from 'react'
import { useRouter } from 'next/navigation'
import Shell from '../../components/Shell'
import { api, getSession } from '../../lib/client'

const input = (label, name, data, setData, type = 'text') => <label key={name}>{label}<input type={type} value={data[name] || ''} onChange={e => setData({ ...data, [name]: e.target.value })} /></label>
export default function Register() {
  const router = useRouter()
  const [ready, setReady] = useState(false)
  const [caseData, setCaseData] = useState({ title: '', status: 'DRAFT', priority: 'NORMAL' })
  const [client, setClient] = useState({ kind: 'INDIVIDUAL' })
  const [clients, setClients] = useState([])
  const [selectedClient, setSelectedClient] = useState('')
  const [party, setParty] = useState({ kind: 'ORGANIZATION' })
  const [files, setFiles] = useState([])
  const [error, setError] = useState('')
  const [busy, setBusy] = useState(false)
  useEffect(() => { if (!getSession()) router.push('/'); else { setReady(true); api('/clients').then(setClients).catch(() => {}) } }, [router])
  async function save(status) {
    setBusy(true); setError('')
    try {
      const created = await api('/cases', { method: 'POST', body: JSON.stringify({ ...caseData, status, client_id: selectedClient || null, client: !selectedClient && client.name ? client : null, opposing_party: party.name ? party : null }) })
      for (const file of files) {
        const form = new FormData(); form.append('file', file)
        await api(`/cases/${created.id}/documents`, { method: 'POST', body: form })
      }
      router.push(`/cases/${created.id}`)
    } catch (e) { setError(e.message) } finally { setBusy(false) }
  }
  if (!ready) return null
  return <Shell title="Register new case" subtitle="Create a matter and build its case record." role="LAWYER"><div className="form-page"><section className="panel form-section"><div className="eyebrow">01 / CASE INFORMATION</div><h2>Case information</h2><div className="form-grid">{input('Case title *', 'title', caseData, setCaseData)}{input('Case type', 'case_type', caseData, setCaseData)}{input('Case number', 'case_number', caseData, setCaseData)}{input('Court', 'court', caseData, setCaseData)}<label>Priority<select value={caseData.priority} onChange={e => setCaseData({ ...caseData, priority: e.target.value })}><option>NORMAL</option><option>HIGH</option><option>LOW</option></select></label>{input('Filing date', 'filing_date', caseData, setCaseData, 'date')}</div></section><section className="panel form-section"><div className="eyebrow">02 / CLIENT DETAILS</div><h2>Client details</h2><div className="form-grid"><label className="wide">Select existing client<select value={selectedClient} onChange={e => setSelectedClient(e.target.value)}><option value="">Create a new client below</option>{clients.map(c => <option key={c.id} value={c.id}>{c.name}</option>)}</select></label>{!selectedClient && <><label>Client type<select value={client.kind} onChange={e => setClient({ ...client, kind: e.target.value })}><option>INDIVIDUAL</option><option>ORGANIZATION</option></select></label>{input('Name', 'name', client, setClient)}{input('Phone', 'phone', client, setClient)}{input('Email', 'email', client, setClient, 'email')}{input('Address', 'address', client, setClient)}</>}</div></section><section className="panel form-section"><div className="eyebrow">03 / OPPOSING PARTY</div><h2>Opposing party</h2><div className="form-grid">{input('Name', 'name', party, setParty)}<label>Type<select value={party.kind} onChange={e => setParty({ ...party, kind: e.target.value })}><option>ORGANIZATION</option><option>INDIVIDUAL</option></select></label>{input('Contact', 'contact', party, setParty)}{input('Address', 'address', party, setParty)}{input('Opposing counsel', 'counsel', party, setParty)}</div></section><section className="panel form-section"><div className="eyebrow">04 / CASE DETAILS</div><h2>Case details</h2><div className="form-grid">{input('Main issue', 'main_issue', caseData, setCaseData)}<label className="wide">Description<textarea rows="4" value={caseData.description || ''} onChange={e => setCaseData({ ...caseData, description: e.target.value })} /></label></div></section><section className="panel form-section"><div className="eyebrow">05 / INITIAL DOCUMENTS</div><h2>Initial documents</h2><label className="dropzone">Choose PDF, DOCX, or TXT files<input type="file" accept=".pdf,.docx,.txt" multiple onChange={e => setFiles(Array.from(e.target.files))} /></label>{files.map(f => <div className="file-line" key={f.name}>{f.name} <span>Ready to upload</span></div>)}</section>{error && <div className="error">{error}</div>}<div className="form-actions"><button disabled={busy || !caseData.title.trim()} onClick={() => save('DRAFT')}>Save as draft</button><button className="primary" disabled={busy || !caseData.title.trim()} onClick={() => save('ACTIVE')}>{busy ? 'Creating case…' : 'Register case & process documents'}</button></div></div></Shell>
}
