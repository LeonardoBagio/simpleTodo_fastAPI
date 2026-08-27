<script setup lang="ts">
// Root shell. The andon direction contract is injected at the top of <body>
// by server/plugins/contract.ts so it survives the production build.
</script>

<template>
  <div>
    <NuxtLayout>
      <NuxtPage />
    </NuxtLayout>
    <ToastHost />
  </div>
</template>
