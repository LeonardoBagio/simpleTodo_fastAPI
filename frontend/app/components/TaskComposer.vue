<script setup lang="ts">
import type { TodoPublic, TodoState } from '~/types/api'

const props = defineProps<{ editing: TodoPublic | null; busy?: boolean }>()
const emit = defineEmits<{
  (e: 'create', payload: { title: string; description: string; state: TodoState }): void
  (e: 'update', payload: { id: number; title: string; description: string; state: TodoState }): void
  (e: 'cancel'): void
}>()

const title = ref('')
const description = ref('')
const state = ref<TodoState>('todo')
const titleEl = ref<HTMLInputElement | null>(null)

watch(
  () => props.editing,
  (t) => {
    if (t) {
      title.value = t.title
      description.value = t.description
      state.value = t.state
      nextTick(() => titleEl.value?.focus())
    } else {
      reset()
    }
  },
)

function reset() {
  title.value = ''
  description.value = ''
  state.value = 'todo'
}

function submit() {
  const t = title.value.trim()
  if (!t) {
    titleEl.value?.focus()
    return
  }
  const payload = {
    title: t,
    description: description.value.trim(),
    state: state.value,
  }
  if (props.editing) {
    emit('update', { id: props.editing.id, ...payload })
  } else {
    emit('create', payload)
    reset()
    titleEl.value?.focus()
  }
}
</script>

<template>
  <form
    class="plate p-4 sm:p-5"
    :class="editing ? 'ring-1 ring-lamp-doing/40' : ''"
    @submit.prevent="submit"
  >
    <div class="mb-3 flex items-center gap-2">
      <span class="hazard-rule h-3 w-8 rounded-sm" />
      <h2 class="engraved text-xs text-enamel-dim">
        {{ editing ? `Editando ordem #${String(editing.id).padStart(4, '0')}` : 'Nova ordem de serviço' }}
      </h2>
    </div>

    <div class="flex flex-col gap-3">
      <input
        ref="titleEl"
        v-model="title"
        class="field font-placard text-[15px] uppercase tracking-[0.03em]"
        type="text"
        maxlength="120"
        placeholder="Título da tarefa"
        aria-label="Título da tarefa"
      />
      <textarea
        v-model="description"
        class="field min-h-[64px] resize-y text-sm"
        placeholder="Descrição / detalhes operacionais (opcional)"
        aria-label="Descrição da tarefa"
      />

      <div class="flex flex-wrap items-center justify-between gap-3">
        <div class="flex flex-col gap-1.5">
          <span class="engraved text-[9px] text-enamel-faint">Estado inicial</span>
          <StateSelect v-model="state" />
        </div>

        <div class="flex items-center gap-2">
          <button
            v-if="editing"
            type="button"
            class="btn-console btn-steel text-xs"
            @click="emit('cancel')"
          >
            Cancelar
          </button>
          <button
            type="submit"
            class="btn-console btn-amber text-sm"
            :disabled="busy"
          >
            <Icon :name="editing ? 'check' : 'plus'" :size="16" />
            {{ editing ? 'Salvar' : 'Registrar' }}
          </button>
        </div>
      </div>
    </div>
  </form>
</template>
