import api from './api.js'

export const productService = {
  getAll(params = {}) {
    return api.get('/products', { params })
  },
  getById(id) {
    return api.get(`/products/${id}`)
  },
  getCategories() {
    return api.get('/categories')
  },
}
