import axios from 'axios';
import { useAuthStore } from '@/stores/auth';

const apiClient = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL,
  withCredentials: true,
});

// 요청 인터셉터 (예: 토큰 헤더 붙이는 경우 - HttpOnly면 자동 쿠키 전송되므로 생략 가능)
// apiClient.interceptors.request.use((config) => {
//   // HttpOnly 쿠키면 JS로 접근 불가해서 보통 헤더 안 붙여도 됨
//   // 하지만 토큰을 JS로 저장했다면 config.headers.Authorization = `Bearer ...` 할 수도 있음
//   return config;
// });

// 응답 인터셉터 - 401 처리
apiClient.interceptors.response.use(
  (response) => response,
  async (error) => {
    if (error.response) {
      const status = error.response.status;
      switch (status) {
        case 401:
          const authStore = useAuthStore();
          // 1) refresh_token 시도
          try {
            await authStore.refreshTokens();
            // refresh 성공 시, 다시 원 요청을 재시도
            return apiClient.request(error.config);
          } catch (refreshError) {
            // 2) refresh도 실패 → 로그인 페이지로
            authStore.logout();
          }
          break;

        case 403:
          // 403 처리 (예: 권한 없음)
          // -> 안내 메시지, 페이지 이동, 등등
          console.warn('Access Denied (403)');
          break;

        case 500:
          // 500 처리
          console.error('Server error (500)');
          break;

        default:
          break;
      }
      return Promise.reject(error);
    }

    if ( !error.response) {
      // 네트워크 에러, 서버 다운, CORS 차단 등
      console.error("Network/connection error", error);
      // 사용자에게 "서버 접속 실패" 등의 메시지 표시 가능
      return Promise.reject(error);
    }
  }
);

export default apiClient;
