<script setup lang="ts">
withDefaults(
  defineProps<{ compact?: boolean; tone?: 'light' | 'dark' }>(),
  { compact: false, tone: 'light' },
)
</script>

<template>
  <span class="inline-flex items-center gap-2.5 select-none">
    <!-- Monochrome gauge mark -->
    <span
      class="relative grid place-items-center rounded-[8px]"
      :class="[
        compact ? 'h-8 w-8' : 'h-10 w-10',
        tone === 'dark' ? 'bg-white' : 'bg-ink',
      ]"
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
          :stroke="tone === 'dark' ? '#1a1a1a' : '#ffffff'"
          stroke-opacity="0.5"
          stroke-width="1.6"
          stroke-linecap="round"
        />
        <path
          d="M12 16l5-4.2"
          :stroke="tone === 'dark' ? '#1a1a1a' : '#ffffff'"
          stroke-width="1.8"
          stroke-linecap="round"
        />
        <circle
          cx="12"
          cy="16"
          r="1.7"
          :fill="tone === 'dark' ? '#1a1a1a' : '#ffffff'"
        />
      </svg>
    </span>
    <span class="leading-none">
      <span
        class="block font-head font-black tracking-tight"
        :class="[
          compact ? 'text-[15px]' : 'text-lg',
          tone === 'dark' ? 'text-white' : 'text-ink',
        ]"
        >Simple<span :class="tone === 'dark' ? 'text-white/50' : 'text-mist'"
          >·</span
        >Todo</span
      >
      <span
        v-if="!compact"
        class="engraved block text-[9px] mt-0.5"
        :class="tone === 'dark' ? 'text-white/55' : 'text-muted'"
        >Painel de controle de tarefas</span
      >
    </span>
  </span>
</template>
