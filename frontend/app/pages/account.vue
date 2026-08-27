<script setup lang="ts">
useHead({ title: 'Simple Todo — Minha conta' })

const auth = useAuthStore()
const todos = useTodosStore()
const toast = useToasts()

const username = ref(auth.user?.username ?? '')
const email = ref(auth.user?.email ?? '')
const password = ref('')
const busy = ref(false)

const confirmingDelete = ref(false)
const deleteConfirm = ref('')
const deleting = ref(false)

async function save() {
  if (busy.value) return
  if (!password.value) {
    toast.warn('Confirme com sua senha para salvar as alterações.')
    return
  }
  busy.value = true
  try {
    await auth.updateAccount({
      username: username.value.trim(),
      email: email.value.trim(),
      password: password.value,
    })
    password.value = ''
    toast.ok('Dados do operador atualizados.')
  } catch (err) {
    toast.error(errMessage(err))
  } finally {
    busy.value = false
  }
}

async function destroy() {
  if (deleteConfirm.value.trim().toUpperCase() !== 'EXCLUIR') {
    toast.warn('Digite EXCLUIR para confirmar.')
    return
  }
  deleting.value = true
  try {
    await auth.deleteAccount()
    todos.reset()
    toast.warn('Conta excluída.')
    await navigateTo('/login')
  } catch (err) {
    toast.error(errMessage(err))
  } finally {
    deleting.value = false
  }
}
</script>

<template>
  <div class="mx-auto flex max-w-xl flex-col gap-6">
    <div>
      <h1 class="font-placard text-2xl font-bold uppercase tracking-[0.02em] text-enamel">
        Minha conta
      </h1>
      <p class="mt-1 font-mono text-xs text-enamel-faint">
        Operador #{{ String(auth.user?.id ?? 0).padStart(4, '0') }}
      </p>
    </div>

    <!-- Credentials -->
    <form class="plate flex flex-col gap-4 p-6" @submit.prevent="save">
      <div class="flex items-center gap-2">
        <span class="hazard-rule h-3 w-8 rounded-sm" />
        <h2 class="engraved text-xs text-enamel-dim">Credenciais</h2>
      </div>

      <label class="block">
        <span class="engraved mb-1.5 block text-[10px] text-enamel-faint">Usuário</span>
        <input v-model="username" class="field" type="text" required />
      </label>

      <label class="block">
        <span class="engraved mb-1.5 block text-[10px] text-enamel-faint">E-mail</span>
        <input v-model="email" class="field" type="email" required />
      </label>

      <label class="block">
        <span class="engraved mb-1.5 block text-[10px] text-enamel-faint">
          Nova senha (obrigatória para salvar)
        </span>
        <input
          v-model="password"
          class="field"
          type="password"
          autocomplete="new-password"
          placeholder="••••••••"
        />
        <span class="mt-1.5 block text-[11px] text-enamel-faint">
          O backend regrava a senha a cada atualização de conta, então informe a
          senha desejada para confirmar.
        </span>
      </label>

      <div class="flex justify-end">
        <button type="submit" class="btn-console btn-amber text-sm" :disabled="busy">
          <Icon name="check" :size="16" />
          {{ busy ? 'Salvando…' : 'Salvar alterações' }}
        </button>
      </div>
    </form>

    <!-- Danger zone -->
    <section
      class="rounded-md border border-lamp-trash/40 bg-lamp-trash/[0.06] p-6"
    >
      <div class="flex items-center gap-2">
        <AndonLamp state="trash" :size="13" />
        <h2 class="engraved text-xs text-lamp-trash">Zona de risco</h2>
      </div>
      <p class="mt-2 text-sm text-enamel-dim">
        Excluir a conta remove o operador e é irreversível.
      </p>

      <div v-if="!confirmingDelete" class="mt-4">
        <button
          type="button"
          class="btn-console text-xs"
          style="color: #df5140; border: 1px solid rgba(223, 81, 64, 0.5)"
          @click="confirmingDelete = true"
        >
          <Icon name="trash" :size="15" /> Excluir minha conta
        </button>
      </div>

      <div v-else class="mt-4 flex flex-col gap-3">
        <label class="block">
          <span class="mb-1.5 block text-[11px] text-enamel-dim"
            >Digite <span class="font-mono text-lamp-trash">EXCLUIR</span> para confirmar</span
          >
          <input
            v-model="deleteConfirm"
            class="field"
            style="border-color: rgba(223, 81, 64, 0.5)"
            type="text"
            placeholder="EXCLUIR"
          />
        </label>
        <div class="flex items-center gap-2">
          <button
            type="button"
            class="btn-console btn-steel text-xs"
            @click="(confirmingDelete = false), (deleteConfirm = '')"
          >
            Cancelar
          </button>
          <button
            type="button"
            class="btn-console text-xs"
            style="color: #fff; background: linear-gradient(180deg, #e5604f, #df5140)"
            :disabled="deleting"
            @click="destroy"
          >
            {{ deleting ? 'Excluindo…' : 'Confirmar exclusão' }}
          </button>
        </div>
      </div>
    </section>
  </div>
</template>
