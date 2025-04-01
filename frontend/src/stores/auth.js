import { defineStore } from 'pinia';
import apiClient from '@/services/apiClient.js';

export const useAuthStore = defineStore('auth', {
  state: () => ({
    user: null,     // 유저 정보
    isLoggedIn: false,
    isRefreshing: false,
    refreshTried: false,
  }),
  actions: {
    async login(email, password) {
      const res = await apiClient.post('/api/login', { email, password });
      if (res.status === 200) {
        // user 정보를 /me API 등에서 재호출하거나, 응답 바디에 담아줄 수도 있음
        this.isLoggedIn = true;
        // this.user = ...
      }
      // 에러 처리 등은 try-catch
    },
    async refreshTokens() {
      try {
        this.isRefreshing = true;
        const res = await apiClient.post('/api/refresh_token');
        if (res.status === 200) {
          // 새 access_token, refresh_token 쿠키가 세팅되었을 것
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
    async logout() {
      this.isLoggedIn = false;
      this.user = null;
      this.refreshTried = false;
    },
    async fetchCurrentUser() {
      try {
        const res = await apiClient.get('/api/userinfo');
        this.user = res.data;
        this.isLoggedIn = true;
      } catch (err) {
        // 401인 경우 → 만료 가능성. refresh 시도
        if (err.response && err.response.status === 401) {
          // 이미 refresh 시도했거나, 현재 refresh 중이면 무한 루프 방지
          if (this.refreshTried || this.isRefreshing) {
            console.log('Already tried refresh or is refreshing. Logging out...');
            this.logout();
          } else {
            console.log('Try refresh token...');
            this.refreshTried = true;
            const success = await this.refreshTokens();
            if (success) {
              // refresh 성공 시 → 다시 시도
              console.log('Refresh success. Retry fetchCurrentUser...');
              await this.fetchCurrentUser();
            } else {
              // refresh 실패 시 → 로그아웃
              console.log('Refresh failed. Logging out...');
              this.logout();
            }
          }
        } else {
          // 401 외 다른 오류 처리
          console.error('fetchCurrentUser error:', err);
        }
      }
    },
  },
});
