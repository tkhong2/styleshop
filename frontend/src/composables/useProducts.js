import { ref } from 'vue'
import { productService } from '@/services/productService.js'

export function useProducts() {
  const products = ref([])
  const loading = ref(false)
  const error = ref(null)

  async function fetchProducts(params = {}) {
    loading.value = true
    error.value = null
    try {
      const data = await productService.getAll(params)
      products.value = data
    } catch (e) {
      error.value = e.message
    } finally {
      loading.value = false
    }
  }

  return { products, loading, error, fetchProducts }
}

export function useProduct() {
  const product = ref(null)
  const loading = ref(false)
  const error = ref(null)

  async function fetchProduct(id) {
    loading.value = true
    error.value = null
    try {
      product.value = await productService.getById(id)
    } catch (e) {
      error.value = e.message
    } finally {
      loading.value = false
    }
  }

  return { product, loading, error, fetchProduct }
}
