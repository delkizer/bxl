<template>
  <div class="main-container">
    <div class="tie-container">
      <!-- 상단 헤더/타이틀 -->
      <header class="tie-header">
        <h2 class="tie-title">TIE 선택</h2>

        <!-- dayList 배열을 순회해 옵션 생성 -->
        <div class="tie-select-wrapper">
          <label for="tie-select" class="sr-only">경기일 선택</label>
          <select
            id="tie-select"
            v-model="selectedDay"
            @change="filterTies"
            class="tie-select"
          >
            <option value="">전체</option>
            <option
              v-for="(day, index) in dayList"
              :key="index"
              :value="day.day_num"
            >
              {{ day.day_num }}일차 ({{ day.game_date }})
            </option>
          </select>
        </div>
      </header>

      <section class="tie-list">
        <!-- ties_list 배열을 순회 -->
        <article
          v-for="tie in ties_list"
          :key="tie.tie_no"
          class="tie-card"
          @click="selectTie(tie)"
        >
          <h3 class="tie-card-title">{{ tie.tie_no }} TIE ({{ tie.game_date }})</h3>
          <p class="tie-score">
            {{ tie.team1_name }}
            {{ tie.team1_point_sum }} : {{ tie.team2_point_sum }}
            {{ tie.team2_name }}
          </p>
        </article>
      </section>

      <!-- 하단/우측 액션 -->
      <footer class="tie-footer">
        <button class="btn btn-primary" @click="goTie">새로등록</button>
        <button class="btn btn-secondary" @click="goBack">뒤로가기</button>
        <button class="btn btn-tertiary" @click="goHome">메인가기</button>
      </footer>
    </div>

    <!-- 모달 -->
    <CoderModal
      :visible="showModal"
      title="TIE 상세정보 확인"
      :message="modalMessage"
      confirmButtonLabel="CODER"
      PlayerButtonLabel="PLAYER"
      OfficialButtonLabel="OFFICIAL"
      cancelButtonLabel="CANCEL"
      @confirm="onConfirmSelectTie"
      @official="onOfficialSelectTie"
      @player="onPlayerSelectTie"
      @cancel="onCancelSelectTie"
    />
  </div>
</template>

<script>
import { useCoderStore } from "@/stores/coder.js";
import coderApi from "@/api/coderApi.js";
import CoderModal from "@/components/modal/CoderModal.vue";

export default {
  name: "TieList",
  components: {
    CoderModal,
  },
  data() {
    return {
      ties_list: [],
      selectedDay: null,
      showModal: false,
      selectedTie: null,
    };
  },
  async mounted() {
    try {
      const response = await coderApi.getGameList({});
      this.ties_list = response.data;
    } catch (error) {
      console.error(error);
    }
  },
  computed: {
    filterTies() {
      if (!this.selectedDay) {
        return this.ties_list;
      }
      return this.ties_list.filter(
        (tie) => tie.game_date === this.selectedDay
      );
    },
    dayList() {
      const dayMap = new Map();
      for (const tie of this.ties_list) {
        if (!dayMap.has(tie.day_num)) {
          dayMap.set(tie.day_num, tie.game_date);
        }
      }
      const result = [];
      for (const [dayNum, gameDate] of dayMap.entries()) {
        result.push({ day_num: dayNum, game_date: gameDate });
      }
      return result.sort((a, b) => a.day_num - b.day_num);
    },
    modalMessage() {
      if (!this.selectedTie) return "";
      return `${this.selectedTie.tie_no} TIE(${this.selectedTie.game_date})를 CODER로 이동하시겠습니까?`;
    },
  },
  methods: {
    goBack() {
      this.$router.go(-1);
    },
    goHome() {
      this.$router.push("/");
    },
    goTie() {
      const coderStore = useCoderStore();
      coderStore.clearTieData();
      this.$router.push("/codertie");
    },
    selectTie(tie) {
      this.selectedTie = tie;
      this.showModal = true;
    },
    onConfirmSelectTie() {
      const coderStore = useCoderStore();
      coderStore.setTieData(
        this.selectedTie.tournament_uuid,
        this.selectedTie.tie_no,
        this.selectedTie.game_date
      );
      this.showModal = false;
      this.$router.push({ name: "coder" });
    },
    onOfficialSelectTie() {
      const coderStore = useCoderStore();
      coderStore.setTieData(
        this.selectedTie.tournament_uuid,
        this.selectedTie.tie_no,
        this.selectedTie.game_date
      );
      this.showModal = false;
      this.$router.push("/coderofficials");
    },
    onPlayerSelectTie() {
      const coderStore = useCoderStore();
      coderStore.setTieData(
        this.selectedTie.tournament_uuid,
        this.selectedTie.tie_no,
        this.selectedTie.game_date
      );
      this.showModal = false;
      this.$router.push("/codertie");
    },
    onCancelSelectTie() {
      this.showModal = false;
    },
  },
};
</script>

<style scoped>
/*
  1) .main-container:
     - 기본적으로 화면 전체에 걸쳐 펼쳐짐 (width: 100%, min-height: 100vh)
     - 1024px 이상에서 position: absolute 중앙 정렬
*/
.main-container {
  width: 100%;
  min-height: 100vh;
  background-color: #f8fafc; /* 아주 밝은 그레이-블루 톤 */
  display: flex;
  justify-content: center;
  align-items: center;
  padding: 2rem;
  box-sizing: border-box;
}

@media (min-width: 1024px) {
  .main-container {
    position: absolute;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);
  }
}

/*
  2) .tie-container:
     - 내부 카드 목록 및 헤더, 버튼을 담는 메인 컨테이너
*/
.tie-container {
  width: 100%;
  max-width: 600px;  /* 적절한 최대 너비 */
  background-color: #fff;
  border-radius: 8px;
  box-shadow: 0 4px 12px rgba(0,0,0,0.1);
  padding: 1.5rem;
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

/* ------- 헤더 ------- */
.tie-header {
  display: flex;
  flex-wrap: wrap;
  align-items: center;
  gap: 1rem;
  justify-content: space-between;
}

.tie-title {
  font-size: 1.5rem;
  font-weight: bold;
  margin: 0;
}

.tie-select-wrapper {
  position: relative;
}

/* 스크린 리더 전용 */
.sr-only {
  position: absolute;
  width: 1px;
  height: 1px;
  margin: -1px;
  overflow: hidden;
  clip-path: inset(100%);
  clip: rect(1px, 1px, 1px, 1px);
  border: 0;
  padding: 0;
}

/* 셀렉트박스 스타일 */
.tie-select {
  padding: 0.5rem 1rem;
  border-radius: 4px;
  font-size: 1rem;
  border: 1px solid #ddd;
  outline: none;
  transition: border 0.2s ease;
}
.tie-select:focus {
  border-color: #aaa;
}

/* ------- 리스트 & 카드 ------- */
.tie-list {
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
}

.tie-card {
  background-color: #ffffff;
  border: 1px solid #e5e7eb;
  border-radius: 6px;
  padding: 1rem;
  cursor: pointer;
  transition: box-shadow 0.2s ease, background-color 0.2s ease;
}

.tie-card:hover {
  box-shadow: 0 2px 8px rgba(0,0,0,0.1);
  background-color: #f9fafb;
}

.tie-card-title {
  margin: 0 0 0.25rem 0;
  font-size: 1.125rem;
  font-weight: 600;
}

.tie-score {
  margin: 0;
  color: #555;
}

/* ------- 버튼 푸터 ------- */
.tie-footer {
  display: flex;
  justify-content: flex-end;
  gap: 0.5rem;
}

/* 공통 버튼 스타일 */
.btn {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  border: none;
  border-radius: 4px;
  font-weight: 500;
  padding: 0.5rem 1rem;
  cursor: pointer;
  transition: background-color 0.2s ease, transform 0.2s ease;
  font-size: 0.9rem;
}

/* 공통 hover/active 스타일 */
.btn:hover {
  opacity: 0.9;
}
.btn:active {
  transform: scale(0.98);
}

/* 버튼 색상 변형 (Primary / Secondary / Tertiary) */
.btn-primary {
  background-color: #1D4ED8;
  color: #fff;
}
.btn-secondary {
  background-color: #6B7280; /* Grayer tone */
  color: #fff;
}
.btn-tertiary {
  background-color: #9CA3AF;
  color: #fff;
}

/* 반응형: 모바일에서 글자 등 살짝 줄이기 */
@media screen and (max-width: 480px) {
  .tie-title {
    font-size: 1.25rem;
  }
  .btn {
    font-size: 0.8rem;
  }
}
</style>
