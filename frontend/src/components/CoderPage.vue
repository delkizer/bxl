<template>
  <div class="coder-container">
    <!-- 흰색 사각형 박스 -->
    <div class="scoreboard-box">
      <!-- 상단: "WARM UP" / "2:00" -->
      <div class="warmup-info">
        <h2>WARM UP</h2>
        <div class="time">2:00</div>
      </div>

      <!-- 팀명, 점수 배치 -->
      <div class="teams-row">
        <!-- 왼쪽 팀 -->
        <div class="team1">
          <div>Team 1</div>
          <div>Hurricanes</div>
        </div>

        <!-- 점수 -->
        <div class="score-display">
          <span class="team1-score">0</span>
          <span class="dash">-</span>
          <span class="team2-score">0</span>
        </div>

        <!-- 오른쪽 팀 -->
        <div class="team2">
          <div>Team 2</div>
          <div>Rockets</div>
        </div>
      </div>
    </div>
    <!-- 하단 버튼 3개 -->
    <div class="clock-buttons-row">
      <div class="clock-button">
        Warm Up Clock <br />
        2:00
      </div>
      <div class="clock-button">
        Match Clock <br />
        10:00
      </div>
      <div class="clock-button">
        Break Clock <br />
        1:00
      </div>
    </div>

    <!-- 하단 영역 수정된 구조 -->
    <div class="bottom-container">
      <!-- 왼쪽 박스 (Hurricanes +1/-1 등) -->
      <div class="bottom-side-box">
        <div class="bottom-label-box left-box">
          <div>Hurricanes</div>
          <div class="btn">+1</div>
          <div class="btn">-1</div>
          <div class="wins-box">
            <span>Wins</span>
            <div class="spinner-buttons">
              <button class="arrow-btn" @click="incrementWins">▲</button>
              <button class="arrow-btn" @click="decrementWins">▼</button>
            </div>
          </div>
        </div>
      </div>

      <!-- 중앙 요소들 컨테이너 -->
      <div class="bottom-center-content">
        <!-- Reset Score 버튼 -->
        <div class="bottom-label-box center-box">
          Reset Score
        </div>

        <!-- 새로운 레이아웃 구조 -->
        <div class="clock-setting-container">
          <!-- 왼쪽 +버튼 컬럼 -->
          <div class="side-buttons-col plus-buttons">
            <button>+1</button>
            <button>+5</button>
            <button>+10</button>
          </div>

          <!-- 중앙 라벨 -->
          <div class="bottom-label-box warmup-setting-label">
            Warm Up Clock Setting
          </div>

          <!-- 오른쪽 -버튼 컬럼 -->
          <div class="side-buttons-col minus-buttons">
            <button>-1</button>
            <button>-5</button>
            <button>-10</button>
          </div>
        </div>

        <!-- Start/Reset 버튼 행 -->
        <div class="start-reset-row">
          <button>Start</button>
          <button>Reset</button>
        </div>
        <!-- 하단 게임 번호 라벨 행 -->
        <div class="game-labels-row">
          <div class="game-label">Gm<br>1</div>
          <div class="game-label">Gm<br>2</div>
          <div class="game-label">Gm<br>3</div>
          <div class="game-label">Gm<br>4</div>
          <div class="game-label">SD</div>
          <div class="game-label">SS</div>
        </div>
      </div>

      <!-- 오른쪽 박스 (Rockets +1/-1 등) -->
      <div class="bottom-side-box">
        <div class="bottom-label-box right-box">
          <div>Rockets</div>
          <div class="btn">+1</div>
          <div class="btn">-1</div>
          <div class="wins-box">
            <span>Wins</span>
            <div class="spinner-buttons">
              <button class="arrow-btn" @click="incrementWins">▲</button>
              <button class="arrow-btn" @click="decrementWins">▼</button>
            </div>
          </div>
        </div>
      </div>
    </div>

    <div class="additional-buttons-row">
      <div class="function-label">
        Next Match
      </div>
      <div class="function-label">
        Result
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: "CoderPage", // 공식 프로젝트 이름
  // 지금은 단순 레이블이므로 별도 데이터는 없어도 됨
  // 향후 data, methods, computed 등을 추가하여 기능 구현
};
</script>

<style scoped>
* {
  box-sizing: border-box;
}

/* 부모 컨테이너 (파란 배경) */
.coder-container {
  position: absolute; /* or fixed */
  top: 0;
  left: 0;
  width: 800px;
  padding: 20px;
  background-color: #4a7ab7;
  color: #000; /* 기본 글자색 */
  font-family: "Arial", sans-serif;
}

/* 흰색 사각형 박스 */
.scoreboard-box {
  background-color: #fff;
  border: 2px solid #2b4d75;
  border-radius: 4px;
  padding: 6px; /* 여백 통일 */
  width: 100%;
  text-align: center;
  margin-bottom: 10px; /* 아래 요소와 간격 */
}

/* "WARM UP" / "2:00" 영역 */
.warmup-info {
  margin-bottom: 5px;
}

.warmup-info h2 {
  margin-bottom: 2px;
  font-size: 1.2rem;
}

.warmup-info .time {
  font-size: 1rem;
}

.teams-row {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin: 0 auto 0px auto;
}

/* 왼쪽, 오른쪽 팀 영역 */
.team1, .team2 {
  width: 25%;
  text-align: center;
  font-size: 1rem;
}

/* 점수 영역 */
.score-display {
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 10px;
}

.team1-score, .team2-score {
  font-size: 1.3rem;
  font-weight: bold;
}

.dash {
  font-size: 1.5rem;
}

/* 하단 버튼 3개 영역 */
.clock-buttons-row {
  display: flex;
  justify-content: center;
  gap: 20px;
  margin-top: 5px;
  margin-bottom: 20px; /* 아래 요소와 간격 추가 */
}

/* 버튼(또는 작은 박스) 스타일 */
.clock-button {
  background-color: #fff;
  border: 2px solid #2b4d75;
  border-radius: 4px;
  width: 150px;
  padding: 10px;
  text-align: center;
  font-size: 1rem;
  line-height: 1.4;
}

/* 하단 컨테이너 레이아웃 수정 */
.bottom-container {
  display: flex;
  justify-content: space-between;
  width: 100%;
}

/* 왼쪽/오른쪽 컨테이너 */
.bottom-side-box {
  width: 120px; /* 고정 너비 설정 */
}

/* 중앙 요소 컨테이너 */
.bottom-center-content {
  display: flex;
  flex-direction: column;
  align-items: center; /* 중앙 정렬 */
  gap: 2px; /* 요소 간 간격 축소 */
}

/* 공통 스타일: 하얀 박스 형태 */
.bottom-label-box {
  background-color: #fff;
  border: 2px solid #2b4d75;
  border-radius: 4px;
  padding: 10px;
  width: 120px;
  text-align: center;
}

/* 공통 버튼 스타일 ( +1, -1, 화살표 등 ) */
.btn, .arrow-btn {
  background: none;
  border: 2px solid #2b4d75;
  border-radius: 4px;
  padding: 4px 8px;
  font-size: 1rem;
  cursor: pointer;
  margin-top: 5px;
}

/* Wins 박스 */
.wins-box {
  background-color: #fff;
  border: 2px solid #2b4d75;
  border-radius: 4px;
  padding: 10px;
  width: 80px;
  text-align: center;
  box-sizing: border-box;
  margin: 5px auto 0 auto; /* (top right bottom left) */
}

/* 스핀 버튼들(▲, ▼) 세로 배치 */
.spinner-buttons {
  display: flex;
  flex-direction: column;
  gap: 4px;
  margin-top: 8px;
}

/* Warm Up Clock Setting 섹션 */
.warmup-setting-row {
  text-align: center;   /* 가로 중앙 정렬 */
  margin-top: 5px;      /* 상단 여백 추가 */
}

/* 상단 큰 라벨 박스 */
.warmup-setting-label {
  display: inline-block;
  background-color: #fff;
  border: 2px solid #2b4d75;
  border-radius: 4px;
  padding: 10px 20px;
  margin-bottom: 5px;
  font-size: 0.9rem;
  min-width: 200px;
  text-align: center;
}

/* 사이드 버튼 컬럼 공통 스타일 */
.side-buttons-col {
  display: flex;
  flex-direction: column;
  gap: 5px;
  width: 80px;
}

/* 중앙 영역: Start/Reset 버튼 */
.center-buttons-area {
  display: flex;
  flex-direction: column;
  width: calc(100% - 180px);
}

/* 중앙 버튼들: Start/Reset */
.center-large-buttons {
  display: flex;
  justify-content: space-between;
  gap: 15px;
}

.center-large-buttons button {
  width: calc(50% - 10px);
  height: 75px;
  font-size: 1.2rem !important;
}

/* 게임 번호 라벨 행 */
.game-labels-row {
  display: flex;
  justify-content: space-between;
  width: 100%;
  max-width: 600px;
  margin: 15px auto 0;
  gap: 10px;
}

/* 게임 라벨 스타일 */
.game-label {
  border: 2px solid #2b4d75;
  border-radius: 4px;
  background-color: #fff;
  font-size: 0.9rem;
  padding: 5px;
  text-align: center;
  width: calc(100% / 6 - 10px);
  height: 60px;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  line-height: 1.3;
}

/* 공통 버튼 스타일 */
.new-layout-container button {
  width: 80px;   /* 버튼 폭 증가 */
  height: 40px;  /* 버튼 높이 */
  background-color: #fff;
  border: 2px solid #2b4d75;
  border-radius: 4px;
  cursor: pointer;
  font-size: 1rem;
  margin: 0;
  box-sizing: border-box;
}

/* 추가 버튼 행 스타일 */
.additional-buttons-row {
  display: flex;
  justify-content: center;
  gap: 20px;
}

/* 기능 라벨 스타일 */
.function-label {
  background-color: #fff;
  border: 2px solid #2b4d75;
  border-radius: 4px;
  padding: 10px 20px;
  font-size: 1rem;
  text-align: center;
  min-width: 120px;
}

/* 시계 설정 컨테이너 */
.clock-setting-container {
  display: flex;
  justify-content: space-between;
  align-items: center;
  width: 100%;
  max-width: 650px;
  margin: 0 auto 0px;
}

/* 사이드 버튼 컬럼 */
.side-buttons-col {
  display: flex;
  flex-direction: column;
  gap: 10px;
  width: 80px;
}

/* Start/Reset 행 */
.start-reset-row {
  display: flex;
  justify-content: center;
  gap: 15px;
  margin-bottom: 00px;
}

.start-reset-row button {
  width: 100px;
  height: 40px;
  font-size: 1.0rem;
  background-color: #fff;
  border: 2px solid #2b4d75;
  border-radius: 4px;
}
</style>
