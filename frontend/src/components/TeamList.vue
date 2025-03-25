<template>
  <div class="tour-list-container">
    <section class="tour-list">
      <div
        v-for="tour in tour_list"
        :key="tour.tournament_uuid"
        class="tour-item"
        @click="selectTour( tour )"
      >
        <!-- 상단에는 TIE 번호와 날짜 표시 -->
        <h3>{{ tour.tournament_title }} </h3>
        <!-- 팀명, 국가코드, 점수를 원하는 형태로 구성 -->
        <p>
          {{tour.nation_name}} {{tour.city_name}} {{tour.start_date}} - {{tour.end_date}}
        </p>
      </div>
    </section>
    <!-- 하단/우측 액션 -->
    <footer class="tour-footer">
      <button @click="goPage">새로등록</button>
      <button @click="goBack">뒤로가기</button>
      <button @click="goHome">메인가기</button>
    </footer>
  </div>
</template>

<script>
import tourApi from '@/api/tourApi.js';

export default {
  name: 'TourList',
  data() {
    return {
      // TIE 목록 예시
      tour_list: [],
     }
  },
  async mounted() {
    try {
      const response = await tourApi.getTourList({})
      this.tour_list = response.data
    } catch ( error ) {
      console.error(error);
    }
  },
  computed: {
  },
  methods: {
    goBack() {
      // 이전 화면으로
      this.$router.go(-1);
    },
    goHome() {
      this.$router.push('/')
    },
    goPage() {
      // 이전 화면으로
      this.$router.push('/tourpage');
    },
    selectTour(tour) {
      this.$router.push(`/tourpage/${tour.tournament_uuid}`);
    },
  },
}
</script>

<style scoped>
.tour-list-container {
  position: absolute;
  width: 400px;
  margin: 0 auto;
  padding: 16px;
  top: 50%;      /* 수직 중앙 */
  left: 50%;     /* 수평 중앙 */
  transform: translate(-50%, -50%); /* 자기 크기의 절반만큼 이동해 완전 중앙 정렬 */
}

.tour-list {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.tour-item {
  border: 1px solid #ccc;
  border-radius: 6px;
  padding: 16px;
  cursor: pointer;
  transition: background 0.3s;
}

.tour-item:hover {
  background: #f2f2f2;
}

.tour-footer {
  margin-top: 24px;
  display: flex;
  gap: 12px;
  justify-content: flex-end;
}
</style>
