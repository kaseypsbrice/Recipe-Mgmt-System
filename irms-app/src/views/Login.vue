<template>
  <main class="pt-10 px-64">
    <div class="text-3xl py-3 font-bold">Login</div>
    <form @submit.prevent="onSubmit" class="flex flex-col gap-4 w-1/3">
      <input
        v-model="username"
        type="text"
        placeholder="Username"
        class="border p-2"
        required
      />
      <input
        v-model="password"
        type="password"
        placeholder="Password"
        class="border p-2"
        required
      />
      <button type="submit" class="bg-amber-800 text-white p-2">
        Sign In
      </button>
    </form>
  </main>
</template>

<script>
import { ref } from 'vue';
import { useRouter } from 'vue-router';
import { useAuth } from '../auth';

export default {
  setup() {
    // --- Reactive variables --- //
    const username = ref('');
    const password = ref('');
    // ------------------------- //
    const router = useRouter();
    const { login } = useAuth(); // Extracts login method

    async function onSubmit() {
      try {
        await login(username.value, password.value);
        router.push('/profile');
        // Attempts to login with username and password
      } catch (err) {
        alert('Invalid credentials');
      }
    }

    return { username, password, onSubmit };
  },
};
</script>
