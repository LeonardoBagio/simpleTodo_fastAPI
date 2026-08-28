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
    class="grid grid-cols-2 gap-2.5 sm:grid-cols-3 lg:grid-cols-5"
    role="group"
    aria-label="Leituras por estado"
  >
    <button
      v-for="s in LIFECYCLE"
      :key="s"
      type="button"
      class="flex items-center gap-3 rounded-md border px-3 py-2.5 text-left transition-all"
      :class="
        active === s
          ? 'border-ink bg-ink text-white shadow-md'
          : 'border-black/[0.08] bg-white text-ink shadow-sm hover:-translate-y-0.5 hover:shadow-md'
      "
      :aria-pressed="active === s"
      @click="toggle(s)"
    >
      <AndonLamp :state="s" :size="12" />
      <span class="min-w-0 leading-tight">
        <span
          class="block font-head text-[9px] font-bold uppercase tracking-[0.1em]"
          :class="active === s ? 'text-white/60' : 'text-muted'"
          >{{ stateMeta(s).label }}</span
        >
        <span
          class="font-head text-xl font-black tabular-nums leading-none"
          :class="active === s ? 'text-white' : 'text-ink'"
          >{{ String(counts[s]).padStart(2, '0') }}</span
        >
      </span>
    </button>
  </div>
</template>
