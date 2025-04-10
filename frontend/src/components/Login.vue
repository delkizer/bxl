<template>
  <div class="login-page">
    <div class="login-box">
      <h1>Login</h1>
      <form @submit.prevent="onLogin">
        <div class="input-wrapper">
          <label for="username">User ID</label>
          <input
            type="text"
            id="username"
            v-model="username"
            placeholder="Enter your username"
          />
        </div>
        <div class="input-wrapper">
          <label for="password">Password</label>
          <input
            type="password"
            id="password"
            v-model="password"
            placeholder="Enter your password"
          />
        </div>
        <button type="submit" class="login-btn">Log In</button>
      </form>
    </div>
  </div>
</template>

<script>
import axios from 'axios'

const apiClient = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL,
  withCredentials: true,
})

export default {
  name: 'LoginPage',
  data() {
    return {
      username: '',
      password: ''
    };
  },
  methods: {
    async onLogin() {
      try {
        const res = await apiClient.post('/api/login', {
          email: this.username,
          password: this.password
        })
        if (res.status === 200) {
          console.log('로그인 성공', res.data)
          this.$router.push('/')
        }
      } catch (error) {
        console.error(error);
        alert('로그인 중 오류가 발생했습니다. 다시 시도해주세요.');
      }
    }
  }
};
</script>

<style scoped>
/*
  1) login-page:
     - 화면 너비 < 1024px: flexbox 중앙
     - 화면 너비 >= 1024px: absolute 중앙
     - 밝은 배경(#f8fafc)
*/
.login-page {
  width: 100%;
  min-height: 100vh;
  background-color: #f8fafc;
  display: flex;
  align-items: center;
  justify-content: center;
  box-sizing: border-box;
  padding: 2rem;
}

/* 1024px 이상일 때 절대 위치로 완전 중앙 */
@media (min-width: 1024px) {
  .login-page {
    position: absolute;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);
  }
}

/*
  2) login-box:
     - 흰색 카드 스타일
*/
.login-box {
  width: 400px;
  background-color: #fff;
  border-radius: 8px;
  box-shadow: 0 4px 12px rgba(0,0,0,0.1);
  padding: 2rem;
  box-sizing: border-box;
}

/* 타이틀 */
.login-box h1 {
  text-align: center;
  margin-bottom: 1.5rem;
  font-family: Arial, sans-serif;
  font-size: 1.5rem;
  font-weight: bold;
}

/* input-wrapper */
.input-wrapper {
  margin-bottom: 1rem;
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.input-wrapper label {
  font-size: 0.9rem;
  font-weight: bold;
  font-family: Arial, sans-serif;
}

/* 인풋 */
.input-wrapper input {
  padding: 0.75rem;
  border: 1px solid #ddd;
  border-radius: 4px;
  font-size: 0.9rem;
  outline: none;
}

.input-wrapper input:focus {
  border-color: #93c5fd; /* 포커스 시 파랑 테두리 */
  box-shadow: 0 0 0 3px rgba(147,197,253,0.3);
}

/*
  3) 로그인 버튼
     - 기존 “저장(녹색)” 계열과 통일감
*/
.login-btn {
  width: 100%;
  padding: 0.75rem;
  background-color: #70c16b; /* 초록 */
  color: #fff;
  font-size: 1rem;
  font-weight: bold;
  font-family: Arial, sans-serif;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  transition: background-color 0.2s ease, transform 0.2s ease;
}

.login-btn:hover {
  background-color: #64ad5f;
}
.login-btn:active {
  transform: scale(0.98);
}
</style>
