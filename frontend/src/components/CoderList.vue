<template>
  <div class="tie-list-container">
    <!-- 상단 헤더/타이틀 -->
    <header class="tie-header">
      <h2>TIE 선택</h2>
      <!-- dayList 배열을 순회해 옵션 생성 -->
      <select v-model="selectedDay" @change="filterTies">
        <option value=""></option>
        <option
          v-for="(day, index) in dayList"
          :key="index"
          :value="day.day_num"
        >
          {{ day.day_num }}일차 ({{ day.game_date }})
        </option>
      </select>
    </header>

    <section class="tie-list">
      <!-- ties_list 배열을 순회 -->
      <div
        v-for="tie in ties_list"
        :key="tie.tie_no"
        class="tie-item"
        @click="selectTie(tie)"
      >
        <!-- 상단에는 TIE 번호와 날짜 표시 -->
        <h3>{{ tie.tie_no }} TIE ({{ tie.game_date}}) </h3>

        <!-- 팀명, 국가코드, 점수를 원하는 형태로 구성 -->
        <p>
          {{ tie.team1_name }}
          {{ tie.team1_point_sum }} : {{ tie.team2_point_sum }}
          {{ tie.team2_name }}
        </p>
      </div>
    </section>
    <!-- 하단/우측 액션 -->
    <footer class="tie-footer">
      <button @click="goTie">새로등록</button>
      <button @click="goBack">뒤로가기</button>
      <button @click="goHome">메인가기</button>
    </footer>
  </div>
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

</template>

<script>
import {useCoderStore} from "@/stores/coder.js";
import coderApi from '@/api/coderApi.js';
import CoderModal from "@/components/modal/CoderModal.vue";

export default {
  name: 'TieList',
  components: {
    CoderModal,
  },
  data() {
    return {
      // TIE 목록 예시
      ties_list: [],
      selectedDay: null,
      showModal: false,
      selectedTie: null,
    }
  },
  async mounted() {
    try {
      const response = await coderApi.getGameList({})
      this.ties_list = response.data;
    } catch ( error ) {
      console.error(error);
    }
  },
  computed: {
    filterTies() {
      // selectedDay가 null 이거나 ties_list가 비어있으면 그냥 전체 리턴
      if (!this.selectedDay) {
        return this.ties_list
      }
      // game_date가 selectedDay와 같은 tie만 필터
      return this.ties_list.filter(tie => tie.game_date === this.selectedDay)
    },
    dayList() {
      // { day_num -> game_date } 식으로 저장 (혹은 Set/Map을 사용)
      const dayMap = new Map();

      for (const tie of this.ties_list) {
        // 이미 있는 day_num은 덮어쓰지 않고, 없으면 추가
        if (!dayMap.has(tie.day_num)) {
          dayMap.set(tie.day_num, tie.game_date);
        }
      }
      // dayMap을 배열 [{ day_num, game_date }, ...] 로 변환
      // 그리고 day_num 기준 오름차순 정렬
      const result = [];
      for (const [dayNum, gameDate] of dayMap.entries()) {
        result.push({ day_num: dayNum, game_date: gameDate });
      }
      return result.sort((a, b) => a.day_num - b.day_num);
    },
    // 모달 메시지 구성 (선택된 tie가 있을 때만)
    modalMessage() {
      if (!this.selectedTie) return '';
      return `${this.selectedTie.tie_no} TIE(${this.selectedTie.game_date})를 CODER로 이동하시겠습니까?`;
    }
  },
  methods: {
    goBack() {
      // 이전 화면으로
      this.$router.go(-1);
    },
    goHome() {
      this.$router.push('/')
    },
    goTie() {
      const coderStore = useCoderStore();
      coderStore.clearTieData()
      this.$router.push('/codertie')
    },
    selectTie(tie) {
      // tie 항목 클릭 시 모달 표시
      this.selectedTie = tie;
      this.showModal = true;
    },
    // 모달 확인 버튼
    onConfirmSelectTie() {
      // CODER 로직
      const coderStore = useCoderStore();
      coderStore.setTieData(
        this.selectedTie.tournament_uuid, this.selectedTie.tie_no, this.selectedTie.game_date);
      this.showModal = false;
      this.$router.push({ name: 'coder' });
    },
    onOfficialSelectTie() {
      const coderStore = useCoderStore();
      coderStore.setTieData(
        this.selectedTie.tournament_uuid, this.selectedTie.tie_no, this.selectedTie.game_date,);
      this.showModal = false;
      this.$router.push('/coderofficials');

    },
    onPlayerSelectTie() {
      const coderStore = useCoderStore();
      coderStore.setTieData(
        this.selectedTie.tournament_uuid, this.selectedTie.tie_no, this.selectedTie.game_date,);
      this.showModal = false;
      this.$router.push('/codertie');
    },
    onCancelSelectTie() {
      this.showModal = false;
    }
  },
}
</script>

<style scoped>
.tie-list-container {
  position: absolute;
  width: 400px;
  margin: 0 auto;
  padding: 16px;
  top: 50%;      /* 수직 중앙 */
  left: 50%;     /* 수평 중앙 */
  transform: translate(-50%, -50%); /* 자기 크기의 절반만큼 이동해 완전 중앙 정렬 */
}

.tie-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 16px;
}

.tie-list {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.tie-item {
  border: 1px solid #ccc;
  border-radius: 6px;
  padding: 16px;
  cursor: pointer;
  transition: background 0.3s;
}

.tie-item:hover {
  background: #f2f2f2;
}

.tie-footer {
  margin-top: 24px;
  display: flex;
  gap: 12px;
  justify-content: flex-end;
}
</style>
