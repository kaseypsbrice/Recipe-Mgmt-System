import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '@/views/Home.vue'
import ExploreView from '@/views/Explore.vue'
import ProfileView from '@/views/Profile.vue'
import CreateNewRecipeView from '@/views/CreateNewRecipe.vue'
import LoginView from '@/views/Login.vue'
import SignupView from '@/views/Signup.vue'
import RecipeView from '@/views/Recipe.vue'
import EditRecipeView from '@/views/EditRecipe.vue'
import { useAuth } from '../auth'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: HomeView
    },
    {
      path: '/login',
      component: LoginView
    },
    {
      path: '/signup',
      component: SignupView
    },
    {
      path: '/explore',
      name: 'explore',
      component: ExploreView
    },
    {
      path: '/profile',
      name: 'profile',
      component: ProfileView
    },
    {
      path: '/create-new-recipe',
      name: 'create-new-recipe',
      component: CreateNewRecipeView
    },
    {
      path: '/recipe/:id',
      name: 'RecipeDetail',
      component: RecipeView
    },
    {
      path: '/edit-recipe/:id',
      name: 'EditRecipe',
      component: EditRecipeView
    }
  ],
})

// Synchronous guard, return a redirect or undefined
router.beforeEach((to, from) => {
  const { isLoggedIn } = useAuth()
  if (to.meta.requiresAuth && !isLoggedIn.value) {
    return { path: '/login', query: { redirect: to.fullPath } }
  }
  // return nothing -> proceed normally
})

export default router
