import apiClient from '@/services/apiClient'

export default {
  getGameTies(params = {}) {
    return apiClient.get(`/api/gameties`, {params})
  },
  getGmaeuuids(params = {}) {
    return apiClient.get(`/api/gameuuids/`, {params})
  },
  getOfficials(params = {}) {
    return apiClient.get(`/api/officials/`, {params})
  }
}
