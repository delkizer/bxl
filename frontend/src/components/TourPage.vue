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
            id="start_date"
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
              :value="nation.code.trim()"
            >
              {{ nation.code_desc }}
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

      <!-- 버튼 영역 -->
      <div class="button-container">
        <button class="btn btn-save" @click="saveData">저장</button>
        <button class="btn btn-cancel" @click="showExitModal = true">종료</button>
        <button class="btn btn-delete" @click="handleDelete" v-if="tournament_uuid">
          삭제
        </button>
        <!-- v-if="existingUuid" : 수정 모드일 때만 삭제 버튼 표시 -->
      </div>
    </div>

    <!-- 검증 에러 모달 -->
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

    <!-- 삭제 모달 -->
    <ConfirmationModal
      :visible="showDeleteModal"
      title="삭제 확인"
      message="정말로 삭제하시겠습니까? 삭제 후에는 복구가 불가능합니다."
      confirmButtonLabel="확인"
      cancelButtonLabel="취소"
      @confirm="handleDeleteConfirm"
      @cancel="handleDeleteCancel"
    />
  </div>
</template>

<script>
import tourApi from "@/api/tourApi.js";
import Confirmation from "@/components/modal/Confirmation.vue";

export default {
  name: "TournamentInfoPage",
  components: { ConfirmationModal: Confirmation },
  data() {
    return {
      tournament_uuid: null,
      tournament_title: "",
      start_date: "",
      end_date: "",
      nationList: [],
      nation_code: "KOR",
      city_name: "서울",
      stadium_name: "장충체육관",
      is_bxl: true,

      // 모달 표시 여부
      showSaveModal: false,
      showExitModal: false,
      showValidationModal: false,

      // 삭제 모달
      showDeleteModal: false,
    };
  },
  async mounted() {
    this.tournament_uuid = this.$route.params.uuid;
    if (this.tournament_uuid) {
      await this.loadTournamentData(this.tournament_uuid);
    }
    try {
      const response = await tourApi.getNationList({});
      this.nationList = response.data;
    } catch (error) {
      console.error("국가 목록 로드 실패:", error);
    }
  },
  methods: {
    handleExitConfirm() {
      this.showExitModal = false;
      this.$router.push("/");
    },
    handleExitCancel() {
      this.showExitModal = false;
    },

    async handleSaveConfirm() {
      try {
        this.showSaveModal = false;
        const payload = {
          tournament_title: this.tournament_title,
          start_date: this.start_date,
          end_date: this.end_date,
          nation_code: this.nation_code,
          city_name: this.city_name,
          stadium_name: this.stadium_name,
          is_bxl: this.is_bxl,
          ...(this.tournament_uuid ? {tournament_uuid: this.tournament_uuid} : {})
        };
        console.log(payload)
        const response = await tourApi.postTourPage( payload);
        console.log("대회 등록 완료:", response.data);
        alert("대회 등록 완료");
        this.$router.push("/tourlist");
      } catch (error) {
        console.error("대회 등록 실패:", error);
        alert("대회 등록 실패");
      }
    },
    handleSaveCancel() {
      this.showSaveModal = false;
    },

    saveData() {
      if (
        !this.tournament_title ||
        !this.start_date ||
        !this.end_date ||
        !this.city_name ||
        !this.stadium_name
      ) {
        this.showValidationModal = true;
      } else {
        this.showSaveModal = true;
      }
    },
    closeValidationModal() {
      this.showValidationModal = false;
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
    },
    async loadTournamentData(uuid) {
      console.log("로드할 UUID:", uuid);
      try {
        const response = await tourApi.getTourList({ tournament_uuid: uuid });
        const data = response.data;
        const item = data[0];

        this.tournament_title = item.tournament_title;
        this.start_date = item.start_date;
        this.end_date = item.end_date;
        this.nation_code = item.nation_code;
        this.city_name = item.city_name;
        this.stadium_name = item.stadium_name;
      } catch (e) {
        console.error("기존 대회 불러오기 실패:", e);
      }
    },

    // 삭제 버튼 클릭 -> 삭제 모달
    handleDelete() {
      // 수정 모드가 아닐 때( uuid 없음 )는 삭제 불가 처리
      if (!this.tournament_uuid) {
        alert("새 대회 등록 모드에서는 삭제할 수 없습니다.");
        return;
      }
      this.showDeleteModal = true;
    },
    // 삭제 확정 -> API 호출
    async handleDeleteConfirm() {
      try {
        // deleteTourPage : URI/tourpage/{tournament_uuid}로 DELETE 요청
        await tourApi.deleteTourPage(this.tournament_uuid);
        alert("대회가 삭제되었습니다.");
        this.$router.push("/tourlist");
      } catch (error) {
        console.log("삭제 실패:", error);
        alert("삭제 실패");
      } finally {
        this.showDeleteModal = false;
      }
    },
    handleDeleteCancel() {
      this.showDeleteModal = false;
    },
  },
};
</script>

<style scoped>
.game-info-page {
  width: 100%;
  min-height: 100vh;
  background-color: #f8fafc;
  display: flex;
  align-items: center;
  justify-content: center;
  box-sizing: border-box;
  padding: 1.5rem;
}

@media (min-width: 1024px) {
  .game-info-page {
    position: absolute;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);
  }
}

.form-container {
  width: 600px;
  max-width: 90%;
  background-color: #f9fafb;
  border-radius: 8px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
  padding: 1.5rem;
  box-sizing: border-box;

  display: flex;
  flex-direction: column;
  gap: 1.25rem;
}

.form-row {
  display: flex;
  gap: 1rem;
}

@media (max-width: 960px) {
  .form-row {
    flex-direction: column;
  }
}

.form-group {
  display: flex;
  flex-direction: column;
  background-color: #fff;
  padding: 0.75rem;
  border-radius: 4px;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.05);
  border: 1px solid #eee;
}

.form-group label {
  font-weight: bold;
  font-size: 0.95rem;
  text-align: center;
  margin-bottom: 0.5rem;
}

.form-control {
  padding: 0.5rem 0.75rem;
  border: 1px solid #d1d5db;
  border-radius: 4px;
  font-size: 0.95rem;
  outline: none;
}
.form-control:focus {
  border-color: #93c5fd;
  box-shadow: 0 0 0 3px rgba(147, 197, 253, 0.3);
}
select.form-control {
  appearance: none;
  background-image: url("data:image/svg+xml,%3csvg ...");
  background-repeat: no-repeat;
  background-position: right 8px center;
  background-size: 16px;
  padding-right: 2rem;
}

.left {
  width: 120px;
  min-width: 100px;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}
.middle {
  flex: 1;
}
.right {
  flex: 2;
}

.button-container {
  display: flex;
  justify-content: flex-end;
  gap: 1rem;
  margin-top: 1rem;
}

.btn {
  padding: 0.75rem 1.5rem;
  font-size: 1rem;
  border: none;
  border-radius: 4px;
  font-weight: bold;
  cursor: pointer;
  transition: background-color 0.2s ease, transform 0.2s ease;
}

/* 녹색 */
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

/* 기존 종료용 붉은색 */
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

/* 삭제 전용: 더 강렬한 붉은색 */
.btn-delete {
  background-color: #dc2626; /* Tailwind Red-600 */
  color: #fff;
}
.btn-delete:hover {
  background-color: #b91c1c; /* Tailwind Red-700 */
}
.btn-delete:active {
  transform: scale(0.98);
}
</style>
