import { defineStore } from 'pinia'
import type { UserPublic } from '~/types/api'

export const useAuthStore = defineStore('auth', {
  state: () => ({
    user: null as UserPublic | null,
    ready: false,
  }),
  getters: {
    isAuthenticated: (s) => !!s.user,
    initials: (s) =>
      s.user?.username?.slice(0, 2).toUpperCase() ?? '??',
  },
  actions: {
    async fetchSession() {
      // On SSR (a full reload / F5) the plain $fetch to an internal route does
      // NOT forward the browser's cookies, so the session would come back null
      // and drop the user to /login. useRequestFetch() forwards the incoming
      // request headers (including the httpOnly token cookie) during SSR; on
      // the client, $fetch already sends same-origin cookies automatically.
      const fetcher = import.meta.server ? useRequestFetch() : $fetch
      const { user } = await fetcher<{ user: UserPublic | null }>(
        '/api/auth/session',
      )
      this.user = user
      this.ready = true
      return user
    },

    async login(email: string, password: string) {
      const { user } = await $fetch<{ user: UserPublic | null }>(
        '/api/auth/login',
        { method: 'POST', body: { email, password } },
      )
      this.user = user
      this.ready = true
      return user
    },

    async register(username: string, email: string, password: string) {
      const { user } = await $fetch<{ user: UserPublic | null }>(
        '/api/auth/register',
        { method: 'POST', body: { username, email, password } },
      )
      this.user = user
      this.ready = true
      return user
    },

    async updateAccount(payload: {
      username: string
      email: string
      password: string
    }) {
      if (!this.user) throw new Error('Sem sessão.')
      const updated = await $fetch<UserPublic>(
        `/api/backend/users/${this.user.id}`,
        { method: 'PUT', body: payload },
      )
      this.user = updated
      return updated
    },

    async deleteAccount() {
      if (!this.user) return
      await $fetch(`/api/backend/users/${this.user.id}`, { method: 'DELETE' })
      this.user = null
    },

    async logout() {
      await $fetch('/api/auth/logout', { method: 'POST' })
      this.user = null
    },
  },
})
