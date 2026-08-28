<script setup lang="ts">
import type { TodoState } from '~/types/api'

const props = defineProps<{ modelValue: TodoState }>()
const emit = defineEmits<{ (e: 'update:modelValue', s: TodoState): void }>()
</script>

<template>
  <div
    class="inline-flex flex-wrap gap-1.5"
    role="radiogroup"
    aria-label="Definir estado"
  >
    <button
      v-for="s in LIFECYCLE"
      :key="s"
      type="button"
      role="radio"
      :aria-checked="props.modelValue === s"
      :title="stateMeta(s).label"
      class="inline-flex items-center gap-1.5 rounded-pill border px-2.5 py-1 font-head text-[10px] font-bold uppercase tracking-[0.08em] transition-colors"
      :class="
        props.modelValue === s
          ? 'border-ink bg-ink text-white'
          : 'border-black/[0.12] bg-white text-muted hover:border-black/25 hover:text-ink'
      "
      @click="emit('update:modelValue', s)"
    >
      <AndonLamp :state="s" :size="9" />
      {{ stateMeta(s).label }}
    </button>
  </div>
</template>
