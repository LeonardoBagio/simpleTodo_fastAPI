<script setup lang="ts">
import type { TodoState } from '~/types/api'

const props = defineProps<{ modelValue: TodoState }>()
const emit = defineEmits<{ (e: 'update:modelValue', s: TodoState): void }>()
</script>

<template>
  <div
    class="inline-flex overflow-hidden rounded-[5px] border border-steel-600 bg-steel-950"
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
      class="flex items-center gap-1.5 border-r border-steel-700 px-2.5 py-1.5 last:border-r-0 transition-colors"
      :class="
        props.modelValue === s
          ? 'bg-steel-700'
          : 'bg-transparent hover:bg-steel-850'
      "
      @click="emit('update:modelValue', s)"
    >
      <AndonLamp :state="s" :size="11" />
      <span
        class="engraved text-[10px]"
        :class="
          props.modelValue === s ? 'text-enamel' : 'text-enamel-faint'
        "
        >{{ stateMeta(s).label }}</span
      >
    </button>
  </div>
</template>
