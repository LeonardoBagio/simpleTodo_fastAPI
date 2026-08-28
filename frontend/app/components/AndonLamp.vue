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
/* Clean colour dot on a light surface. Unlit (draft) reads as a hollow,
   muted ring; lit states fill in with a soft glow; doing pulses. */
.andon-lamp {
  display: inline-block;
  width: var(--d);
  height: var(--d);
  border-radius: 9999px;
  background: color-mix(in srgb, var(--lamp) 22%, #fff);
  box-shadow: inset 0 0 0 1.5px color-mix(in srgb, var(--lamp) 55%, transparent);
  flex: none;
}

.andon-lamp.is-lit {
  background: radial-gradient(
    circle at 34% 30%,
    color-mix(in srgb, var(--lamp) 55%, #fff) 0%,
    var(--lamp) 70%
  );
  box-shadow:
    inset 0 0 0 1px color-mix(in srgb, var(--lamp) 80%, transparent),
    0 0 6px 1px color-mix(in srgb, var(--lamp) 40%, transparent);
}

.andon-lamp.is-pulse {
  animation: lamp-flicker 1.6s cubic-bezier(0.4, 0, 0.6, 1) infinite;
}

@keyframes lamp-flicker {
  0%,
  100% {
    box-shadow:
      inset 0 0 0 1px color-mix(in srgb, var(--lamp) 80%, transparent),
      0 0 8px 2px color-mix(in srgb, var(--lamp) 55%, transparent);
  }
  50% {
    box-shadow:
      inset 0 0 0 1px color-mix(in srgb, var(--lamp) 80%, transparent),
      0 0 4px 0 color-mix(in srgb, var(--lamp) 25%, transparent);
  }
}

@media (prefers-reduced-motion: reduce) {
  .andon-lamp.is-pulse {
    animation: none;
  }
}
</style>
