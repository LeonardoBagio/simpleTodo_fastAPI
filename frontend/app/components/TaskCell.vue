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
    class="task-cell group relative rounded-md border px-4 py-3.5 transition-[transform,box-shadow,border-color] duration-200"
    :class="[
      isDoing
        ? 'border-lamp-doing/45 -translate-y-0.5 z-10'
        : 'border-steel-600 hover:border-steel-500',
      dimmed ? 'opacity-60 hover:opacity-100' : '',
    ]"
    :style="{
      background: isDoing
        ? 'linear-gradient(180deg, rgba(242,164,28,0.06), transparent 42%), #23272d'
        : 'linear-gradient(180deg, rgba(255,255,255,0.025), transparent 40%), #21252b',
      boxShadow: isDoing
        ? '0 1px 0 rgba(255,255,255,0.06) inset, 0 16px 34px -14px rgba(0,0,0,0.75), 0 0 24px -6px rgba(242,164,28,0.28)'
        : '0 1px 0 rgba(255,255,255,0.04) inset, 0 -1px 0 rgba(0,0,0,0.4) inset, 0 3px 6px rgba(0,0,0,0.3)',
    }"
  >
    <!-- panel rivets -->
    <span class="rivet absolute left-2 top-2 opacity-70" />
    <span class="rivet absolute right-2 top-2 opacity-70" />

    <div class="flex items-start gap-3.5">
      <div class="flex flex-col items-center gap-1.5 pt-0.5">
        <AndonLamp :state="todo.state" :size="16" />
        <span
          class="engraved text-[8px] leading-none"
          :style="{ color: meta.color }"
          >{{ meta.status }}</span
        >
      </div>

      <div class="min-w-0 flex-1">
        <h3
          class="font-placard text-[15px] font-semibold uppercase tracking-[0.03em] text-enamel leading-snug"
          :class="{ 'line-through decoration-lamp-done/70': todo.state === 'done' }"
        >
          {{ todo.title }}
        </h3>
        <p
          v-if="todo.description"
          class="mt-1 text-[13.5px] leading-relaxed text-enamel-dim break-words"
        >
          {{ todo.description }}
        </p>

        <div
          class="mt-2.5 flex items-center gap-3 font-mono text-[10.5px] text-enamel-faint"
        >
          <span>#{{ String(todo.id).padStart(4, '0') }}</span>
          <span class="h-2.5 w-px bg-steel-600" />
          <span>{{ fmtDate(todo.updated_at) }}</span>
        </div>
      </div>

      <!-- Quick actions -->
      <div class="flex items-center gap-1">
        <button
          v-if="!isTerminal"
          type="button"
          class="grid h-8 w-8 place-items-center rounded text-enamel-dim transition-colors hover:bg-steel-700 hover:text-lamp-doing disabled:opacity-40"
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
          class="grid h-8 w-8 place-items-center rounded text-enamel-dim transition-colors hover:bg-steel-700 hover:text-enamel"
          title="Editar tarefa"
          aria-label="Editar tarefa"
          @click="emit('edit', todo)"
        >
          <Icon name="edit" :size="16" />
        </button>
        <button
          type="button"
          class="grid h-8 w-8 place-items-center rounded text-enamel-dim transition-colors hover:bg-lamp-trash/15 hover:text-lamp-trash disabled:opacity-40"
          :disabled="busy"
          :title="todo.state === 'trash' ? 'Excluir definitivamente' : 'Enviar ao descarte'"
          aria-label="Descartar tarefa"
          @click="emit('remove', todo)"
        >
          <Icon name="trash" :size="16" />
        </button>
      </div>
    </div>

    <!-- State rail, revealed on hover/focus for precise control -->
    <div
      class="mt-3 overflow-hidden opacity-0 transition-opacity duration-150 focus-within:opacity-100 group-hover:opacity-100"
    >
      <StateSelect
        :model-value="todo.state"
        @update:model-value="(s) => emit('state', { id: todo.id, state: s })"
      />
    </div>
  </article>
</template>
