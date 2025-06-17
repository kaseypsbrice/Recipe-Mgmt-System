<template>
  <main class="pt-10 px-64">
    <!-- Heading -->
    <div class="text-3xl py-3 font-bold text-shadow-md">Create A New Recipe</div>
    <div class="text-lg">Enter the details below to create a new recipe.</div>
    <!-- Divider -->
    <hr class="my-5 border-amber-800">

    <!-- Create Recipe Form -->
    <form class="create-recipe-form">
      <div class="w-full grid grid-cols-2 gap-5 p-10">
        <!-- Recipe Name -->
        <div class="flex flex-col gap-3">
          <label for="recipeName" class="text-lg">Recipe Name</label>
          <input type="text" name="recipeName" required placeholder="" class="input-field btn-bar" />
        </div>

        <!-- Servings-->
        <div class="flex flex-col gap-3">
          <label for="servings" class="text-lg">Servings</label>
          <input type="text" name="servings" required placeholder="" class="input-field btn-bar" />
        </div>

        <!-- Recipe Description -->
        <div class="flex flex-col gap-3">
          <label for="recipeDescription" class="text-lg">Recipe Description</label>
          <input type="text" name="recipeDescription" required placeholder="" class="input-field btn-bar" />
        </div>

        <!-- Cook Time -->
        <div class="flex flex-col gap-3">
          <label for="cookTime" class="text-lg">Time</label>
          <input type="text" name="cookTime" required placeholder="" class="input-field btn-bar" />
        </div>

        <!-- Steps -->
        <div class="flex flex-col gap-3 relative">
          <label for="steps" class="text-lg">Steps</label>
          <input type="text" name="steps" required placeholder="" class="input-field btn-bar" />
          <!-- Add Step Button -->
          <div class="btn-bar add-btn top-full mt-5 cursor-pointer">
            +
          </div>
        </div>

        <!-- Ingredients -->
        <div class="flex flex-col gap-3 relative">
          <label for="ingredients" class="text-lg">Ingredients</label>
          <input type="text" name="ingredients" required placeholder="" class="input-field btn-bar" />
          <!-- Add Ingredient Button -->
          <div class="btn-bar add-btn top-full mt-5 cursor-pointer">
            +
          </div>
        </div>
      </div>
      <!-- Button Container -->
      <div class="flex absolute bottom-0 w-full p-10 gap-10">
        <!-- Submit Button -->
        <button class="btn-bar submit-btn cursor-pointer">Submit</button>
        <!-- Cancel Button -->
        <button class="btn-bar cancel-btn cursor-pointer">
          <RouterLink to="/profile">Cancel</RouterLink>
        </button>
      </div>
    </form>
  </main>
</template>
