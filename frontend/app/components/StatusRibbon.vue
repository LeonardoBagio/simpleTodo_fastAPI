<script setup lang="ts">
import type { TodoState } from '~/types/api'

const props = defineProps<{
  counts: Record<TodoState, number>
  active: TodoState | ''
}>()
const emit = defineEmits<{ (e: 'select', s: TodoState | ''): void }>()

function toggle(s: TodoState) {
  emit('select', props.active === s ? '' : s)
}
</script>

<template>
  <div
    class="plate flex flex-wrap items-stretch gap-px overflow-hidden p-px"
    role="group"
    aria-label="Leituras por estado"
  >
    <button
      v-for="s in LIFECYCLE"
      :key="s"
      type="button"
      class="group flex min-w-[92px] flex-1 items-center gap-2.5 px-3 py-2 text-left transition-colors"
      :class="
        active === s
          ? 'bg-steel-700'
          : 'bg-steel-850 hover:bg-steel-800'
      "
      :aria-pressed="active === s"
      @click="toggle(s)"
    >
      <AndonLamp :state="s" :size="13" />
      <span class="leading-tight">
        <span class="engraved block text-[10px] text-enamel-faint">{{
          stateMeta(s).label
        }}</span>
        <span
          class="font-mono text-lg tabular-nums leading-none"
          :class="active === s ? 'text-enamel' : 'text-enamel-dim'"
          >{{ String(counts[s]).padStart(2, '0') }}</span
        >
      </span>
    </button>
  </div>
</template>
