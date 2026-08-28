<script setup lang="ts">
const props = defineProps<{ modelValue: number | null; allLabel?: string }>()
const emit = defineEmits<{
  (e: 'update:modelValue', id: number | null): void
}>()

const catalog = useCatalogStore()
const open = ref(false)
const triggerEl = ref<HTMLElement | null>(null)
const panelStyle = ref<Record<string, string>>({})

const PANEL_W = 224

const current = computed(() =>
  props.modelValue != null
    ? catalog.categoryById[props.modelValue]
    : undefined,
)

// Painel teleportado ao body (fixed) para não ficar atrás dos cards.
function place() {
  const el = triggerEl.value
  if (!el) return
  const r = el.getBoundingClientRect()
  let left = r.left
  if (left + PANEL_W > window.innerWidth - 8) left = window.innerWidth - PANEL_W - 8
  if (left < 8) left = 8
  const below = window.innerHeight - r.bottom
  const openUp = below < 260 && r.top > below
  panelStyle.value = openUp
    ? {
        left: `${left}px`,
        bottom: `${window.innerHeight - r.top + 6}px`,
        width: `${PANEL_W}px`,
      }
    : {
        left: `${left}px`,
        top: `${r.bottom + 6}px`,
        width: `${PANEL_W}px`,
      }
}

function toggle() {
  open.value = !open.value
  if (open.value) nextTick(place)
}

function pick(id: number | null) {
  emit('update:modelValue', id)
  open.value = false
}

function onReflow() {
  if (open.value) place()
}

onMounted(() => {
  window.addEventListener('scroll', onReflow, true)
  window.addEventListener('resize', onReflow)
})
onBeforeUnmount(() => {
  window.removeEventListener('scroll', onReflow, true)
  window.removeEventListener('resize', onReflow)
})
</script>

<template>
  <div class="relative inline-block">
    <button
      ref="triggerEl"
      type="button"
      class="inline-flex items-center gap-2 rounded-pill border px-3 py-1.5 font-head text-[11px] font-bold uppercase tracking-[0.08em] transition-colors"
      :class="
        current
          ? 'border-transparent text-white'
          : 'border-black/[0.12] bg-white text-muted hover:border-black/25'
      "
      :style="current ? { background: current.color } : {}"
      :aria-expanded="open"
      aria-haspopup="listbox"
      @click="toggle"
    >
      <span>{{ current ? current.label : (allLabel ?? 'Sem categoria') }}</span>
      <Icon
        name="chevron"
        :size="12"
        class="rotate-90"
        :class="current ? 'text-white/70' : 'text-mist'"
      />
    </button>

    <Teleport to="body">
      <div v-if="open" class="fixed inset-0 z-[60]" @click="open = false" />
      <Transition name="menu">
        <div
          v-if="open"
          class="card fixed z-[61] max-h-[320px] overflow-auto !rounded-md p-1.5 shadow-lg"
          :style="panelStyle"
          role="listbox"
        >
          <button
            type="button"
            role="option"
            :aria-selected="modelValue == null"
            class="flex w-full items-center gap-2.5 rounded-[7px] px-2 py-1.5 text-left text-sm text-muted transition-colors hover:bg-cloud"
            @click="pick(null)"
          >
            <span class="h-2.5 w-2.5 rounded-full border border-black/20" />
            {{ allLabel ?? 'Sem categoria' }}
          </button>
          <button
            v-for="c in catalog.categories"
            :key="c.id"
            type="button"
            role="option"
            :aria-selected="modelValue === c.id"
            class="flex w-full items-center gap-2.5 rounded-[7px] px-2 py-1.5 text-left text-sm transition-colors"
            :class="
              modelValue === c.id
                ? 'bg-ink text-white'
                : 'text-ink hover:bg-cloud'
            "
            @click="pick(c.id)"
          >
            <span
              class="h-2.5 w-2.5 rounded-full"
              :style="{ background: c.color }"
            />
            {{ c.label }}
          </button>
        </div>
      </Transition>
    </Teleport>
  </div>
</template>

<style scoped>
.menu-enter-active,
.menu-leave-active {
  transition:
    transform 0.14s cubic-bezier(0.16, 1, 0.3, 1),
    opacity 0.14s ease;
  transform-origin: top left;
}
.menu-enter-from,
.menu-leave-to {
  transform: scale(0.97) translateY(-4px);
  opacity: 0;
}
</style>
