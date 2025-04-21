<template>
  <div class="main-container">
    <!-- 헤더 섹션: 제목 등 -->
    <header class="header">
      <h1 class="title">Welcome to BXL</h1>
    </header>

    <!-- 버튼 그리드 -->
    <div class="buttons-grid">
      <button class="btn coder"
              @click="goToCoderPage"
              data-step="1"
              :data-guide="[
                '경기 진행용 Coder 화면으로 이동합니다.',
                'Match·Timer·Score를 실시간 제어합니다.'
              ].join('\n')"
      >
        <span class="btn-text">Coder's Page</span>
      </button>
      <button class="btn scorer" @click="goToScorerPage"
              data-step="2"
              :data-guide="[
                '실시간 입력기 화면으로 이동합니다.',
                ].join('\n')"
      >
        <span class="btn-text">Scorer's Page</span>
      </button>
      <button class="btn tour" @click="goToTourPage"
              data-step="3"
              :data-guide="[
                '대회(Tournament) 정보를 조회·편집합니다.'
                ].join('\n')"
      >
        <span class="btn-text">Tour's Page</span>
      </button>
      <button class="btn team" @click="goToGamePage"
              data-step="4"
              :data-guide="[
                '팀·선수·경기(Game) 데이터를 관리합니다.'
                ].join('\\n')"
      >
        <span class="btn-text">Team's Page</span>
      </button>
      <button class="btn official" @click="goToOfficialPage"
              data-step="5"
              :data-guide="[
                '심판(Official) 배정·조회 화면으로 이동합니다.'
                ].join('\\n')"
      >
        <span class="btn-text">Official's Page</span>
      </button>
    </div>
  </div>
</template>

<script>
export default {
  name: 'MainPage',
  methods: {
    goToCoderPage() {
      this.$router.push('/coderlist');
    },
    goToScorerPage() {
      this.$router.push('/coderList');
    },
    goToTourPage() {
      this.$router.push('/tourlist');
    },
    goToGamePage() {
      this.$router.push('/teamlist');
    },
    goToOfficialPage() {
      this.$router.push('/officiallist');
    }
  }
}
</script>

<style scoped>
/* -------------------- 레이아웃 & 컨테이너 -------------------- */
.main-container {
  /* 전체 레이아웃이 세로로 쌓이고, 아이템을 중앙 정렬 */
  display: flex;
  flex-direction: column;
  align-items: center;
  min-height: 100vh;  /* 내용이 많으면 자동으로 늘어남 */
  padding: 2rem 1rem;
  background-color: #f0f4f8; /* 부드러운 라이트 톤 배경 */
}

/* 헤더 섹션 */
.header {
  text-align: center;
  margin-bottom: 2rem;
}

.title {
  font-size: 2rem;
  font-weight: bold;
  color: #333;
}

/* 버튼 컨테이너 (Grid 레이아웃) */
.buttons-grid {
  display: grid;
  gap: 1.5rem;
  /* 화면 크기에 따라 버튼이 자동으로 재정렬 */
  grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
  width: 100%;
  max-width: 900px;
}

/* -------------------- 버튼 스타일 -------------------- */
.btn {
  display: flex;
  justify-content: center;
  align-items: center;
  padding: 1.5rem 1rem;
  border: none;
  border-radius: 12px; /* 부드러운 라운드 */
  font-size: 1.1rem;
  font-weight: bold;
  cursor: pointer;
  box-shadow: 0 3px 6px rgba(0, 0, 0, 0.16); /* 미세한 그림자 */
  transition: transform 0.2s ease, box-shadow 0.2s ease;
}

.btn:hover {
  /* 호버 시 약간의 확대 및 그림자 강조 */
  transform: translateY(-2px);
  box-shadow: 0 8px 16px rgba(0, 0, 0, 0.2);
}

.btn:active {
  /* 클릭 시 살짝 눌리는 느낌 */
  transform: translateY(0);
  box-shadow: 0 3px 6px rgba(0, 0, 0, 0.16);
}

/* 버튼 내부 텍스트 */
.btn-text {
  color: #fff; /* 각 배경색과 대비되는 흰색 */
}

/* -------------------- 각 버튼별 컬러 -------------------- */
/* 필요에 따라 동일 톤 & 채도의 다양한 컬러를 활용 */
.coder {
  background-color: #1D4ED8; /* 파랑: Tailwind Blue 700 예시 */
}
.scorer {
  background-color: #10B981; /* 초록: Tailwind Green 500 예시 */
}
.tour {
  background-color: #F59E0B; /* 옐로우/오렌지 계열 */
}
.team {
  background-color: #EF4444; /* 레드 */
}
.official {
  background-color: #6366F1; /* 인디고 계열 */
}

/* 반응형 폰트 크기 (선택적 적용) */
@media screen and (max-width: 480px) {
  .title {
    font-size: 1.5rem;
  }
  .btn {
    font-size: 1rem;
    padding: 1rem;
  }
}

@media (min-width: 1024px) {
  .main-container {
    position: absolute;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);
  }
}
</style>
