<template>
  <div class="game-info-page">
    <div class="form-container">
      <div class="form-row">
        <div class="form-group left">
          <label>대회 선택</label>
        </div>
        <div class="form-group middle">
          <!-- 대회 배열을 순회해 옵션 생성 -->
          <select class="form-control" v-model="selectedTour">
            <option value=""></option>
            <option
              v-for="(tour, index) in tourList"
              :key="index"
              :value="tour.tournament_uuid"
            >
              {{tour.tournament_title}}
            </option>
          </select>

        </div>
      </div>

      <!-- 팀 이름 입력 -->
      <div class="form-row">
        <div class="form-group left">
          <label>팀이름</label>
        </div>
        <div class="form-group middle">
          <input class="form-control" v-model="teamName" />
        </div>
      </div>


      <!-- 선수 정보 (반복) -->
      <div class="form-row">
        <!-- 왼쪽 라벨은 한 번만 표시 -->
        <div class="form-group left">
          <label>소속선수</label>
        </div>
        <!-- 오른쪽에 여러 선수 필드를 반복해서 넣기 위한 래퍼 -->
        <div class="player-wrapper">
          <!-- 여기서 반복 -->
          <div v-for="(player, index) in players" :key="index" class="player-row">
            <!-- 이름 입력 -->
            <div class="player-row-line">
              <div class="form-group middle"><input class="form-control" v-model="player.first_name" placeholder="퍼스트 이름" /></div>
              <div class="form-group middle"><input class="form-control" v-model="player.family_name" placeholder="패밀리 이름"/></div>
              <div class="form-group middle"><input class="form-control" v-model="player.nick_name" placeholder="닉네임"/></div>
              <button class="btn btn-cancel small" @click="openRemoveModal(index)">-</button>
            </div>
            <div class="player-row-line">
              <!-- 국가 -->
              <div class="form-group middle">
                <label>국가</label>
                <select class="form-control" v-model="player.nation_code">
                  <option v-for="nation in nations" :key="nation.code" :value="nation.code.trim()">{{ nation.code_desc }}</option>
                </select>
              </div>
              <!-- 성별 -->
              <div class="form-group right">
                <label>성별</label>
                <select class="form-control" v-model="player.gender">
                  <option value="">성별</option>
                  <option value="M">남</option>
                  <option value="W">여</option>
                </select>
              </div>

              <!-- 핸드 -->
              <div class="form-group middle">
                <label>핸드</label>
                <select class="form-control" v-model="player.hand">
                  <option value="">핸드</option>
                  <option value="right">오른손</option>
                  <option value="left">왼손</option>
                </select>
              </div>

              <!-- 주종목 -->
              <div class="form-group middle">
                <label>주종목</label>
                <select class="form-control" v-model="player.primary_discipline">
                  <option value="">주종목</option>
                  <option value="SGL">단식</option>
                  <option value="DBL">복식</option>
                  <option value="MXD">혼합복식</option>
                </select>
              </div>
            </div>
          </div>

          <!-- 추가되는 선수 정보 시작-->
          <div class="player-row">
            <div class="player-row-line">
              <div class="form-group middle"><input class="form-control" v-model="newPlayer.first_name" placeholder="퍼스트 이름"/></div>
              <div class="form-group middle"><input class="form-control" v-model="newPlayer.family_name" placeholder="패밀리 이름"/></div>
              <div class="form-group middle"><input class="form-control" v-model="newPlayer.nick_name" placeholder="닉네임"/></div>
            </div>
            <div class="player-row-line">
              <div class="form-group middle">
                <select class="form-control" v-model="newPlayer.nation_code">
                  <option value="">국가선택</option>
                  <option v-for="nation in nations" :key="nation.code" :value="nation.code.trim()">
                    {{ nation.code_desc }}
                  </option>
                </select>
              </div>
              <div class="form-group right">
                <select class="form-control" v-model="newPlayer.gender">
                  <option value="">성별</option><option value="M">남</option><option value="W">여</option>
                </select>
              </div>
              <div class="form-group middle">
                <select class="form-control" v-model="newPlayer.hand">
                  <option value="">핸드</option><option value="right">오른손</option><option value="left">왼손</option>
                </select>
              </div>
              <div class="form-group middle">
                <select class="form-control" v-model="newPlayer.primary_discipline">
                  <option value="">주종목</option><option value="SGL">단식</option><option value="DBL">복식</option><option value="MXD">혼합복식</option>
                </select>
              </div>
            </div>
          </div>
          <!-- 추가되는 선수 정보 종료-->
        </div>
      </div>

      <!-- 버튼 영역 -->
      <div class="button-container">
        <!-- 등록(새로운 선수 추가) -->
        <button class="btn btn-save" @click="openAddModal">등록</button>
        <!-- 저장 -->
        <button class="btn btn-save" @click="openSaveModal">저장</button>
        <!-- 종료 -->
        <button class="btn btn-cancel" @click="openExitModal">종료</button>
      </div>
    </div>
  </div>
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
      message="저장하시겠습니까? 등록 버튼을 눌라서 소속 선수 명단에 등록하지 않은 선수는 등록되지 않습니다. "
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
</template>

<script>
import teamApi from "@/api/teamApi.js";
import tourApi  from "@/api/tourApi.js";
import Confirmation from "@/components/modal/Confirmation.vue";

export default {
  name: 'TeamPage',
  components: {ConfirmationModal: Confirmation},

  data() {
    return {
      newPlayer: {
        first_name: '',
        family_name: '',
        nick_name: '',
        nation_code: '',
        gender: '',
        hand: '',
        primary_discipline: '',
      },
      teamName: '',
      nations: [],
      players: [],
      tourList: [],
      selectedTour: "",

      // 모달 표시 여부
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
        if ( this.$route.params.team_code ) {
          const response = await teamApi.getPlayerList(this.$route.params.team_code);
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
    //유효성 검사 (필수 항목 체크)
    validateInput() {
      // 대회선택 / 팀 이름
      if (!this.selectedTour || !this.teamName.trim() ) {
        return false;
      }
      // 필요하다면 선수 목록 체크도 추가
      return true;
    },
    //등록 로직 모달
    openAddModal() {
      // (선택) newPlayer.player_name이 비었으면 모달로 알림
      if (!this.newPlayer.first_name.trim() || !this.newPlayer.family_name.trim()
      || !this.newPlayer.nick_name.trim() || !this.newPlayer.nation_code.trim()
      || !this.newPlayer.gender.trim() || !this.newPlayer.hand.trim()
      || !this.newPlayer.primary_discipline.trim() ){
        this.showValidationModal = true;
      } else {
        this.showAddModal = true;
      }
    },
    handleAddConfirm() {
      // 실제 등록 로직: addPlayer()
      this.addPlayer();
      // 모달 닫기
      this.showAddModal = false;
    },
    handleAddCancel() {
      this.showAddModal = false;
    },
    addPlayer() {
      if (this.newPlayer.first_name.trim() !== ''  && this.newPlayer.family_name.trim() !== '' ) {
        this.players.push({
          first_name: this.newPlayer.first_name,
          family_name: this.newPlayer.family_name,
          nick_name: this.newPlayer.nick_name,
          nation_code: this.newPlayer.nation_code,
          gender: this.newPlayer.gender,
          hand: this.newPlayer.hand,
          primary_discipline: this.newPlayer.primary_discipline,
        });
        // 입력 필드 초기화
        this.newPlayer.first_name = '';
        this.newPlayer.family_name = '';
        this.newPlayer.nick_name = '';
        this.newPlayer.nation_code = '';
        this.newPlayer.gender = '';
        this.newPlayer.hand = '';
        this.newPlayer.primary_discipline = '';
      } else {
        alert('이름을 입력해주세요.');
      }
    },
    removePlayer(index) {
      this.players.splice(index, 1);
    },
    // 저장 버튼 클릭 → 서버에 POST
    async saveData() {
      // players_info: 서버 스펙에 맞게 가공
      const playersInfo = this.players.map((p) => ({
        player_uuid: p.player_uuid,      // 기존 uuid
        first_name: p.first_name,
        family_name: p.family_name,
        nick_name: p.nick_name,
        nation_code: p.nation_code,
        gender: p.gender,
        hand: p.hand,
        primary_discipline: p.primary_discipline,
      }));

      // 최종 전송할 데이터 구조
      const param = {
        tournament_uuid: this.selectedTour,
        team_name: this.teamName,
        team_code: this.$route.params.team_code || null,
        players_info: playersInfo
      };

      console.log('저장할 데이터:', param);

      try {
        const response = await teamApi.postTeamPage(param);
        console.log('저장 완료:', response.data);
        alert('저장되었습니다.');
      } catch (error) {
        console.error('저장 중 오류:', error);
        alert('저장에 실패했습니다.');
      }
    },
    openSaveModal() {
      // 필요 시 save 전 유효성 검사
      if (!this.validateInput()) {
        this.showValidationModal = true;
        return;
      }
      this.showSaveModal = true;
    },
    handleSaveConfirm() {
      // 실제 서버 저장 로직
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
      // 정말 종료 → 홈으로 이동
      this.showExitModal = false;
      this.$router.push('/');
    },
    handleExitCancel() {
      this.showExitModal = false;
    },
    closeValidationModal() {
      this.showValidationModal = false;
    },
    // 삭제 모달 열기
    openRemoveModal(index) {
      this.removeIndex = index;      // 어떤 선수를 지울지 인덱스 저장
      this.showRemoveModal = true;   // 모달 표시
    },
    // 삭제 모달에서 '확인'을 눌렀을 때
    handleRemoveConfirm() {
      // 실제 선수 삭제
      this.players.splice(this.removeIndex, 1);

      // 모달 닫고 인덱스도 정리
      this.showRemoveModal = false;
      this.removeIndex = null;
    },

    // 삭제 모달에서 '취소'를 눌렀을 때
    handleRemoveCancel() {
      this.showRemoveModal = false;
      this.removeIndex = null;
    },

  }
};
</script>

<style scoped>
.game-info-page {
  /*
    1) 화면의 가운데 배치
    2) 내용이 많으면 내부 스크롤
  */
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);

  /* 배경, 크기, 스크롤 설정 */
  background-color: #4b7cb6;  /* 안쪽 박스는 흰색 바탕 */
  width: 1024px;               /* 고정 폭 예시 */
  max-width: 90%;            /* 화면이 좁아지면 90%까지만 줄어듦 */
  max-height: 90vh;          /* 뷰포트 90% 높이로 제한 */
  overflow-y: auto;          /* 세로 스크롤 */

  /* 내부 여백 */
  padding: 20px;
}

/* form-container: 기본 흐름 */
.form-container {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

/* 각 행(라벨+필드) 레이아웃 */
.form-row {
  display: flex;
  gap: 10px;
  /* 가로로 배치, 필요 시 align-items로 높이 조정 가능 */
}

/* 왼쪽 라벨 영역 */
.form-group.left {
  width: 100px;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

/* 선수 목록 래퍼 */
.player-wrapper {
  display: flex;
  flex-wrap: wrap;
  gap: 15px;
}

/* 개별 선수 한 칸(2줄) */
.player-row {
  display: flex;
  flex-direction: column;
  gap: 10px;
  margin-bottom: 5px;
}

/* player-row 내부 한 줄 */
.player-row-line {
  display: flex;
  flex-wrap: nowrap;
  gap: 10px;
}

/* 공통 입력 컨테이너 스타일 */
.form-group {
  display: flex;
  flex-direction: column;
  background-color: #fff;
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

/* 셀렉트 화살표 커스텀 예시 */
select.form-control {
  appearance: none;
  background-image: url("data:image/svg+xml;charset=UTF-8,%3csvg...");
  background-repeat: no-repeat;
  background-position: right 8px center;
  background-size: 16px;
  padding-right: 30px;
}

/* 버튼 영역 */
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

/* 반응형 처리 */
@media (max-width: 960px) {
  .form-row {
    flex-direction: column;
  }
  .form-group.left {
    width: 100%;
    max-width: 100%;
    justify-content: flex-start;
  }
  .form-group.middle,
  .form-group.right {
    max-width: 100%;
  }
}

</style>
