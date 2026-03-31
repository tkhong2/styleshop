import api from './api.js'

export const reviewService = {
  getByProduct(productId) {
    return api.get(`/reviews/${productId}`)
  },
  create(payload) {
    return api.post('/reviews', payload)
  },
}
