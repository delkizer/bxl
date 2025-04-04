import { defineStore } from "pinia";

export const useCoderStore = defineStore('coderStore', {
  // state: 저장할 상태(데이터)
  state: () => ({
    tournament_uuid: null,
    tieNo: null,
    gameDate: null
  }),
  persist: {
    enabled: true,
    strategies: [
      {
        key:'coder-stroe',
        storage : localStorage
      }
    ]
  },
  // actions: state를 변경하거나 서버 통신 로직 등
  actions: {
    setTieData(tournament_uuid, tieNo, gameDate) {
      this.tournament_uuid = tournament_uuid;
      this.tieNo = tieNo
      this.gameDate = gameDate
    },
    clearTieData() {
      this.tournament_uuid = null;
      this.tieNo = null
      this.gameDate = null
    }
  },
  // getters: state 기반으로 파생 데이터를 만들거나, 복잡한 계산
  getters: {
    tieLabel: (state) => {
      if (!state.tieNo || !state.gameDate) return ''
      return `${state.tieNo}번 TIE (${state.gameDate})`
    }
  }
})

