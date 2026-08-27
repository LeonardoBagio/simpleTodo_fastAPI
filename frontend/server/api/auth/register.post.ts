import type { UserPublic } from '~/types/api'

interface TokenResponse {
  access_token: string
  token_type: string
}

// Create the account (POST /users) then immediately log in, so registration
// lands the visitor straight on their board.
export default defineEventHandler(async (event) => {
  const body = await readBody<{
    username?: string
    email?: string
    password?: string
  }>(event)

  const username = body?.username?.trim()
  const email = body?.email?.trim()
  const password = body?.password ?? ''

  if (!username || !email || !password) {
    throw createError({
      statusCode: 422,
      message: 'Informe usuário, e-mail e senha.',
    })
  }

  const base = backendBase(event)

  try {
    await $fetch<UserPublic>(`${base}/users/`, {
      method: 'POST',
      body: { username, email, password },
    })

    const form = new URLSearchParams()
    form.set('username', email)
    form.set('password', password)

    const token = await $fetch<TokenResponse>(`${base}/auth/token`, {
      method: 'POST',
      headers: { 'content-type': 'application/x-www-form-urlencoded' },
      body: form.toString(),
    })

    setToken(event, token.access_token)
    const user = await fetchCurrentUser(event, token.access_token)
    return { user }
  } catch (err) {
    throw toClientError(err)
  }
})
