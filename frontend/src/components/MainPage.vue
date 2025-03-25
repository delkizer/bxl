<template>
  <div class="main-container">
    <div class="centered-line"></div>
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
  </div>
    <div class="buttons-wrapper additional-buttons">
    <div class="button tour-button" @click="goToTourPage">
      <p>BXL</p>
      <p>Tour's Page</p>
    </div>
    <div class="button game-button" @click="goToGamePage">
      <p>BXL</p>
      <p>Game's Page</p>
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
      this.$router.push('/tourlist')
    },
    goToGamePage() {
      this.$router.push('/gamelist')
    }
  }
}
</script>

<style scoped>
.main-container {
  width: 100%;
  height: 100vh;
  background-color: #4b7cb6;
  position: relative;
  overflow: hidden;
}

/* 가시적 중앙선(테스트용, 필요없으면 제거) */
.centered-line {
  position: absolute;
  top: 0;
  left: 50%;
  width: 1px;
  height: 100%;
  background-color: rgba(255, 0, 0, 0.3);
  z-index: 10;
  pointer-events: none;
}

.buttons-wrapper {
  position: fixed;
  top: 30%;
  left: 0;
  right: 0;
  display: flex;
  justify-content: center;
  transform: translateY(-50%);
}

.additional-buttons {
  /* 새로 추가된 버튼 영역 스타일 */
  position: fixed;
  top: 65%;
  left: 0;
  right: 0;
  display: flex;
  justify-content: center;
  transform: translateY(-50%);
}


.button {
  width: 300px;
  height: 275px;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  border: 2px solid #333;
  font-family: Arial, sans-serif;
  cursor: pointer;
  box-shadow: 0px 0px 10px rgba(0, 0, 0, 0.3);
  flex-shrink: 0;
}

.button p {
  margin: 10px 0;
  font-size: 32px;
  font-weight: normal;
  text-align: center;
}

.corder-button {
  background-color: red;
  color: black;
  margin-right: 40px;
}

.scorer-button {
  background-color: white;
  color: black;
  margin-left: 40px;
}

.tour-button {
  background-color: #4CAF50;
  color: black;
  margin-right: 40px;
}

.game-button {
  background-color: #FFC107;
  color: black;
  margin-left: 40px;
}



/* 화면이 작을 때 */
@media screen and (max-width: 960px) {
  .buttons-wrapper {
    flex-direction: column;
    align-items: center;
  }

  .corder-button {
    margin-right: 0;
    margin-bottom: 40px;
  }

  .scorer-button {
    margin-left: 0;
  }
}

</style>
