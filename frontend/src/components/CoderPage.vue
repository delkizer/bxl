<template>
  <!-- 전체를 감싸는 래퍼 (필요시) -->
  <div>
    <!-- 1) scoreboard 영역 -->
    <div class="scoreboard">
      <div class="warmup-header">
        <!-- 상단: WARM UP / 시간 -->
        <div class="warmup-row">
          <span class="warmup-title">WARM UP</span>
          <span class="warmup-time">{{ formattedWarmUpTime }}</span>
        </div>
        <!-- 팀명 / 점수 -->
        <div class="teams-row">
          <span class="team-name">{{ teamA.name }}</span>
          <span class="score">{{ teamA.score }} - {{ teamB.score }}</span>
          <span class="team-name">{{ teamB.name }}</span>
        </div>
      </div>
    </div>

    <!-- 2) 별도의 라벨 영역 -->
    <div class="label-section">
      <div class="label-row">
        <div class="clock-box">
          <p class="clock-title">Warm Up Clock</p>
          <p>{{ formattedWarmUpTime }}</p>
        </div>
        <div class="clock-box">
          <p>Match Clock</p>
          <p>{{ formattedMatchTime }}</p>
        </div>
        <div class="clock-box">
          <p>Break Clock</p>
          <p>{{ formattedBreakTime }}</p>
        </div>
      </div>
      <!-- 중앙에 Reset Score 박스/버튼 -->
      <div class="reset-row">
        <div class="reset-box" @click="resetScore">Reset Score</div>
      </div>
      <!-- Warm Up Clock Setting 영역 -->
      <div class="warmup-clock-setting-row">
        <div class="warmup-clock-setting-col">
          <div class="warmup-clock-adjust-box">+1</div>
          <div class="warmup-clock-adjust-box">+5</div>
          <div class="warmup-clock-adjust-box">+10</div>
        </div>
        <!-- 중앙 영역을 감싸는 컨테이너 추가 -->
        <div class="warmup-clock-setting-center">
          <div class="warmup-clock-setting-box">
            Warm Up Clock Setting
          </div>
          <!-- START, RESET 버튼을 중앙 영역 아래에 배치 -->
          <div class="warmup-control-row">
            <div class="warmup-control-box" @click="startWarmUp">START</div>
            <div class="warmup-control-box" @click="resetWarmUpClock">RESET</div>
          </div>
        </div>
        <div class="warmup-clock-setting-col">
          <div class="warmup-clock-adjust-box">+1</div>
          <div class="warmup-clock-adjust-box">+5</div>
          <div class="warmup-clock-adjust-box">+10</div>
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
export default {
  name: "ScoreboardAndLabels",
  data() {
    return {
      // 예시: 2분, 10분, 1분
      warmUpTime: 120,
      matchTime: 600,
      breakTime: 60,
      teamA: {
        name: "Hurricanes",
        score: 0,
      },
      teamB: {
        name: "Rockets",
        score: 0,
      },
    };
  },
  computed: {
    formattedWarmUpTime() {
      return this.formatTime(this.warmUpTime);
    },
    formattedMatchTime() {
      return this.formatTime(this.matchTime);
    },
    formattedBreakTime() {
      return this.formatTime(this.breakTime);
    },
  },
  methods: {
    // 초 -> "mm:ss" 변환
    formatTime(sec) {
      const m = String(Math.floor(sec / 60)).padStart(2, "0");
      const s = String(sec % 60).padStart(2, "0");
      return `${m}:${s}`;
    },
    // 시작 및 리셋 관련 메서드 (예시)
    startWarmUp() {
      // 워밍업 시작 로직
    },
    resetWarmUpClock() {
      // 워밍업 리셋 로직
    },
    resetScore() {
      this.teamA.score = 0;
      this.teamB.score = 0;
    },
  },
};
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
</style>
