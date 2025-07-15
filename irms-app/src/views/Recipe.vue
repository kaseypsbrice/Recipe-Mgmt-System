<script setup>
import { ref, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import axios from 'axios'

const route = useRoute()
const recipeId = route.params.id

const recipe = ref(null)
const error = ref('')

async function fetchRecipe() {
  try {
    const res = await axios.get(`/recipes/${recipeId}`)
    recipe.value = res.data
  } catch (e) {
    error.value = 'Failed to load recipe.'
  }
}

onMounted(() => {
  fetchRecipe()
})
</script>

<template>
  <main class="p-10 max-w-3xl mx-auto">
    <div v-if="error" class="text-red-600 font-bold">{{ error }}</div>

    <div v-else-if="recipe">
      <h1 class="text-3xl font-bold mb-4">{{ recipe.name }}</h1>

      <img 
        v-if="recipe.img_path" 
        :src="recipe.img_path" 
        alt="Recipe cover image" 
        class="w-full max-h-96 object-cover rounded mb-4" 
      />

      <p class="mb-4">{{ recipe.description }}</p>

      <div class="mb-4 text-sm text-gray-600">
        Servings: {{ recipe.servings }} | Cook time: {{ recipe.cook_time_min }} minutes
      </div>

      <section class="mb-6">
        <h2 class="text-2xl font-semibold mb-2">Ingredients</h2>
        <ul class="list-disc pl-5">
          <li v-for="ingredient in recipe.ingredients" :key="ingredient.ingredient_id">
            {{ ingredient.quantity }} {{ ingredient.unit }} {{ ingredient.name }}
          </li>
        </ul>
      </section>

      <section>
        <h2 class="text-2xl font-semibold mb-2">Steps</h2>
        <ol class="list-decimal pl-5 space-y-4">
          <li v-for="step in recipe.steps" :key="step.step_id">
            <p>{{ step.instruction }}</p>
            <img 
              v-if="step.img_path" 
              :src="step.img_path" 
              alt="Step image" 
              class="mt-2 max-w-full rounded"
            />
          </li>
        </ol>
      </section>
    </div>

    <div v-else>
      Loading...
    </div>
  </main>
</template>