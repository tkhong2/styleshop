import { defineStore } from 'pinia'
import { ref } from 'vue'

export const useHistoryStore = defineStore('history', () => {
  const items = ref(JSON.parse(localStorage.getItem('viewed') || '[]'))

  function add(product) {
    items.value = [product, ...items.value.filter(p => p.id !== product.id)].slice(0, 10)
    localStorage.setItem('viewed', JSON.stringify(items.value))
  }

  return { items, add }
})
