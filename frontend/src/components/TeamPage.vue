<template>
  <div class="game-info-page">
    <div class="form-container">
      <!-- 대회 선택 -->
      <div class="form-row">
        <div class="form-group left">
          <label>대회 선택</label>
        </div>
        <div class="form-group middle">
          <select class="form-control" v-model="selectedTour">
            <option value=""></option>
            <option
              v-for="(tour, index) in tourList"
              :key="index"
              :value="tour.tournament_uuid"
            >
              {{ tour.tournament_title }}
            </option>
          </select>
        </div>
      </div>

      <!-- 팀 이름 -->
      <div class="form-row">
        <div class="form-group left">
          <label>팀이름</label>
        </div>
        <div class="form-group middle">
          <input class="form-control" v-model="teamName" />
        </div>
      </div>

      <!-- 선수 정보 -->
      <div class="form-row">
        <div class="form-group left">
          <label>소속선수</label>
        </div>
        <div class="player-wrapper">
          <!-- 이미 등록된 선수들 -->
          <div
            v-for="(player, index) in players"
            :key="index"
            class="player-row"
          >
            <div class="player-row-line">
              <div class="form-group middle">
                <input
                  class="form-control"
                  v-model="player.first_name"
                  placeholder="퍼스트 이름"
                />
                <input
                  class="form-control"
                  v-model="player.family_name"
                  placeholder="패밀리 이름"
                />
                <input
                  class="form-control"
                  v-model="player.nick_name"
                  placeholder="닉네임"
                />
              </div>
              <button
                class="btn btn-cancel small"
                @click="openRemoveModal(index)"
              >
                -
              </button>
            </div>
            <div class="player-row-line">
              <div class="form-group middle">
                <label>국가</label>
                <select class="form-control" v-model="player.nation_code">
                  <option
                    v-for="nation in nations"
                    :key="nation.code"
                    :value="nation.code.trim()"
                  >
                    {{ nation.code_desc }}
                  </option>
                </select>
              </div>
              <div class="form-group right">
                <label>성별</label>
                <select class="form-control" v-model="player.gender">
                  <option value="">성별</option>
                  <option value="M">남</option>
                  <option value="W">여</option>
                </select>
              </div>
              <div class="form-group middle">
                <label>핸드</label>
                <select class="form-control" v-model="player.hand">
                  <option value="">핸드</option>
                  <option value="right">오른손</option>
                  <option value="left">왼손</option>
                </select>
              </div>
              <div class="form-group middle">
                <label>주종목</label>
                <select
                  class="form-control"
                  v-model="player.primary_discipline"
                >
                  <option value="">주종목</option>
                  <option value="SGL">단식</option>
                  <option value="DBL">복식</option>
                  <option value="MXD">혼합복식</option>
                </select>
              </div>
            </div>
          </div>

          <!-- 새 선수 추가 영역 -->
          <div class="player-row">
            <div class="player-row-line">
              <div class="form-group middle">
                <input
                  class="form-control"
                  v-model="newPlayer.first_name"
                  placeholder="퍼스트 이름"
                />
                <input
                  class="form-control"
                  v-model="newPlayer.family_name"
                  placeholder="패밀리 이름"
                />
                <input
                  class="form-control"
                  v-model="newPlayer.nick_name"
                  placeholder="닉네임"
                />
              </div>
            </div>
            <div class="player-row-line">
              <div class="form-group middle">
                <select class="form-control" v-model="newPlayer.nation_code">
                  <option value="">국가선택</option>
                  <option
                    v-for="nation in nations"
                    :key="nation.code"
                    :value="nation.code.trim()"
                  >
                    {{ nation.code_desc }}
                  </option>
                </select>
              </div>
              <div class="form-group right">
                <select class="form-control" v-model="newPlayer.gender">
                  <option value="">성별</option>
                  <option value="M">남</option>
                  <option value="W">여</option>
                </select>
              </div>
              <div class="form-group middle">
                <select class="form-control" v-model="newPlayer.hand">
                  <option value="">핸드</option>
                  <option value="right">오른손</option>
                  <option value="left">왼손</option>
                </select>
              </div>
              <div class="form-group middle">
                <select
                  class="form-control"
                  v-model="newPlayer.primary_discipline"
                >
                  <option value="">주종목</option>
                  <option value="SGL">단식</option>
                  <option value="DBL">복식</option>
                  <option value="MXD">혼합복식</option>
                </select>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- 버튼 영역 -->
      <div class="button-container">
        <!-- 등록 (새 선수) -->
        <button class="btn btn-register" @click="openAddModal">등록</button>
        <!-- 저장 -->
        <button class="btn btn-save" @click="openSaveModal">저장</button>
        <!-- 종료 -->
        <button class="btn btn-cancel" @click="openExitModal">종료</button>
      </div>
    </div>

    <!-- 모달들(ConfirmationModal)은 위치 fixed 이므로
         세로 스크롤이 길어도 뷰포트 중앙에 보임 -->
    <!-- (1) 입력 누락 모달 -->
    <ConfirmationModal
      :visible="showValidationModal"
      title="입력 오류"
      message="필수 항목이 비어 있습니다. 확인 후 다시 시도해주세요."
      confirmButtonLabel="확인"
      :hideCancel="true"
      @confirm="closeValidationModal"
    />
    <!-- (2) 등록 모달 -->
    <ConfirmationModal
      :visible="showAddModal"
      title="등록 확인"
      message="새 선수를 등록하시겠습니까?"
      confirmButtonLabel="확인"
      cancelButtonLabel="취소"
      @confirm="handleAddConfirm"
      @cancel="handleAddCancel"
    />
    <!-- (3) 저장 모달 -->
    <ConfirmationModal
      :visible="showSaveModal"
      title="저장 확인"
      message="저장하시겠습니까? 등록 버튼을 누르지 않은 선수는 반영되지 않습니다."
      confirmButtonLabel="확인"
      cancelButtonLabel="취소"
      @confirm="handleSaveConfirm"
      @cancel="handleSaveCancel"
    />
    <!-- (4) 종료 모달 -->
    <ConfirmationModal
      :visible="showExitModal"
      title="종료 확인"
      message="메인 화면으로 이동하시겠습니까?"
      confirmButtonLabel="확인"
      cancelButtonLabel="취소"
      @confirm="handleExitConfirm"
      @cancel="handleExitCancel"
    />
    <!-- (5) 삭제 확인 모달 -->
    <ConfirmationModal
      :visible="showRemoveModal"
      title="삭제 확인"
      message="정말 이 선수를 삭제하시겠습니까?"
      confirmButtonLabel="확인"
      cancelButtonLabel="취소"
      @confirm="handleRemoveConfirm"
      @cancel="handleRemoveCancel"
    />
  </div>
</template>

<script>
/* 기존 로직 그대로 */

import teamApi from "@/api/teamApi.js";
import tourApi from "@/api/tourApi.js";
import Confirmation from "@/components/modal/Confirmation.vue";

export default {
  name: "TeamPage",
  components: { ConfirmationModal: Confirmation },
  data() {
    return {
      newPlayer: {
        first_name: "",
        family_name: "",
        nick_name: "",
        nation_code: "",
        gender: "",
        hand: "",
        primary_discipline: "",
      },
      teamName: "",
      nations: [],
      players: [],
      tourList: [],
      selectedTour: "",
      showValidationModal: false,
      showAddModal: false,
      showSaveModal: false,
      showExitModal: false,
      showRemoveModal: false,
      removeIndex: null,
    };
  },
  mounted() {
    this.fetchData();
  },
  methods: {
    async fetchData() {
      try {
        if (this.$route.params.team_code) {
          const response = await teamApi.getPlayerList(
            this.$route.params.team_code
          );
          this.players = response.data || [];
          if (this.players.length > 0) {
            this.teamName = this.players[0].team_name;
            this.selectedTour = this.players[0].tournament_uuid;
          }
        }
        const response2 = await tourApi.getNationList();
        this.nations = response2.data;
        const response3 = await tourApi.getTourList();
        this.tourList = response3.data;
      } catch (error) {
        console.log(error);
      }
    },
    validateInput() {
      if (!this.selectedTour || !this.teamName.trim()) {
        return false;
      }
      return true;
    },
    openAddModal() {
      if (
        !this.newPlayer.first_name.trim() ||
        !this.newPlayer.family_name.trim() ||
        !this.newPlayer.nick_name.trim() ||
        !this.newPlayer.nation_code.trim() ||
        !this.newPlayer.gender.trim() ||
        !this.newPlayer.hand.trim() ||
        !this.newPlayer.primary_discipline.trim()
      ) {
        this.showValidationModal = true;
      } else {
        this.showAddModal = true;
      }
    },
    handleAddConfirm() {
      this.addPlayer();
      this.showAddModal = false;
    },
    handleAddCancel() {
      this.showAddModal = false;
    },
    addPlayer() {
      if (
        this.newPlayer.first_name.trim() !== "" &&
        this.newPlayer.family_name.trim() !== ""
      ) {
        this.players.push({ ...this.newPlayer });
        // 입력 필드 초기화
        this.newPlayer = {
          first_name: "",
          family_name: "",
          nick_name: "",
          nation_code: "",
          gender: "",
          hand: "",
          primary_discipline: "",
        };
      } else {
        alert("이름을 입력해주세요.");
      }
    },
    openRemoveModal(index) {
      this.removeIndex = index;
      this.showRemoveModal = true;
    },
    handleRemoveConfirm() {
      this.players.splice(this.removeIndex, 1);
      this.showRemoveModal = false;
      this.removeIndex = null;
    },
    handleRemoveCancel() {
      this.showRemoveModal = false;
      this.removeIndex = null;
    },
    async saveData() {
      const playersInfo = this.players.map((p) => ({
        player_uuid: p.player_uuid,
        first_name: p.first_name,
        family_name: p.family_name,
        nick_name: p.nick_name,
        nation_code: p.nation_code,
        gender: p.gender,
        hand: p.hand,
        primary_discipline: p.primary_discipline,
      }));

      const param = {
        tournament_uuid: this.selectedTour,
        team_name: this.teamName,
        team_code: this.$route.params.team_code || null,
        players_info: playersInfo,
      };
      console.log("저장할 데이터:", param);

      try {
        const response = await teamApi.postTeamPage(param);
        console.log("저장 완료:", response.data);
        alert("저장되었습니다.");
      } catch (error) {
        console.error("저장 중 오류:", error);
        alert("저장에 실패했습니다.");
      }
    },
    openSaveModal() {
      if (!this.validateInput()) {
        this.showValidationModal = true;
        return;
      }
      this.showSaveModal = true;
    },
    handleSaveConfirm() {
      this.saveData();
      this.showSaveModal = false;
    },
    handleSaveCancel() {
      this.showSaveModal = false;
    },
    openExitModal() {
      this.showExitModal = true;
    },
    handleExitConfirm() {
      this.showExitModal = false;
      this.$router.push("/");
    },
    handleExitCancel() {
      this.showExitModal = false;
    },
    closeValidationModal() {
      this.showValidationModal = false;
    },
  },
};
</script>

<style scoped>
/*
  1) 바탕(배경):
     - 1024px 미만에서는 flexbox 중앙
     - 1024px 이상에서는 absolute 중앙
     - 밝은 톤(#f8fafc)
*/
.game-info-page {
  width: 100%;
  min-height: 100vh;
  background-color: #f8fafc;
  display: flex;
  align-items: center;
  justify-content: center;
  box-sizing: border-box;
  padding: 2rem;
}

@media (min-width: 1024px) {
  .game-info-page {
    position: absolute;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);
  }
}

/*
  2) form-container:
     - 넓이 800px, 세로 최대 90vh
     - 내부 스크롤
     - 흰색 카드 스타일
*/
.form-container {
  width: 800px;
  max-height: 90vh;
  overflow-y: auto;
  background-color: #fff;
  border-radius: 8px;
  box-shadow: 0 4px 12px rgba(0,0,0,0.1);
  padding: 1.5rem;
  box-sizing: border-box;

  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

/* 각 행 */
.form-row {
  display: flex;
  gap: 10px;
}

/* 왼쪽 라벨 */
.form-group.left {
  width: 120px;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

/* 중간 / 오른쪽 등 */
.form-group.middle, .form-group.right {
  display: flex;
  flex-direction: column;
  background-color: #fff;
  padding: 10px;
  border-radius: 5px;
  box-shadow: 0 1px 3px rgba(0,0,0,0.05);
}

/* player-wrapper + player-row */
.player-wrapper {
  display: flex;
  flex-wrap: wrap;
  gap: 15px;
}
.player-row {
  display: flex;
  flex-direction: column;
  gap: 10px;
  margin-bottom: 5px;
}
.player-row-line {
  display: flex;
  flex-wrap: nowrap;
  gap: 10px;
}

/* 라벨 + 인풋 스타일 */
.form-group label {
  font-weight: bold;
  font-size: 0.9rem;
  text-align: center;
  margin-bottom: 5px;
}

/* 공통 인풋/셀렉트 */
.form-control {
  padding: 0.5rem 0.75rem;
  border: 1px solid #ddd;
  border-radius: 4px;
  font-size: 0.9rem;
  margin: 1px;
}

/* 버튼 영역 */
.button-container {
  display: flex;
  justify-content: flex-end;
  gap: 1rem;
  margin-top: 1rem;
}

/* 버튼 스타일(등록, 저장, 종료) */
.btn {
  padding: 0.65rem 1.2rem;
  font-size: 1rem;
  border: none;
  border-radius: 4px;
  font-weight: bold;
  cursor: pointer;
  transition: background-color 0.2s ease, transform 0.2s ease;
}

/* (3) 등록/저장 색상 구분 */
/* 등록 => 다른 계열의 녹색 */
.btn-register {
  background-color: #4CAF50; /* 밝은 초록 */
  color: #fff;
}
.btn-register:hover {
  background-color: #43a047;
}
.btn-register:active {
  transform: scale(0.98);
}

/* 저장 => 기존과 비슷한 초록(#70c16b) */
.btn-save {
  background-color: #70c16b;
  color: #fff;
}
.btn-save:hover {
  background-color: #64ad5f;
}
.btn-save:active {
  transform: scale(0.98);
}

/* 종료 => 붉은색 */
.btn-cancel {
  background-color: #f56b6b;
  color: #fff;
}
.btn-cancel:hover {
  background-color: #eb5e5e;
}
.btn-cancel:active {
  transform: scale(0.98);
}

/* 작은 버튼( - ) */
.small {
  padding: 0.4rem 0.6rem;
  font-size: 0.8rem;
  align-self: center;
}

/* 반응형 */
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
