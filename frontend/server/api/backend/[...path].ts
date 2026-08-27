// Authenticated pass-through to FastAPI. The browser calls /api/backend/<path>;
// we attach the httpOnly bearer token, forward method/query/body, and retry
// once through /auth/refresh_token if the token has just expired.
export default defineEventHandler(async (event) => {
  let token = readToken(event)
  if (!token) {
    throw createError({ statusCode: 401, message: 'Sessão expirada.' })
  }

  const path = (getRouterParam(event, 'path') || '').replace(/^\/+/, '')
  const base = backendBase(event)
  const target = `${base}/${path}`
  const method = event.method
  const query = getQuery(event)
  const body =
    method === 'GET' || method === 'HEAD' ? undefined : await readBody(event)

  const call = (bearer: string) =>
    $fetch.raw(target, {
      method: method as any,
      query,
      body,
      headers: { Authorization: `Bearer ${bearer}` },
    })

  try {
    const res = await call(token)
    setResponseStatus(event, res.status)
    return res._data
  } catch (err) {
    const status = (err as { response?: { status?: number } })?.response?.status
    if (status !== 401) throw toClientError(err)

    // Try a single refresh + retry before giving up on the session.
    try {
      const refreshed = await $fetch<{ access_token: string }>(
        `${base}/auth/refresh_token`,
        { method: 'POST', headers: { Authorization: `Bearer ${token}` } },
      )
      token = refreshed.access_token
      setToken(event, token)
      const res = await call(token)
      setResponseStatus(event, res.status)
      return res._data
    } catch {
      clearToken(event)
      throw createError({ statusCode: 401, message: 'Sessão expirada.' })
    }
  }
})
