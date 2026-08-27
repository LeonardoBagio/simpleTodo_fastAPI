export default defineEventHandler((event) => {
  clearToken(event)
  return { ok: true }
})
