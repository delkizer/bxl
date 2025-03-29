import apiClient from '@/services/apiClient'

export default {
  // 게임 리스트를 가져오는 API (GET)
  getGameList(params = {}) {
    return apiClient.get('/api/gamelist', { params })
  },
  getMatchTypeList(params = {}) {
    return apiClient.get('/api/matchtype/list', { params })
  }

}
