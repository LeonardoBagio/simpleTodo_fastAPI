<template>
  <div class="relative flex min-h-screen flex-col">
    <main class="flex flex-1 items-center justify-center px-4 py-12">
      <div class="w-full max-w-sm">
        <div class="mb-8 flex flex-col items-center gap-4">
          <Wordmark />
          <span class="divider" />
        </div>
        <slot />
      </div>
    </main>

    <footer class="px-4 pb-8 text-center engraved text-[10px] tracking-[0.14em] text-muted">
      Simple Todo · acesso ao painel
    </footer>
  </div>
</template>
