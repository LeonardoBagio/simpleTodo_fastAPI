<script setup lang="ts">
import type { TodoState } from '~/types/api'

const props = withDefaults(
  defineProps<{ state: TodoState; size?: number }>(),
  { size: 14 },
)

const meta = computed(() => stateMeta(props.state))
</script>

<template>
  <span
    class="andon-lamp"
    :class="{ 'is-lit': meta.lit, 'is-pulse': meta.pulse }"
    :style="{
      '--lamp': meta.color,
      '--d': size + 'px',
    }"
    role="img"
    :aria-label="`Estado: ${meta.label}`"
  />
</template>

<style scoped>
.andon-lamp {
  display: inline-block;
  width: var(--d);
  height: var(--d);
  border-radius: 9999px;
  background: radial-gradient(
    circle at 34% 30%,
    color-mix(in srgb, var(--lamp) 55%, #000) 0%,
    color-mix(in srgb, var(--lamp) 30%, #000) 60%,
    #0c0e11 100%
  );
  /* Dark recessed bezel around an unlit lamp */
  box-shadow:
    0 0 0 1px rgba(0, 0, 0, 0.6),
    0 1px 1px rgba(0, 0, 0, 0.5) inset;
  flex: none;
}

.andon-lamp.is-lit {
  background: radial-gradient(
    circle at 34% 30%,
    #fff 0%,
    var(--lamp) 34%,
    color-mix(in srgb, var(--lamp) 60%, #000) 100%
  );
  box-shadow:
    0 0 0 1px rgba(0, 0, 0, 0.55),
    0 0 6px 1px color-mix(in srgb, var(--lamp) 70%, transparent),
    0 0 14px 2px color-mix(in srgb, var(--lamp) 40%, transparent);
}

.andon-lamp.is-pulse {
  animation: lamp-flicker 1.6s cubic-bezier(0.4, 0, 0.6, 1) infinite;
}

@keyframes lamp-flicker {
  0%,
  100% {
    box-shadow:
      0 0 0 1px rgba(0, 0, 0, 0.55),
      0 0 7px 1px color-mix(in srgb, var(--lamp) 75%, transparent),
      0 0 18px 3px color-mix(in srgb, var(--lamp) 50%, transparent);
  }
  50% {
    box-shadow:
      0 0 0 1px rgba(0, 0, 0, 0.55),
      0 0 4px 0 color-mix(in srgb, var(--lamp) 45%, transparent),
      0 0 9px 1px color-mix(in srgb, var(--lamp) 22%, transparent);
  }
}

@media (prefers-reduced-motion: reduce) {
  .andon-lamp.is-pulse {
    animation: none;
  }
}
</style>
