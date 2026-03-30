import { defineStore } from 'pinia'
import { ref, computed } from 'vue'

export const useWishlistStore = defineStore('wishlist', () => {
  const items = ref(JSON.parse(localStorage.getItem('wishlist') || '[]'))

  function persist() {
    localStorage.setItem('wishlist', JSON.stringify(items.value))
  }

  const isWishlisted = computed(() => (id) => items.value.some(p => p.id === id))

  function toggle(product) {
    const idx = items.value.findIndex(p => p.id === product.id)
    if (idx >= 0) items.value.splice(idx, 1)
    else items.value.push(product)
    persist()
    return idx < 0 // true = added
  }

  function remove(id) {
    items.value = items.value.filter(p => p.id !== id)
    persist()
  }

  return { items, isWishlisted, toggle, remove }
})
