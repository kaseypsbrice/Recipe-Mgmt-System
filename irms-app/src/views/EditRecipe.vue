<script setup>
import { ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import axios from 'axios'

axios.defaults.baseURL = 'http://localhost:8000'

const DEFAULT_IMAGE = 'http://localhost:8000/static/images/default_recipe_cover_image.jpg'
const route = useRoute()
const router = useRouter()
const recipeId = route.params.id

const form = ref({
  name: '',
  description: '',
  servings: 1,
  cook_time_min: 0,
  img_path: DEFAULT_IMAGE,
  steps: [{ instruction: '', img_path: '' }],
  ingredients: [{ name: '', quantity: null, unit: '' }],
})

const submitStatus = ref({ success: false, error: '' })
const isSubmitting = ref(false)

onMounted(async () => {
  if (!recipeId) return
  try {
    const { data } = await axios.get(`/recipes/${recipeId}`)
    form.value = {
      name: data.name,
      description: data.description,
      servings: data.servings,
      cook_time_min: data.cook_time_min,
      img_path: data.img_path || DEFAULT_IMAGE,
      steps: data.steps.map(s => ({ instruction: s.instruction, img_path: s.img_path || '' })),
      ingredients: data.ingredients.map(i => ({ name: i.name, quantity: i.quantity, unit: i.unit })),
    }
  } catch (e) {
    console.error('Failed to load recipe:', e)
  }
})

function handleCoverUpload(e) {
  const file = e.target.files[0]
  if (file?.type.startsWith('image/')) {
    const reader = new FileReader()
    reader.onload = () => (form.value.img_path = reader.result)
    reader.readAsDataURL(file)
  } else {
    form.value.img_path = DEFAULT_IMAGE
  }
}

function addStep() {
  form.value.steps.push({ instruction: '', img_path: '' })
}
function removeStep(idx) {
  if (form.value.steps.length > 1) {
    form.value.steps.splice(idx, 1)
  }
}
function handleStepImageUpload(e, idx) {
  const file = e.target.files[0]
  if (file?.type.startsWith('image/')) {
    const reader = new FileReader()
    reader.onload = () => (form.value.steps[idx].img_path = reader.result)
    reader.readAsDataURL(file)
  } else {
    form.value.steps[idx].img_path = ''
  }
}

function addIngredient() {
  form.value.ingredients.push({ name: '', quantity: null, unit: '' })
}
function removeIngredient(idx) {
  if (form.value.ingredients.length > 1) {
    form.value.ingredients.splice(idx, 1)
  }
}

async function onSubmit() {
  isSubmitting.value = true
  submitStatus.value = { success: false, error: '' }

  const token = localStorage.getItem('token')
  if (!token) {
    submitStatus.value.error = 'You must be logged in'
    isSubmitting.value = false
    return
  }

  if (form.value.name.trim().length < 3) {
    submitStatus.value.error = 'Recipe name must be at least 3 chars'
    isSubmitting.value = false
    return
  }

  try {
    const method = recipeId ? 'put' : 'post'
    const url = recipeId ? `/recipes/${recipeId}` : '/create_recipe'
    const res = await axios[method](url, form.value, {
      headers: { Authorization: `Bearer ${token}` }
    })

    const id = recipeId || res.data.recipe_id
    submitStatus.value.success = true
    setTimeout(() => router.push(`/recipe/${id}`), 1200)
  } catch (err) {
    submitStatus.value.error = err.response?.data.detail || 'Submission failed'
  } finally {
    isSubmitting.value = false
  }
}
</script>

<template>
  <main class="pt-10 px-64">
    <!-- Heading -->
    <div class="text-3xl py-3 font-bold text-shadow-md">Edit Recipe</div>
    <div class="text-lg">Edit an existing recipe by modifying the details below.</div>
    <!-- Divider -->
    <hr class="my-5 border-amber-800">

    <!-- Create Recipe Form -->
    <form @submit.prevent="onSubmit" class="create-recipe-form">

      <div v-if="submitStatus.success" class="mb-4 p-3 bg-green-100 text-green-800 rounded">
        Recipe submitted successfully!
      </div>
      <div v-if="submitStatus.error" class="mb-4 p-3 bg-red-100 text-red-800 rounded">
        {{ submitStatus.error }}
      </div>

      <div class="w-full grid grid-cols-2 gap-5 p-10">
        <!-- Recipe Name -->
        <div class="flex flex-col gap-3">
          <label class="text-lg">Recipe Name</label>
          <input v-model="form.name" type="text" required class="input-field btn-bar" />
        </div>

        <!-- Cover image upload option -->
        <div class="flex flex-col gap-3">
          <label for="coverImage" class="text-lg">Cover Image</label>
          <input id="coverImage" name="coverImage" type="file" accept="image/*" @change="handleCoverUpload"
            class="input-field btn-bar" />
          <img v-if="form.img_path" :src="form.img_path" alt="Cover Preview"
            class="mt-2 w-32 h-32 object-cover rounded" />
        </div>

        <!-- Recipe Description -->
        <div class="flex flex-col gap-3">
          <label class="text-lg">Recipe Description</label>
          <input v-model="form.description" type="text" required class="input-field btn-bar" />
        </div>

        <!-- Servings-->
        <div class="flex flex-col gap-3">
          <label class="text-lg">Servings</label>
          <input v-model.number="form.servings" type="number" required min="1" class="input-field btn-bar" />
        </div>

        <!-- Cook Time -->
        <div class="flex flex-col gap-3">
          <label class="text-lg">Time</label>
          <input v-model.number="form.cook_time_min" type="number" required step="0.1" class="input-field btn-bar" />
        </div>

        <!-- Steps -->
        <div class="flex flex-col gap-3 relative">
          <label class="text-lg">Steps</label>

          <div v-for="(step, idx) in form.steps" :key="idx" class="relative flex items-center btn-bar mb-4">
            <button v-if="idx > 0" type="button" @click="removeStep(idx)"
              class="relative justify-center pl-5 text-red-600 text-xl leading-none mr-5 cursor-pointer">×</button>

            <textarea v-model="form.steps[idx].instruction" required placeholder="Step instruction"
              class="w-full h-full pr-14 rounded-[10px] input-field"></textarea>

            <!-- Image upload per step -->
            <input type="file" :id="`stepImage-${idx}`" accept="image/*" class="hidden"
              @change="e => handleStepImageUpload(e, idx)" />

            <div class="flex items-center gap-4 mt-2">
              <!-- after the textarea -->
              <!-- Image preview -->
              <img v-if="form.steps[idx].img_path" :src="form.steps[idx].img_path" alt="Preview"
                class="step-img-preview" />
              <!-- Upload icon -->
              <label :for="`stepImage-${idx}`" class="upload-btn cursor-pointer">
                <img src="../assets/upload.svg" alt="Upload" />
              </label>
              <input type="file" :id="`stepImage-${idx}`" accept="image/*" class="hidden"
                @change="e => handleStepImageUpload(e, idx)" />

              <!-- Remove image using X -->
              <button v-if="form.steps[idx].img_path" type="button" @click.prevent="form.steps[idx].img_path = ''"
                class="text-amber-700 font-bold absolute cursor-pointer" style="font-size:1.25rem; line-height:1;">
                ×
              </button>
            </div>

          </div>

          <!-- Add Step button -->
          <div @click="addStep" class="btn-bar add-btn top-full mt-5 cursor-pointer">
            + Add Step
          </div>
        </div>

        <!-- Ingredients -->
        <div class="flex flex-col gap-3 relative">
          <label class="text-lg">Ingredients</label>

          <div v-for="(ing, idx) in form.ingredients" :key="idx"
            class="relative flex-col items-center btn-bar mb-4 space-x-2 p-4">
            <button v-if="idx > 0" type="button" @click="removeIngredient(idx)"
              class="relative justify-center text-red-600 text-xl leading-none mr-5 cursor-pointer">×</button>

            <input v-model="form.ingredients[idx].name" type="text" required placeholder="Ingredient"
              class="input-field btn-bar" />
            <input v-model.number="form.ingredients[idx].quantity" type="number" step="0.01" required placeholder="Qty"
              class="input-field btn-bar" />
            <select v-model="form.ingredients[idx].unit" required class="input-field btn-bar">
              <option disabled value="">Unit</option>
              <option value="g">g</option>
              <option value="kg">kg</option>
              <option value="ml">ml</option>
              <option value="cup">cup</option>
              <option value="tbsp">tbsp</option>
            </select>
          </div>

          <div @click="addIngredient" class="btn-bar add-btn top-full mt-5 cursor-pointer">
            + Add Ingredient
          </div>
        </div>
      </div>

      <!-- Submit button -->
      <div class="flex w-full p-10 gap-10 mt-20">
        <button type="submit" class="btn-bar submit-btn cursor-pointer">Submit</button>
        <!-- Cancel Button -->
        <RouterLink to="/profile" class="btn-bar cancel-btn cursor-pointer inline-block text-center">
          Cancel
        </RouterLink>
      </div>
    </form>
  </main>
</template>