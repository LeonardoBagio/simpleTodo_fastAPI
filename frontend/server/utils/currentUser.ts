import type { H3Event } from 'h3'
import type { UserPublic } from '~/types/api'

/** Decode a JWT payload without verifying (we only read the `sub` claim). */
function decodeSub(token: string): string | null {
  try {
    const payload = token.split('.')[1]
    if (!payload) return null
    const json = Buffer.from(
      payload.replace(/-/g, '+').replace(/_/g, '/'),
      'base64',
    ).toString('utf8')
    const data = JSON.parse(json) as { sub?: string }
    return data.sub ?? null
  } catch {
    return null
  }
}

/**
 * The backend has no `/me` endpoint: the JWT `sub` carries the user's email,
 * and GET /users returns the id + username. We reconcile the two so the client
 * gets a full profile (needed for the account page's PUT/DELETE /users/{id}).
 */
export async function fetchCurrentUser(
  event: H3Event,
  token: string,
): Promise<UserPublic | null> {
  const email = decodeSub(token)
  if (!email) return null

  const users = await $fetch<UserPublic[]>(`${backendBase(event)}/users/`, {
    headers: { Authorization: `Bearer ${token}` },
    query: { limit: 1000, offset: 0 },
  })

  return users.find((u) => u.email === email) ?? null
}
