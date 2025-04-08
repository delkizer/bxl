import { defineStore } from "pinia";
import coderApi from "@/api/coderApi.js";

const DEFAULT_TIMES = {
  warmUp: 10,
  match: 15,
  break: 9,
}

function formatTime(sec) {
  const m = String(Math.floor(sec / 60)).padStart(2, "0");
  const s = String(sec % 60).padStart(2, "0");
  return `${m}:${s}`;
}


export const useCoderStore = defineStore('coderStore', {
  // state: 저장할 상태(데이터)
  state: () => ({
    tournament_uuid: null,
    tieNo: null,
    gameDate: null,

    // 추가: 팀별 상태
    teamA: {
      name: 'Hurricanes',
      score: 0,
      game: 0,
      point: 0,
    },
    teamB: {
      name: 'Rockets',
      score: 0,
      game: 0,
      point: 0,
    },

    // 추가: Warm Up, Match, Break
    warmUpTime: DEFAULT_TIMES.warmUp,
    warmUpTimer: null,
    isWarmUpRunning: false,
    matchTime: DEFAULT_TIMES.match,
    breakTime: DEFAULT_TIMES.break,

    // "MATCH", "BREAK", "WARMUP" 3가지 가능
    currentTimeTarget: "WARMUP",

    matchNo: 0,
    matchPoint: 0,

    ws: null,

  }),
  persist: {
    enabled: true,
    strategies: [
      {
        key:'coder-st',
        storage : localStorage
      }
    ]
  },
  // actions: state를 변경하거나 서버 통신 로직 등
  actions: {
    async fetchCoderInfo() {
      try {
        // 1. state에 있는 tournament_uuid, tieNo를 params로
        const params = {
          tournament_uuid: this.tournament_uuid,
          tie_no: this.tieNo,
        }

        // 2. API 요청
        const res = await coderApi.getCoderInfo(params)
        // 응답 형식: [{ game_no, team1_name, team1_score, ...}]

        const data = res.data
        if (Array.isArray(data) && data.length > 0) {
          const item = data[0]

          // 3. store state 갱신
          // team1 -> teamA, team2 -> teamB, etc
          this.teamA.name  = item.team1_name
          this.teamA.score = item.team1_score
          // 필요시 item.team1_game / item.team1_point 등도 서버에서 내려주면 반영

          this.teamB.name  = item.team2_name
          this.teamB.score = item.team2_score

          // matchNo, matchPoint, gameNo, etc
          this.matchNo    = item.match_no
          this.matchPoint = item.match_point

          // game_no -> this.teamA.game or something
          // match_status, game_status, etc
        } else {
          console.log('No coder data found.')
        }

      } catch (err) {
        console.error('fetchCoderInfo error:', err)
      }
    },

    // -------------------------------
    // WebSocket 관련 action
    // -------------------------------
    initWebSocket() {
      // 혹시 기존 소켓이 열려 있으면 정리
      if (this.ws) {
        this.closeWebSocket();
        this.ws = null;
      }

      const url = `ws://localhost:8080/ws/${this.tournament_uuid}/${this.tieNo}`;
      console.log(url)
      this.ws = new WebSocket(url);

      // 연결 성공
      this.ws.onopen = () => {
        console.log("WebSocket connected");
        // 필요시 서버에 초기 데이터 전송
        // this.ws.send(JSON.stringify({ action: "HELLO_SERVER" }));
      };

      // 서버로부터 메시지 수신
      this.ws.onmessage = (event) => {
        try {
          const msgData = JSON.parse(event.data);
          console.log("WS msgData received:", msgData);

          if (msgData.action === "broadcast" && msgData.resource === "score") {
            const payload = msgData.payload;
            if (payload.teamA) {
              this.teamA.score = payload.teamA.score;
              this.teamA.game  = payload.teamA.game;
              this.teamA.point = payload.teamA.point;
            }
            if (payload.teamB) {
              this.teamB.score = payload.teamB.score;
              this.teamB.game  = payload.teamB.game;
              this.teamB.point = payload.teamB.point;
            }
          }

          // 그 외 필요한 상태 업데이트

        } catch (error) {
          console.error("WS message parse error:", error);
        }
      };

      this.ws.onerror = (error) => {
        console.error("WebSocket error:", error);
      };

      // 연결 종료(서버에서 끊거나, 네트워크 문제 등)
      this.ws.onclose = () => {
        console.log("WebSocket closed");
        this.ws = null;
      };

    },

    // 필요시 수동으로 소켓 닫는 액션
    closeWebSocket() {
      if (this.ws && typeof this.ws.close === "function") {
        this.ws.close();
        this.ws = null;
      }
    },

    startWarmUp() {
      // 이미 타이머가 동작 중이라면 중복 시작 안 함
      if (this.isWarmUpRunning) return;

      this.isWarmUpRunning = true

      // 1초 간격으로 warmUpTime--
      this.warmUpTimer = setInterval(() => {
        // 시간이 아직 남아 있으면 1초씩 감소
        if (this.warmUpTime > 0) {
          this.warmUpTime--
        } else {
          // 0초가 되면 멈춤
          clearInterval(this.warmUpTimer)
          this.warmUpTimer = null
          this.isWarmUpRunning = false
        }
      }, 1000)
    },

    // 멈추거나 타이머 중단(예: 0초이거나, 다른 이유로 정지)
    stopWarmUp() {
      if (this.warmUpTimer) {
        clearInterval(this.warmUpTimer)
        this.warmUpTimer = null
      }
      this.isWarmUpRunning = false
    },

    cycleTimeTarget() {
      if (this.currentTimeTarget === "MATCH") {
        this.currentTimeTarget = "BREAK";
      } else if (this.currentTimeTarget === "BREAK") {
        this.currentTimeTarget = "WARMUP";
      } else {
        // WARMUP이면 다시 MATCH
        this.currentTimeTarget = "MATCH";
      }
    },

    adjustSelectedTime(sec) {
      if (this.currentTimeTarget === "MATCH") {
        this.matchTime += sec;
        if (this.matchTime < 0) this.matchTime = 0;
      } else if (this.currentTimeTarget === "BREAK") {
        this.breakTime += sec;
        if (this.breakTime < 0) this.breakTime = 0;
      } else {
        // WARMUP
        this.warmUpTime += sec;
        if (this.warmUpTime < 0) this.warmUpTime = 0;
      }
    },

    // 타이머 초기화
    resetWarmUpClock() {
      this.warmUpTime = DEFAULT_TIMES.warmUp
      // 혹시 타이머가 돌아가는 중이라면 멈춤
      if (this.warmUpTimer) {
        clearInterval(this.warmUpTimer)
        this.warmUpTimer = null
      }
      this.isWarmUpRunning = false
    },

    resetSelectedTime() {
      if (this.currentTimeTarget === 'MATCH') {
        this.matchTime = DEFAULT_TIMES.match;   // match 기본값
      } else if (this.currentTimeTarget === 'BREAK') {
        this.breakTime = DEFAULT_TIMES.break;    // break 기본값
      } else {
        // 'WARMUP'
        this.warmUpTime = DEFAULT_TIMES.warmUp;  // warm up 기본값
      }
    },

    setTieData(tournament_uuid, tieNo, gameDate) {
      this.tournament_uuid = tournament_uuid;
      this.tieNo = tieNo
      this.gameDate = gameDate
    },
    clearTieData() {
      this.tournament_uuid = null;
      this.tieNo = null
      this.gameDate = null
    },

    // 추가: Score/Point/Game 증감 로직
    incrementScore(team) {
      if (team === 'A') this.teamA.score++;
      else this.teamB.score++;
    },
    decrementScore(team) {
      if (team === 'A') {
        this.teamA.score = Math.max(this.teamA.score - 1, 0);
      } else {
        this.teamB.score = Math.max(this.teamB.score - 1, 0);
      }
    },
    incrementGame(team) {
      if (team === 'A') this.teamA.game++;
      else this.teamB.game++;
    },
    decrementGame(team) {
      if (team === 'A') {
        this.teamA.game = Math.max(this.teamA.game - 1, 0);
      } else {
        this.teamB.game = Math.max(this.teamB.game - 1, 0);
      }
    },
    incrementPoint(team) {
      if (team === 'A') this.teamA.point++;
      else this.teamB.point++;
    },
    decrementPoint(team) {
      if (team === 'A') {
        this.teamA.point = Math.max(this.teamA.point - 1, 0);
      } else {
        this.teamB.point = Math.max(this.teamB.point - 1, 0);
      }
    },

    // 추가: Reset Score
    resetScore() {
      this.teamA.score = 0;
      this.teamA.game = 0;
      this.teamA.point = 0;
      this.teamB.score = 0;
      this.teamB.game = 0;
      this.teamB.point = 0;
    },

  },

   getters: {
    tieLabel: (state) => {
      if (!state.tieNo || !state.gameDate) return ''
      return `${state.tieNo}번 TIE (${state.gameDate})`
    },
    formattedWarmUpTime: (state) => formatTime(state.warmUpTime),
    formattedMatchTime:  (state) => formatTime(state.matchTime),
    formattedBreakTime:  (state) => formatTime(state.breakTime),
    currentTargetLabel: (state) => {
      if (state.currentTimeTarget === "MATCH") return "Match Clock Setting";
      if (state.currentTimeTarget === "BREAK") return "Break Clock Setting";
      if (state.currentTimeTarget === "WARMUP") return "Warm Up Clock Setting";
    },
  }
})

