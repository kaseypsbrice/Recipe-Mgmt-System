<script setup>
import { ref, computed, onMounted } from 'vue'
import axios from 'axios'
import { useAuth } from '../auth'
import { useRouter, RouterLink } from 'vue-router'

axios.defaults.baseURL = 'http://localhost:8000'

const defaultImage = 'http://localhost:8000/static/images/default_recipe_cover_image.jpg'

const { state, isLoggedIn, fetchUser } = useAuth()
const router = useRouter()

const user = computed(() => state.user)
const recipes = ref([])
const error = ref('')
const submitStatus = ref({ success: false, error: '' })

function logout() {
    if (confirm("Are you sure you want to log out?")) {
        localStorage.removeItem('token')
        state.token = null
        state.user = null
        console.log("Info: Logged out of session.")
        router.push('/')
    }
}

async function deleteRecipe(id) {
  const ok = confirm("Are you sure you want to delete this recipe? This cannot be undone.")
  if (!ok) return
  // Confirm user wants to delete recipe

  try {
    const token = localStorage.getItem('token')
    await axios.delete(`/recipes/${id}`, {
      headers: { Authorization: `Bearer ${token}` }
    }) // Call API

    recipes.value = recipes.value.filter(r => r.recipe_id !== id)
    // Remove from recipe array

    submitStatus.value = { success: true, error: '' }
  } catch (err) {
    submitStatus.value = {
      success: false,
      error: err.response?.data.detail || 'Delete failed'
    }
  }
}

onMounted(async () => {
    if (state.token && !state.user) await fetchUser()

    if (state.token) {
        try {
            const res = await axios.get('/my_recipes', {
                headers: { Authorization: `Bearer ${state.token}` }
            })
            recipes.value = res.data
        } catch (err) {
            error.value = 'Failed to load your recipes'
            console.error(err)
        }
    }
})
</script>

<template>
    <main class="pt-10 px-64">
        <div v-if="isLoggedIn">
            <div class="text-3xl py-3 font-bold text-shadow-md">Profile</div>
            <div class="flex items-center w-full">
                <div class="text-lg" v-if="user">@{{ user.username }}</div>
                <div class="logout-btn btn-bar cursor-pointer" @click="logout">Logout</div>
            </div>
            <hr class="my-5 border-amber-800" />
            <div class="flex items-center w-full gap-4">
                <div class="w-1/2 flex">
                    <div class="search-bar btn-bar">
                        <img src="../assets/search-icon.svg" style="height: 1.3em; width: 1.3em;" />
                        <input type="search" placeholder="Search..." class="search-input" />
                    </div>
                </div>
                <div class="create-new-recipe-btn btn-bar cursor-pointer">
                    <RouterLink to="/create-new-recipe">Create New Recipe</RouterLink>
                </div>
                <div class="settings-btn btn-bar cursor-pointer">Settings</div>
            </div>
            <div class="explore-recipes-container" v-if="recipes.length > 0">
                <div v-for="recipe in recipes" :key="recipe.recipe_id" class="hover:cursor-pointer"
                    @click="() => router.push(`/recipe/${recipe.recipe_id}`)">
                    <div class="recipe-box">
                        <div class="w-full flex justify-between px-6 py-2 ">
                            <div class="text-base pr-1 font-semibold">{{ recipe.name }}</div>
                            <div class="text-base text-gray-600">@{{ user.username }}</div>
                        </div>
                        <div class="recipe-box-img h-48 bg-gray-200">
                            <img :src="recipe.img_path || defaultImage" alt="Recipe Image"
                                class="w-full h-full object-cover" />
                        </div>
                        <div class="flex justify-between w-full px-6">
                            <div class="text-left text-red-800 underline" @click.stop.prevent="deleteRecipe(recipe.recipe_id)">
                                Delete
                            </div>
                            <RouterLink :to="`/edit-recipe/${recipe.recipe_id}`" @click.stop
                                class="pb-2 underline text-blue-800 text-right w-full">
                                Edit
                            </RouterLink>
                        </div>
                    </div>
                </div>
            </div>

            <div v-else>
                <p>You don't have any recipes yet.</p>
            </div>
        </div>

        <div v-else>
            <p class="text-center mt-20">You must be logged in to view this page.
                <RouterLink to="/login" class="text-amber-800 underline">Login here</RouterLink>
            </p>
            <p class="text-center mt-4">
                Don’t have an account?
                <RouterLink to="/signup" class="text-amber-800 underline">
                    Create one here
                </RouterLink>
            </p>
        </div>
    </main>
</template>