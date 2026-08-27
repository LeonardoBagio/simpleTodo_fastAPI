// Populate the auth store from the httpOnly cookie during SSR so the first
// paint already knows whether the visitor is signed in (no auth flash).
export default defineNuxtPlugin(async () => {
  const auth = useAuthStore()
  if (!auth.ready) {
    try {
      await auth.fetchSession()
    } catch {
      auth.ready = true
    }
  }
})
