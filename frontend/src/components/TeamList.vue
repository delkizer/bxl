<template>
  <div class="tour-list-container">
    <!-- 대회 배열을 순회해 옵션 생성 -->
    <select v-model="selectedTour" @change="filterTour">
      <option value=""></option>
      <option
        v-for="(tour, index) in tourList"
        :key="index"
        :value="tour.tournament_uuid"
      >
        {{tour.tournament_title}}
      </option>
    </select>

    <section class="tour-list">
      <div
        v-for="team in team_list"
        :key="team.team_code"
        class="tour-item"
        @click="selectTour( team )"
      >
        <!-- 상단에는 TIE 번호와 날짜 표시 -->
        <p> {{team.start_date}}
          {{ team.tournament_title }}
          {{team.nation_name}} {{team.city_name}} :
        </p>
        <p>
          {{team.team_name}} ( {{team.player_cnt}}명 )
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
import teamApi from '@/api/teamApi.js';
import tourApi from '@/api/tourApi.js';

export default {
  name: 'TeamList',
  data() {
    return {
      selectedTour: "",
      tourList: [],
      allTeams: [],    // 팀 전체 목록(백업용)
      team_list: [],   // 현재 화면에 보이는 팀 목록
     }
  },
  async mounted() {
    try {
      const response = await teamApi.getTeamList()
      this.team_list = response.data
      this.allTeams = response.data

      const response2 = await tourApi.getTourList()
      this.tourList = response2.data

    } catch ( error ) {
      console.error(error);
    }
  },
  computed: {
  },
  methods: {
    filterTour() {
      console.log(this.selectedTour)
      if (!this.selectedTour ) {
        this.team_list = this.allTeams;
      }

      if (this.selectedTour === '') {
        this.team_list = this.allTeams;
      }
      else {
        // 빈 값이 아닐 때 필터 로직
        this.team_list = this.allTeams.filter(
          team => team.tournament_uuid === this.selectedTour
        );
      }
    },
    goBack() {
      // 이전 화면으로
      this.$router.go(-1);
    },
    goHome() {
      this.$router.push('/')
    },
    goPage() {
      // 이전 화면으로
      this.$router.push('/teampage');
    },
    selectTour(team) {
      this.$router.push(`/teampage/${team.team_code}`);
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
