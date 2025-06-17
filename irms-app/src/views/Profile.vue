<template>
  <main class="pt-10 px-64">
    <!-- Heading -->
    <div class="text-3xl py-3 font-bold text-shadow-md">Profile</div>
    <div class="text-lg">@username</div>
    <!-- Divider -->
    <hr class="my-5 border-amber-800">
    <!-- Search Bar -->
    <div class="w-1/3">
      <div class="search-bar">
        <img src="../assets/search-icon.svg" style="height: 1.3em; width: 1.3em;">
        <input type="search" placeholder="Search..." class="search-input" />
      </div>
    </div>
    <!-- Create New Recipe Button -->
    <div class="create-new-recipe-btn"></div>
    <!-- Settings Button -->
    <!-- <div class="settings-btn"></div> -->

    <!-- Explore Recipes -->
    <div class="explore-recipes-container">
      <!-- This will be an iterated backend task -->

      <!-- Recipe Display Box Layout -->
      <div class="recipe-box">
        <div class="w-full flex justify-between px-6 py-2">
          <div class="text-base pr-1">Recipe Name</div>
          <div class="text-base text-gray-600">@username</div>
        </div>
        <div class="recipe-box-img">img</div>
      </div>

      <!-- Added some more to test column layout -->
      <div class="recipe-box"></div>
      <div class="recipe-box"></div>
      <div class="recipe-box"></div>
      <div class="recipe-box"></div>
      <div class="recipe-box"></div>
    </div>
  </main>
</template>
