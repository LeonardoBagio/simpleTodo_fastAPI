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
  <div class="card p-6 sm:p-7">
    <div class="mb-5">
      <h1 class="engraved text-[11px] text-muted">Criar conta</h1>
      <span class="divider mt-2" />
    </div>

    <form class="flex flex-col gap-4" @submit.prevent="submit">
      <label class="block">
        <span class="engraved mb-1.5 block text-[10px] text-muted">Usuário</span>
        <input
          v-model="username"
          class="field"
          type="text"
          autocomplete="username"
          required
          placeholder="seu-usuario"
        />
      </label>

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
          autocomplete="new-password"
          required
          minlength="4"
          placeholder="••••••••"
        />
      </label>

      <button type="submit" class="btn btn-primary mt-1 w-full" :disabled="busy">
        <Icon name="plus" :size="16" />
        {{ busy ? 'Criando…' : 'Criar conta e entrar' }}
      </button>
    </form>

    <p class="mt-6 border-t border-black/[0.07] pt-4 text-center text-sm text-muted">
      Já tem acesso?
      <NuxtLink to="/login" class="font-semibold text-ink underline decoration-ink/30 hover:decoration-ink">
        Entrar
      </NuxtLink>
    </p>
  </div>
</template>
