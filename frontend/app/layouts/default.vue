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
  toast.ok('Sessão encerrada. Até logo.')
  await navigateTo('/login')
}
</script>

<template>
  <div class="min-h-screen">
    <!-- Dark fixed header (portfolio) -->
    <header class="sticky top-0 z-30 border-b border-white/10 bg-black/90 backdrop-blur">
      <div class="mx-auto flex h-[68px] max-w-[1120px] items-center gap-4 px-4 sm:px-6">
        <NuxtLink to="/" aria-label="Ir para o painel">
          <Wordmark tone="dark" />
        </NuxtLink>

        <nav class="ml-auto flex items-center gap-2">
          <NuxtLink
            to="/"
            class="hidden rounded-pill px-3.5 py-2 font-head text-xs font-bold uppercase tracking-[0.08em] transition-colors sm:inline-flex sm:items-center sm:gap-1.5"
            :class="
              route.path === '/'
                ? 'bg-white text-ink'
                : 'text-white/60 hover:text-white'
            "
          >
            <Icon name="gauge" :size="15" /> Painel
          </NuxtLink>

          <div class="relative">
            <button
              type="button"
              class="flex items-center gap-2 rounded-pill border border-white/15 py-1.5 pl-1.5 pr-2.5 transition-colors hover:border-white/35"
              :aria-expanded="menuOpen"
              aria-haspopup="menu"
              @click="menuOpen = !menuOpen"
            >
              <span
                class="grid h-7 w-7 place-items-center rounded-full bg-white font-head text-xs font-bold text-ink"
                >{{ auth.initials }}</span
              >
              <span class="hidden text-sm text-white/85 sm:inline">{{
                auth.user?.username
              }}</span>
              <Icon name="chevron" :size="14" class="rotate-90 text-white/45" />
            </button>

            <Transition name="menu">
              <div
                v-if="menuOpen"
                class="card absolute right-0 mt-2 w-52 overflow-hidden !rounded-md p-0 shadow-lg"
                role="menu"
                @click="menuOpen = false"
              >
                <div class="border-b border-black/[0.07] px-4 py-3">
                  <p class="truncate text-sm font-semibold text-ink">
                    {{ auth.user?.username }}
                  </p>
                  <p class="truncate text-[11px] text-muted">
                    {{ auth.user?.email }}
                  </p>
                </div>
                <NuxtLink
                  to="/account"
                  class="flex items-center gap-2.5 px-4 py-2.5 text-sm text-muted transition-colors hover:bg-cloud hover:text-ink"
                  role="menuitem"
                >
                  <Icon name="user" :size="16" /> Minha conta
                </NuxtLink>
                <button
                  type="button"
                  class="flex w-full items-center gap-2.5 px-4 py-2.5 text-left text-sm text-muted transition-colors hover:bg-lamp-trash/10 hover:text-lamp-trash"
                  role="menuitem"
                  @click="logout"
                >
                  <Icon name="power" :size="16" /> Sair
                </button>
              </div>
            </Transition>
          </div>
        </nav>
      </div>
    </header>

    <!-- backdrop to close the menu -->
    <div v-if="menuOpen" class="fixed inset-0 z-20" @click="menuOpen = false" />

    <main class="mx-auto max-w-[1120px] px-4 py-8 sm:px-6 sm:py-12">
      <slot />
    </main>
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
