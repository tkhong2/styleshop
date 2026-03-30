import { defineStore } from 'pinia'
import { ref, computed } from 'vue'

export const useCartStore = defineStore('cart', () => {
  const items = ref(JSON.parse(localStorage.getItem('cart') || '[]'))
  const isOpen = ref(false)

  function persist() {
    localStorage.setItem('cart', JSON.stringify(items.value))
  }

  const totalItems = computed(() => items.value.reduce((s, i) => s + i.quantity, 0))
  const totalPrice = computed(() => items.value.reduce((s, i) => s + i.price * i.quantity, 0))

  function addItem(product, size, color) {
    const existing = items.value.find(i => i.id === product.id && i.size === size && i.color === color)
    if (existing) existing.quantity++
    else items.value.push({ ...product, size, color, quantity: 1 })
    persist()
    isOpen.value = true
  }

  function removeItem(id, size, color) {
    items.value = items.value.filter(i => !(i.id === id && i.size === size && i.color === color))
    persist()
  }

  function updateQuantity(id, size, color, quantity) {
    const item = items.value.find(i => i.id === id && i.size === size && i.color === color)
    if (!item) return
    if (quantity <= 0) removeItem(id, size, color)
    else { item.quantity = quantity; persist() }
  }

  function clearCart() {
    items.value = []
    persist()
  }

  return { items, isOpen, totalItems, totalPrice, addItem, removeItem, updateQuantity, clearCart }
})
