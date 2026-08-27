import { defineStore } from 'pinia'
import type {
  TodoCreate,
  TodoPublic,
  TodoState,
  TodoUpdate,
} from '~/types/api'

interface Filter {
  title: string
  state: TodoState | ''
}

export const useTodosStore = defineStore('todos', {
  state: () => ({
    items: [] as TodoPublic[],
    loading: false,
    saving: false,
    loaded: false,
    filter: { title: '', state: '' } as Filter,
  }),
  getters: {
    // Board rows in lifecycle order, honoring the active filter.
    visible(state): TodoPublic[] {
      return state.items.filter((t) => {
        if (state.filter.state && t.state !== state.filter.state) return false
        if (
          state.filter.title &&
          !t.title.toLowerCase().includes(state.filter.title.toLowerCase())
        )
          return false
        return true
      })
    },
    counts(state): Record<TodoState, number> {
      const base: Record<TodoState, number> = {
        draft: 0,
        todo: 0,
        doing: 0,
        done: 0,
        trash: 0,
      }
      for (const t of state.items) base[t.state]++
      return base
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

    async advance(todo: TodoPublic) {
      const order: TodoState[] = ['draft', 'todo', 'doing', 'done']
      const idx = order.indexOf(todo.state)
      const next = idx >= 0 && idx < order.length - 1 ? order[idx + 1] : 'done'
      return this.patch(todo.id, { state: next })
    },

    async setState(id: number, state: TodoState) {
      return this.patch(id, { state })
    },

    async remove(id: number) {
      await $fetch(`/api/backend/todo/${id}`, { method: 'DELETE' })
      this.items = this.items.filter((t) => t.id !== id)
    },

    reset() {
      this.items = []
      this.loaded = false
      this.filter = { title: '', state: '' }
    },
  },
})
