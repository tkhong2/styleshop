import { createApp } from 'vue'
import { createPinia } from 'pinia'
import vue3GoogleLogin from 'vue3-google-login'
import App from '@/App.vue'
import '@/assets/style.css'
import '@fortawesome/fontawesome-free/css/all.min.css'

// Wake up Render backend nếu đang sleep
fetch(import.meta.env.VITE_API_BASE_URL?.replace('/api', '') + '/').catch(() => {})

const app = createApp(App)
const pinia = createPinia()
app.use(pinia) // Pinia TRƯỚC router để guard có thể dùng store

import('@/router/index.js').then(({ default: router }) => {
  app.use(router)
  app.use(vue3GoogleLogin, {
    clientId: '532996264964-8tfficegp4q2tdavi84c5119cl3jgid0.apps.googleusercontent.com'
  })
  app.mount('#app')
})
