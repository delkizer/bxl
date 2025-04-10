<template>
  <!-- 바탕(배경) -->
  <div class="team-list-page">
    <!-- 실제 내용 컨테이너(카드) -->
    <div class="team-list-container">
      <!-- 상단 셀렉트 박스 -->
      <select v-model="selectedTour" @change="filterTour" class="tour-select">
        <option value="">-- 모든 대회 보기 --</option>
        <option
          v-for="(tour, index) in tourList"
          :key="index"
          :value="tour.tournament_uuid"
        >
          {{ tour.tournament_title }}
        </option>
      </select>

      <!-- 리스트 영역 -->
      <section class="team-list">
        <div
          v-for="team in team_list"
          :key="team.team_code"
          class="team-item"
          @click="selectTour(team)"
        >
          <p>
            {{ team.start_date }}
            {{ team.tournament_title }}
            {{ team.nation_name }} {{ team.city_name }} :
          </p>
          <p>{{ team.team_name }} ( {{ team.player_cnt }}명 )</p>
        </div>
      </section>

      <!-- 하단/우측 액션 -->
      <footer class="team-footer">
        <button class="btn btn-save" @click="goPage">새로등록</button>
        <button class="btn btn-cancel" @click="goBack">뒤로가기</button>
        <button class="btn btn-tertiary" @click="goHome">메인가기</button>
      </footer>
    </div>
  </div>
</template>

<script>
import teamApi from "@/api/teamApi.js";
import tourApi from "@/api/tourApi.js";

export default {
  name: "TeamList",
  data() {
    return {
      selectedTour: "",
      tourList: [],
      allTeams: [], // 전체 팀 목록(백업)
      team_list: [], // 현재 화면에 보여질 팀 목록
    };
  },
  async mounted() {
    try {
      // 팀 목록
      const response = await teamApi.getTeamList();
      this.team_list = response.data;
      this.allTeams = response.data;

      // 대회 목록
      const response2 = await tourApi.getTourList();
      this.tourList = response2.data;
    } catch (error) {
      // 예외 케이스 처리
      if (
        error.response &&
        error.response.status === 404 &&
        error.response.data.detail === "User not found"
      ) {
        // 404 + "User not found" 시 별도 처리 없음
        return;
      }
      console.error(error);
    }
  },
  methods: {
    filterTour() {
      if (!this.selectedTour) {
        // 선택 해제 → 전체 목록
        this.team_list = this.allTeams;
      } else {
        // 해당 tournament_uuid만 필터
        this.team_list = this.allTeams.filter(
          (team) => team.tournament_uuid === this.selectedTour
        );
      }
    },
    goBack() {
      this.$router.go(-1);
    },
    goHome() {
      this.$router.push("/");
    },
    goPage() {
      this.$router.push("/teampage");
    },
    selectTour(team) {
      // team_code가 URI 파라미터
      this.$router.push(`/teampage/${team.team_code}`);
    },
  },
};
</script>

<style scoped>
/*
  1) team-list-page:
     - 작은 화면(1024px 미만): flex 중앙 정렬
     - 1024px 이상: absolute 중앙
     - 밝은 배경색
*/
.team-list-page {
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
  .team-list-page {
    position: absolute;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);
  }
}

/*
  2) team-list-container:
     - 카드형 컨테이너
     - 최대 폭 400px (필요 시 조정)
*/
.team-list-container {
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

/* 상단 select */
.tour-select {
  padding: 0.5rem 1rem;
  border: 1px solid #ddd;
  border-radius: 4px;
  font-weight: bold;
}

/* 3) 팀 리스트(카드) */
.team-list {
  display: flex;
  flex-direction: column;
  gap: 12px;
}
.team-item {
  border: 1px solid #ccc;
  border-radius: 6px;
  padding: 16px;
  cursor: pointer;
  transition: background 0.3s;
}
.team-item:hover {
  background: #f2f2f2;
}

/* 4) 하단 버튼 영역 */
.team-footer {
  display: flex;
  gap: 12px;
  justify-content: flex-end;
}

/* ----------------------------
   5) 버튼 색상 (저장/종료/기타)
----------------------------- */
.btn {
  padding: 0.75rem 1.25rem;
  border: none;
  border-radius: 4px;
  font-weight: bold;
  cursor: pointer;
  transition: background-color 0.2s ease, transform 0.2s ease;
}

/* “새로등록” → 녹색 */
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

/* “뒤로가기” → 빨강 */
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

/* “메인가기” → 회색 */
.btn-tertiary {
  background-color: #9CA3AF;
  color: #fff;
}
.btn-tertiary:hover {
  opacity: 0.9;
}
.btn-tertiary:active {
  transform: scale(0.98);
}
</style>
