<template>
    <div>
        <h1>Recipes</h1>
        <RecipeCard v-for="recipe in recipes" :key="recipe.id" :recipe="recipe" />
    </div>
</template>

<script>
import axios from 'axios';
import RecipeCard from './RecipeCard.vue';

export default {
    components: {RecipeCard},
    data() {
        return {
            recipes: [],
        };
    },
    async created() {
        const response = await axios.get('http://your-backend-url/api/recipes');
        this.recipes = response.data;
    },
};
</script>