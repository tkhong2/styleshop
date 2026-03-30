import { defineStore } from 'pinia'
import { ref, computed } from 'vue'

export const useAuthStore = defineStore('auth', () => {
  const user = ref(JSON.parse(localStorage.getItem('user') || 'null'))
  const token = ref(localStorage.getItem('token') || null)
  const isLoggedIn = computed(() => !!token.value)

  // Mock auth - replace with real API calls when backend is ready
  async function login(email, password) {
    if (!email || !password) throw new Error('Vui lòng nhập đầy đủ thông tin')
    const mockUser = { id: 1, name: email.split('@')[0], email }
    const mockToken = 'mock-token-' + Date.now()
    token.value = mockToken
    user.value = mockUser
    localStorage.setItem('token', mockToken)
    localStorage.setItem('user', JSON.stringify(mockUser))
  }

  async function register(name, email, password) {
    if (!name || !email || !password) throw new Error('Vui lòng nhập đầy đủ thông tin')
    if (password.length < 6) throw new Error('Mật khẩu tối thiểu 6 ký tự')
    const mockUser = { id: Date.now(), name, email }
    const mockToken = 'mock-token-' + Date.now()
    token.value = mockToken
    user.value = mockUser
    localStorage.setItem('token', mockToken)
    localStorage.setItem('user', JSON.stringify(mockUser))
  }

  function loginWithGoogle(googleUser) {
    const mockToken = 'google-token-' + Date.now()
    token.value = mockToken
    user.value = { ...googleUser, id: Date.now() }
    localStorage.setItem('token', mockToken)
    localStorage.setItem('user', JSON.stringify(user.value))
  }

  function logout() {
    token.value = null
    user.value = null
    localStorage.removeItem('token')
    localStorage.removeItem('user')
  }

  return { user, token, isLoggedIn, login, register, loginWithGoogle, logout }
})
