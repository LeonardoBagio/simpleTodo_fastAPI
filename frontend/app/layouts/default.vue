<script setup lang="ts">
const auth = useAuthStore()
const todos = useTodosStore()
const toast = useToasts()
const route = useRoute()

const menuOpen = ref(false)

async function logout() {
  menuOpen.value = false
  await auth.logout()
  todos.reset()
  toast.ok('Console desligado. Até logo.')
  await navigateTo('/login')
}
</script>

<template>
  <div class="min-h-screen">
    <header class="sticky top-0 z-30 border-b border-steel-700 bg-steel-900/85 backdrop-blur">
      <div class="hazard-rule h-1 w-full opacity-80" />
      <div class="mx-auto flex max-w-5xl items-center gap-4 px-4 py-3 sm:px-6">
        <NuxtLink to="/" aria-label="Ir para o painel">
          <Wordmark />
        </NuxtLink>

        <nav class="ml-auto flex items-center gap-1">
          <NuxtLink
            to="/"
            class="btn-console text-xs"
            :class="route.path === '/' ? 'btn-steel' : 'text-enamel-dim hover:text-enamel'"
          >
            <Icon name="gauge" :size="16" /> Painel
          </NuxtLink>

          <div class="relative">
            <button
              type="button"
              class="flex items-center gap-2 rounded-md border border-steel-600 bg-steel-800 py-1.5 pl-1.5 pr-2.5 transition-colors hover:border-steel-500"
              :aria-expanded="menuOpen"
              aria-haspopup="menu"
              @click="menuOpen = !menuOpen"
            >
              <span
                class="grid h-7 w-7 place-items-center rounded font-mono text-xs font-semibold text-steel-900"
                style="background: linear-gradient(180deg, #f7b73f, #f2a41c)"
                >{{ auth.initials }}</span
              >
              <span class="hidden text-sm text-enamel sm:inline">{{
                auth.user?.username
              }}</span>
              <Icon name="chevron" :size="14" class="rotate-90 text-enamel-faint" />
            </button>

            <Transition name="menu">
              <div
                v-if="menuOpen"
                class="absolute right-0 mt-2 w-48 overflow-hidden rounded-md border border-steel-600 bg-steel-800 shadow-raised"
                role="menu"
                @click="menuOpen = false"
              >
                <div class="border-b border-steel-700 px-3 py-2.5">
                  <p class="truncate text-sm text-enamel">{{ auth.user?.username }}</p>
                  <p class="truncate font-mono text-[11px] text-enamel-faint">
                    {{ auth.user?.email }}
                  </p>
                </div>
                <NuxtLink
                  to="/account"
                  class="flex items-center gap-2.5 px-3 py-2.5 text-sm text-enamel-dim transition-colors hover:bg-steel-700 hover:text-enamel"
                  role="menuitem"
                >
                  <Icon name="user" :size="16" /> Minha conta
                </NuxtLink>
                <button
                  type="button"
                  class="flex w-full items-center gap-2.5 px-3 py-2.5 text-left text-sm text-enamel-dim transition-colors hover:bg-lamp-trash/15 hover:text-lamp-trash"
                  role="menuitem"
                  @click="logout"
                >
                  <Icon name="power" :size="16" /> Desligar sessão
                </button>
              </div>
            </Transition>
          </div>
        </nav>
      </div>
    </header>

    <!-- backdrop to close the menu -->
    <div v-if="menuOpen" class="fixed inset-0 z-20" @click="menuOpen = false" />

    <main class="mx-auto max-w-5xl px-4 py-6 sm:px-6 sm:py-8">
      <slot />
    </main>

    <footer class="mx-auto max-w-5xl px-4 pb-8 sm:px-6">
      <div class="flex items-center gap-3 border-t border-steel-800 pt-4 font-mono text-[11px] text-enamel-faint">
        <span class="rivet" />
        <span>SIMPLE·TODO CONSOLE</span>
        <span class="ml-auto">FastAPI · Nuxt · JWT</span>
      </div>
    </footer>
  </div>
</template>

<style scoped>
.menu-enter-active,
.menu-leave-active {
  transition:
    transform 0.16s cubic-bezier(0.16, 1, 0.3, 1),
    opacity 0.16s ease;
  transform-origin: top right;
}
.menu-enter-from,
.menu-leave-to {
  transform: scale(0.96) translateY(-4px);
  opacity: 0;
}
</style>
