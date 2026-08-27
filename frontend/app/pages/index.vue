<script setup lang="ts">
import type { TodoPublic, TodoState } from '~/types/api'

useHead({ title: 'Simple Todo — Painel' })

const todos = useTodosStore()
const toast = useToasts()

const editing = ref<TodoPublic | null>(null)
const busyId = ref<number | null>(null)
const composer = ref<HTMLElement | null>(null)

await useAsyncData('todos', () => todos.fetch(), { server: false })

// Board order: active work first (see BOARD_ORDER), then most-recently touched.
const ordered = computed(() =>
  [...todos.visible].sort((a, b) => {
    const la = BOARD_ORDER.indexOf(a.state)
    const lb = BOARD_ORDER.indexOf(b.state)
    if (la !== lb) return la - lb
    return b.updated_at.localeCompare(a.updated_at)
  }),
)

const activeCount = computed(
  () => todos.counts.draft + todos.counts.todo + todos.counts.doing,
)

async function onCreate(payload: {
  title: string
  description: string
  state: TodoState
}) {
  try {
    await todos.create(payload)
    toast.ok('Ordem registrada no painel.')
  } catch (err) {
    toast.error(errMessage(err))
  }
}

async function onUpdate(payload: {
  id: number
  title: string
  description: string
  state: TodoState
}) {
  const { id, ...rest } = payload
  try {
    await todos.patch(id, rest)
    editing.value = null
    toast.ok('Ordem atualizada.')
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
    toast.ok(`#${String(t.id).padStart(4, '0')} → ${stateMeta(r.state).label}`)
  } catch (err) {
    toast.error(errMessage(err))
  } finally {
    busyId.value = null
  }
}

async function onSetState(payload: { id: number; state: TodoState }) {
  busyId.value = payload.id
  try {
    await todos.setState(payload.id, payload.state)
  } catch (err) {
    toast.error(errMessage(err))
  } finally {
    busyId.value = null
  }
}

async function onRemove(t: TodoPublic) {
  busyId.value = t.id
  try {
    if (t.state === 'trash') {
      await todos.remove(t.id)
      toast.warn(`Ordem #${String(t.id).padStart(4, '0')} excluída.`)
    } else {
      await todos.setState(t.id, 'trash')
      toast.warn('Ordem enviada ao descarte.')
    }
    if (editing.value?.id === t.id) editing.value = null
  } catch (err) {
    toast.error(errMessage(err))
  } finally {
    busyId.value = null
  }
}
</script>

<template>
  <div class="flex flex-col gap-6">
    <!-- Console heading -->
    <div class="flex flex-wrap items-end justify-between gap-3">
      <div>
        <h1 class="font-placard text-2xl font-bold uppercase tracking-[0.02em] text-enamel">
          Painel de operações
        </h1>
        <p class="mt-1 font-mono text-xs text-enamel-faint">
          {{ activeCount }} ordem(ns) ativa(s) · {{ todos.counts.done }} concluída(s)
        </p>
      </div>
    </div>

    <!-- Composer -->
    <div ref="composer">
      <TaskComposer
        :editing="editing"
        :busy="todos.saving"
        @create="onCreate"
        @update="onUpdate"
        @cancel="editing = null"
      />
    </div>

    <!-- Controls: search + status ribbon -->
    <div class="flex flex-col gap-3 lg:flex-row lg:items-stretch">
      <div class="relative lg:w-64">
        <span class="pointer-events-none absolute left-3 top-1/2 -translate-y-1/2 text-enamel-faint">
          <Icon name="search" :size="16" />
        </span>
        <input
          v-model="todos.filter.title"
          class="field pl-9"
          type="search"
          placeholder="Localizar ordem…"
          aria-label="Filtrar por título"
        />
      </div>
      <div class="min-w-0 flex-1">
        <StatusRibbon
          :counts="todos.counts"
          :active="todos.filter.state"
          @select="(s) => (todos.filter.state = s)"
        />
      </div>
    </div>

    <!-- Board -->
    <section aria-label="Ordens de serviço">
      <!-- Loading -->
      <div v-if="todos.loading && !todos.loaded" class="grid gap-3 sm:grid-cols-2">
        <div
          v-for="i in 4"
          :key="i"
          class="h-28 animate-pulse rounded-md border border-steel-700 bg-steel-850"
        />
      </div>

      <!-- Empty -->
      <div
        v-else-if="ordered.length === 0"
        class="plate flex flex-col items-center gap-3 px-6 py-14 text-center"
      >
        <div class="hazard-rule h-2 w-24 rounded-sm opacity-80" />
        <p class="font-placard text-lg uppercase tracking-wide text-enamel">
          {{ todos.items.length === 0 ? 'Painel sem ordens' : 'Nenhuma ordem no filtro' }}
        </p>
        <p class="max-w-xs text-sm text-enamel-dim">
          {{
            todos.items.length === 0
              ? 'Registre a primeira ordem de serviço no compositor acima para acender o painel.'
              : 'Ajuste a busca ou limpe o filtro de estado para ver todas as ordens.'
          }}
        </p>
        <button
          v-if="todos.items.length > 0"
          type="button"
          class="btn-console btn-steel text-xs"
          @click="(todos.filter.state = ''), (todos.filter.title = '')"
        >
          <Icon name="reset" :size="15" /> Limpar filtros
        </button>
      </div>

      <!-- Grid -->
      <div v-else class="grid items-start gap-3 sm:grid-cols-2">
        <TaskCell
          v-for="t in ordered"
          :key="t.id"
          :todo="t"
          :busy="busyId === t.id"
          @advance="onAdvance"
          @state="onSetState"
          @edit="startEdit"
          @remove="onRemove"
        />
      </div>
    </section>
  </div>
</template>
