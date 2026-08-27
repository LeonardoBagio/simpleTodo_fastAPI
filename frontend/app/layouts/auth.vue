<template>
  <div class="relative flex min-h-screen flex-col">
    <div class="hazard-rule h-1 w-full" />

    <main class="flex flex-1 items-center justify-center px-4 py-10">
      <div class="w-full max-w-sm">
        <div class="mb-7 flex justify-center">
          <Wordmark />
        </div>
        <slot />
      </div>
    </main>

    <footer class="px-4 pb-6 text-center font-mono text-[11px] text-enamel-faint">
      SIMPLE·TODO · acesso ao console
    </footer>
  </div>
</template>
