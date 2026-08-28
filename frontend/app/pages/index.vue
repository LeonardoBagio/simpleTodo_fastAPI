<script setup lang="ts">
import type { TodoPublic } from '~/types/api'

useHead({ title: 'Simple Todo — Painel' })

const todos = useTodosStore()
const catalog = useCatalogStore()
const toast = useToasts()

const editing = ref<TodoPublic | null>(null)
const showComposer = ref(false)
const busyId = ref<number | null>(null)
const composer = ref<HTMLElement | null>(null)

function openComposer() {
  showComposer.value = true
  nextTick(() =>
    composer.value?.scrollIntoView({ behavior: 'smooth', block: 'start' }),
  )
}

function onCancel() {
  editing.value = null
  showComposer.value = false
}

await useAsyncData('catalog', () => catalog.fetch(), { server: false })
await useAsyncData('todos', () => todos.fetch(), { server: false })

// Ordena por grupo do status (A fazer → Em andamento → Concluídos) e depois
// pela edição mais recente.
const ordered = computed(() =>
  [...todos.visible].sort((a, b) => {
    const ga = catalog.statusById[a.status_id]?.group
    const gb = catalog.statusById[b.status_id]?.group
    const la = GROUP_ORDER.indexOf(ga!)
    const lb = GROUP_ORDER.indexOf(gb!)
    if (la !== lb) return la - lb
    return b.updated_at.localeCompare(a.updated_at)
  }),
)

const activeCount = computed(
  () =>
    todos.items.filter(
      (t) => catalog.statusById[t.status_id]?.group !== 'concluidos',
    ).length,
)
const doneCount = computed(
  () =>
    todos.items.filter(
      (t) => catalog.statusById[t.status_id]?.group === 'concluidos',
    ).length,
)

async function onCreate(payload: {
  title: string
  description: string
  status_id: number | null
  category_id: number | null
  issue: string | null
}) {
  try {
    await todos.create(payload)
    showComposer.value = false
    toast.ok('Tarefa adicionada.')
  } catch (err) {
    toast.error(errMessage(err))
  }
}

async function onUpdate(payload: {
  id: number
  title: string
  description: string
  status_id: number
  category_id: number | null
  issue: string | null
}) {
  const { id, ...rest } = payload
  try {
    await todos.patch(id, rest)
    editing.value = null
    toast.ok('Tarefa atualizada.')
  } catch (err) {
    toast.error(errMessage(err))
  }
}

function startEdit(t: TodoPublic) {
  editing.value = t
  nextTick(() =>
    composer.value?.scrollIntoView({ behavior: 'smooth', block: 'start' }),
  )
}

async function onAdvance(t: TodoPublic) {
  busyId.value = t.id
  try {
    const r = await todos.advance(t)
    const label = catalog.statusById[r.status_id]?.label ?? ''
    toast.ok(`#${String(t.id).padStart(4, '0')} → ${label}`)
  } catch (err) {
    toast.error(errMessage(err))
  } finally {
    busyId.value = null
  }
}

async function onSetStatus(payload: { id: number; status_id: number }) {
  busyId.value = payload.id
  try {
    await todos.setStatus(payload.id, payload.status_id)
  } catch (err) {
    toast.error(errMessage(err))
  } finally {
    busyId.value = null
  }
}

async function onRemove(t: TodoPublic) {
  busyId.value = t.id
  try {
    await todos.remove(t.id)
    toast.warn(`Tarefa #${String(t.id).padStart(4, '0')} excluída.`)
    if (editing.value?.id === t.id) editing.value = null
  } catch (err) {
    toast.error(errMessage(err))
  } finally {
    busyId.value = null
  }
}

// Proxies para os dropdowns coloridos: null = "todos" (filtro vazio '').
const statusFilter = computed({
  get: () => (todos.filter.status_id === '' ? null : todos.filter.status_id),
  set: (v: number | null) => (todos.filter.status_id = v ?? ''),
})
const categoryFilter = computed({
  get: () =>
    todos.filter.category_id === '' ? null : todos.filter.category_id,
  set: (v: number | null) => (todos.filter.category_id = v ?? ''),
})
</script>

<template>
  <div class="flex flex-col gap-8">
    <!-- Section heading -->
    <div>
      <h1 class="section-title text-[clamp(1.6rem,1.2rem+1.6vw,2.2rem)]">
        Painel de tarefas
      </h1>
      <span class="divider mt-3" />
      <p class="section-desc mt-3">
        {{ activeCount }} ativa(s) · {{ doneCount }} concluída(s) ·
        {{ todos.items.length }} no total
      </p>
    </div>

    <!-- Composer -->
    <div v-if="showComposer || editing" ref="composer">
      <TaskComposer
        :editing="editing"
        :busy="todos.saving"
        @create="onCreate"
        @update="onUpdate"
        @cancel="onCancel"
      />
    </div>
    <div v-else>
      <button type="button" class="btn btn-primary text-sm" @click="openComposer">
        <Icon name="plus" :size="16" /> Nova tarefa
      </button>
    </div>

    <!-- Controls: search + two filter selects (andamento, categoria) -->
    <div class="flex flex-col gap-3 sm:flex-row sm:items-end">
      <div class="relative sm:max-w-xs sm:flex-1">
        <span class="pointer-events-none absolute left-3 top-1/2 -translate-y-1/2 text-muted">
          <Icon name="search" :size="16" />
        </span>
        <input
          v-model="todos.filter.title"
          class="field pl-9"
          type="search"
          placeholder="Localizar tarefa…"
          aria-label="Filtrar por título"
        />
      </div>

      <StateSelect
        v-model="statusFilter"
        all-label="Todos os andamentos"
        class="w-full sm:w-auto"
      />

      <CategorySelect
        v-model="categoryFilter"
        all-label="Todas as categorias"
        class="w-full sm:w-auto"
      />
    </div>

    <!-- Board -->
    <section aria-label="Tarefas">
      <!-- Loading -->
      <div
        v-if="todos.loading && !todos.loaded"
        class="grid gap-5 [grid-template-columns:repeat(auto-fill,minmax(280px,1fr))]"
      >
        <div
          v-for="i in 6"
          :key="i"
          class="h-44 animate-pulse rounded-md border border-black/[0.06] bg-white/70"
        />
      </div>

      <!-- Empty -->
      <div
        v-else-if="ordered.length === 0"
        class="card flex flex-col items-center gap-3 px-6 py-16 text-center"
      >
        <span class="divider" />
        <p class="section-title text-lg">
          {{ todos.items.length === 0 ? 'Sem tarefas ainda' : 'Nada no filtro' }}
        </p>
        <p class="max-w-xs text-sm text-muted">
          {{
            todos.items.length === 0
              ? 'Clique em “Nova tarefa” acima para adicionar a primeira.'
              : 'Ajuste a busca ou limpe os filtros para ver todas as tarefas.'
          }}
        </p>
        <button
          v-if="todos.items.length > 0"
          type="button"
          class="btn btn-outline mt-1 text-xs"
          @click="
            (todos.filter.status_id = ''),
              (todos.filter.category_id = ''),
              (todos.filter.title = '')
          "
        >
          <Icon name="reset" :size="15" /> Limpar filtros
        </button>
      </div>

      <!-- Grid -->
      <div
        v-else
        class="grid items-start gap-5 [grid-template-columns:repeat(auto-fill,minmax(280px,1fr))]"
      >
        <TaskCell
          v-for="(t, i) in ordered"
          :key="t.id"
          v-reveal="Math.min(i * 55, 330)"
          :todo="t"
          :busy="busyId === t.id"
          @advance="onAdvance"
          @state="onSetStatus"
          @edit="startEdit"
          @remove="onRemove"
        />
      </div>
    </section>
  </div>
</template>
