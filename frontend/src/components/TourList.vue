<template>
  <div class="tour-list-page">
    <div class="tour-list-container">
      <!-- 리스트 영역 -->
      <section class="tour-list">
        <div
          v-for="tour in tour_list"
          :key="tour.tournament_uuid"
          class="tour-item"
          @click="selectTour(tour)"
        >
          <h3>{{ tour.tournament_title }}</h3>
          <p>
            {{ tour.nation_name }}
            {{ tour.city_name }}
            {{ tour.start_date }} - {{ tour.end_date }}
          </p>
        </div>
      </section>

      <!-- 하단/우측 액션 -->
      <footer class="tour-footer">
        <button class="btn btn-primary" @click="goPage">새로등록</button>
        <button class="btn btn-secondary" @click="goBack">뒤로가기</button>
        <button class="btn btn-tertiary"  @click="goHome">메인가기</button>
      </footer>
    </div>
  </div>
</template>

<script>
import tourApi from "@/api/tourApi.js";

export default {
  name: "TourList",
  data() {
    return {
      tour_list: [],
    };
  },
  async mounted() {
    try {
      const response = await tourApi.getTourList({});
      this.tour_list = response.data;
    } catch (error) {
      console.error(error);
    }
  },
  methods: {
    goBack() {
      this.$router.go(-1);
    },
    goHome() {
      this.$router.push("/");
    },
    goPage() {
      this.$router.push("/tourpage");
    },
    selectTour(tour) {
      this.$router.push(`/tourpage/${tour.tournament_uuid}`);
    },
  },
};
</script>

<style scoped>
/* ------------------------------------
   1) 최상위 래퍼: 작은 화면(1024px 미만)에서는
      Flexbox로 화면 중앙 정렬,
      1024px 이상이면 position absolute 중앙
------------------------------------- */
.tour-list-page {
  width: 100%;
  min-height: 100vh;
  display: flex;            /* 작은 화면에선 flex 중앙 정렬 */
  justify-content: center;
  align-items: center;
  box-sizing: border-box;
  padding: 2rem;
}

/* 1024px 이상이면 absolute 중앙 정렬 */
@media (min-width: 1024px) {
  .tour-list-page {
    position: absolute;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);
  }
}

/* ------------------------------------
   2) 실제 카드 목록을 담는 컨테이너
   - 고정 폭(400px) or 원하는 크기
   - 스크롤, 배경색, 등등 원하는 스타일 추가 가능
------------------------------------- */
.tour-list-container {
  width: 400px;
  max-width: 90%;
  background-color: #fff;
  padding: 16px;
  border-radius: 8px;
  box-shadow: 0 4px 10px rgba(0,0,0,0.1);
  box-sizing: border-box;
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

/* ------------------------------------
   리스트 스타일
------------------------------------- */
.tour-list {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

/* 각 아이템(카드) */
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

/* ------------------------------------
   푸터(버튼 그룹)
------------------------------------- */
.tour-footer {
  display: flex;
  gap: 12px;
  justify-content: flex-end;
}

/* (선택) 버튼 스타일 정제 */
button {
  padding: 0.75rem 1.25rem;
  border: none;
  border-radius: 4px;
  background-color: #ddd;
  font-weight: bold;
  cursor: pointer;
  transition: background 0.2s ease;
}

button:hover {
  background-color: #ccc;
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

</style>
