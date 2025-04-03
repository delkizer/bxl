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
      try {
        // 1) 서버에 /api/userinfo 요청 (쿠키는 withCredentials 로 자동 전송)
        const res = await apiClient.get('/api/userinfo');
        this.user = res.data;
        this.isLoggedIn = true;

      } catch (err) {
        if (err.response && err.response.status === 401) {
          // 2) 만료 or 인증 안 됨
          if (this.refreshTried || this.isRefreshing) {
            // 이미 refresh 시도했으면 → 무한 루프 방지
            console.log('Already tried refresh or is refreshing. Logging out...');
            this.logout();
            if (router.currentRoute.value.name !== 'login') {
              router.push('/login');
            }
          } else {
            // 3) 아직 refresh 안 했다면 -> refreshTokens() 시도
            console.log('Try refresh token...');
            this.refreshTried = true;

            const success = await this.refreshTokens();
            if (success) {
              console.log('Refresh success. Retry fetchCurrentUser...');
              await this.fetchCurrentUser();
            } else {
              console.log('Refresh failed. Logging out...');
              this.logout();
              if (router.currentRoute.value.name !== 'login') {
                router.push('/login');
              }
            }
          }
        } else {
          // 401 외 다른 오류
          console.error('fetchCurrentUser error:', err);
        }
      }
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
