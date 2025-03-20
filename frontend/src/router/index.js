// src/router/index.js
import { createRouter, createWebHistory } from 'vue-router'
import MainPage from '@/components/MainPage.vue'
import CoderPage from '@/components/CoderPage.vue'
import ScorerPage from '@/components/ScorerPage.vue'
import GameInfoPage from "@/components/GameInfoPage.vue";
import LoginPage from "@/components/Login.vue";
import {useAuthStore} from "@/stores/auth";

const routes = [
    { path: '/', name: 'home', component: MainPage, meta: { requiresAuth: true } },

    { path: '/login', name: 'login', component: LoginPage },

    { path: '/coder',  name: 'coder', component: CoderPage },

    { path: '/scorer', name: 'scorer', component: ScorerPage },

    { path: '/gameinfo', name: 'gameinfo', component: GameInfoPage, },
]

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes
})

router.beforeEach(async (to, from, next) => {
  const  authStore = useAuthStore();
  if ( !authStore.isLoggedIn) {
    try{
      await authStore.fetchCurrentUser();
    } catch ( error) {
      console.error(error);
    }
  }

  if ( to.meta.requiresAuth && !authStore.isLoggedIn) {
    return next('/login');
  }

  return next();
})

export default router
