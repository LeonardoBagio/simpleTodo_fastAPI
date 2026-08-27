<script setup lang="ts">
withDefaults(defineProps<{ compact?: boolean }>(), { compact: false })
</script>

<template>
  <span class="inline-flex items-center gap-2.5 select-none">
    <!-- Console gauge mark -->
    <span
      class="relative grid place-items-center rounded-[7px] plate"
      :class="compact ? 'h-8 w-8' : 'h-10 w-10'"
    >
      <svg
        :width="compact ? 18 : 22"
        :height="compact ? 18 : 22"
        viewBox="0 0 24 24"
        fill="none"
        aria-hidden="true"
      >
        <path
          d="M4 16a8 8 0 0116 0"
          stroke="#5a6270"
          stroke-width="1.6"
          stroke-linecap="round"
        />
        <path
          d="M12 16l5-4.2"
          stroke="#f2a41c"
          stroke-width="1.8"
          stroke-linecap="round"
        />
        <circle cx="12" cy="16" r="1.7" fill="#f2a41c" />
      </svg>
    </span>
    <span class="leading-none">
      <span
        class="block font-stencil text-enamel tracking-tight"
        :class="compact ? 'text-[15px]' : 'text-lg'"
        >Simple<span class="text-lamp-doing">·</span>Todo</span
      >
      <span
        v-if="!compact"
        class="engraved block text-[9px] text-enamel-faint mt-0.5"
        >Painel de controle de tarefas</span
      >
    </span>
  </span>
</template>
