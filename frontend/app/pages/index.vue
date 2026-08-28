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
  <div class="flex flex-col gap-8">
    <!-- Section heading -->
    <div>
      <h1 class="section-title text-[clamp(1.6rem,1.2rem+1.6vw,2.2rem)]">
        Painel de tarefas
      </h1>
      <span class="divider mt-3" />
      <p class="section-desc mt-3">
        {{ activeCount }} ativa(s) · {{ todos.counts.done }} concluída(s) ·
        {{ todos.items.length }} no total
      </p>
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
    <div class="flex flex-col gap-4">
      <div class="relative sm:max-w-xs">
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
      <StatusRibbon
        :counts="todos.counts"
        :active="todos.filter.state"
        @select="(s) => (todos.filter.state = s)"
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
          class="h-40 animate-pulse rounded-md border border-black/[0.06] bg-white/70"
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
              ? 'Adicione a primeira tarefa no formulário acima para começar.'
              : 'Ajuste a busca ou limpe o filtro de estado para ver todas as tarefas.'
          }}
        </p>
        <button
          v-if="todos.items.length > 0"
          type="button"
          class="btn btn-outline mt-1 text-xs"
          @click="(todos.filter.state = ''), (todos.filter.title = '')"
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
          @state="onSetState"
          @edit="startEdit"
          @remove="onRemove"
        />
      </div>
    </section>
  </div>
</template>
