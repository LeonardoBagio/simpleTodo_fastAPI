import type { H3Event } from 'h3'

export const TOKEN_COOKIE = 'st_token'

const cookieBase = {
  httpOnly: true,
  sameSite: 'lax' as const,
  path: '/',
  // Access token lifetime is short; the cookie simply outlives a page reload.
  maxAge: 60 * 60 * 8,
}

export function backendBase(event: H3Event): string {
  const url = useRuntimeConfig(event).backendUrl as string
  return url.replace(/\/+$/, '')
}

export function readToken(event: H3Event): string | undefined {
  return getCookie(event, TOKEN_COOKIE)
}

export function setToken(event: H3Event, token: string) {
  setCookie(event, TOKEN_COOKIE, token, {
    ...cookieBase,
    secure: !import.meta.dev,
  })
}

export function clearToken(event: H3Event) {
  deleteCookie(event, TOKEN_COOKIE, { path: '/' })
}

/**
 * Normalise a FastAPI/HTTPX-style error into an H3 error we can forward to the
 * browser without leaking the backend origin.
 */
export function toClientError(err: unknown) {
  const e = err as {
    response?: { status?: number; _data?: { detail?: unknown } }
    statusCode?: number
    data?: { detail?: unknown }
  }
  const status = e?.response?.status ?? e?.statusCode ?? 502
  const detail = e?.response?._data?.detail ?? e?.data?.detail
  const message =
    typeof detail === 'string'
      ? detail
      : status === 502
        ? 'O servidor de tarefas não respondeu.'
        : 'Não foi possível concluir a solicitação.'
  return createError({ statusCode: status, statusMessage: message, message })
}
