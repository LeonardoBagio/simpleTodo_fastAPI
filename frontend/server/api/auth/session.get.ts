// Returns the current user (or null) based on the httpOnly cookie. Also
// refreshes the access token so an active session keeps rolling forward.
export default defineEventHandler(async (event) => {
  const token = readToken(event)
  if (!token) return { user: null }

  try {
    const user = await fetchCurrentUser(event, token)
    if (!user) {
      clearToken(event)
      return { user: null }
    }

    // Opportunistic refresh: mint a fresh access token from the valid bearer.
    try {
      const refreshed = await $fetch<{ access_token: string }>(
        `${backendBase(event)}/auth/refresh_token`,
        {
          method: 'POST',
          headers: { Authorization: `Bearer ${token}` },
        },
      )
      if (refreshed?.access_token) setToken(event, refreshed.access_token)
    } catch {
      // Refresh is best-effort; the existing token is still valid here.
    }

    return { user }
  } catch {
    clearToken(event)
    return { user: null }
  }
})
