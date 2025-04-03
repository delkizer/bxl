import { defineStore } from 'pinia';
import apiClient from '@/services/apiClient';
import router from '@/router';

export const useAuthStore = defineStore('auth', {
  state: () => ({
    user: null,
    isLoggedIn: false,
    isRefreshing: false,
    refreshTried: false,
  }),
  actions: {
    async fetchCurrentUser() {
        const res = await apiClient.get('/api/userinfo');
        this.user = res.data;
        this.isLoggedIn = true;
    },

    async refreshTokens() {
      if (this.isRefreshing) return false;
      this.isRefreshing = true;
      try {
        const res = await apiClient.post('/api/refresh_token');
        if (res.status === 200) {
          console.log('Token refreshed.');
          return true;
        }
      } catch (err) {
        console.error('Refresh token failed:', err);
      } finally {
        this.isRefreshing = false;
      }
      return false;
    },

    logout() {
      this.isLoggedIn = false;
      this.user = null;
      this.refreshTried = false;
      // 필요하다면 쿠키 삭제 로직 추가(서버에 /api/logout 등)
      router.push('/login');
    },
  },
});
