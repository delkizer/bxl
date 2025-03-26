// src/router/index.js
import { createRouter, createWebHistory } from 'vue-router'
import MainPage from '@/components/MainPage.vue'
import CoderPage from '@/components/CoderPage.vue'
import CoderTie from '@/components/CoderTie.vue'
import CoderList from '@/components/CoderList.vue'
import ScorerPage from '@/components/ScorerPage.vue'
import GameInfoPage from "@/components/GameInfoPage.vue";
import TourPage from "@/components/TourPage.vue";
import TourList from "@/components/TourList.vue";
import TeamList from "@/components/TeamList.vue";
import TeamPage from "@/components/TeamPage.vue";
import LoginPage from "@/components/Login.vue";
import {useAuthStore} from "@/stores/auth";

const routes = [
  { path: '/', name: 'home', component: MainPage, meta: { requiresAuth: true } },

  { path: '/login', name: 'login', component: LoginPage },

  { path: '/coder',  name: 'coder', component: CoderPage, meta: { requiresAuth: true } },
  { path: '/coderlist', name: 'coderlist', component: CoderList, meta: { requiresAuth: true } },
  { path: '/codertie', name: 'codertie', component: CoderTie, meta: { requiresAuth: true } },

  { path: '/scorer', name: 'scorer', component: ScorerPage, meta: { requiresAuth: true } },

  { path: '/gameinfo', name: 'gameinfo', component: GameInfoPage, meta: { requiresAuth: true } },

  { path: '/teamlist', name: 'teamlist', component: TeamList, meta: { requiresAuth: true } },
  { path: '/teampage/:team_code?', name: 'teampage', component: TeamPage, meta: { requiresAuth: true } },

  { path: '/tourlist', name: 'tourlist', component: TourList, meta: { requiresAuth: true } },
  { path: '/tourpage/:uuid?', name: 'tourpage', component: TourPage, meta: { requiresAuth: true } },
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
