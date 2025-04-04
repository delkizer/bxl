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
  },
  putOfficials(params = {}) {
    return apiClient.put(`/api/officials`, params)
  },
  postOfficials(params = {}) {
    return apiClient.post(`/api/officials`, params)
  },
  deleteOfficials(params = {}) {
    return apiClient.delete('/api/officials', {
      data: params
    })
  },
}
