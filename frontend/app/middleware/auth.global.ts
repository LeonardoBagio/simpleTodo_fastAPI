const PUBLIC_ROUTES = new Set(['/login', '/register'])

export default defineNuxtRouteMiddleware(async (to) => {
  const auth = useAuthStore()

  // On the client's very first navigation the SSR plugin already ran; on a
  // pure SPA transition where it hasn't, resolve the session once.
  if (!auth.ready) {
    try {
      await auth.fetchSession()
    } catch {
      auth.ready = true
    }
  }

  const isPublic = PUBLIC_ROUTES.has(to.path)

  if (!auth.isAuthenticated && !isPublic) {
    return navigateTo({ path: '/login', query: { next: to.fullPath } })
  }

  if (auth.isAuthenticated && isPublic) {
    return navigateTo('/')
  }
})
