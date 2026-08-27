<script setup lang="ts">
definePageMeta({ layout: 'auth' })
useHead({ title: 'Simple Todo — Registrar operador' })

const auth = useAuthStore()
const toast = useToasts()

const username = ref('')
const email = ref('')
const password = ref('')
const busy = ref(false)

async function submit() {
  if (busy.value) return
  busy.value = true
  try {
    await auth.register(username.value.trim(), email.value.trim(), password.value)
    toast.ok('Operador registrado. Bem-vindo ao console.')
    await navigateTo('/')
  } catch (err) {
    toast.error(errMessage(err, 'Não foi possível registrar.'))
  } finally {
    busy.value = false
  }
}
</script>

<template>
  <div class="plate p-6">
    <div class="mb-5 flex items-center gap-2">
      <span class="hazard-rule h-3 w-8 rounded-sm" />
      <h1 class="engraved text-sm text-enamel-dim">Registrar operador</h1>
    </div>

    <form class="flex flex-col gap-4" @submit.prevent="submit">
      <label class="block">
        <span class="engraved mb-1.5 block text-[10px] text-enamel-faint">Usuário</span>
        <input
          v-model="username"
          class="field"
          type="text"
          autocomplete="username"
          required
          placeholder="operador"
        />
      </label>

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
          autocomplete="new-password"
          required
          minlength="4"
          placeholder="••••••••"
        />
      </label>

      <button type="submit" class="btn-console btn-amber mt-1 justify-center" :disabled="busy">
        <Icon name="plus" :size="16" />
        {{ busy ? 'Registrando…' : 'Registrar e entrar' }}
      </button>
    </form>

    <p class="mt-5 border-t border-steel-700 pt-4 text-center text-sm text-enamel-dim">
      Já tem acesso?
      <NuxtLink to="/login" class="text-lamp-doing underline decoration-lamp-doing/40 hover:decoration-lamp-doing">
        Ligar console
      </NuxtLink>
    </p>
  </div>
</template>
