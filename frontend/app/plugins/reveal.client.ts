// Scroll-reveal, mirroring the portfolio's `.reveal` → `.is-visible` pattern.
// Usage: add `v-reveal` (optionally `v-reveal="120"` for a stagger delay in ms)
// to any element. Elements start hidden (.reveal) and fade/slide in once they
// enter the viewport. Falls back to instantly visible when IntersectionObserver
// is unavailable or the user prefers reduced motion.
export default defineNuxtPlugin((nuxtApp) => {
  const reduce =
    typeof window !== 'undefined' &&
    window.matchMedia?.('(prefers-reduced-motion: reduce)').matches

  const supported =
    typeof window !== 'undefined' && 'IntersectionObserver' in window

  let observer: IntersectionObserver | null = null
  if (supported && !reduce) {
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
  }

  nuxtApp.vueApp.directive('reveal', {
    mounted(el: HTMLElement, binding) {
      el.classList.add('reveal')
      const delay = Number(binding.value) || 0
      if (delay) el.style.transitionDelay = `${delay}ms`

      if (!observer) {
        el.classList.add('is-visible')
        return
      }
      observer.observe(el)
    },
    unmounted(el: HTMLElement) {
      observer?.unobserve(el)
    },
  })
})
