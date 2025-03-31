<template>
  <div class="main-container">
    <!-- 첫 번째 줄 -->
    <div class="buttons-wrapper">
      <div class="button corder-button" @click="goToCoderPage">
        <p>BXL</p>
        <p>Coder's Page</p>
      </div>
      <div class="button scorer-button" @click="goToScorerPage">
        <p>BXL</p>
        <p>Scorer's Page</p>
      </div>
    </div>

    <!-- 두 번째 줄 -->
    <div class="buttons-wrapper">
      <div class="button tour-button" @click="goToTourPage">
        <p>BXL</p>
        <p>Tour's Page</p>
      </div>
      <div class="button team-button" @click="goToGamePage">
        <p>BXL</p>
        <p>Team's Page</p>
      </div>
    </div>

    <!-- 세 번째 줄 -->
    <div class="buttons-wrapper">
      <div class="button official-button" @click="goToOfficialPage">
        <p>BXL</p>
        <p>Official's Page</p>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'MainPage',
  methods: {
    goToCoderPage() {
      this.$router.push('/coderlist');
    },
    goToScorerPage() {
      this.$router.push('/scorer');
    },
    goToTourPage() {
      this.$router.push('/tourlist');
    },
    goToGamePage() {
      this.$router.push('/teamlist');
    },
    goToOfficialPage() {
      this.$router.push('/officiallist');
    }
  }
}
</script>

<style scoped>
/* 브라우저 전체를 100%로 쓰기 위해 html, body 초기 세팅 */
html, body {
  margin: 0;
  padding: 0;
  height: 100%;
}

/* 메인 컨테이너를 화면 정중앙에 배치 */
.main-container {
  position: absolute;
  width: 800px;
  margin: 0 auto;
  padding: 16px;
  top: 50%;      /* 수직 중앙 */
  left: 50%;     /* 수평 중앙 */
  transform: translate(-50%, -50%); /* 자기 크기의 절반만큼 이동해 완전 중앙 정렬 */
}

/* 각 줄(버튼 묶음)을 가로로 배치하고 중앙 정렬 */
.buttons-wrapper {
  display: flex;
  justify-content: center;
  margin: 20px 0; /* 줄 간격 */
}

/* 공통 버튼 스타일 */
.button {
  width: 300px;
  height: 165px; /* 기존 높이(275px)의 약 60% */
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  border: 2px solid #333;
  font-family: Arial, sans-serif;
  cursor: pointer;
  box-shadow: 0px 0px 10px rgba(0, 0, 0, 0.3);
  margin: 0 20px; /* 버튼 간 좌우 간격 */
}

/* 글자 스타일 */
.button p {
  margin: 5px 0;
  font-size: 32px;
  text-align: center;
}

/* 버튼별 색상 구분 */
.corder-button {
  background-color: red;
  color: black;
}

.scorer-button {
  background-color: white;
  color: black;
}

.tour-button {
  background-color: #4CAF50;
  color: black;
}

.team-button {
  background-color: #FFC107;
  color: black;
}

.official-button {
  background-color: #9c27b0;
  color: white;
}

/* 반응형 처리: 960px 이하에서는 한 줄에 2개 버튼이 겹치지 않도록 세로로 배치 */
@media screen and (max-width: 960px) {
  .buttons-wrapper {
    flex-direction: column;
  }
  .button {
    margin: 10px 0;
  }
}
</style>
