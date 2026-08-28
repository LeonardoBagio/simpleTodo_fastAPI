<script setup lang="ts">
definePageMeta({ layout: 'auth' })
useHead({ title: 'Simple Todo — Acessar console' })

const auth = useAuthStore()
const toast = useToasts()
const route = useRoute()

const email = ref('')
const password = ref('')
const busy = ref(false)

async function submit() {
  if (busy.value) return
  busy.value = true
  try {
    await auth.login(email.value.trim(), password.value)
    const next = (route.query.next as string) || '/'
    toast.ok('Console ligado.')
    await navigateTo(next)
  } catch (err) {
    toast.error(errMessage(err, 'E-mail ou senha incorretos.'))
  } finally {
    busy.value = false
  }
}
</script>

<template>
  <div class="card p-6 sm:p-7">
    <div class="mb-5">
      <h1 class="engraved text-[11px] text-muted">Acesso ao painel</h1>
      <span class="divider mt-2" />
    </div>

    <form class="flex flex-col gap-4" @submit.prevent="submit">
      <label class="block">
        <span class="engraved mb-1.5 block text-[10px] text-muted">E-mail</span>
        <input
          v-model="email"
          class="field"
          type="email"
          autocomplete="email"
          required
          placeholder="voce@exemplo.com"
        />
      </label>

      <label class="block">
        <span class="engraved mb-1.5 block text-[10px] text-muted">Senha</span>
        <input
          v-model="password"
          class="field"
          type="password"
          autocomplete="current-password"
          required
          placeholder="••••••••"
        />
      </label>

      <button type="submit" class="btn btn-primary mt-1 w-full" :disabled="busy">
        <Icon name="power" :size="16" />
        {{ busy ? 'Entrando…' : 'Entrar' }}
      </button>
    </form>

    <p class="mt-6 border-t border-black/[0.07] pt-4 text-center text-sm text-muted">
      Ainda sem acesso?
      <NuxtLink to="/register" class="font-semibold text-ink underline decoration-ink/30 hover:decoration-ink">
        Criar conta
      </NuxtLink>
    </p>
  </div>
</template>
