<template>
  <main class="pt-10 px-64">
    <div class="text-3xl py-3 font-bold">Sign Up</div>
    <form @submit.prevent="onSubmit" class="flex flex-col gap-4 w-1/3">
      <input v-model="username" type="text" placeholder="Username" class="border p-2" required />
      <input v-model="password" type="password" placeholder="Password" class="border p-2" required />
      <button type="submit" class="bg-amber-800 text-white p-2">
        Create Account
      </button>
    </form>
    <p class="mt-4">
      Already have an account?
      <RouterLink to="/login" class="text-amber-800 underline">
        Sign In
      </RouterLink>
    </p>
  </main>
</template>

<script>
import { ref } from 'vue'
import axios from 'axios'
import { useRouter } from 'vue-router'

axios.defaults.baseURL = 'http://localhost:8000'

export default {
  setup() {
    const username = ref('')
    const password = ref('')
    const router = useRouter()

    async function onSubmit() {
      if (!username.value || !password.value) {
        alert('Signup failed: All fields are required')
        return
      }
      try {
        await axios.post('/users/create_user', {
          username: username.value,
          password: password.value,
        }) // Attempts to sign-up with username and password input
        router.push('/login')
        // Redirects user to the login page
      } catch (err) {
        alert('Signup failed: ' + err.response?.data?.detail || err.message)
      }
    }

    return { username, password, onSubmit }
  },
}
</script>
