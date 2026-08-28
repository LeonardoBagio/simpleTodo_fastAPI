// Scroll-reveal, mirroring the portfolio's `.reveal` → `.is-visible` pattern.
// Registered universally so the `v-reveal` directive RESOLVES on the server
// (a client-only plugin makes SSR warn "Failed to resolve directive" and
// breaks hydration). All DOM/observer work happens in `mounted`, which Vue
// runs on the client only.
//
// Usage: add `v-reveal` (optionally `v-reveal="120"` for a stagger delay in
// ms). Elements start hidden (.reveal) and fade/slide in on entering the
// viewport. Falls back to instantly visible when IntersectionObserver is
// unavailable or the user prefers reduced motion.
export default defineNuxtPlugin((nuxtApp) => {
  let observer: IntersectionObserver | null = null

  function ensureObserver() {
    if (observer || typeof window === 'undefined') return observer
    const reduce = window.matchMedia?.(
      '(prefers-reduced-motion: reduce)',
    ).matches
    if (reduce || !('IntersectionObserver' in window)) return null
    observer = new IntersectionObserver(
      (entries, obs) => {
        for (const entry of entries) {
          if (entry.isIntersecting) {
            entry.target.classList.add('is-visible')
            obs.unobserve(entry.target)
          }
        }
      },
      { threshold: 0.12, rootMargin: '0px 0px -40px 0px' },
    )
    return observer
  }

  nuxtApp.vueApp.directive('reveal', {
    // mounted runs on the client only (Vue skips directive hooks during SSR).
    mounted(el: HTMLElement, binding) {
      el.classList.add('reveal')
      const delay = Number(binding.value) || 0
      if (delay) el.style.transitionDelay = `${delay}ms`

      const obs = ensureObserver()
      if (!obs) {
        el.classList.add('is-visible')
        return
      }
      obs.observe(el)
    },
    unmounted(el: HTMLElement) {
      observer?.unobserve(el)
    },
  })
})
