<script setup lang="ts">
// Small authored icon set, one consistent 1.7 stroke weight, square caps to
// match the console's machined character. No emoji, no icon font.
const props = withDefaults(
  defineProps<{ name: string; size?: number | string }>(),
  { size: 18 },
)

const paths: Record<string, string> = {
  plus: 'M10 4v12M4 10h12',
  search:
    'M9 3a6 6 0 104.24 10.24L17 17M9 3a6 6 0 016 6 6 6 0 01-6 6',
  trash:
    'M4 6h12M8 6V4h4v2M6 6l1 10h6l1-10M9 9v4M11 9v4',
  edit: 'M4 16h4l9-9-4-4-9 9v4zM12 4l4 4',
  check: 'M4 10l4 4 8-9',
  chevron: 'M7 5l5 5-5 5',
  power: 'M10 3v7M6 5a6 6 0 108 0',
  user: 'M10 10a3 3 0 100-6 3 3 0 000 6zM4 17c0-3 2.7-5 6-5s6 2 6 5',
  close: 'M5 5l10 10M15 5L5 15',
  arrow: 'M4 10h11M11 6l4 4-4 4',
  gauge:
    'M10 4a6 6 0 016 6M10 4a6 6 0 00-6 6M10 10l3.5-2.2M4 15h12',
  filter: 'M3 5h14l-5.2 6v4l-3.6 2v-6L3 5z',
  reset: 'M4 10a6 6 0 106-6M4 4v4h4',
}

const d = computed(() => paths[props.name] ?? paths.gauge)
</script>

<template>
  <svg
    :width="size"
    :height="size"
    viewBox="0 0 20 20"
    fill="none"
    stroke="currentColor"
    stroke-width="1.7"
    stroke-linecap="square"
    stroke-linejoin="miter"
    aria-hidden="true"
  >
    <path :d="d" />
  </svg>
</template>
