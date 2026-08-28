<script setup lang="ts">
import type { TodoPublic } from '~/types/api'

const props = defineProps<{ editing: TodoPublic | null; busy?: boolean }>()
const emit = defineEmits<{
  (
    e: 'create',
    payload: {
      title: string
      description: string
      status_id: number | null
      category_id: number | null
      issue: string | null
    },
  ): void
  (
    e: 'update',
    payload: {
      id: number
      title: string
      description: string
      status_id: number
      category_id: number | null
      issue: string | null
    },
  ): void
  (e: 'cancel'): void
}>()

const catalog = useCatalogStore()

const title = ref('')
const description = ref('')
const statusId = ref<number | null>(null)
const categoryId = ref<number | null>(null)
const issue = ref('')
const titleEl = ref<HTMLInputElement | null>(null)

watch(
  () => props.editing,
  (t) => {
    if (t) {
      title.value = t.title
      description.value = t.description
      statusId.value = t.status_id
      categoryId.value = t.category_id
      issue.value = t.issue ?? ''
      nextTick(() => titleEl.value?.focus())
    } else {
      reset()
    }
  },
)

// Pré-seleciona "Não iniciada" ao criar, assim que o catálogo carrega.
watchEffect(() => {
  if (
    !props.editing &&
    statusId.value == null &&
    catalog.defaultStatusId != null
  ) {
    statusId.value = catalog.defaultStatusId
  }
})

function reset() {
  title.value = ''
  description.value = ''
  statusId.value = catalog.defaultStatusId
  categoryId.value = null
  issue.value = ''
}

function submit() {
  const t = title.value.trim()
  if (!t) {
    titleEl.value?.focus()
    return
  }
  const base = {
    title: t,
    description: description.value.trim(),
    category_id: categoryId.value,
    issue: issue.value.trim() || null,
  }
  if (props.editing) {
    emit('update', {
      id: props.editing.id,
      status_id: statusId.value ?? props.editing.status_id,
      ...base,
    })
  } else {
    emit('create', { status_id: statusId.value, ...base })
    reset()
    titleEl.value?.focus()
  }
}
</script>

<template>
  <form
    class="card p-5 sm:p-6 transition-shadow"
    :class="editing ? 'ring-1 ring-ink/25' : ''"
    @submit.prevent="submit"
  >
    <div class="mb-4">
      <h2 class="engraved text-[11px] text-muted">
        {{ editing ? `Editando tarefa #${String(editing.id).padStart(4, '0')}` : 'Nova tarefa' }}
      </h2>
      <span class="divider mt-2" />
    </div>

    <div class="flex flex-col gap-3">
      <input
        ref="titleEl"
        v-model="title"
        class="field font-head text-[15px] font-bold uppercase tracking-[0.02em]"
        type="text"
        maxlength="120"
        placeholder="Título da tarefa"
        aria-label="Título da tarefa"
      />
      <textarea
        v-model="description"
        class="field min-h-[64px] resize-y text-sm"
        placeholder="Descrição / detalhes (opcional)"
        aria-label="Descrição da tarefa"
      />

      <div class="flex flex-wrap items-start gap-x-6 gap-y-3">
        <div class="flex flex-col gap-1.5">
          <span class="engraved text-[9px] text-muted">Andamento</span>
          <StateSelect v-model="statusId" />
        </div>
        <div class="flex flex-col gap-1.5">
          <span class="engraved text-[9px] text-muted">Categoria</span>
          <CategorySelect v-model="categoryId" />
        </div>
        <div class="flex flex-col gap-1.5">
          <span class="engraved text-[9px] text-muted">Issue</span>
          <input
            v-model="issue"
            class="field !w-40 !py-1.5 text-sm"
            type="text"
            maxlength="40"
            placeholder="#3159 / GH-12"
            aria-label="Issue"
          />
        </div>
      </div>

      <div class="flex items-center justify-end gap-2">
        <button
          type="button"
          class="btn btn-outline text-xs"
          @click="emit('cancel')"
        >
          Cancelar
        </button>
        <button type="submit" class="btn btn-primary text-sm" :disabled="busy">
          <Icon :name="editing ? 'check' : 'plus'" :size="16" />
          {{ editing ? 'Salvar' : 'Adicionar' }}
        </button>
      </div>
    </div>
  </form>
</template>
