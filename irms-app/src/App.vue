<script setup>
import { RouterLink, RouterView } from 'vue-router'
</script>

<template>
  <!-- Navbar Container -->
  <header class="sticky top-0 z-10 flex justify-center bg-[#FFF1E2] border border-amber-800">
    <div class="bg-[#E3C2A5] flex-grow border-r border-amber-800"></div>

    <!-- Navbar -->
    <nav class="w-1/4 flex flex-wrap justify-between items-center px-20 py-4 gap-y-4 bg-[#FFF1E2] text-sm">
      <RouterLink to="/">HOME</RouterLink>
      <RouterLink to="/explore">EXPLORE</RouterLink>
      <RouterLink to="/profile">PROFILE</RouterLink>
    </nav>

    <div class="bg-[#E3C2A5] flex-grow border-l border-amber-800"></div>
  </header>

  <!-- Page Content -->
  <RouterView />

</template>
