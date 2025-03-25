import apiClient from '@/services/apiClient'

export default {
  postTeamPage(params = {}) {
    return apiClient.post('/api/teampage', params)
  },
  getTeamList(params = {}) {
    return apiClient.get('/api/teamlist', {params})
  },
  getPlayerList(teamCode) {
    return apiClient.get(`/api/teams/${teamCode}/players`);
  }
}
