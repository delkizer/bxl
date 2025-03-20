import { defineStore } from 'pinia';
import apiClient from '@/services/apiClient.js';

export const useAuthStore = defineStore('auth', {
  state: () => ({
    user: null,     // 유저 정보
    isLoggedIn: false,
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
      // 서버가 /api/refresh 로 refresh_token을 검증 후 새 access_token 발급해준다고 가정
      const res = await apiClient.post('/api/refresh');
      // 200이면 쿠키가 갱신됨. user 정보나 응답을 확인할 수도 있음
    },
    async logout() {
      this.isLoggedIn = false;
      this.user = null;
      // 서버에 /api/logout 같은 게 있다면 호출해서 쿠키 만료시켜도 됨
      // 라우터 이동 등
    },
    async fetchCurrentUser() {
      // 앱 로딩 시 유저 정보를 가져와 세션 상태 파악
      try {
        const res = await apiClient.get('/api/me');
        this.user = res.data;
        this.isLoggedIn = true;
      } catch (err) {
        this.isLoggedIn = false;
        this.user = null;
      }
    }
  },
});
