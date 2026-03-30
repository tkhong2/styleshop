import axios from 'axios'

const api = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000/api',
  timeout: 10000,
})

// Request interceptor - attach token if exists
api.interceptors.request.use((config) => {
  const token = localStorage.getItem('token')
  if (token) config.headers.Authorization = `Bearer ${token}`
  return config
})

// Response interceptor - normalize errors
api.interceptors.response.use(
  (res) => res.data,
  (err) => {
    const message = err.response?.data?.detail || 'Đã có lỗi xảy ra'
    return Promise.reject(new Error(message))
  }
)

export default api
