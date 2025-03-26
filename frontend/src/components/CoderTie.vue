<template>
  <div class="game-info-page">
    <div class="form-container">
      <!-- 대회정보 -->
      <div class="form-row">
        <div class="form-group left">
          <label>대회정보</label>
        </div>
        <div class="form-group middle">
          <select class="form-control" v-model="selectedTournament">
            <option v-for="tour in tournamentList" :key="tour" :value="tour">
              {{ tour }}
            </option>
          </select>
        </div>
        <div class="form-group middle">
          <input type="date" class="form-control" v-model="matchDate" />
        </div>
        <div class="form-group middle">
          <select class="form-control" v-model="selectedTEI">
            <option v-for="tei in teiList" :key="tei" :value="tei">
              {{ tei }}
            </option>
          </select>
        </div>
      </div>
      <!-- MATCH 선택 (25개 Select) -->
      <div class="form-row">
        <div class="form-group left">
          <select class="form-control" v-model="selectedTeam1">
            <option v-for="team in teamList" :key="team" :value="team">
              {{ team }}
            </option>
          </select>
        </div>
        <div class="form-group middle match-wrapper">
          <!-- 5행 × 5열 구조 -->
          <div
            v-for="(row, rowIndex) in matchRows"
            :key="rowIndex"
            class="match-row"
          >
            <!-- 각 행에 5개의 Select -->
            <select
              class="form-control"
              v-for="(val, colIndex) in row"
              :key="colIndex"
              v-model="selectedMatchValues[rowIndex][colIndex]"
            >
              <!-- 일단 예시로 playerList 재활용 -->
              <option v-for="player in playerList" :key="player" :value="player">
                {{ player }}
              </option>
            </select>
          </div>
        </div>
      </div>
      <!-- MATCH 선택 (25개 Select) -->
      <div class="form-row">
        <div class="form-group left">
          <select class="form-control" v-model="selectedTeam1">
            <option v-for="team in teamList" :key="team" :value="team">
              {{ team }}
            </option>
          </select>
        </div>
        <div class="form-group middle match-wrapper">
          <!-- 5행 × 5열 구조 -->
          <div
            v-for="(row, rowIndex) in matchRows"
            :key="rowIndex"
            class="match-row"
          >
            <!-- 각 행에 5개의 Select -->
            <select
              class="form-control"
              v-for="(val, colIndex) in row"
              :key="colIndex"
              v-model="selectedMatchValues[rowIndex][colIndex]"
            >
              <!-- 일단 예시로 playerList 재활용 -->
              <option v-for="player in playerList" :key="player" :value="player">
                {{ player }}
              </option>
            </select>
          </div>
        </div>
      </div>

      <!-- 버튼 -->
      <div class="button-container">
        <button class="btn btn-save" @click="handleSave">저장</button>
        <button class="btn btn-cancel" @click="handleCancel">종료</button>
      </div>

    </div>
  </div>
</template>

<script>
export default {
  name: "GameInfoPage",
  data() {
    return {
      // 예시: 대회목록, TEI목록, 팀목록
      tournamentList: ["25 BXL 배드민턴 대회", "다른 대회명", "또 다른 대회명"],
      selectedTournament: "25 BXL 배드민턴 대회",

      matchDate: "",
      teiList: ["TEI 1", "TEI 2", "TEI 3", "TEI 4", "TEI 5"
        , "TEI 6", "TEI 7", "TEI 8", "TEI 9"],
      selectedTEI: "TEI 1",

      teamList: ["TEAM1 선택", "TEAM2 선택", "Rockets", "Tigers", "Lions"],
      selectedTeam1: "TEAM1 선택",

      // 매치 25개 셀렉트에 들어갈 옵션(예시로 선수 목록)
      playerList: ["이용석", "김예지", "신수인", "이사야", "선수선택", "남자단식", "여자단식", "여자복식", "MATCH4", "3X3", "1", "2", "3", "승점"],

      // 화면에 보이는 5×5 셀렉트의 초기값 구조
      matchRows: [
        // row 1 (남자단식, 이용석, 선수선택, 선수선택, 1)
        ["남자단식", "이용석", "선수선택", "선수선택", "1"],
        // row 2 (여자단식, 김예지, 선수선택, 선수선택, 2)
        ["여자단식", "김예지", "선수선택", "선수선택", "2"],
        // row 3 (여자복식, 신수인, 이사야, 선수선택, 승점)
        ["여자복식", "신수인", "이사야", "선수선택", "승점"],
        // row 4 (MATCH4, 선수선택, 선수선택, 선수선택, 승점)
        ["MATCH4", "선수선택", "선수선택", "선수선택", "승점"],
        // row 5 (3X3, 선수선택, 선수선택, 선수선택, 3)
        ["3X3", "선수선택", "선수선택", "선수선택", "3"]
      ],

      // v-model로 제어할 5×5 매치 선택값
      // (초기에는 matchRows와 동일하게 세팅)
      selectedMatchValues: [
        ["남자단식", "이용석", "선수선택", "선수선택", "1"],
        ["여자단식", "김예지", "선수선택", "선수선택", "2"],
        ["여자복식", "신수인", "이사야", "선수선택", "승점"],
        ["MATCH4", "선수선택", "선수선택", "선수선택", "승점"],
        ["3X3", "선수선택", "선수선택", "선수선택", "3"]
      ]
    };
  },
  methods: {
    handleSave() {
      // 나중에 실제 저장 로직 추가
      alert("저장 버튼 클릭\n\n" + JSON.stringify(this.selectedMatchValues, null, 2));
    },
    handleCancel() {
      // 나중에 실제 종료/취소 로직 추가
      alert("종료 버튼 클릭");
    }
  }
};
</script>

<style scoped>
/* ------------------------------
   전체 배경 및 레이아웃
------------------------------ */
.game-info-page {
  width: 800px;
  margin: 0 auto; /* 가로 중앙정렬 */
  background-color: #4b7cb6;
  padding: 20px;
  min-height: 100vh;
  box-sizing: border-box;

  /* 자식 배치용 flex (필요하다면) */
  display: flex;
  flex-direction: column;
  align-items: center; /* 이건 내부 콘텐츠를 가운데로 모으는 옵션 */
  justify-content: start; /* start로 해서 세로 상단부터 배치 */

  position: absolute;
  top: 50%;
  left: 50%;

  /* 자기 자신의 너비·높이의 절반만큼 좌상단으로 이동하여 정중앙 배치 */
  transform: translate(-50%, -50%);

}

.form-container {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

/* ------------------------------
   각 행(라벨+필드) 레이아웃
------------------------------ */
.form-row {
  display: flex;
  align-items: flex-start;
  gap: 10px;
}

/* 왼쪽 라벨 영역 */
.form-group.left {
  width: 100px;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

/* ------------------------------
   입력 요소에 대한 스타일
------------------------------ */
.form-group {
  display: flex;
  flex-direction: column;
  background-color: white;
  padding: 10px;
  border-radius: 5px;
  box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
}

.form-group label {
  font-weight: bold;
  font-size: 16px;
  text-align: center;
  margin-bottom: 5px;
}

.form-control {
  padding: 8px 12px;
  border: 1px solid #ddd;
  border-radius: 4px;
  font-size: 16px;
}

/* 셀렉트 기본 화살표 커스텀 */
select.form-control {
  appearance: none;
  background-image: url("data:image/svg+xml;charset=UTF-8,%3csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24' fill='none' stroke='%23333' stroke-width='2' stroke-linecap='round' stroke-linejoin='round'%3e%3cpolyline points='6 9 12 15 18 9'%3e%3c/polyline%3e%3c/svg%3e");
  background-repeat: no-repeat;
  background-position: right 8px center;
  background-size: 16px;
  padding-right: 30px;
}

/* ------------------------------
   매치 선택(25개) 래퍼
------------------------------ */
.match-wrapper {
  display: flex;
  flex-direction: column; /* 세로로 행 나열 */
  gap: 10px;
}

/* 각 행 안에 있는 5개 셀렉트들 */
.match-row {
  display: flex;
  flex-direction: row;
  gap: 10px;
}

/* ------------------------------
   버튼 영역
------------------------------ */
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
  background-color: #70c16b;
  color: #fff;
}

.btn-cancel {
  background-color: #f56b6b;
  color: #fff;
}

/* ------------------------------
   반응형 처리
------------------------------ */
@media (max-width: 960px) {
  .form-row {
    flex-direction: column;
  }
  .left {
    width: 100%;
    justify-content: flex-start;
  }
}
</style>
