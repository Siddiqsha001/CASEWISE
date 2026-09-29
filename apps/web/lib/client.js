export const disclaimer = 'AI-generated information should be reviewed and verified by a qualified legal professional.'
const key = 'casewise.session'
export function getSession() {
  if (typeof window === 'undefined') return null
  try { return JSON.parse(localStorage.getItem(key) || 'null') } catch { return null }
}
export function setSession(value) { localStorage.setItem(key, JSON.stringify(value)) }
export function clearSession() { localStorage.removeItem(key) }
export async function api(path, options = {}) {
  let session = getSession()
  if (!session) throw new Error('Sign in required')
  const send = async token => {
    const headers = new Headers(options.headers || {})
    headers.set('authorization', `Bearer ${token}`)
    if (options.body && !(options.body instanceof FormData)) headers.set('content-type', 'application/json')
    return fetch(`/api${path}`, { ...options, headers })
  }
  let response = await send(session.access_token)
  if (response.status === 401 && session.refresh_token) {
    try {
      session = await auth('token?grant_type=refresh_token', { refresh_token: session.refresh_token })
      setSession(session)
      response = await send(session.access_token)
    } catch {
      clearSession()
      throw new Error('Session expired. Please sign in again.')
    }
  }
  if (!response.ok) {
    let payload = {}
    try { payload = await response.json() } catch {}
    if (response.status === 401) {
      clearSession()
      const error = new Error('Session expired or rejected. Please sign in again.')
      error.status = 401
      throw error
    }
    const error = new Error(typeof payload.detail === 'string' ? payload.detail : `Request failed (${response.status})`)
    error.status = response.status
    throw error
  }
  const type = response.headers.get('content-type') || ''
  return type.includes('application/json') ? response.json() : response.blob()
}
export async function auth(path, body) {
  const base = process.env.NEXT_PUBLIC_SUPABASE_URL
  const publishableKey = process.env.NEXT_PUBLIC_SUPABASE_PUBLISHABLE_KEY
  if (!base || !publishableKey) throw new Error('Supabase Auth is not configured')
  let response
  try {
    response = await fetch(`${base.replace(/\/$/, '')}/auth/v1/${path}`, {
      method: 'POST',
      headers: { 'content-type': 'application/json', apikey: publishableKey },
      body: JSON.stringify(body)
    })
  } catch {
    throw new Error('Cannot reach Supabase Auth. Check your network and Supabase project URL.')
  }
  const raw = await response.text()
  let data
  try { data = JSON.parse(raw) } catch {
    throw new Error(`Supabase Auth returned HTTP ${response.status} without a valid response.`)
  }
  if (!response.ok) throw new Error(data.msg || data.error_description || data.message || data.error || `Authentication failed (${response.status})`)
  return data
}
