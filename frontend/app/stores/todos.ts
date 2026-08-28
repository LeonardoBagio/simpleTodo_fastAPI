import { defineStore } from 'pinia'
import type { TodoCreate, TodoPublic, TodoUpdate } from '~/types/api'

interface Filter {
  title: string
  status_id: number | ''
  category_id: number | ''
}

export const useTodosStore = defineStore('todos', {
  state: () => ({
    items: [] as TodoPublic[],
    loading: false,
    saving: false,
    loaded: false,
    filter: { title: '', status_id: '', category_id: '' } as Filter,
  }),
  getters: {
    // Tarefas visíveis honrando os filtros ativos.
    visible(state): TodoPublic[] {
      return state.items.filter((t) => {
        if (state.filter.status_id && t.status_id !== state.filter.status_id)
          return false
        if (
          state.filter.category_id &&
          t.category_id !== state.filter.category_id
        )
          return false
        if (
          state.filter.title &&
          !t.title.toLowerCase().includes(state.filter.title.toLowerCase())
        )
          return false
        return true
      })
    },
    // Contagem por status_id.
    countByStatus(state): Record<number, number> {
      const acc: Record<number, number> = {}
      for (const t of state.items) acc[t.status_id] = (acc[t.status_id] ?? 0) + 1
      return acc
    },
  },
  actions: {
    async fetch() {
      this.loading = true
      try {
        const res = await $fetch<{ todos: TodoPublic[] }>(
          '/api/backend/todo/',
          { query: { limit: 1000, offset: 0 } },
        )
        this.items = res.todos
        this.loaded = true
      } finally {
        this.loading = false
      }
    },

    async create(payload: TodoCreate) {
      this.saving = true
      try {
        const created = await $fetch<TodoPublic>('/api/backend/todo/', {
          method: 'POST',
          body: payload,
        })
        this.items = [created, ...this.items]
        return created
      } finally {
        this.saving = false
      }
    },

    async patch(id: number, payload: TodoUpdate) {
      const updated = await $fetch<TodoPublic>(`/api/backend/todo/${id}`, {
        method: 'PATCH',
        body: payload,
      })
      this.items = this.items.map((t) => (t.id === id ? updated : t))
      return updated
    },

    // Avança pelo fluxo curado (ver ADVANCE_FLOW em utils/states).
    async advance(todo: TodoPublic) {
      const catalog = useCatalogStore()
      const current = catalog.statusById[todo.status_id]
      const nextCode = advanceCode(current?.code ?? '')
      if (!nextCode) return todo
      const next = catalog.statusByCode[nextCode]
      if (!next || next.id === todo.status_id) return todo
      return this.patch(todo.id, { status_id: next.id })
    },

    async setStatus(id: number, status_id: number) {
      return this.patch(id, { status_id })
    },

    async remove(id: number) {
      await $fetch(`/api/backend/todo/${id}`, { method: 'DELETE' })
      this.items = this.items.filter((t) => t.id !== id)
    },

    reset() {
      this.items = []
      this.loaded = false
      this.filter = { title: '', status_id: '', category_id: '' }
    },
  },
})
