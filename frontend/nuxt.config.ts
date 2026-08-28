// https://nuxt.com/docs/api/configuration/nuxt-config
export default defineNuxtConfig({
  compatibilityDate: '2025-01-01',
  devtools: { enabled: false },

  modules: ['@pinia/nuxt', '@nuxtjs/tailwindcss', '@nuxtjs/google-fonts'],

  // Our main.css carries the @tailwind directives plus the console's @layer
  // rules, so hand it to the Tailwind module as the single stylesheet entry
  // (prevents the module from injecting a second, duplicate tailwind.css).
  tailwindcss: {
    cssPath: '~/assets/css/main.css',
  },

  pinia: {
    storesDirs: ['app/stores/**'],
  },

  imports: {
    dirs: ['stores'],
  },

  // Server-only base URL for the FastAPI backend. The browser never talks to
  // FastAPI directly — every call goes through this app's server routes (BFF),
  // which attach the httpOnly access token. Override with NUXT_BACKEND_URL.
  runtimeConfig: {
    backendUrl: 'http://localhost:8000',
    public: {
      appName: 'Simple Todo',
    },
  },

  googleFonts: {
    families: {
      // Headings, labels, buttons, numeric readouts (uppercase + tracking)
      Montserrat: [400, 700, 900],
      // Body / running text
      Raleway: [400, 600, 700],
    },
    display: 'swap',
    download: true,
    preload: true,
  },

  app: {
    head: {
      htmlAttrs: { lang: 'pt-BR' },
      title: 'Simple Todo — Painel',
      link: [{ rel: 'icon', type: 'image/svg+xml', href: '/favicon.svg' }],
      meta: [
        { charset: 'utf-8' },
        { name: 'viewport', content: 'width=device-width, initial-scale=1' },
        {
          name: 'description',
          content:
            'Simple Todo — painel de controle das suas tarefas, com ciclo de estados draft, todo, doing, done e trash.',
        },
        { name: 'theme-color', content: '#e5e5e5' },
      ],
    },
  },
})
