<script>
import { ref, onMounted, computed } from 'vue';
import axios from 'axios'
import { useAuth } from '../auth';

export default {
    setup() {
        const { state, isLoggedIn, fetchUser } = useAuth();

        const user = computed(() => state.user);
        const recipes = ref([]);  // <--- to store user's recipes
        const error = ref('');

        onMounted(async () => {
            if (state.token && !state.user) {
                await fetchUser();
            }

            if (state.token) {
                try {
                    const res = await axios.get('/my_recipes', {
                        headers: { Authorization: `Bearer ${state.token}` }
                    });
                    recipes.value = res.data;
                } catch (err) {
                    error.value = 'Failed to load your recipes';
                    console.error(err);
                }
            }
        });

        return {
            user,
            isLoggedIn,
            recipes,
            error,
        };
    },
};
axios.defaults.baseURL = 'http://localhost:8000'
</script>

<template>
    <main class="pt-10 px-64">
        <div v-if="isLoggedIn">
            <div class="text-3xl py-3 font-bold text-shadow-md">Profile</div>
            <div class="text-lg" v-if="user">@{{ user.username }}</div>
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
                <div v-for="recipe in recipes" :key="recipe.recipe_id"
                    class="recipe-box border rounded-md shadow-md overflow-hidden mb-6">
                    <div class="w-full flex justify-between px-6 py-2 bg-gray-100">
                        <div class="text-base pr-1 font-semibold">{{ recipe.name }}</div>
                        <div class="text-base text-gray-600" v-if="recipe.user_id === user?.user_id">@{{ user.username }}</div>
                    </div>
                    <div class="recipe-box-img h-48 bg-gray-200">
                        <img :src="recipe.img_path || defaultImage" alt="Recipe Image"
                            class="w-full h-full object-cover" />
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