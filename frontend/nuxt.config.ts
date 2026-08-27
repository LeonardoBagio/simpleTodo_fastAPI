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
      // Placards / engraved panel labels
      'Saira Condensed': [500, 600, 700],
      // Console wordmark
      'Saira Stencil One': [400],
      // Workhorse UI / content
      Saira: [400, 500, 600, 700],
      // Readouts, IDs, counts, timestamps
      'Spline Sans Mono': [400, 500, 600],
    },
    display: 'swap',
    download: true,
    preload: true,
  },

  app: {
    head: {
      htmlAttrs: { lang: 'pt-BR' },
      title: 'Simple Todo — Painel',
      meta: [
        { charset: 'utf-8' },
        { name: 'viewport', content: 'width=device-width, initial-scale=1' },
        {
          name: 'description',
          content:
            'Simple Todo — painel de controle das suas tarefas, com ciclo de estados draft, todo, doing, done e trash.',
        },
        { name: 'theme-color', content: '#191c20' },
      ],
    },
  },
})
