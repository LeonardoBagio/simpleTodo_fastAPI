import { defineStore } from 'pinia'
import type { Category, Status, StatusGroup } from '~/types/api'

// Cadastros globais (Status e Categoria). Buscados uma vez e reutilizados
// para mapear os ids das tarefas em label/cor/grupo.
export const useCatalogStore = defineStore('catalog', {
  state: () => ({
    statuses: [] as Status[],
    categories: [] as Category[],
    loaded: false,
  }),
  getters: {
    statusById(state): Record<number, Status> {
      return Object.fromEntries(state.statuses.map((s) => [s.id, s]))
    },
    categoryById(state): Record<number, Category> {
      return Object.fromEntries(state.categories.map((c) => [c.id, c]))
    },
    statusByCode(state): Record<string, Status> {
      return Object.fromEntries(state.statuses.map((s) => [s.code, s]))
    },
    // Status agrupados na ordem do ciclo de vida, para o dropdown agrupado.
    statusesByGroup(): { group: StatusGroup; label: string; items: Status[] }[] {
      return GROUP_ORDER.map((group) => ({
        group,
        label: GROUP_LABEL[group],
        items: this.statuses
          .filter((s) => s.group === group)
          .sort((a, b) => a.sort_order - b.sort_order),
      })).filter((g) => g.items.length > 0)
    },
    defaultStatusId(): number | null {
      const first = this.statusByCode['nao_iniciada']
      return first ? first.id : (this.statuses[0]?.id ?? null)
    },
  },
  actions: {
    async fetch() {
      if (this.loaded) return
      const [statuses, categories] = await Promise.all([
        $fetch<{ statuses: Status[] }>('/api/backend/catalog/statuses'),
        $fetch<{ categories: Category[] }>('/api/backend/catalog/categories'),
      ])
      this.statuses = statuses.statuses
      this.categories = categories.categories
      this.loaded = true
    },
    reset() {
      this.statuses = []
      this.categories = []
      this.loaded = false
    },
  },
})
