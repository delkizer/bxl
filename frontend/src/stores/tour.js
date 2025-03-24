import { defineStore } from "pinia";

export const useTourStore = defineStore('tourStore', {
  // state: 저장할 상태(데이터)
  state: () => ({
    start_date: null,
    gameDate: null
  }),

  // actions: state를 변경하거나 서버 통신 로직 등
  actions: {
    setTieData(tieNo, gameDate) {
      this.tieNo = tieNo
      this.gameDate = gameDate
    },

    clearTieData() {
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
