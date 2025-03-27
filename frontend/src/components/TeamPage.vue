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
          <div
            v-for="(player, index) in players"
            :key="index"
            class="player-row"
          >
            <!-- 이름 입력 -->
            <div class="form-group middle">
              <input class="form-control" v-model="player.player_name" />
            </div>
            <!-- 성별 선택 -->
            <div class="form-group right">
              <select class="form-control" v-model="player.gender">
                <option value="M">남</option>
                <option value="W">여</option>
              </select>
            </div>
            <button class="btn btn-cancel small" @click="removePlayer(index)">-</button>
          </div>

          <div class="player-row">
            <div class="form-group middle">
              <input
                class="form-control"
                v-model="newPlayer.first_name"
                placeholder="퍼스트 이름"
              />
            </div>
            <div class="form-group middle">
              <input
                class="form-control"
                v-model="newPlayer.family_name"
                placeholder="패밀리 이름"
              />
            </div>
            <div class="form-group middle">
              <input
                class="form-control"
                v-model="newPlayer.nick_name"
                placeholder="닉네임"
              />
            </div>
          </div>
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
            <select class="form-control" v-model="newPlayer.primaryDiscipline">
              <option value="">주종목</option>
              <option value="SGL">단식</option>
              <option value="DBL">복식</option>
              <option value="MXD">혼합복식</option>
            </select>
          </div>
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
      message="저장하시겠습니까?"
      confirmButtonLabel="확인"
      cancelButtonLabel="취소"
      @confirm="handleSaveConfirm"
      @cancel="handleSaveCancel"
    />

    <!-- (4) 종료 모달 -->
    <ConfirmationModal
      :visible="showExitModal"
      title="종료 확인"
      message="정말 종료하시겠습니까?"
      confirmButtonLabel="확인"
      cancelButtonLabel="취소"
      @confirm="handleExitConfirm"
      @cancel="handleExitCancel"
    />
</template>

<script>
import teamApi from "@/api/teamApi.js";
import tourApi  from "@/api/tourApi.js";
import ConfirmationModal from "@/components/ConfirmationModal.vue";

export default {
  name: 'TeamPage',
  components: {ConfirmationModal},

  data() {
    return {
      newPlayer: {
        first_name: '',
        family_name: '',
        nick_name: '',
        nation_code: '',
        gender: '',
        hand: '',
        primaryDiscipline: '',
      },
      teamName: '',
      nations: [],
      selectedCountry: '',
      players: [],
      tourList: [],
      selectedTour: "",

      // 모달 표시 여부
      showValidationModal: false,
      showAddModal: false,
      showSaveModal: false,
      showExitModal: false
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
          this.players = response.data;
          this.teamName = this.players[0].team_name;
          this.selectedCountry = this.players[0].nation_code
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
      || !this.newPlayer.primaryDiscipline.trim() ){
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
      if (this.newPlayer.player_name.trim() !== '') {
        this.players.push({
          player_name: this.newPlayer.player_name,
          gender: this.newPlayer.gender
        });
        // 입력 필드 초기화
        this.newPlayer.player_name = '';
        this.newPlayer.gender = 'M';
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
        player_name: p.player_name,
        gender: p.gender
      }));

      // 최종 전송할 데이터 구조
      const param = {
        tournament_uuid: this.players[0].tournament_uuid,
        team_name: this.teamName,
        team_code: this.$route.params.team_code,
        nation_code: this.selectedCountry,
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
    }
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

  /* 배경색, 크기, 기타 스타일 */
  background-color: #4b7cb6;
  width: 500px;
  min-height: 400px;

  /* 내부 요소 정렬 방식 */
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;

  /* 내부 여백 */
  padding: 20px;

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
  /* 고정 높이 제거 (height: 70px; 불필요 시 삭제) */
  width: 100px;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

/* 선수 필드들을 가로로 쌓는 래퍼 */
.player-wrapper {
  display: flex;
  flex-direction: row; /* 가로 나열 */
  flex-wrap: wrap;     /* 줄바꿈 허용(공간 부족 시) */
  gap: 15px;
}

/* 개별 선수 한 칸(이름+성별) */
.player-row {
  display: flex;
  align-items: center;
  gap: 10px;

  /* 아래쪽 간격 주어, 행들이 붙지 않게 */
  margin-bottom: 5px;
}

/* ------------------------------
   입력 요소에 대한 스타일
------------------------------ */
.form-group {
  /* 공통 박스 스타일 */
  display: flex;
  flex-direction: column;
  background-color: white;
  padding: 10px; /* padding을 조금 줄임 */
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
   가운데/오른쪽 .form-group
   (필요 시 flex: 1; 제거 또는 조정)
------------------------------ */
.form-group.middle,
.form-group.right {
  /* 확장 필요하면 유지, 불필요하면 주석 처리
     flex: 1;
  */
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
  /* 예시: 저장 버튼 색상 */
  background-color: #70c16b;
  color: #fff;
}

.btn-cancel {
  /* 예시: 취소/종료 버튼 색상 */
  background-color: #f56b6b;
  color: #fff;
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
    max-width: 100%;
    justify-content: flex-start;
  }
  .middle,
  .right {
    max-width: 100%;
  }
}
</style>
