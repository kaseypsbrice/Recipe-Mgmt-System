<script setup>
import { ref, onMounted, computed } from 'vue'
import { useRoute } from 'vue-router'
import axios from 'axios'

const route = useRoute()
const recipeId = route.params.id

const recipe = ref(null)
const error = ref('')
const selectedServings = ref(1)

async function fetchRecipe() {
  try {
    const res = await axios.get(`/recipes/${recipeId}`)
    recipe.value = res.data
    selectedServings.value = res.data.servings
  } catch (e) {
    error.value = 'Failed to load recipe.'
  }
}

onMounted(() => {
  fetchRecipe()
})

const scaledIngredients = computed(() => {
  if (!recipe.value) return []
  const ratio = selectedServings.value / recipe.value.servings
  // ratio = new / original
  // Calculates how much bigger the quantity is compared to the original value
  return recipe.value.ingredients.map(ing => ({
    ...ing,
    quantity: Math.round(ing.quantity * ratio * 100) / 100
    // Multiplies each ingredient by the ratio and rounds the result
    // to the nearest 2 decimals to account for float values.
  }))
})
</script>

<template>
  <main class="p-10 max-w-3xl mx-auto">
    <div v-if="error" class="text-red-600 font-bold">{{ error }}</div>

    <div v-else-if="recipe">
      <h1 class="text-3xl font-bold mb-4">{{ recipe.name }}</h1>

      <img v-if="recipe.img_path" :src="recipe.img_path" alt="Recipe cover image"
        class="w-full max-h-96 object-cover rounded mb-4" />

      <p class="mb-4">{{ recipe.description }}</p>

      <hr class="mb-10 border-amber-800">

      <!-- Adjustable serving sizes -->
      <div class="mb-4 text-sm text-gray-600 flex items-center">
        <label class="mr-2">Servings</label>
        <input v-model.number="selectedServings" type="number" min="1" class="input-field btn-bar w-20 text-center" />
        <span class="mx-2">|</span>
        Cook time: {{ recipe.cook_time_min }} minutes
      </div>

      <hr class="mt-10 mb-10 border-amber-800">

      <section class="mb-6">
        <h2 class="text-2xl font-semibold mb-2">Ingredients</h2>
        <ul class="list-disc pl-5">
          <li v-for="ingredient in scaledIngredients" :key="ingredient.ingredient_id">
            {{ ingredient.quantity }} {{ ingredient.unit }} {{ ingredient.name }}
          </li>
        </ul>
      </section>

      <section>
        <h2 class="text-2xl font-semibold mb-2">Steps</h2>
        <ol class="list-decimal pl-5 space-y-4">
          <li v-for="step in recipe.steps" :key="step.step_id">
            <p>{{ step.instruction }}</p>
            <img v-if="step.img_path" :src="step.img_path" alt="Step image" class="mt-2 max-w-full rounded" />
          </li>
        </ol>
      </section>
    </div>

    <div v-else>
      Loading...
    </div>
  </main>
</template>