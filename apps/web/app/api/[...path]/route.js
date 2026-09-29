const base = process.env.AI_SERVICE_URL || 'http://ai:8000'

async function proxy(request, { params }) {
  const { path } = await params
  const url = `${base}/api/${path.map(encodeURIComponent).join('/')}${new URL(request.url).search}`
  const headers = new Headers()
  const authorization = request.headers.get('authorization')
  if (authorization) headers.set('authorization', authorization)
  const type = request.headers.get('content-type')
  if (type) headers.set('content-type', type)
  try {
    const response = await fetch(url, {
      method: request.method,
      headers,
      body: ['GET', 'HEAD'].includes(request.method) ? undefined : await request.arrayBuffer(),
      cache: 'no-store'
    })
    const out = new Headers()
    for (const key of ['content-type', 'content-disposition']) {
      if (response.headers.has(key)) out.set(key, response.headers.get(key))
    }
    return new Response(response.body, { status: response.status, headers: out })
  } catch {
    return Response.json({ detail: 'CaseWise service is unavailable' }, { status: 503 })
  }
}
export const GET = proxy
export const POST = proxy
export const PATCH = proxy
export const DELETE = proxy
