<template>
  <div class="game-info-page">
    <div class="form-container">

      <!-- 대회, 날짜, tie_no, 팀1, 팀2 선택 등 상단 UI는 그대로 유지 -->
      <div class="form-row">
        <div class="form-group left"
            data-step="1"
            data-guide="대회를 선택하면 해당 대회의 팀·선수 목록이 로드됩니다."
        >
          <label>대회정보</label>
        </div>
        <div class="form-group middle">
          <select
            class="form-control"
            v-model="gameData.tournament_uuid"
            @change="onTournamentChange"
            :disabled="isEditMode"
          >
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
          <input
            type="date"
            class="form-control"
            v-model="gameData.game_date"
            :disabled="isEditMode"
            data-step="2"
            data-guide="경기일을 지정합니다."
          />
        </div>
        <div class="form-group middle">
          <select
            class="form-control"
            v-model="gameData.tie_no"
            :disabled="isEditMode"
            data-step="3"
            data-guide="Tie 번호(1~9) 를 지정합니다."
          >
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
          <select
            class="form-control"
            v-model="gameData.team1_code"
            @change="onTeam1Change"
            :disabled="isEditMode"
            data-step="4"
            :data-guide="[
                '팀1을 선택합니다.',
                '이미 선택된 팀2와 동일 팀은',
                '비활성화됩니다.'
              ].join('\n')"
          >
            <option value="">-- 팀 선택 --</option>
            <option
              v-for="team in teamList"
              :key="team.team_code"
              :value="team.team_code"
              :disabled="team.team_code === gameData.team2_code"
            >
              {{ team.team_name }}
            </option>
          </select>
        </div>

        <div class="form-group left">
          <label>Team2</label>
        </div>
        <div class="form-group middle">
          <select
            class="form-control"
            v-model="gameData.team2_code"
            @change="onTeam2Change"
            :disabled="isEditMode"
            data-step="5"
            :data-guide="[
              '팀2를 선택합니다.',
              'Team1과 중복되지 않도록 주의하세요.'
            ].join('\n')"
          >
            <option value="">-- 팀 선택 --</option>
            <option
              v-for="team in teamList"
              :key="team.team_code"
              :value="team.team_code"
              :disabled="team.team_code === gameData.team1_code"
            >
              {{ team.team_name }}
            </option>
          </select>
        </div>
      </div>

      <!-- 매치 정보 (5경기) -->
      <div class="matches-container"
           data-step="5"
           :data-guide="[ '각 Match 행에서 매치 타입을 고르면 자동으로 필요한 선수 수(점수)가 설정됩니다.'
           , '수정 시에는 출전하는 선수만 교체가 가능합니다.'].join('\n')"
      >
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
              :disabled="isEditMode"
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
            <select
              class="form-control point-select"
              v-model="matchItem.match_point"
              :disabled="isEditMode"
            >
              <option value="1">1점</option>
              <option value="2">2점</option>
              <option value="3">3점</option>
            </select>
          </div>

          <!-- TEAM1 선수 영역 -->
          <div class="team-block">
            <p class="team-label">Team1 Players</p>
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
        </div>
      </div>

      <!-- 버튼 -->
      <div class="button-container"
      >
        <button class="btn btn-save" @click="handleSave"
           data-step="99"
           :data-guide="[ '저장:현재 입력 내용을 저장합니다.', '종료:저장하지 않고 대시보드로 돌아갑니다.'].join('\n')"
        >저장</button>
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
    </div>
  </div>
</template>

<script>
import tourApi from "@/api/tourApi.js";
import teamApi from "@/api/teamApi.js";
import coderApi from "@/api/coderApi.js";
import Confirmation from "@/components/modal/Confirmation.vue";
import { useCoderStore } from "@/stores/coder.js";

export default {
  name: "GameInfoPage",
  components: { ConfirmationModal: Confirmation },
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
            team2_player: [],
          },
          {
            match_no: 2,
            match_type: "",
            match_point: 1,
            team1_player: [],
            team2_player: [],
          },
          {
            match_no: 3,
            match_type: "",
            match_point: 1,
            team1_player: [],
            team2_player: [],
          },
          {
            match_no: 4,
            match_type: "",
            match_point: 1,
            team1_player: [],
            team2_player: [],
          },
          {
            match_no: 5,
            match_type: "",
            match_point: 1,
            team1_player: [],
            team2_player: [],
          },
        ],
      },
      tourList: [],
      teamList: [],
      matchTypeList: [],

      playerListTeam1: [],
      playerListTeam2: [],

      match_info: [
        { match_no: 1, match_type: "" },
        { match_no: 2, match_type: "" },
        { match_no: 3, match_type: "" },
        { match_no: 4, match_type: "" },
        { match_no: 5, match_type: "" },
      ],

      // 모달 표시 여부
      showSaveModal: false,
      showExitModal: false,
    };
  },
  computed: {
    isEditMode() {
      const coderStore = useCoderStore();
      return !!coderStore.tieNo;
    },
  },
  mounted() {
    if (this.isEditMode) {
      const coderStore = useCoderStore();
      let tournament_uuid = coderStore.tournament_uuid;
      let tie_no = coderStore.tieNo;
      let game_date = coderStore.gameDate;
      coderStore.setTieData(tournament_uuid, tie_no, game_date);
    }
    this.fetchInitialData();
  },
  methods: {
    async fetchInitialData() {
      try {
        // 1) 대회 목록
        const tourRes = await tourApi.getTourList();
        this.tourList = tourRes.data;

        // 2) 매치타입 목록
        const matchRes = await coderApi.getMatchTypeList();
        this.matchTypeList = matchRes.data;

        // 3) 팀 목록
        const teamRes = await teamApi.getTeamList();
        this.teamList = teamRes.data;

        // 4) 수정 모드일 경우 Tie 데이터 호출
        if (this.isEditMode) {
          const coderStore = useCoderStore();
          const tieRes = await coderApi.getTiePage({
            tournament_uuid: coderStore.tournament_uuid,
            tie_no: coderStore.tieNo,
            game_date: coderStore.gameDate,
          });
          this.gameData = tieRes.data;

          if (this.gameData.team1_code) {
            await this.onTeam1Change();
          }
          if (this.gameData.team2_code) {
            await this.onTeam2Change();
          }

          this.gameData.match_info.forEach((matchItem, idx) => {
            if (matchItem.match_type) {
              this.onMatchTypeChange(idx);
            }
          });
        }
      } catch (error) {
        console.error(error);
      }
    },
    onTournamentChange() {
      if (!this.gameData.tournament_uuid) {
        this.teamList = [];
        return;
      }
      teamApi
        .getTeamList({ tournament_uuid: this.gameData.tournament_uuid })
        .then((res) => {
          this.teamList = res.data;
        })
        .catch((err) => console.error(err));
    },
    onTeam1Change() {
      const tCode = this.gameData.team1_code;
      if (!tCode) {
        this.playerListTeam1 = [];
        return;
      }
      teamApi
        .getPlayerList(tCode)
        .then((res) => {
          this.playerListTeam1 = res.data;
        })
        .catch((err) => console.error(err));
    },
    onTeam2Change() {
      const tCode = this.gameData.team2_code;
      if (!tCode) {
        this.playerListTeam2 = [];
        return;
      }
      teamApi
        .getPlayerList(tCode)
        .then((res) => {
          this.playerListTeam2 = res.data;
        })
        .catch((err) => console.error(err));
    },
    onMatchTypeChange(idx) {
      const matchItem = this.gameData.match_info[idx];
      const currentType = matchItem.match_type;

      let neededPlayers = 1;
      if (currentType === "MSIG" || currentType === "WSIG") {
        neededPlayers = 1;
      } else if (currentType === "MDBL" || currentType === "WDBL") {
        neededPlayers = 2;
      } else if (currentType === "03X3") {
        neededPlayers = 3;
      }

      matchItem.match_point = neededPlayers;

      let oldT1 = matchItem.team1_player;
      let oldT2 = matchItem.team2_player;

      // Team1 길이 조절
      if (oldT1.length < neededPlayers) {
        const extra = neededPlayers - oldT1.length;
        oldT1 = [...oldT1, ...Array(extra).fill("")];
      } else if (oldT1.length > neededPlayers) {
        oldT1 = oldT1.slice(0, neededPlayers);
      }

      // Team2 길이 조절
      if (oldT2.length < neededPlayers) {
        const extra = neededPlayers - oldT2.length;
        oldT2 = [...oldT2, ...Array(extra).fill("")];
      } else if (oldT2.length > neededPlayers) {
        oldT2 = oldT2.slice(0, neededPlayers);
      }

      matchItem.team1_player = oldT1;
      matchItem.team2_player = oldT2;
    },
    isUsedElsewhere(matchCode, currentIndex) {
      if (!matchCode) return false;
      return this.gameData.match_info.some((item, idx) => {
        if (idx === currentIndex) return false;
        return item.match_type === matchCode;
      });
    },
    handleSave() {
      console.log(">>> 최종 데이터:", this.gameData);
      this.showSaveModal = true;
    },
    handleSaveConfirm() {
      this.postTiePage(this.gameData)
        .then((res) => {
          console.log(">>> 저장 완료:", res.data);
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
      this.showExitModal = true;
    },
    handleExitConfirm() {
      this.showExitModal = false;
      this.$router.push("/");
    },
    handleExitCancel() {
      this.showExitModal = false;
    },
    async postTiePage(params = {}) {
      try {
        let response;
        if (this.isEditMode) {
          response = await coderApi.postTieModify(params);
        } else {
          response = await coderApi.postTiePage(params);
        }
        return response;
      } catch (error) {
        console.error(">>> postTiePage API 오류:", error);
        throw error;
      }
    },
  },
};
</script>

<style scoped>
/* -----------------------------------
   1) .game-info-page
   - 기본(화면폭 < 1024px): Flexbox 중앙 정렬
   - 1024px 이상: 절대 위치로 완전 중앙
------------------------------------ */
.game-info-page {
  width: 100%;
  min-height: 100vh;
  background-color: #4b7cb6;
  display: flex;
  justify-content: center;
  align-items: center;
  box-sizing: border-box;
  padding: 20px;
}

/* 1024px 이상이면 position: absolute 중앙 */
@media (min-width: 1024px) {
  .game-info-page {
    position: absolute;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);
  }
}

/* -----------------------------------
   2) .form-container: 실질적인 컨텐츠 영역
   - 폭 1024px, 화면이 좁을 때는 95%로 줄임
   - 세로 스크롤 가능 (max-height: 90vh)
------------------------------------ */
.form-container {
  width: 1024px;
  max-width: 95%;
  max-height: 90vh;
  overflow-y: auto;
  background-color: #fff;
  padding: 20px;
  box-sizing: border-box;
  border-radius: 8px;

  /* 약간의 그림자 */
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);

  display: flex;
  flex-direction: column;
  gap: 20px; /* 내부 요소 간격 */
}

/* 각 행(라벨+필드) */
.form-row {
  display: flex;
  align-items: flex-start;
  gap: 10px;
}

/* 왼쪽 라벨 영역 (고정 폭) */
.form-group.left {
  width: 100px;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

/* 공통 .form-group 스타일 */
.form-group {
  display: flex;
  flex-direction: column;
  background-color: #fff;
  padding: 10px;
  border-radius: 5px;
  box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
}

/* 라벨 */
.form-group label {
  font-weight: bold;
  font-size: 16px;
  text-align: center;
  margin-bottom: 5px;
}

/* 공통 form-control */
.form-control {
  padding: 8px 12px;
  border: 1px solid #ddd;
  border-radius: 4px;
  font-size: 16px;
}

/* 커스텀 select 화살표 */
select.form-control {
  appearance: none;
  background-image: url("data:image/svg+xml,%3csvg ...");
  background-repeat: no-repeat;
  background-position: right 8px center;
  background-size: 16px;
  padding-right: 30px;
}

/* ------------ match-row (각 매치) ------------ */
.match-row {
  display: flex;
  flex-direction: column;
  background-color: #fff;
  padding: 15px;
  border-radius: 5px;
  box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
  gap: 10px;
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
}

.team-block {
  display: flex;
  flex-direction: column;
  gap: 10px;
  border: 1px solid #eee;
  border-radius: 5px;
  padding: 10px;
  background-color: #fafafa;
}

.team-label {
  font-weight: bold;
  margin: 0 0 5px 0;
}

.player-row-line {
  display: flex;
  flex-direction: row;
  flex-wrap: nowrap;
  gap: 10px;
}

.player-select-wrap {
  display: flex;
  flex-direction: row;
  gap: 10px;
}

.player-select {
  width: 100px;
  flex-shrink: 0;
}

/* ------------ matches-container (5경기) ------------ */
.matches-container {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

/* ------------ 버튼 ------------ */
.button-container {
  display: flex;
  justify-content: flex-end;
  gap: 20px;
  margin-top: 40px;
}

/* 공통 버튼 */
.btn {
  padding: 15px 30px;
  font-size: 18px;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  font-weight: bold;
  color: #fff;
  box-shadow: 0 2px 5px rgba(0, 0, 0, 0.2);
}

/* 저장 & 취소 */
.btn-save {
  background-color: #70c16b; /* 초록 */
}
.btn-cancel {
  background-color: #f56b6b; /* 빨강 */
}

/* 반응형: 960px 이하에서 행 배치 변경 */
@media (max-width: 960px) {
  .form-row {
    flex-direction: column;
  }
  .form-group.left {
    width: 100%;
    justify-content: flex-start;
  }
}

</style>
