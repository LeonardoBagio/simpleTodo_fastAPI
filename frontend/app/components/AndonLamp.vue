<script setup lang="ts">
// Ponto de estado genérico: a cor vem do cadastro (catalog). Pulsa quando
// `pulse` (usado no status "Em andamento").
withDefaults(
  defineProps<{ color: string; size?: number; pulse?: boolean }>(),
  { size: 10, pulse: false },
)
</script>

<template>
  <span
    class="status-dot"
    :class="{ 'is-pulse': pulse }"
    :style="{ '--lamp': color, '--d': size + 'px' }"
    role="img"
  />
</template>

<style scoped>
.status-dot {
  display: inline-block;
  width: var(--d);
  height: var(--d);
  border-radius: 9999px;
  background: radial-gradient(
    circle at 34% 30%,
    color-mix(in srgb, var(--lamp) 55%, #fff) 0%,
    var(--lamp) 70%
  );
  box-shadow:
    inset 0 0 0 1px color-mix(in srgb, var(--lamp) 80%, transparent),
    0 0 5px 0 color-mix(in srgb, var(--lamp) 35%, transparent);
  flex: none;
}

.status-dot.is-pulse {
  animation: dot-flicker 1.6s cubic-bezier(0.4, 0, 0.6, 1) infinite;
}

@keyframes dot-flicker {
  0%,
  100% {
    box-shadow:
      inset 0 0 0 1px color-mix(in srgb, var(--lamp) 80%, transparent),
      0 0 8px 2px color-mix(in srgb, var(--lamp) 55%, transparent);
  }
  50% {
    box-shadow:
      inset 0 0 0 1px color-mix(in srgb, var(--lamp) 80%, transparent),
      0 0 3px 0 color-mix(in srgb, var(--lamp) 25%, transparent);
  }
}

@media (prefers-reduced-motion: reduce) {
  .status-dot.is-pulse {
    animation: none;
  }
}
</style>
