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
    matchTime: DEFAULT_TIMES.match,
    breakTime: DEFAULT_TIMES.break,

    // "MATCH", "BREAK", "WARMUP" 3가지 가능
    currentTimeTarget: "WARMUP",

    gameInfo: {
      matchNo:0,
      gameNo: 0,
      gameType: "",
      suddenDeath: false,
      shuttleShowdown: false,
    },

    ws: null,

    isNonStop: false,

    isRunning: false,
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

        } else {
          console.log('No coder data found.')
        }

      } catch (err) {
        console.error('fetchCoderInfo error:', err)
      }
    },

    setGameNo(newGameNo) {
      // 1) 먼저 store 상태 갱신 (옵션)
      this.gameInfo.gameNo = newGameNo;

      // 2) WebSocket으로 메시지 전송
      if (this.ws && this.ws.readyState === WebSocket.OPEN) {
        const msg = {
          action: "update",
          resource: "game",
          payload: {
            game_no: newGameNo,
          },
        };
        this.ws.send(JSON.stringify(msg));
        console.log("Sent WS:", msg);
      } else {
        console.warn("WebSocket not open. Cannot update game_no.");
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

      const url = `${import.meta.env.VITE_WEBSOCKET_URL}/ws/${this.tournament_uuid}/${this.tieNo}`;
      console.log(url)
      this.ws = new WebSocket(url);

      // 연결 성공
      this.ws.onopen = () => {
        console.log("WebSocket connected");
      };

      // 서버로부터 메시지 수신
      this.ws.onmessage = (event) => {
        try {
          const msgData = JSON.parse(event.data);
          console.log("WS msgData received:", msgData);

          if (msgData.action === "broadcast" ) {
            const payload = msgData.payload;
            if (payload.scoreBoard.teamA) {
              this.teamA.score = payload.scoreBoard.teamA.score;
              this.teamA.game  = payload.scoreBoard.teamA.game;
              this.teamA.point = payload.scoreBoard.teamA.point;
            }
            if (payload.scoreBoard.teamB) {
              this.teamB.score = payload.scoreBoard.teamB.score;
              this.teamB.game  = payload.scoreBoard.teamB.game;
              this.teamB.point = payload.scoreBoard.teamB.point;
            }
            if (payload.timeInfo) {
              this.warmUpTime = payload.timeInfo.warmupTime;
              this.matchTime  = payload.timeInfo.matchTime;
              this.breakTime  = payload.timeInfo.breakTime;
            }
            if (payload.gameInfo) {
              this.gameInfo.matchNo = payload.gameInfo.matchNo;
              this.gameInfo.gameNo = payload.gameInfo.gameNo;
              this.gameInfo.gameType = payload.gameInfo.gameType;
              this.gameInfo.suddenDeath = payload.gameInfo.suddenDeath;
              this.gameInfo.shuttleShowdown = payload.gameInfo.shuttleShowdown;
            }
            if (typeof payload.nonStop === "boolean") {
              this.isNonStop = payload.nonStop;
            }
            if (payload.currentState) {
              this.currentState = payload.currentState;
            }
            if (typeof payload.isRunning === "boolean") {
              this.isRunning = payload.isRunning;
            }
          }


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

    // -----------------------------
    // 시간(Start/Pause/Adjust) 관련
    // -----------------------------
    startTimer() {
      // 기존 local setInterval, isWarmUpRunning 등은 제거
      // 대신 서버에 "start" 요청만 보냄
      if (!this.ws || this.ws.readyState !== WebSocket.OPEN) {
        console.error("WebSocket not open. Can't start timer.");
        return;
      }
      // currentTimeTarget: "WARMUP" | "MATCH" | "BREAK"
      const key = this.currentTimeTarget.toLowerCase(); // "warmup" | "match" | "break"
      const msg = {
        action: "update",
        resource: "time",
        payload: {
          [key]: "start", // ex) { warmup: "start" }
        },
      };
      this.ws.send(JSON.stringify(msg));
    },

    pauseTimer() {
      if (!this.ws || this.ws.readyState !== WebSocket.OPEN) {
        console.error("WebSocket not open. Can't pause timer.");
        return;
      }
      const key = this.currentTimeTarget.toLowerCase();
      const msg = {
        action: "update",
        resource: "time",
        payload: {
          [key]: "pause", // ex) { match: "pause" }
        },
      };
      this.ws.send(JSON.stringify(msg));
    },

    // 공통 메서드: WebSocket으로 점수 업데이트 요청을 보냄
    sendScoreUpdate(team, field, change) {
      if (!this.ws) {
        console.error("WebSocket not connected");
        return;
      }
      // 예: 연결 상태가 OPEN이 아닐 수도 있으므로 체크
      if (this.ws.readyState !== WebSocket.OPEN) {
        console.error("WebSocket not OPEN. Current state:", this.ws.readyState);
        return;
      }

      const msg = {
        action: "update",
        resource: "score",
        payload: {
          team,     // "A" or "B"
          field,    // "score" | "game" | "point"
          change,   // "increase" | "decrease"
        },
      };

      // 실제 전송
      this.ws.send(JSON.stringify(msg));
    },

    // 필요시 수동으로 소켓 닫는 액션
    closeWebSocket() {
      if (this.ws && typeof this.ws.close === "function") {
        this.ws.close();
        this.ws = null;
      }
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

      if (this.ws && this.ws.readyState === WebSocket.OPEN) {
        // sec > 0일 때는 "increase", sec < 0일 때는 "decrease"로 구분
        const direction = sec > 0 ? "increase" : "decrease";
        // +5나 -5처럼 절대값만 보내기 위해 Math.abs() 사용
        const absSec = Math.abs(sec);

        // currentTimeTarget은 "WARMUP" | "MATCH" | "BREAK" 중 하나
        // 요구사항에서 payload에 "warmup": "increase" 형태로 보내려면
        // 키를 소문자로 변환하여 동적으로 매핑
        const key = this.currentTimeTarget.toLowerCase();
        // 예: key = 'warmup' | 'match' | 'break'

        const msg = {
          action: "update",
          resource: "time",
          payload: {
            [key]: direction,
            sec: absSec
          },
        };

        this.ws.send(JSON.stringify(msg));
      }
    },

    // 타이머 초기화
    resetClock() {
      const msg = {
        action: "update",
        resource: "time",
        payload: {
          "reset" : true
        },
      };

      // 실제 전송
      this.ws.send(JSON.stringify(msg));
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
      this.sendScoreUpdate(team, 'score', 'increase');
    },
    decrementScore(team) {
      if (team === 'A') {
        this.teamA.score = Math.max(this.teamA.score - 1, 0);
      } else {
        this.teamB.score = Math.max(this.teamB.score - 1, 0);
      }
      this.sendScoreUpdate(team, 'score', 'decrease');
    },
    incrementGame(team) {
      if (team === 'A') this.teamA.game++;
      else this.teamB.game++;
      this.sendScoreUpdate(team, 'game', 'increase');
    },
    decrementGame(team) {
      if (team === 'A') {
        this.teamA.game = Math.max(this.teamA.game - 1, 0);
      } else {
        this.teamB.game = Math.max(this.teamB.game - 1, 0);
      }
      this.sendScoreUpdate(team, 'game', 'decrease');
    },
    incrementPoint(team) {
      if (team === 'A') this.teamA.point++;
      else this.teamB.point++;
      this.sendScoreUpdate(team, 'point', 'increase');
    },
    decrementPoint(team) {
      if (team === 'A') {
        this.teamA.point = Math.max(this.teamA.point - 1, 0);
      } else {
        this.teamB.point = Math.max(this.teamB.point - 1, 0);
      }
      this.sendScoreUpdate(team, 'point', 'decrease');
    },

    // 추가: Reset Score
    resetScore() {
      this.teamA.score = 0;
      this.teamB.score = 0;
      this.sendScoreUpdate('A', 'score', 'reset');
      this.sendScoreUpdate('B', 'score', 'reset');
    },

    setNonStop(value) {
      this.isNonStop = value;

      // WebSocket 연결 상태 확인
      if (this.ws && this.ws.readyState === WebSocket.OPEN) {
        const msg = {
          action: "update",
          resource: "time",
          payload: {
            nonStop: this.isNonStop,
          },
        };
        this.ws.send(JSON.stringify(msg));
      } else {
        console.warn("WebSocket not open. Cannot send nonStop update.");
      }
    },

    sendNextMatch() {
      if (!this.ws || this.ws.readyState !== WebSocket.OPEN) {
        console.warn("WebSocket not open. Can't send Next Match.");
        return;
      }
      const msg = {
        action: "update",
        resource: "game",
        payload: {
          nextMatch: true,
        },
      };
      this.ws.send(JSON.stringify(msg));
      console.log("WS -> Next Match:", msg);
    },

    sendResult() {
      if (!this.ws || this.ws.readyState !== WebSocket.OPEN) {
        console.warn("WebSocket not open. Can't send Result.");
        return;
      }
      const msg = {
        action: "update",
        resource: "game",
        payload: {
          result: true,
        },
      };
      this.ws.send(JSON.stringify(msg));
      console.log("WS -> Result:", msg);
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
      if (state.currentTimeTarget === "MATCH") return "Match";
      if (state.currentTimeTarget === "BREAK") return "Break";
      if (state.currentTimeTarget === "WARMUP") return "Warm Up";
    },
     currentTimeLabel: (state) => {
      if (state.currentTimeTarget === "MATCH") return formatTime(state.warmUpTime);
      if (state.currentTimeTarget === "BREAK") return formatTime(state.breakTime);
      if (state.currentTimeTarget === "WARMUP") return formatTime(state.matchTime);
     },
    currentGameLabel: (state) => {
      const { gameNo, gameType, suddenDeath } = state.gameInfo;
      if (!gameNo || !gameType) return "";
      const base = `Game ${gameNo} (${gameType})`;
      return suddenDeath ? `${base} [SD]` : base;
    },
  }
})

