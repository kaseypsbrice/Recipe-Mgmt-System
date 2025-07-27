<script setup>
import { useRouter } from 'vue-router'
import { ref } from 'vue'
import axios from 'axios'

axios.defaults.baseURL = 'http://localhost:8000'
// Default URL for Axios requests-- :8000 is the FastAPI endpoint

const DEFAULT_IMAGE_URL = 'http://localhost:8000/static/images/default_recipe_cover_image.jpg'
// Default cover image for recipes where there's no user input. 

// --- Reactive state definitions for form input --- // 
const steps = ref([''])
const imgPreviews = ref([null])
const ingredients = ref([
  { name: '', quantity: 0, unit: '' }
])
const coverImagePreview = ref('')
const recipeName = ref('')
const recipeDescription = ref('')
const servings = ref('')
const cookTime = ref('')
// ------------------------------------------------- //

function handleCoverUpload(e) {
  const file = e.target.files[0]
  if (file && file.type.startsWith('image/')) {
    const reader = new FileReader()
    reader.onload = () => (coverImagePreview.value = reader.result)
    reader.readAsDataURL(file)
  } else {
    coverImagePreview.value = null
  }
}
// Grabs the selected file and loads the preview image in the UI.
// Reads the file as a base84 URL. If the input is invalid, it'll reset the preview.

function addStep() {
  steps.value.push('')
  imgPreviews.value.push(null)
}
// Adds a new blank step instruction

function addIngredient() {
  ingredients.value.push({ name: '', quantity: 0, unit: '' })
}
// Adds a new blank ingredient entry

function handleImageUpload(event, idx) {
  const file = event.target.files[0]
  if (file && file.type.startsWith('image/')) {
    const reader = new FileReader()
    reader.onload = () => {
      imgPreviews.value[idx] = reader.result
    }
    reader.readAsDataURL(file)
  } else {
    imgPreviews.value[idx] = null
  }
}
// Loads step images, inserts provided image into an array for step images.
// Clears the image if it's an invalid input.

function removeStep(idx) {
  steps.value.splice(idx, 1)
  imgPreviews.value.splice(idx, 1)
}

function removeIngredient(idx) {
  ingredients.value.splice(idx, 1)
}

// --- Code that implements creation of recipe --- //

const router = useRouter()

const submitStatus = ref({
  success: false,
  error: ''
})
// Tracks submission status of form.

async function onSubmit() {
  console.log('Info: onSubmit fired')
  submitStatus.value = { success: false, error: '' } 
  // ^ Resets status for each attempt at submission

  const token = localStorage.getItem('token') // Stores JWT from local storage
  if (!token) {
    submitStatus.value.error = 'You must be logged in'
    return
  }

  if (recipeName.value.trim().length < 3) {
    submitStatus.value.error = 'Recipe name must be at least 3 characters long'
    return
  }

  const payload = {
    name: recipeName.value,
    description: recipeDescription.value,
    servings: parseInt(servings.value),
    cook_time_min: parseInt(cookTime.value),
    img_path: coverImagePreview.value || DEFAULT_IMAGE_URL,
    steps: steps.value.map((instr, i) => ({
      instruction: instr,
      img_path: imgPreviews.value[i] || ''
    })),
    ingredients: ingredients.value.map(ing => ({
      name: ing.name,
      quantity: ing.quantity,
      unit: ing.unit
    }))
  }
  // Builds a request payload with form values and image previews.

  try {
    const res = await axios.post('/create_recipe', payload, {
      headers: {
        Authorization: `Bearer ${token}`
      }
    }) // Posts our request to create a new recipe

    const { recipe_id } = res.data // Gets newly created recipe ID from response
    submitStatus.value.success = true

    setTimeout(() => {
      router.push(`/recipe/${recipe_id}`) // Navigate to recipe's page
    }, 1200)

  } catch (err) {
    if (err.response) {
      submitStatus.value.error = err.response.data.detail || 'Submission error'
    } else {
      submitStatus.value.error = 'Network error'
    } // Provide detailed error response if request fails.
  }
}

</script>

<template>
  <main class="pt-10 px-64">
    <!-- Heading -->
    <div class="text-3xl py-3 font-bold text-shadow-md">Create A New Recipe</div>
    <div class="text-lg">Enter the details below to create a new recipe.</div>
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
          <label for="recipeName" class="text-lg">Recipe Name</label>
          <input v-model="recipeName" type="text" name="recipeName" required placeholder=""
            class="input-field btn-bar" />
        </div>
        <!-- Cover image upload option -->
        <div class="flex flex-col gap-3">
          <label for="coverImage" class="text-lg">Cover Image</label>
          <input id="coverImage" name="coverImage" type="file" accept="image/*" @change="handleCoverUpload" class="input-field btn-bar" />
          <img v-if="coverImagePreview" :src="coverImagePreview" alt="Cover Preview"
            class="mt-2 w-32 h-32 object-cover rounded" />
        </div>

        <!-- Recipe Description -->
        <div class="flex flex-col gap-3">
          <label for="recipeDescription" class="text-lg">Recipe Description</label>
          <input v-model="recipeDescription" type="text" name="recipeDescription" required placeholder=""
            class="input-field btn-bar" />
        </div>

        <!-- Servings-->
        <div class="flex flex-col gap-3">
          <label for="servings" class="text-lg">Servings</label>
          <input v-model.number="servings" type="number" name="servings" required min="1" step="1"
            class="input-field btn-bar" />
        </div>

        <!-- Cook Time -->
        <div class="flex flex-col gap-3">
          <label for="cookTime" class="text-lg">Time</label>
          <input v-model.number="cookTime" id="cookTime" type="number" placeholder="Minutes" required step="0.1"
            class="input-field btn-bar">
        </div>

        <!-- Steps -->
        <div class="flex flex-col gap-3 relative">
          <label class="text-lg">Steps</label>

          <!-- loop over each step -->
          <div v-for="(step, idx) in steps" :key="idx" class="relative flex items-center btn-bar mb-4">
            <!-- Remove step option: X -->
            <button v-if="idx > 0" type="button" @click="removeStep(idx)"
              class="relative justify-center pl-5 text-red-600 text-xl leading-none mr-5 cursor-pointer">
              ×
            </button>
            <textarea v-model="steps[idx]" name="steps" required placeholder="Step instruction"
              class="w-full h-full pr-14 rounded-[10px] input-field"></textarea>

            <!-- Image upload per step -->
            <input type="file" :id="`stepImage-${idx}`" accept="image/*" class="hidden"
              @change="e => handleImageUpload(e, idx)" />

            <div class="flex items-center gap-4 mt-2">
              <!-- after the textarea -->
              <!-- Image preview -->
              <img v-if="imgPreviews[idx]" :src="imgPreviews[idx]" alt="Preview" class="step-img-preview" />

              <!-- Upload icon -->
              <label :for="`stepImage-${idx}`" class="upload-btn cursor-pointer">
                <img src="../assets/upload.svg" alt="Upload" />
              </label>
              <input type="file" :id="`stepImage-${idx}`" accept="image/*" class="hidden"
                @change="e => handleImageUpload(e, idx)" />

              <!-- Remove image using X -->
              <button v-if="imgPreviews[idx]" type="button" @click.prevent="imgPreviews[idx] = null"
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

          <!-- loop over each ingredient -->
          <div v-for="(ing, idx) in ingredients" :key="idx"
            class="relative flex-col items-center btn-bar mb-4 space-x-2 p-4">
            <!-- Remove ingredient option: X -->
            <button v-if="idx > 0" type="button" @click="removeIngredient(idx)"
              class="relative justify-center text-red-600 text-xl leading-none mr-5 cursor-pointer">
              ×
            </button>
            <!-- Ingredient name -->
            <input v-model="ing.name" type="text" required placeholder="Ingredient" class="input-field btn-bar" />
            <!-- Ingredient quantity -->
            <input v-model.number="ing.quantity" type="number" step="0.01" required placeholder="Qty"
              class="input-field btn-bar" />
            <!-- Ingredient measurement -->
            <select v-model="ing.unit" required class="input-field btn-bar">
              <option disabled value="">Unit</option>
              <option value="g">g</option>
              <option value="kg">kg</option>
              <option value="ml">ml</option>
              <option value="cup">cup</option>
              <option value="tbsp">tbsp</option>
            </select>
          </div>

          <!-- Add Ingredient button -->
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