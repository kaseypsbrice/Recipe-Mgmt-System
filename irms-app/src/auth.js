import { reactive, computed } from 'vue'
import axios from 'axios'

const state = reactive({
  token: localStorage.getItem('token') || '',
  user: null,
})

// Point axios at FastAPI server
axios.defaults.baseURL = 'http://localhost:8000'
axios.interceptors.request.use(config => {
  if (state.token) config.headers.Authorization = `Bearer ${state.token}`
  return config
})

export function useAuth() {
  const isLoggedIn = computed(() => !!state.token)

  // Form-encoded for OAuth2PasswordRequestForm
  async function login(username, password) {
    const form = new URLSearchParams()
    form.append('username', username)
    form.append('password', password)
    form.append('grant_type', 'password')

    const { data } = await axios.post('/token', form)
    state.token = data.access_token
    localStorage.setItem('token', data.access_token)
    await fetchUser()
  }

  async function fetchUser() {
    try {
      const { data } = await axios.get('/users/me')
      state.user = data
    } catch {
      // invalid or expired token
      state.token = ''
      state.user = null
      localStorage.removeItem('token')
    }
  }

  function logout() {
    state.token = ''
    state.user = null
    localStorage.removeItem('token')
  }

  return {
    state,
    isLoggedIn,
    login,
    fetchUser,
    logout,
  }
}
