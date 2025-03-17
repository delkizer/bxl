// src/router/index.js
import { createRouter, createWebHistory } from 'vue-router'
import MainPage from '@/components/MainPage.vue'
import CoderPage from '@/components/CoderPage.vue'
import ScorerPage from '@/components/ScorerPage.vue'
import GameInfoPage from "@/components/GameInfoPage.vue";

const routes = [
    {
      path: '/',
      name: 'home',
      component: MainPage
    },
    {
      path: '/coder',
      name: 'coder',
      component: CoderPage
    },
    {
      path: '/scorer',
      name: 'scorer',
      component: ScorerPage
    },
    {
      path: '/gameinfo',
      name: 'gameinfo',
      component: GameInfoPage,
    },
]

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes
})

export default router
