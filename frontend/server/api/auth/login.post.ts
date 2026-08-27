import type { UserPublic } from '~/types/api'

interface TokenResponse {
  access_token: string
  token_type: string
}

// Exchange email + password for a JWT and stash it in an httpOnly cookie.
// FastAPI's /auth/token expects an OAuth2 form body (username = email).
export default defineEventHandler(async (event) => {
  const body = await readBody<{ email?: string; password?: string }>(event)
  const email = body?.email?.trim()
  const password = body?.password ?? ''

  if (!email || !password) {
    throw createError({
      statusCode: 422,
      message: 'Informe e-mail e senha.',
    })
  }

  const form = new URLSearchParams()
  form.set('username', email)
  form.set('password', password)

  try {
    const token = await $fetch<TokenResponse>(
      `${backendBase(event)}/auth/token`,
      {
        method: 'POST',
        headers: { 'content-type': 'application/x-www-form-urlencoded' },
        body: form.toString(),
      },
    )

    setToken(event, token.access_token)
    const user = await fetchCurrentUser(event, token.access_token)
    return { user }
  } catch (err) {
    throw toClientError(err)
  }
})
