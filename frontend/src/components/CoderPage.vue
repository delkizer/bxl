<template>
  <!-- 전체를 감싸는 래퍼 (필요시) -->
  <div>
    <!-- 1) scoreboard 영역 -->
    <div class="scoreboard">
      <div class="warmup-header">
        <!-- 상단: WARM UP / 시간 -->
        <div class="warmup-row">
          <span class="warmup-title">WARM UP</span>
          <span class="warmup-time">{{ coderStore.formattedWarmUpTime }}</span>
        </div>
        <!-- 팀명 / 점수 -->
        <div class="teams-row">
          <span class="team-name">{{ coderStore.teamA.name }}</span>
          <span class="score">{{ coderStore.teamA.score }} - {{ coderStore.teamB.score }}</span>
          <span class="team-name">{{ coderStore.teamB.name }}</span>
        </div>
      </div>
    </div>

    <!-- 2) 별도의 라벨 영역 -->
    <div class="label-section">
      <div class="label-row">
        <div class="clock-box">
          <p class="clock-title">Warm Up Clock</p>
          <p>{{ coderStore.formattedWarmUpTime }}</p>
        </div>
        <div class="clock-box">
          <p>Match Clock</p>
          <p>{{ coderStore.formattedMatchTime }}</p>
        </div>
        <div class="clock-box">
          <p>Break Clock</p>
          <p>{{ coderStore.formattedBreakTime }}</p>
        </div>
      </div>
      <!-- 중앙에 Reset Score 박스/버튼 -->
      <div class="reset-row">
        <div class="reset-box" @click="coderStore.resetScore">Reset Score</div>
      </div>
      <!-- Warm Up Clock Setting 영역 -->
      <div class="warmup-clock-setting-row">
        <div class="win-tracker">
          <div class="win-tracker-team">{{ coderStore.teamA.name }}</div>

          <!-- 여기서 badminton-stats를 사용 -->
          <div class="win-tracker-row badminton-stats">
            <!-- POINT 칸 -->
            <div class="stats-box">
              <span class="tracker-label">POINT</span>
              <div class="arrow-button" @click="coderStore.incrementPoint('A')"><span class="arrow-up"></span></div>
              <span class="tracker-value">{{ coderStore.teamA.point }}</span>
              <div class="arrow-button" @click="coderStore.decrementPoint('A')"><span class="arrow-down"></span></div>
            </div>

            <!-- GAME 칸 -->
            <div class="stats-box">
              <span class="tracker-label">GAME</span>
              <div class="arrow-button" @click="coderStore.incrementGame('A')"><span class="arrow-up"></span></div>
              <span class="tracker-value">{{ coderStore.teamA.game }}</span>
              <div class="arrow-button" @click="coderStore.decrementGame('A')"><span class="arrow-down"></span></div>
            </div>

            <!-- SCORE 칸 -->
            <div class="stats-box">
              <span class="tracker-label">SCORE</span>
              <div class="arrow-button" @click="coderStore.incrementScore('A')"><span class="arrow-up"></span></div>
              <span class="tracker-value">{{ coderStore.teamA.score }}</span>
              <div class="arrow-button" @click="coderStore.decrementScore('A')"><span class="arrow-down"></span></div>
            </div>

          </div>
        </div>
        <div class="warmup-clock-setting-col">
          <div class="warmup-clock-adjust-box" @click="coderStore.adjustSelectedTime(1)">+1</div>
          <div class="warmup-clock-adjust-box" @click="coderStore.adjustSelectedTime(5)">+5</div>
          <div class="warmup-clock-adjust-box" @click="coderStore.adjustSelectedTime(10)">+10</div>
        </div>
        <!-- 중앙 영역을 감싸는 컨테이너 추가 -->
        <div class="warmup-clock-setting-center">
          <div class="non-stop-row">
            <label><input type="checkbox" v-model="coderStore.isNonStop" @change="onNonStopChange"/> Non-Stop Mode</label>
          </div>
          <div class="warmup-clock-setting-box" @click="coderStore.cycleTimeTarget">
            {{ coderStore.currentTargetLabel}}
          </div>
          <!-- START, RESET 버튼을 중앙 영역 아래에 배치 -->
          <div class="warmup-control-row">
            <button class="warmup-control-box" @click="coderStore.startTimer()">START</button>
            <button class="warmup-control-box" @click="coderStore.pauseTimer()">PAUSE</button>
            <button class="warmup-control-box" @click="onResetClick">RESET</button>
          </div>
        </div>
        <div class="warmup-clock-setting-col">
          <div class="warmup-clock-adjust-box" @click="coderStore.adjustSelectedTime(-1)">-1</div>
          <div class="warmup-clock-adjust-box" @click="coderStore.adjustSelectedTime(-5)">-5</div>
          <div class="warmup-clock-adjust-box" @click="coderStore.adjustSelectedTime(-10)">-10</div>
        </div>
        <div class="win-tracker">
          <div class="win-tracker-team">
            {{ coderStore.teamB.name }}
          </div>
          <!-- 예: 3개 칸(Score/Game/Point)을 가로로 나열 -->
          <div class="win-tracker-row badminton-stats">
            <!-- 1) SCORE 칸 -->
            <div class="stats-box">
              <span class="tracker-label">SCORE</span>
              <!-- 위쪽 화살표(증가) -->
              <div class="arrow-button" @click="coderStore.incrementScore('B')">
                <span class="arrow-up"></span>
              </div>
              <!-- 현재 스코어 값 (예: teamB.score) -->
              <span class="tracker-value">{{ coderStore.teamB.score }}</span>
              <!-- 아래쪽 화살표(감소) -->
              <div class="arrow-button" @click="coderStore.decrementScore('B')">
                <span class="arrow-down"></span>
              </div>
            </div>

            <!-- 2) GAME 칸 -->
            <div class="stats-box">
              <span class="tracker-label">GAME</span>
              <div class="arrow-button" @click="coderStore.incrementGame('B')">
                <span class="arrow-up"></span>
              </div>
              <span class="tracker-value">{{ coderStore.teamB.game }}</span>
              <div class="arrow-button" @click="coderStore.decrementGame('B')">
                <span class="arrow-down"></span>
              </div>
            </div>

            <!-- 3) POINT 칸 -->
            <div class="stats-box">
              <span class="tracker-label">POINT</span>
              <div class="arrow-button" @click="coderStore.incrementPoint('B')">
                <span class="arrow-up"></span>
              </div>
              <span class="tracker-value">{{ coderStore.teamB.point }}</span>
              <div class="arrow-button" @click="coderStore.decrementPoint('B')">
                <span class="arrow-down"></span>
              </div>
            </div>
          </div>
        </div>
      </div>
      <div>
        <!-- 추가: 6개 라벨 (가로 배치) -->
        <div class="extra-label-row">
          <div class="extra-label-box">Gm 1</div>
          <div class="extra-label-box">Gm 2</div>
          <div class="extra-label-box">Gm 3</div>
          <div class="extra-label-box">Gm 4</div>
          <div class="extra-label-box">SD</div>
          <div class="extra-label-box">SS</div>
        </div>
        <!-- 새로 추가: Next Match / Result 라벨 행 -->
        <div class="extra-label-row">
          <div class="warmup-control-box extra-label-control">Next Match</div>
          <div class="warmup-control-box extra-label-control">RESULT</div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { useCoderStore } from "@/stores/coder.js";

export default {
  name: "CoderPage",
  mounted() {
    const coderStore = useCoderStore()

    // tieData가 아직 없으면 setTieData()로 설정
    coderStore.setTieData(coderStore.tournament_uuid, coderStore.tieNo, coderStore.gameDate)

    // API 호출
    coderStore.fetchCoderInfo()

    // websocket 호출
    coderStore.initWebSocket()
  },
  beforeUnmount() {
    const coderStore = useCoderStore()

    coderStore.closeWebSocket();
  },
  methods: {
    onResetClick() {
      if (!this.coderStore.isWarmUpRunning) {
        this.coderStore.resetWarmUpClock()
      }
    }
  },
  computed: {
    coderStore() {
      return useCoderStore()
    }
  },
  setup() {
    const coderStore = useCoderStore();

    function onNonStopChange(event) {
      const newVal = event.target.checked;
      coderStore.setNonStop(newVal)
    }

    return {
      coderStore, onNonStopChange
    };
  }
}

</script>

<style scoped>
/* 1) scoreboard 스타일 */
.scoreboard {
  background-color: #ffffff;
  color: #181818;
  padding: 1rem;
  margin-top: 10px;
}

.warmup-header {
  text-align: center;
}

.warmup-row {
  font-size: 1.3rem;
  margin-bottom: 0.5rem;
}
.warmup-title {
  margin-right: 1rem;
  font-weight: bold;
  letter-spacing: -0.02em;
}
.warmup-time {
  font-weight: bold;
}

.teams-row {
  display: flex;
  justify-content: center;
  gap: 1rem;
  font-size: 1rem;
  margin-top: 0.5rem;
}
.team-name {
  font-weight: bold;
}
.score {
  padding: 0 1rem;
}

/* 2) label-section 스타일 */
.label-section {
  margin-top: 1rem;
  text-align: center;
}

.label-row {
  display: inline-flex;
  gap: 2rem;
}

.clock-box {
  background-color: #fff;
  color: #181818;
  border: 1px solid #181818;
  border-radius: 4px;
  width: 120px;
  text-align: center;
  font-weight: bold;
  margin-bottom: 1rem;
}

.clock-box p {
  margin: 0.1rem 0;
}

.clock-box .clock-title {
  letter-spacing: -0.02em;
}

/* Reset Score 중앙 배치 */
.reset-row {
  display: flex;
  justify-content: center;
  margin-top: 1rem;
}

.reset-box {
  background-color: #fff;
  color: #181818;
  border: 1px solid #181818;
  border-radius: 4px;
  padding: 0.5rem 1rem;
  font-weight: bold;
  cursor: pointer;
}

/* Warm Up Clock Setting 전체 영역 */
.warmup-clock-setting-row {
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 1rem;
  margin-top: 1rem;
}

/* 왼쪽/오른쪽 조절 버튼 */
.warmup-clock-setting-col {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.warmup-clock-adjust-box {
  background-color: #fff;
  color: #181818;
  border: 1px solid #181818;
  border-radius: 4px;
  padding: 0.2rem;
  font-weight: bold;
  text-align: center;
  width: 60px;
  cursor: pointer;
}

/* 중앙 영역: Warm Up Clock Setting과 START/RESET 버튼을 감싸는 컨테이너 */
.warmup-clock-setting-center {
  display: flex;
  flex-direction: column;
  align-items: center;
}

/* 중앙의 Warm Up Clock Setting 박스 */
.warmup-clock-setting-box {
  background-color: #fff;
  color: #181818;
  border: 1px solid #181818;
  border-radius: 4px;
  padding: 0.2rem;
  font-weight: bold;
  text-align: center;
  width: 200px;
  cursor: pointer;
}

/* START, RESET 컨트롤 행 (수평 배치) */
.warmup-control-row {
  display: flex;
  gap: 1rem;
  margin-top: 0.5rem;
}

/* START, RESET 버튼 스타일 */
.warmup-control-box {
  background-color: #fff;
  color: #181818;
  border: 1px solid #181818;
  border-radius: 4px;
  padding: 0.2rem 0.5rem;
  font-weight: bold;
  text-align: center;
  cursor: pointer;
}

.extra-label-row {
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 0.5rem;
  margin-top: 0.5rem;
}

.extra-label-box {
  background-color: #fff;
  color: #181818;
  border: 1px solid #181818;
  border-radius: 4px;
  padding: 0.2rem 0.5rem;
  font-weight: bold;
  text-align: center;
  cursor: pointer;
  width: 55px;
}

.extra-label-control {
  width: 100px;  /* 원하는 폭으로 조정 (예: 100px) */
  display: flex;
  justify-content: center;
  align-items: center;
  font-weight: bold;  /* 볼드체 유지 */
}

/* win-tracker 컨테이너 */
.win-tracker {
  margin-top: 0.5rem;
  text-align: center;
  /* 필요시 배경/테두리 추가 */
  background-color: #fff;
  /*
  border: 1px solid #181818;
   */
  border-radius: 4px;
}

/* 팀명 */
.win-tracker-team {
  text-align: center;
  font-weight: bold;
  margin-bottom: 0.5rem;
}

/* -1/+1 버튼 가로 배치 */
.win-tracker-row {
  display: flex;
  flex-direction: column;
  justify-content: center;
  gap: 1rem; /* POINT와 WINS 영역 사이의 간격 */
}

/* 라벨: POINT, WINS 텍스트 */
.tracker-label {
  font-weight: bold;
  /* 필요 시 폰트크기 조정 */
}

/* 점수/승수 값 */
.tracker-value {
  font-weight: bold;
  padding: 0 0.5rem;
  /* 원하면 배경색/테두리 추가 가능 */
}

.win-tracker-wins label {
  font-weight: bold;
}

.win-tracker-wins input[type="number"] {
  width: 60px;
  text-align: center;
}

/* 버튼 컨테이너: 폭 좁은 사각형, 흰 바탕 + 검은 테두리 */
.arrow-button {
  width: 24px;
  height: 24px;
  background-color: #fff;
  border: 1px solid #000;
  border-radius: 4px;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  margin: 0.2rem 0; /* 화살표들 사이의 간격 */
}

/* 위쪽 삼각형 */
.arrow-up {
  width: 0;
  height: 0;
  border-left: 5px solid transparent;
  border-right: 5px solid transparent;
  border-bottom: 6px solid #000; /* 검은색 삼각형 */
}

/* 아래쪽 삼각형 */
.arrow-down {
  width: 0;
  height: 0;
  border-left: 5px solid transparent;
  border-right: 5px solid transparent;
  border-top: 6px solid #000; /* 검은색 삼각형 */
}

/* 가로 배치하되, 각 칸(stats-box)은 세로 스택 */
.win-tracker-row.badminton-stats {
  display: flex;
  justify-content: center; /* 좌우 가운데 정렬 (원하는 대로 조정) */
  gap: 1rem;               /* 칸 사이 간격 */
  flex-direction: row;
}

/* 한 칸(Score/Game/Point)을 세로로 쌓는 박스 */
.stats-box {
  display: flex;
  flex-direction: column;
  align-items: center;
  width: 70px;           /* 폭을 줄이면 전체 가로폭이 줄어듦 */
  padding: 0.3rem 0;     /* 위아래 여백 */
  border: 1px solid #ddd;/* 필요하면 테두리 or 배경색 */
  border-radius: 6px;
}

/* 라벨 (SCORE / GAME / POINT) */
.tracker-label {
  font-weight: bold;
  margin-bottom: 0.2rem;
}

.non-stop-row {
  text-align: center;
  margin-top: 1rem;
  margin-bottom: 1rem;
  background-color: #fff; /* 흰색 배경 추가 */
  padding: 0.5rem; /* 예시: 배경에 약간의 여백 */
  border-radius: 4px; /* 예시: 모서리 둥글림 */
  border: 1px solid #ccc; /* 예시: 테두리 추가 */

}

</style>
