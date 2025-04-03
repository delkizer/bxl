import { defineStore } from 'pinia';
import apiClient from '@/services/apiClient.js';
// router 인스턴스(혹은 useRouter 훅)를 가져옵니다.
import router from '@/router'; // 예: '@/router/index.js'

export const useAuthStore = defineStore('auth', {
  state: () => ({
    user: null,
    isLoggedIn: false,
    isRefreshing: false,
    refreshTried: false,
  }),
  actions: {
    async login(email, password) {
      try {
        const res = await apiClient.post('/api/login', { email, password });
        if (res.status === 200) {
          this.isLoggedIn = true;
          // this.user = ... (옵션: 사용자 정보 저장)
        }
      } catch (err) {
        console.error('login error:', err);
      }
    },

    async refreshTokens() {
      // 이미 refresh 중이라면 재호출 방지
      if (this.isRefreshing) return false;

      // 이미 refreshTried가 true면 다시 시도하지 않고 logout
      if (this.refreshTried) {
        await this.logout();
        return false;
      }

      try {
        this.isRefreshing = true;
        this.refreshTried = true; // 이번에 한 번 refresh

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

      // 실패 처리
      await this.logout();
      return false;
    },

    async logout() {
      this.isLoggedIn = false;
      this.user = null;
      this.refreshTried = false;
      router.push('/login');
    },
    async fetchCurrentUser() {
      try {
        const res = await apiClient.get('/api/userinfo');
        this.user = res.data;
        this.isLoggedIn = true;
      } catch (err) {
        // 토큰 만료나 인증 실패(401) 처리
        if (err.response && err.response.status === 401) {
          // 이미 refresh를 시도했거나, 현재 refresh 중이면 무한 루프 방지
          if (this.refreshTried || this.isRefreshing) {
            console.log('Already tried refresh or is refreshing. Logging out...');
            this.logout();
            // 로그아웃 후 로그인 화면으로 이동
            router.push('/login');
          } else {
            console.log('Try refresh token...');
            this.refreshTried = true;
            const success = await this.refreshTokens();
            if (success) {
              // refresh 성공 시 다시 시도
              console.log('Refresh success. Retry fetchCurrentUser...');
              await this.fetchCurrentUser();
            } else {
              // refresh 실패 시 로그아웃 후 로그인화면 이동
              console.log('Refresh failed. Logging out...');
              this.logout();
              router.push('/login');
            }
          }
        } else {
          // 401 외 다른 오류
          console.error('fetchCurrentUser error:', err);
        }
      }
    },
  },
});
