<script setup lang="ts">
import type { TodoPublic } from '~/types/api'

const props = defineProps<{ todo: TodoPublic; busy?: boolean }>()
const emit = defineEmits<{
  (e: 'advance', t: TodoPublic): void
  (e: 'state', payload: { id: number; status_id: number }): void
  (e: 'edit', t: TodoPublic): void
  (e: 'remove', t: TodoPublic): void
}>()

const catalog = useCatalogStore()

const status = computed(() => catalog.statusById[props.todo.status_id])
const category = computed(() =>
  props.todo.category_id != null
    ? catalog.categoryById[props.todo.category_id]
    : undefined,
)

const isActive = computed(() => status.value?.group === 'em_andamento')
const isDone = computed(() => status.value?.code === 'concluido')

// Próximo passo do fluxo de avanço (null quando já concluído).
const nextCode = computed(() => advanceCode(status.value?.code ?? ''))
const nextLabel = computed(() =>
  nextCode.value ? catalog.statusByCode[nextCode.value]?.label : '',
)

const confirming = ref(false)

const accent = computed(() => status.value?.color ?? '#999999')
</script>

<template>
  <article
    class="group relative rounded-md border bg-surface p-5 transition-all duration-300"
    :class="[
      isActive
        ? '-translate-y-0.5'
        : 'card-lift border-black/[0.07] shadow-sm hover:-translate-y-1',
    ]"
    :style="
      isActive
        ? {
            borderColor: accent + '80',
            background: `linear-gradient(180deg, ${accent}14, #ffffff 55%)`,
            boxShadow: `0 16px 36px -16px rgba(0,0,0,0.18), 0 0 22px -8px ${accent}80`,
          }
        : {}
    "
  >
    <!-- Header: inline status dropdown + quick actions -->
    <div class="flex items-start justify-between gap-3">
      <StateSelect
        :model-value="todo.status_id"
        @update:model-value="(id) => emit('state', { id: todo.id, status_id: id })"
      />

      <div v-if="!confirming" class="flex items-center gap-1">
        <button
          v-if="nextCode"
          type="button"
          class="grid h-8 w-8 place-items-center rounded-md text-muted transition-colors hover:bg-cloud hover:text-ink disabled:opacity-40"
          :disabled="busy"
          :title="`Avançar para ${nextLabel}`"
          aria-label="Avançar status"
          @click="emit('advance', todo)"
        >
          <Icon name="arrow" :size="17" />
        </button>
        <button
          type="button"
          class="grid h-8 w-8 place-items-center rounded-md text-muted transition-colors hover:bg-cloud hover:text-ink"
          title="Editar tarefa"
          aria-label="Editar tarefa"
          @click="emit('edit', todo)"
        >
          <Icon name="edit" :size="16" />
        </button>
        <button
          type="button"
          class="grid h-8 w-8 place-items-center rounded-md text-muted transition-colors hover:bg-lamp-trash/10 hover:text-lamp-trash disabled:opacity-40"
          :disabled="busy"
          title="Excluir tarefa"
          aria-label="Excluir tarefa"
          @click="confirming = true"
        >
          <Icon name="trash" :size="16" />
        </button>
      </div>

      <!-- Confirmação de exclusão (hard-delete) -->
      <div v-else class="flex items-center gap-1.5">
        <span class="engraved text-[9px] text-muted">Excluir?</span>
        <button
          type="button"
          class="rounded-md px-2 py-1 font-head text-[10px] font-bold uppercase tracking-[0.06em] text-white"
          style="background: #df5140"
          :disabled="busy"
          @click="emit('remove', todo)"
        >
          Sim
        </button>
        <button
          type="button"
          class="rounded-md border border-black/15 px-2 py-1 font-head text-[10px] font-bold uppercase tracking-[0.06em] text-muted hover:text-ink"
          @click="confirming = false"
        >
          Não
        </button>
      </div>
    </div>

    <!-- Title + description -->
    <h3
      class="mt-3.5 font-head text-[16px] font-bold uppercase tracking-[0.02em] leading-snug"
      :class="isDone ? 'text-muted line-through decoration-lamp-done/70' : 'text-ink'"
    >
      {{ todo.title }}
    </h3>
    <p
      v-if="todo.description"
      class="mt-1.5 text-sm leading-relaxed text-muted break-words"
    >
      {{ todo.description }}
    </p>

    <!-- Footer: category + issue ... last edit -->
    <div class="mt-4 flex flex-wrap items-center gap-x-3 gap-y-2">
      <span
        v-if="category"
        class="inline-flex items-center rounded-pill px-2.5 py-0.5 font-head text-[11px] font-semibold text-white"
        :style="{ background: category.color }"
        >{{ category.label }}</span
      >
      <span
        v-if="todo.issue"
        class="inline-flex items-center rounded-pill bg-cloud px-2.5 py-0.5 font-head text-[11px] font-bold text-ink"
        >{{ todo.issue.startsWith('#') ? todo.issue : `#${todo.issue}` }}</span
      >
      <span
        class="ml-auto font-head text-[11px] font-semibold tabular-nums text-muted"
        :title="`Última edição: ${fmtDate(todo.updated_at)}`"
        >{{ fmtDate(todo.updated_at) }}</span
      >
    </div>
  </article>
</template>
