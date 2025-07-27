import { reactive, computed } from 'vue'
import axios from 'axios'

const state = reactive({
  token: localStorage.getItem('token') || '',
  user: null,
})
// Creates a reactive state to track the user's token and info.
// Loads the token from localStorage if it exists, user info will be 
// populated after a successful login.

axios.defaults.baseURL = 'http://localhost:8000'
// Sets FastAPI as the default URL endpoint for axios requests

axios.interceptors.request.use(config => {
  if (state.token) config.headers.Authorization = `Bearer ${state.token}`
  return config
})
// Attaches authorisation token to header for all requests

export function useAuth() {
  const isLoggedIn = computed(() => !!state.token)
  // Checks for login status based on reactive dependencies

  async function login(username, password) {
    const form = new URLSearchParams()
    form.append('username', username)
    form.append('password', password)
    form.append('grant_type', 'password')
    // Login using form data required by FastAPI's OAuth2PasswordRequestForm

    const { data } = await axios.post('/token', form)
    // Posts credentials to FastAPI and receives access token in response
    state.token = data.access_token
    // Saves token to reactive state
    localStorage.setItem('token', data.access_token)
    // Saves token to localStorage
    await fetchUser()
    // Fetches and stores current user profile info
  }

  async function fetchUser() {
    // Fetches user details using stored token
    try {
      const { data } = await axios.get('/users/me')
      state.user = data
    } catch {
      // Invalid or expired token
      state.token = ''
      state.user = null
      localStorage.removeItem('token')
    }
  }

  function logout() {
    state.token = ''
    state.user = null
    localStorage.removeItem('token')
  } // Logs user out by clearing state and storage

  return {
    state,
    isLoggedIn,
    login,
    fetchUser,
    logout,
  } // Exposes state and auth functions to components that use useAuth()
}
