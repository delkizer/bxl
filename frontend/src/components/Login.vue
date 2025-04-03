<template>
  <div class="login-container">
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
        <button type="submit">Log In</button>
      </form>
    </div>
  </div>
</template>

<script>
import axios from 'axios'

const apiClient = axios.create({
  baseURL: 'https://bxl-dev.delkizer.com',  // 실제 API 서버 도메인/주소
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
.login-container {
  display: flex;
  justify-content: center;
  align-items: center;
  width: 100%;
  height: 100vh;
  background-color: #4b7cb6;
}

.login-box {
  position: absolute;
  top: 50%;      /* 수직 중앙 */
  left: 50%;     /* 수평 중앙 */
  transform: translate(-50%, -50%); /* 자기 크기의 절반만큼 이동해 완전 중앙 정렬 */
  width: 400px;
  padding: 40px;
  background-color: white;
  border: 2px solid #333;
  border-radius: 8px;
  box-shadow: 0px 0px 10px rgba(0, 0, 0, 0.3);
}

.login-box h1 {
  text-align: center;
  margin-bottom: 30px;
  font-family: Arial, sans-serif;
}

.input-wrapper {
  margin-bottom: 20px;
  display: flex;
  flex-direction: column;
}

.input-wrapper label {
  margin-bottom: 8px;
  font-size: 14px;
  font-weight: bold;
  font-family: Arial, sans-serif;
}

.input-wrapper input {
  padding: 10px;
  border: 1px solid #ccc;
  border-radius: 4px;
}

button[type='submit'] {
  width: 100%;
  padding: 15px;
  background-color: red;
  color: white;
  font-size: 16px;
  font-weight: bold;
  font-family: Arial, sans-serif;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}

button[type='submit']:hover {
  background-color: darkred;
}
</style>
