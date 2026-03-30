import api from './api.js'

export const orderService = {
  create(payload) {
    return api.post('/orders', payload)
  },
  getMyOrders(userId = null) {
    const params = userId ? { user_id: userId } : {}
    return api.get('/orders/me', { params })
  },
  getPaymentStatus(orderId) {
    return api.get(`/orders/${orderId}/payment-status`)
  },
}
