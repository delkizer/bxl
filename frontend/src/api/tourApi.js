import apiClient from '@/services/apiClient'

export default {
  // 국가 코드를 가져오는 API (GET)
  getNationList(params = {}) {
    return apiClient.get('/api/nationlist',  params )
  },
  postTourPage(params = {}) {
    return apiClient.post('/api/tourpage', params)
  },
  getTourList(params = {}) {
    return apiClient.get('/api/tourlist', {params})
  }

}
