import { ref } from 'vue'
import { productService } from '@/services/productService.js'

export function useSearch() {
  const query = ref('')
  const results = ref([])
  const loading = ref(false)
  let debounceTimer = null

  async function search(q) {
    query.value = q
    if (!q.trim()) { results.value = []; return }
    clearTimeout(debounceTimer)
    debounceTimer = setTimeout(async () => {
      loading.value = true
      try {
        const all = await productService.getAll()
        const lower = q.toLowerCase()
        results.value = all.filter(p =>
          p.name.toLowerCase().includes(lower) ||
          p.description.toLowerCase().includes(lower) ||
          p.category.toLowerCase().includes(lower)
        )
      } finally {
        loading.value = false
      }
    }, 300)
  }

  function clear() {
    query.value = ''
    results.value = []
  }

  return { query, results, loading, search, clear }
}
