<template>
  <div class="game-info-page">
    <div class="form-container">

      <!-- 대회, 날짜, tie_no, 팀1, 팀2 선택 등 상단 UI는 그대로 유지 -->
      <div class="form-row">
        <div class="form-group left">
          <label>대회정보</label>
        </div>
        <div class="form-group middle">
          <select class="form-control" v-model="gameData.tournament_uuid" @change="onTournamentChange">
            <option value="">-- 대회 선택 --</option>
            <option
              v-for="tour in tourList"
              :key="tour.tournament_uuid"
              :value="tour.tournament_uuid"
            >
              {{ tour.tournament_title }}
            </option>
          </select>
        </div>
        <div class="form-group middle">
          <input type="date" class="form-control" v-model="gameData.game_date" />
        </div>
        <div class="form-group middle">
          <select class="form-control" v-model="gameData.tie_no">
            <option v-for="n in 9" :key="n" :value="n">
              {{ n }} Tie
            </option>
          </select>
        </div>
      </div>

      <!-- 팀1, 팀2 선택 (두 팀만) -->
      <div class="form-row">
        <div class="form-group left">
          <label>Team1</label>
        </div>
        <div class="form-group middle">
          <select class="form-control" v-model="gameData.team1_code" @change="onTeam1Change">
            <option value="">-- 팀 선택 --</option>
            <option v-for="team in teamList" :key="team.team_code" :value="team.team_code" :disabled="team.team_code === gameData.team2_code" >
              {{ team.team_name }}
            </option>
          </select>
        </div>

        <div class="form-group left">
          <label>Team2</label>
        </div>
        <div class="form-group middle">
          <select class="form-control" v-model="gameData.team2_code" @change="onTeam2Change">
            <option value="">-- 팀 선택 --</option>
            <option v-for="team in teamList" :key="team.team_code" :value="team.team_code" :disabled="team.team_code === gameData.team1_code" >
              {{ team.team_name }}
            </option>
          </select>
        </div>
      </div>

      <!-- 매치 정보 (5경기) -->
      <div class="matches-container">

        <!-- match_info를 반복 렌더링 -->
        <div
          v-for="(matchItem, idx) in gameData.match_info"
          :key="matchItem.match_no"
          class="match-row"
        >
          <!-- 상단 영역: Match No, 매치타입, 점수 -->
          <div class="match-header">
            <p class="match-title">Match No: {{ matchItem.match_no }}</p>

            <!-- 매치 타입 선택 -->
            <select
              class="form-control type-select"
              v-model="matchItem.match_type"
              @change="onMatchTypeChange(idx)"
            >
              <option value="">-- 매치타입 --</option>
              <option
                v-for="mtype in matchTypeList"
                :key="mtype.code"
                :value="mtype.code"
                :disabled="isUsedElsewhere(mtype.code, idx)"
              >
                {{ mtype.match_type }}
              </option>
            </select>

            <!-- 점수 (자동 연동) -->
            <select class="form-control point-select" v-model="matchItem.match_point">
              <option value="1">1점</option>
              <option value="2">2점</option>
              <option value="3">3점</option>
            </select>
          </div>

          <!-- TEAM1 선수 영역 -->
          <div class="team-block">
            <p class="team-label">Team1 Players</p>
            <!-- matchItem.team1_player.player_info -->
            <div class="player-row-line">
              <div
                v-for="(pId, pIndex) in matchItem.team1_player"
                :key="pIndex"
                class="player-select-wrap"
              >
                <select
                  class="form-control player-select"
                  v-model="matchItem.team1_player[pIndex]"
                >
                  <option value="">-- 선수 --</option>
                  <option
                    v-for="p in playerListTeam1"
                    :key="p.player_uuid"
                    :value="p.player_uuid"
                  >
                    {{ p.nick_name }}
                  </option>
                </select>
              </div>
            </div>
          </div>

          <!-- TEAM2 선수 영역 -->
          <div class="team-block">
            <p class="team-label">Team2 Players</p>
            <!-- matchItem.team2_player.player_info -->
            <div class="player-row-line">
              <div
                v-for="(pId, pIndex) in matchItem.team2_player"
                :key="pIndex"
                class="player-select-wrap"
              >
                <select
                  class="form-control player-select"
                  v-model="matchItem.team2_player[pIndex]"
                >
                  <option value="">-- 선수 --</option>
                  <option
                    v-for="p in playerListTeam2"
                    :key="p.player_uuid"
                    :value="p.player_uuid"
                  >
                    {{ p.nick_name }}
                  </option>
                </select>
              </div>
            </div>
          </div>
        </div><!-- /match-row -->
      </div><!-- /matches-container -->

      <!-- 버튼 -->
      <div class="button-container">
        <button class="btn btn-save" @click="handleSave">저장</button>
        <button class="btn btn-cancel" @click="handleCancel">종료</button>
      </div>

      <!-- 저장 모달 -->
      <ConfirmationModal
        :visible="showSaveModal"
        title="저장 확인"
        message="저장을 진행하시겠습니까?"
        confirmButtonLabel="확인"
        cancelButtonLabel="취소"
        @confirm="handleSaveConfirm"
        @cancel="handleSaveCancel"
      />

      <!-- 종료 모달 -->
      <ConfirmationModal
        :visible="showExitModal"
        title="종료 확인"
        message="Home으로 이동하시겠습니까?"
        confirmButtonLabel="확인"
        cancelButtonLabel="취소"
        @confirm="handleExitConfirm"
        @cancel="handleExitCancel"
      />

    </div><!-- /form-container -->
  </div><!-- /game-info-page -->
</template>


<script>
import tourApi from "@/api/tourApi.js";
import teamApi from "@/api/teamApi.js";
import coderApi from "@/api/coderApi.js";
import ConfirmationModal from "@/components/ConfirmationModal.vue";

export default {
  name: "GameInfoPage",
  components: {ConfirmationModal},
  data() {
    return {
      gameData: {
        tournament_uuid: "",
        tie_no: 1,
        game_date: "",
        team1_code: null,
        team2_code: null,
        match_info: [
          {
            match_no: 1,
            match_type: "",
            match_point: 1,
            team1_player: [],
            team2_player: []
          },
          {
            match_no: 2,
            match_type: "",
            match_point: 1,
            team1_player: [],
            team2_player: []
          },
          {
            match_no: 3,
            match_type: "",
            match_point: 1,
            team1_player: [],
            team2_player: []
          },
          {
            match_no: 4,
            match_type: "",
            match_point: 1,
            team1_player: [],
            team2_player: []
          },
          {
            match_no: 5,
            match_type: "",
            match_point: 1,
            team1_player: [],
            team2_player: []
          }
        ]
      },
      tourList: [],       // 대회 목록
      teamList: [],       // 팀 목록
      matchTypeList: [],  // 매치타입 목록

      playerListTeam1: [], // 팀1 선수 목록
      playerListTeam2: [],  // 팀2 선수 목록

      match_info: [
        { match_no: 1, match_type: "" },
        { match_no: 2, match_type: "" },
        { match_no: 3, match_type: "" },
        { match_no: 4, match_type: "" },
        { match_no: 5, match_type: "" }
      ],

      // 모달 표시 여부
      showSaveModal: false,
      showExitModal: false
    };
  },
  mounted() {
    this.fetchInitialData();
  },
  methods: {
    // 대회 목록, 매치타입 목록 등 초기 데이터 가져오기
    async fetchInitialData() {
      try {
        // 1) 대회 목록
        const tourRes = await tourApi.getTourList();
        this.tourList = tourRes.data;

        // 2) 매치타입 목록
        const matchRes = await coderApi.getMatchTypeList();
        this.matchTypeList = matchRes.data;
        // [ {code: "MSIG", match_type:"남자 단식"}, ... ]

        // 3) 팀 목록 (선택된 대회가 있다면 그에 맞춰 가져오도록 할 수도 있음)
        //    or, 대회 선택 시점에 가져올 수도 있음.
        //    여기서는 단순히 전체 팀 목록이라 가정
        const teamRes = await teamApi.getTeamList(/* params if needed */);
        this.teamList = teamRes.data;
      } catch (error) {
        console.error(error);
      }
    },

    // 대회 선택 시점에, 대회별 팀 목록만 가져오고 싶다면 이런 식:
    onTournamentChange() {
      if (!this.gameData.tournament_uuid) {
        this.teamList = [];
        return;
      }
      teamApi.getTeamList({ tournament_uuid: this.gameData.tournament_uuid })
        .then(res => {
          this.teamList = res.data;
        })
        .catch(err => console.error(err));
    },

    // 팀1 선택 시 -> team1_code에 맞는 선수 목록 호출
    onTeam1Change() {
      const tCode = this.gameData.team1_code;
      if (!tCode) {
        this.playerListTeam1 = [];
        return;
      }
      teamApi.getPlayerList(tCode)
        .then(res => {
          this.playerListTeam1 = res.data;
          console.log("Team1 Players:", this.playerListTeam1);
        })
        .catch(err => console.error(err));
    },

    // 팀2 선택 시 -> team2_code에 맞는 선수 목록 호출
    onTeam2Change() {
      const tCode = this.gameData.team2_code;
      if (!tCode) {
        this.playerListTeam2 = [];
        return;
      }
      teamApi.getPlayerList(tCode)
        .then(res => {
          this.playerListTeam2 = res.data;
          console.log("Team2 Players:", this.playerListTeam2);
        })
        .catch(err => console.error(err));
    },

    // 매치타입 바뀔 때 -> 점수, 그리고 player_info 배열 길이 조절
    onMatchTypeChange(idx) {
      const matchItem = this.gameData.match_info[idx];
      const currentType = matchItem.match_type;

      // 필요 슬롯 개수 결정 (단식1, 복식2, 3대3=3 등)
      let neededPlayers = 1;
      if (currentType === "MSIG" || currentType === "WSIG") {
        neededPlayers = 1;
      } else if (currentType === "MDBL" || currentType === "WDBL") {
        neededPlayers = 2;
      } else if (currentType === "03X3") {
        neededPlayers = 3;
      }

      // match_point에 반영 (원하시면 필요Players랑 동일하게 하거나, 별도 로직)
      matchItem.match_point = neededPlayers;

      // 기존 선수 배열
      let oldT1 = matchItem.team1_player; // ex) ["선수A", "", ...]
      let oldT2 = matchItem.team2_player;

      // (A) team1 길이 조절
      if (oldT1.length < neededPlayers) {
        // ex) 1명 -> 2명으로 늘리는 경우
        // 남은 칸만큼 "" 추가
        const extra = neededPlayers - oldT1.length;
        oldT1 = [...oldT1, ...Array(extra).fill("")];
      } else if (oldT1.length > neededPlayers) {
        // ex) 3명 -> 2명으로 줄이는 경우
        // 앞부분 neededPlayers개만 살림
        oldT1 = oldT1.slice(0, neededPlayers);
      }

      // (B) team2 길이 조절
      if (oldT2.length < neededPlayers) {
        const extra = neededPlayers - oldT2.length;
        oldT2 = [...oldT2, ...Array(extra).fill("")];
      } else if (oldT2.length > neededPlayers) {
        oldT2 = oldT2.slice(0, neededPlayers);
      }

      // 수정된 배열을 다시 대입
      matchItem.team1_player = oldT1;
      matchItem.team2_player = oldT2;

      // 디버깅용
      console.log(`[onMatchTypeChange] idx=${idx}, neededPlayers=${neededPlayers}`);
      console.log("Team1 old -> new:", oldT1);
      console.log("Team2 old -> new:", oldT2);
    },
    isUsedElsewhere(matchCode, currentIndex) {
        // 만약 아직 아무것도 선택 안했다면 or matchCode가 빈문자열이면 불필요
        if (!matchCode) return false;

        // match_info 배열을 순회,
        // currentIndex 제외한 나머지 행에 match_type === matchCode가 있으면 true
        return this.gameData.match_info.some((item, idx) => {
          // 자기 자신은 제외
          if (idx === currentIndex) return false;
          // 타입이 동일하면 다른 매치에서 이미 사용 중
          return item.match_type === matchCode;
        });
    },
    handleSave() {
      // 최종 전송 데이터: this.gameData
      console.log(">>> 최종 데이터:", this.gameData);
      this.showSaveModal = true;
    },
    handleSaveConfirm() {
      // 실제 API POST 요청
      this.postTiePage(this.gameData)
        .then((res) => {
          console.log(">>> 저장 완료:", res.data);
          // 저장 후 모달 닫기
          this.showSaveModal = false;
          this.$router.push("/coderlist");
        })
        .catch((err) => {
          console.error(err);
          alert("저장 실패!");
        });
    },
    handleSaveCancel() {
      this.showSaveModal = false;
    },
    handleCancel() {
      this.showSaveModal = false;
    },
    // 종료 모달에서 확인 -> Home으로 이동
    handleExitConfirm() {
      this.showExitModal = false;
      // 라우터 경로에 맞게 수정
      this.$router.push("/");
    },
    // 종료 모달에서 취소
    handleExitCancel() {
      this.showExitModal = false;
    },
    async postTiePage(params = {}) {
      try{
        const response = await  coderApi.postTiePage(params);
        console.log(response);
        return response;
      } catch (error) {
        console.error(">>> postTiePage API 오류:", error);
        throw error;
      }

    },
  }
};
</script>

<style scoped>
/* ------------------------------
   전체 배경 및 레이아웃
------------------------------ */
.game-info-page {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);

  background-color: #4b7cb6;
  width: 1024px;         /* 고정 폭 예시 */
  max-width: 95%;        /* 화면이 좁으면 95%까지만 줄임 */
  max-height: 90vh;      /* 화면 높이의 90%로 제한 */
  overflow-y: auto;      /* 세로 스크롤 표시 */

  /* 내부 여백 */
  padding: 20px;
  box-sizing: border-box;

}

.form-container {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

/* ------------------------------
   각 행(라벨+필드) 레이아웃
------------------------------ */
.form-row {
  display: flex;
  align-items: flex-start;
  gap: 10px;
}

/* 왼쪽 라벨 영역 */
.form-group.left {
  width: 100px;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

/* ------------------------------
   입력 요소에 대한 스타일
------------------------------ */
.form-group {
  display: flex;
  flex-direction: column;
  background-color: white;
  padding: 10px;
  border-radius: 5px;
  box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
}

.form-group label {
  font-weight: bold;
  font-size: 16px;
  text-align: center;
  margin-bottom: 5px;
}

.form-control {
  padding: 8px 12px;
  border: 1px solid #ddd;
  border-radius: 4px;
  font-size: 16px;
}

/* 셀렉트 기본 화살표 커스텀 */
select.form-control {
  appearance: none;
  background-image: url("data:image/svg+xml;charset=UTF-8,%3csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24' fill='none' stroke='%23333' stroke-width='2' stroke-linecap='round' stroke-linejoin='round'%3e%3cpolyline points='6 9 12 15 18 9'%3e%3c/polyline%3e%3c/svg%3e");
  background-repeat: no-repeat;
  background-position: right 8px center;
  background-size: 16px;
  padding-right: 30px;
}

/* ------------------------------
   매치 선택(25개) 래퍼
------------------------------ */
.match-wrapper {
  display: flex;
  flex-direction: column; /* 세로로 행 나열 */
  gap: 10px;
}

/* 각 행 안에 있는 5개 셀렉트들 */
.match-row {
  display: flex;
  flex-direction: column;
  background-color: #fff;
  padding: 15px;
  border-radius: 5px;
  box-shadow: 0 2px 5px rgba(0,0,0,0.1);
  gap: 10px; /* 내부 요소 간격 */
}

.match-header {
  display: flex;
  flex-direction: row;
  align-items: center;
  gap: 20px;
}

.match-title {
  font-weight: bold;
  margin: 0;
  min-width: 120px;
  /* 필요에 따라 스타일링 */
}

.team-block {
  display: flex;
  flex-direction: column; /* 위->아래로 쌓이게 */
  gap: 10px;
  border: 1px solid #eee;
  border-radius: 5px;
  padding: 10px;
  background-color: #fafafa; /* 살짝 배경색 */
}

.team-label {
  font-weight: bold;
  margin: 0 0 5px 0;
}

.player-row-line {
  display: flex;            /* 가로 배치 */
  flex-direction: row;
  flex-wrap: nowrap;        /* 한 줄로 강제 배치 (넘치면 스크롤) */
  gap: 10px;                /* Select들 사이의 간격 */
}

/* 플레이어 select 래퍼 (한 줄) */
.player-select-wrap {
  display: flex;
  flex-direction: row;
  gap: 10px;
}

/* ------------------------------
   버튼 영역
------------------------------ */
.button-container {
  display: flex;
  justify-content: flex-end;
  gap: 20px;
  margin-top: 40px;
}

.btn {
  padding: 15px 30px;
  font-size: 18px;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  background-color: white;
  color: #333;
  font-weight: bold;
  box-shadow: 0 2px 5px rgba(0, 0, 0, 0.2);
}

.btn-save {
  background-color: #70c16b;
  color: #fff;
}

.btn-cancel {
  background-color: #f56b6b;
  color: #fff;
}

.player-select {
  width: 100px;        /* 원하는 픽셀 값(ex.120px) */
  flex-shrink: 0;      /* flex 환경에서 줄어들지 않도록 */
}

.matches-container {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

/* ------------------------------
   반응형 처리
------------------------------ */
@media (max-width: 960px) {
  .form-row {
    flex-direction: column;
  }
  .left {
    width: 100%;
    justify-content: flex-start;
  }
}
</style>
