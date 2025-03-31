import apiClient from '@/services/apiClient'

export default {
  // 게임 리스트를 가져오는 API (GET)
  getGameList(params = {}) {
    return apiClient.get('/api/gamelist', { params })
  },
  getMatchTypeList(params = {}) {
    return apiClient.get('/api/matchtype/list', { params })
  },
  getTiePage(params = {}) {
    return apiClient.get('/api/tiepage', { params })
  },
  postTiePage(params = {}) {
    return apiClient.post('/api/tiepage', params )
  },
  postTieModify(params = {}) {
    return apiClient.post('/api/tiemodify', params )
  }
}
