import { defineStore } from 'pinia'
import { ref } from 'vue'

export const useToastStore = defineStore('toast', () => {
  const toasts = ref([])
  let id = 0

  function add(message, type = 'success', duration = 3000) {
    const toast = { id: ++id, message, type }
    toasts.value.push(toast)
    setTimeout(() => remove(toast.id), duration)
  }

  function remove(toastId) {
    toasts.value = toasts.value.filter(t => t.id !== toastId)
  }

  const success = (msg) => add(msg, 'success')
  const error = (msg) => add(msg, 'error')
  const info = (msg) => add(msg, 'info')

  return { toasts, add, remove, success, error, info }
})
