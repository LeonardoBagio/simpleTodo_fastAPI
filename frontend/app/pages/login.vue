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
  <div class="plate p-6">
    <div class="mb-5 flex items-center gap-2">
      <span class="hazard-rule h-3 w-8 rounded-sm" />
      <h1 class="engraved text-sm text-enamel-dim">Acesso ao console</h1>
    </div>

    <form class="flex flex-col gap-4" @submit.prevent="submit">
      <label class="block">
        <span class="engraved mb-1.5 block text-[10px] text-enamel-faint">E-mail</span>
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
        <span class="engraved mb-1.5 block text-[10px] text-enamel-faint">Senha</span>
        <input
          v-model="password"
          class="field"
          type="password"
          autocomplete="current-password"
          required
          placeholder="••••••••"
        />
      </label>

      <button type="submit" class="btn-console btn-amber mt-1 justify-center" :disabled="busy">
        <Icon name="power" :size="16" />
        {{ busy ? 'Ligando…' : 'Ligar console' }}
      </button>
    </form>

    <p class="mt-5 border-t border-steel-700 pt-4 text-center text-sm text-enamel-dim">
      Ainda sem acesso?
      <NuxtLink to="/register" class="text-lamp-doing underline decoration-lamp-doing/40 hover:decoration-lamp-doing">
        Registrar operador
      </NuxtLink>
    </p>
  </div>
</template>
