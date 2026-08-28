<script setup lang="ts">
import type { TodoPublic, TodoState } from '~/types/api'

const props = defineProps<{ todo: TodoPublic; busy?: boolean }>()
const emit = defineEmits<{
  (e: 'advance', t: TodoPublic): void
  (e: 'state', payload: { id: number; state: TodoState }): void
  (e: 'edit', t: TodoPublic): void
  (e: 'remove', t: TodoPublic): void
}>()

const meta = computed(() => stateMeta(props.todo.state))
const isDoing = computed(() => props.todo.state === 'doing')
const isTerminal = computed(
  () => props.todo.state === 'done' || props.todo.state === 'trash',
)
const dimmed = computed(() => props.todo.state === 'trash')
</script>

<template>
  <article
    class="group relative rounded-md border bg-surface p-5 transition-all duration-300"
    :class="[
      isDoing
        ? 'border-lamp-doing/60 -translate-y-0.5'
        : 'card-lift border-black/[0.07] shadow-sm',
      dimmed ? 'opacity-55 hover:opacity-100' : '',
    ]"
    :style="
      isDoing
        ? {
            background:
              'linear-gradient(180deg, rgba(242,164,28,0.09), #ffffff 55%)',
            boxShadow:
              '0 18px 40px -16px rgba(0,0,0,0.18), 0 0 26px -8px rgba(242,164,28,0.5)',
          }
        : {}
    "
  >
    <!-- Header: state badge + quick actions -->
    <div class="flex items-start justify-between gap-3">
      <span class="pill" :title="meta.label">
        <AndonLamp :state="todo.state" :size="9" />
        {{ meta.status }}
      </span>

      <div class="flex items-center gap-1">
        <button
          v-if="!isTerminal"
          type="button"
          class="grid h-8 w-8 place-items-center rounded-md text-muted transition-colors hover:bg-cloud hover:text-ink disabled:opacity-40"
          :disabled="busy"
          :title="`Avançar para ${
            stateMeta(
              todo.state === 'draft'
                ? 'todo'
                : todo.state === 'todo'
                  ? 'doing'
                  : 'done',
            ).label
          }`"
          aria-label="Avançar estado"
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
          :title="todo.state === 'trash' ? 'Excluir definitivamente' : 'Enviar ao descarte'"
          aria-label="Descartar tarefa"
          @click="emit('remove', todo)"
        >
          <Icon name="trash" :size="16" />
        </button>
      </div>
    </div>

    <!-- Title + description -->
    <h3
      class="mt-4 font-head text-[16px] font-bold uppercase tracking-[0.02em] leading-snug"
      :class="
        todo.state === 'done'
          ? 'text-muted line-through decoration-lamp-done/70'
          : 'text-ink'
      "
    >
      {{ todo.title }}
    </h3>
    <p
      v-if="todo.description"
      class="mt-1.5 text-sm leading-relaxed text-muted break-words"
    >
      {{ todo.description }}
    </p>

    <!-- Meta -->
    <div class="mt-4 flex items-center gap-3 text-[11px] text-muted">
      <span class="font-head font-bold tracking-wide tabular-nums"
        >#{{ String(todo.id).padStart(4, '0') }}</span
      >
      <span class="h-3 w-px bg-black/10" />
      <span>{{ fmtDate(todo.updated_at) }}</span>
    </div>

    <!-- State rail, revealed on hover/focus for precise control -->
    <div
      class="mt-4 overflow-hidden opacity-0 transition-opacity duration-150 focus-within:opacity-100 group-hover:opacity-100"
    >
      <StateSelect
        :model-value="todo.state"
        @update:model-value="(s) => emit('state', { id: todo.id, state: s })"
      />
    </div>
  </article>
</template>
