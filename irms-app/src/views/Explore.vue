<script setup>
import { ref, onMounted } from 'vue'
import axios from 'axios'
import { RouterLink } from 'vue-router'

axios.defaults.baseURL = 'http://localhost:8000'
// Default URL for Axios requests-- :8000 is the FastAPI endpoint

const recipes = ref([])
// Holds array of recipes fetched from the backend
const defaultImage = 'http://localhost:8000/static/images/default_recipe_cover_image.jpg'
// Default cover image for recipes without user added cover images

onMounted(async () => {
  try {
    const res = await axios.get('/recipes')
    // Get request fetches all recipes from backend
    recipes.value = res.data
    // Fills reactive recipe array with data from request
  } catch (err) {
    errorMessage.value = 'Unable to load recipes. Please try again later.'
    console.error('Failed to load recipes:', err)
  }
})
</script>

<template>
  <main class="pt-10 px-64">
    <!-- Heading -->
    <div class="text-3xl py-3 font-bold text-shadow-md">Explore</div>
    <div class="text-lg">Check out the latest recipes posted by members of the community.</div>
    <!-- Divider -->
    <hr class="my-5 border-amber-800">
    <!-- Search Bar -->
    <div class="search-bar btn-bar">
      <img src="../assets/search-icon.svg" style="height: 1.3em; width: 1.3em;">
      <input type="search" placeholder="Search..." class="search-input" />
    </div>

    <!-- Explore Recipes -->
    <div class="explore-recipes-container" v-if="recipes.length > 0">
      <RouterLink v-for="recipe in recipes" :key="recipe.recipe_id" :to="`/recipe/${recipe.recipe_id}`" class="hover:cursor-pointer">
        <!-- Recipe Display Box Layout -->
        <div class="recipe-box">
          <div class="w-full flex justify-between px-6 py-2">
            <div class="text-base pr-1 font-semibold">{{ recipe.name }}</div>
            <div class="text-base text-gray-600">@{{ recipe.user?.username }}</div>
          </div>
          <div class="recipe-box-img">
            <img 
            :src="recipe.img_path || defaultImage"
            alt="Recipe Cover Image"
            class="w-full h-full object-cover"
            />
          </div>
        </div>
      </RouterLink>

    </div>
  </main>
</template>
