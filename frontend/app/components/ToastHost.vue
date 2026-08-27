<script setup lang="ts">
const { toasts, dismiss } = useToasts()

const lampFor: Record<string, string> = {
  ok: '#4bbd6b',
  warn: '#f2a41c',
  error: '#df5140',
}
</script>

<template>
  <div
    class="pointer-events-none fixed inset-x-0 bottom-0 z-50 flex flex-col items-center gap-2 p-4 sm:items-end sm:p-6"
    aria-live="polite"
    role="status"
  >
    <TransitionGroup name="toast">
      <div
        v-for="t in toasts"
        :key="t.id"
        class="pointer-events-auto flex max-w-sm items-center gap-3 rounded-md border border-steel-600 bg-steel-800 px-4 py-3 shadow-raised"
      >
        <span
          class="h-2.5 w-2.5 flex-none rounded-full"
          :style="{
            background: lampFor[t.kind],
            boxShadow: `0 0 8px ${lampFor[t.kind]}`,
          }"
        />
        <span class="text-sm text-enamel">{{ t.message }}</span>
        <button
          type="button"
          class="ml-auto text-enamel-faint transition-colors hover:text-enamel"
          aria-label="Fechar aviso"
          @click="dismiss(t.id)"
        >
          <Icon name="close" :size="15" />
        </button>
      </div>
    </TransitionGroup>
  </div>
</template>

<style scoped>
.toast-enter-active,
.toast-leave-active {
  transition:
    transform 0.3s cubic-bezier(0.16, 1, 0.3, 1),
    opacity 0.3s ease;
}
.toast-enter-from {
  transform: translateY(12px);
  opacity: 0;
}
.toast-leave-to {
  transform: translateY(6px);
  opacity: 0;
}
</style>
