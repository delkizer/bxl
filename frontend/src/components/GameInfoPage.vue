<template>
  <div class="game-info-page">
    <div class="form-container">
      <!-- 첫 번째 줄 -->
      <div class="form-row">
        <div class="form-group left">
          <label>대회정보</label>
        </div>
        <div class="form-group right">
          <input type="text" class="form-control" v-model="competitionInfo"/>
        </div>
      </div>

      <!-- 두 번째 줄 -->
      <div class="form-row">
        <div class="form-group left">
          <label>날짜</label>
        </div>
        <div class="form-group right">
          <input type="date" class="form-control" v-model="game_date" />
        </div>
      </div>

      <!-- 세 번째 줄 -->
      <div class="form-row">
        <div class="form-group left">
          <label>팀 선택</label>
        </div>
        <div class="form-group middle">
          <select class="form-control" v-model="selectedTeam1" @change="onTeamChange('team1')">
            <option value="">선택</option>
            <option value="Rockets" :disabled="selectedTeam2 === 'Rockets'">Rockets</option>
            <option value="Hurricanes" :disabled="selectedTeam2 === 'Hurricanes'">Hurricanes</option>
            <option value="Blitzers" :disabled="selectedTeam2 === 'Blitzers'">Blitzers</option>
            <option value="Lightning" :disabled="selectedTeam2 === 'Lightning'">Lightning</option>
            <option value="직접입력">직접입력</option>
          </select>
        </div>
        <div class="form-group right">
          <select class="form-control" v-model="selectedTeam2" @change="onTeamChange('team2')">
            <option value="">선택</option>
            <option value="Rockets" :disabled="selectedTeam1 === 'Rockets'">Rockets</option>
            <option value="Hurricanes" :disabled="selectedTeam1 === 'Hurricanes'">Hurricanes</option>
            <option value="Blitzers" :disabled="selectedTeam1 === 'Blitzers'">Blitzers</option>
            <option value="Lightning" :disabled="selectedTeam1 === 'Lightning'">Lightning</option>
            <option value="직접입력">직접입력</option>
          </select>
        </div>
      </div>

      <!-- 네 번째 줄 -->
      <div class="form-row">
        <div class="form-group left">
          <label>세트 순서</label>
        </div>
        <div class="form-group set-row">
          <div
            class="set-item"
            v-for="(setValue, index) in setSelections"
            :key="index"
          >
          <select class="form-control compact-select" v-model="setSelections[index]">
            <option value="">({{index+1}})선택</option>
            <option
              v-for="option in allSetOptions"
              :key = "option"
              :value = "option"
              :disabled = "isOptionSelectedElsewhere(option, index)">{{option}}</option>
          </select>
          </div>
        </div>
      </div>
    </div>

    <!-- 하단 버튼 영역 -->
    <div class="button-container">
      <button class="btn btn-save" @click="onSaveClick">저장</button>
      <button class="btn btn-cancel" @click="showExitModal = true">종료</button>
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

    <!-- 검증 에러 모달 (모든 필수 항목 누락 시) -->
    <ConfirmationModal
      :visible="showValidationModal"
      title="입력 오류"
      message="모든 필수 항목을 입력하거나 선택해주세요."
      confirmButtonLabel="확인"
      :hideCancel = "true"
      @confirm="closeValidationModal"
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

    <!-- 모달 (직접입력 시 표시) -->
    <div v-if="showCustomTeamModal" class="modal-overlay">
      <div class="modal-content">
        <h3>새로운 팀 추가</h3>
        <input
          type="text"
          class="modal-input"
          v-model="customTeamName"
          placeholder="팀 이름을 입력하세요."
        />
        <div class="modal-button-container">
          <button class="modal-btn" @click="confirmCustomTeam">확인</button>
          <button class="modal-btn" @click="cancelCustomTeam">취소</button>
        </div>
      </div>
    </div>

  </div>
</template>

<script>
import ConfirmationModal from '@/components/ConfirmationModal.vue'

export default {
  name: 'GameInfoPage',
  components: {
    ConfirmationModal
  },
  data() {
    return {
      competitionInfo: '',
      game_date: '',
      selectedTeam1: '',
      selectedTeam2: '',
      showCustomTeamModal: false, //직업 입력 모달
      customTeamName: '',         //새로 입력할 팀 이름

      showSaveModal: false,       // 저장 모달
      showExitModal: false,       // 종료 모달
      showValidationModal : false,

      allSetOptions: ['남자단식', '여자단식', '남자복식', '여자복식', '3 vs 3'],
      setSelections: ['', '', '', '', ''],
    }
  },
  methods: {
    onSaveClick() {
      if (!this.validateForm()) {
        // 모든 필수 항목이 채워지지 않았다면, 에러 모달을 표시
        this.showValidationModal = true;
      } else {
        // 모든 항목이 채워졌다면, 저장 확인 모달을 표시
        this.showSaveModal = true;
      }
    },
    closeValidationModal() {
      // 에러 모달 닫기
      this.showValidationModal = false;
    },
    // 직접입력 모달
    onTeamChange(teamField) {
      if (teamField === 'team1' && this.selectedTeam1 === '직접입력') {
        this.showCustomTeamModal = true
      }
      else if (teamField === 'team2' && this.selectedTeam2 === '직접입력') {
        this.showCustomTeamModal = true
      }
    },
    confirmCustomTeam() {
      this.showCustomTeamModal = false
      this.customTeamName = ''
    },
    cancelCustomTeam() {
      this.showCustomTeamModal = false
      this.customTeamName = ''
      this.selectedTeam1 = ''
      this.selectedTeam2 = ''
    },
    isOptionSelectedElsewhere(option, index) {
      return this.setSelections.some((sel, idx) => {
        return idx !== index && sel === option
      })
    },
    async handleSaveConfirm() {
      this.showSaveModal = false
      await this.callSaveAPI()
      this.$router.push('/gameinfo')
    },
    handleSaveCancel() {
      this.showSaveModal = false
    },
    handleExitConfirm() {
      this.showExitModal = false
      this.$router.push('/')
    },
    handleExitCancel() {
      this.showExitModal = false
    },
    // 실제 API 로직
    async callSaveAPI() {
      // TODO: API 호출 로직 작성 (axios 등)
      console.log("call SaveAPI")
    },
    validateForm() {
    // 대회정보
    if (!this.competitionInfo) return false;
    // 날짜
    if (!this.date) return false;
    // 팀 선택
    if (!this.selectedTeam1 || !this.selectedTeam2) return false;
    // 세트 순서(각 항목이 비어있지 않아야 함)
    for (let i = 0; i < this.setSelections.length; i++) {
      if (!this.setSelections[i]) {
        return false;
      }
    }
    return true;
  },
  }
}
</script>

<style scoped>
.game-info-page {
  width: 100%;
  min-height: 100vh;
  background-color: #4b7cb6;
  padding: 20px;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
}


.form-container {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.form-row {
  display: flex;
  gap: 20px;
}

.form-group {
  display: flex;
  flex-direction: column;
  background-color: white;
  padding: 15px;
  border-radius: 5px;
  box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
}

.form-group label {
  font-weight: bold;
  font-size: 16px;
  text-align: center;
}

.form-control {
  padding: 8px 12px;
  border: 1px solid #ddd;
  border-radius: 4px;
  font-size: 16px;
}

select.form-control {
  appearance: none;
  background-image: url("data:image/svg+xml;charset=UTF-8,%3csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24' fill='none' stroke='%23333' stroke-width='2' stroke-linecap='round' stroke-linejoin='round'%3e%3cpolyline points='6 9 12 15 18 9'%3e%3c/polyline%3e%3c/svg%3e");
  background-repeat: no-repeat;
  background-position: right 8px center;
  background-size: 16px;
  padding-right: 30px;
}

.left {
  width: 200px;
  height: 70px;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

.right {
  flex: 3;
}

.middle {
  flex: 1;
}

.set-row {
  flex: 3;
  display: flex;
  flex-direction: row;
  justify-content: space-between;
  gap: 5px;
  align-items: center;
}

.set-item {
  width: 80px;
  flex: 1;
  min-width: 0;
  max-width: 150px;
}

.compact-select {
  width: 100%;
  padding-left: 2px;
  padding-right: 15px;
  background-position: right 2px center;
  background-size: 10px;
  font-size: 14px;
}

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
  background-color: white;
}

.btn-cancel {
  background-color: white;
}

.form-row:nth-child(3) .form-group.middle,
.form-row:nth-child(3) .form-group.right {
  flex: 1;
}

/* 모달 관련 스타일 */
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.5); /* 반투명 배경 */
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 9999;
}

.modal-content {
  background-color: #ffffff;
  padding: 20px;
  border-radius: 8px;
  min-width: 300px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.2);
}

.modal-content h3 {
  margin-top: 0;
  margin-bottom: 20px;
  text-align: center;
}

.modal-input {
  width: 100%;
  padding: 10px;
  font-size: 16px;
  margin-bottom: 20px;
}

.modal-button-container {
  display: flex;
  justify-content: space-evenly;
  gap: 10px;
}

.modal-btn {
  background-color: white;
  color: #333;
  border: 1px solid #333;
  padding: 10px 20px;
  font-size: 16px;
  border-radius: 5px;
  cursor: pointer;
  font-weight: bold;
}

.modal-btn:hover {
  background-color: #f0f0f0;
}


@media (max-width: 960px) {
  .form-row {
    flex-direction: column;
  }

  .left {
    width: 100%;
    max-width: 100%;
  }

  .right, .middle {
    max-width: 100%;
  }

  .set-row {
    flex-wrap: wrap;
  }

  .set-item {
    min-width: 120px;
  }
}
</style>
