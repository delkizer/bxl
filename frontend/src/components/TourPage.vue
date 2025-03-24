<template>
  <div class="game-info-page">
    <!-- 폼 전체 컨테이너 -->
    <div class="form-container">
      <!-- 대회이름 -->
      <div class="form-row">
        <div class="form-group left">
          <label for="tournament_title">대회이름</label>
        </div>
        <div class="form-group right">
          <input
            ref="titleInput"
            type="text"
            id="tournament_title"
            class="form-control"
            v-model="tournament_title"
            placeholder="대회이름을 입력하세요"
          />
        </div>
      </div>

      <!-- 대회기간 -->
      <div class="form-row">
        <div class="form-group left">
          <label for="start_date">대회기간</label>
        </div>
        <!-- 시작일 -->
        <div class="form-group middle">
          <input
            ref="startDateInput"
            type="date"
            id="starstart_date"
            class="form-control"
            v-model="start_date"
          />
        </div>
        <!-- 종료일 -->
        <div class="form-group right">
          <input
            ref="endDateInput"
            type="date"
            id="end_date"
            class="form-control"
            v-model="end_date"
          />
        </div>
      </div>

      <!-- 대회장소 -->
      <div class="form-row">
        <div class="form-group left">
          <label for="nationSelect">대회장소</label>
        </div>
        <!-- 국가 -->
        <div class="form-group middle">
          <select id="nation_code" class="form-control" v-model="nation_code">
            <option
              v-for="nation in nationList"
              :key="nation.code"
              :value="nation.code.trim()">
              {{nation.code_desc}}
            </option>
          </select>
        </div>
        <!-- 도시 -->
        <div class="form-group right">
          <input
            ref="cityInput"
            type="text"
            class="form-control"
            v-model="city_name"
            placeholder="예) 서울"
          />
        </div>
      </div>
      <!-- 상세 장소 -->
      <div class="form-row">
        <div class="form-group right" style="flex: 3;">
          <input
            ref="stadiumInput"
            type="text"
            class="form-control"
            v-model="stadium_name"
            placeholder="예) 장충체육관"
          />
        </div>
      </div>
    </div>

    <!-- 버튼 영역 -->
    <div class="button-container">
      <button class="btn btn-save" @click="saveData">
        저장
      </button>
      <button class="btn btn-cancel" @click="showExitModal = true">종료</button>
    </div>
  </div>

    <!-- 검증 에러 모달 (모든 필수 항목 누락 시) -->
    <ConfirmationModal
      :visible="showValidationModal"
      title="입력 오류"
      message="모든 필수 항목을 입력하거나 선택해주세요."
      confirmButtonLabel="확인"
      :hideCancel="true"
      @confirm="closeValidationModal"
    />

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


</template>

<script>
import tourApi from '@/api/tourApi.js';
import ConfirmationModal from "@/components/ConfirmationModal.vue";

export default {
  name: "TournamentInfoPage",
  components: {ConfirmationModal},
  data() {
    return {
      tournament_title: "",
      start_date: "",
      end_date: "",
      nationList: [],
      nation_code: "KOR",
      city_name: "서울",
      stadium_name: "장충체육관",
      is_bxl : true,

      // 모달 표시 여부
      showSaveModal: false,       // 저장 모달
      showExitModal: false,       // 종료 모달
      showValidationModal: false
    };
  },
  async mounted() {
    try {
      const response = await tourApi.getNationList({})
      this.nationList = response.data;
    } catch ( error ) {
          console.error("국가 목록 로드 실패:", error);
    }
  },
  methods: {
    handleExitConfirm() {
      this.showExitModal = false
      this.$router.push('/')
    },
    handleExitCancel() {
      this.showExitModal = false
    },
    async handleSaveConfirm() {
      try{
        this.showSaveModal = false
        const response = await  tourApi.postTourPage({
          "tournament_title":  this.tournament_title,
          "start_date":  this.start_date,
          "end_date":  this.end_date,
          "nation_code":  this.nation_code,
          "city_name":  this.city_name,
          "stadium_name":  this.stadium_name,
          "is_bxl":  this.is_bxl,
        })
      } catch ( error) {
        console.error("대회 등록 실패:", error);
      }
    },
    handleSaveCancel() {
      this.showSaveModal = false
    },

    saveData() {
      // 필수 항목 누락 체크
      if (
        !this.tournament_title ||
        !this.start_date ||
        !this.end_date ||
        !this.city_name ||
        !this.stadium_name
      ) {
        // 모달 열기
        this.showValidationModal = true;
      }
      else {
        this.showSaveModal = true;
      }
    },
    closeValidationModal() {
      // 모달 닫기
      this.showValidationModal = false;
      // 첫 번째 누락 필드에 포커스
      this.focusFirstEmptyField();
    },

    focusFirstEmptyField() {
      if (!this.tournament_title) {
        this.$refs.titleInput.focus();
      } else if (!this.start_date) {
        this.$refs.startDateInput.focus();
      } else if (!this.end_date) {
        this.$refs.endDateInput.focus();
      } else if (!this.city_name) {
        this.$refs.cityInput.focus();
      } else if (!this.stadium_name) {
        this.$refs.stadiumInput.focus();
      }
    }
  }
};
</script>

<style scoped>
.game-info-page {
  position: absolute;
  top: 50%;
  left: 50%;

  /* 자기 자신의 너비·높이의 절반만큼 좌상단으로 이동하여 정중앙 배치 */
  transform: translate(-50%, -50%);

  /* 배경색, 크기, 기타 스타일 */
  background-color: #4b7cb6;
  width: 500px;   /* 적절한 너비 */
  min-height: 400px; /* 혹은 auto, 적절히 조정 */

  /* 내용 정렬(내부 요소들에 대해서) */
  display: flex;
  flex-direction: column;
  align-items: center;    /* 수평 중앙 정렬 */
  justify-content: center;/* 수직 중앙 정렬 */

  /* 필요 시 내부 여백 */
  padding: 20px;
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

/* 반응형 */
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
}

.modal-content h3 {
  margin-top: 0;
  margin-bottom: 20px;
  text-align: center;
}

</style>
