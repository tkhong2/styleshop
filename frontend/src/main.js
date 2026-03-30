import { createApp } from 'vue'
import { createPinia } from 'pinia'
import vue3GoogleLogin from 'vue3-google-login'
import router from '@/router/index.js'
import App from '@/App.vue'
import '@/assets/style.css'
import '@fortawesome/fontawesome-free/css/all.min.css'

const app = createApp(App)
app.use(createPinia())
app.use(router)
app.use(vue3GoogleLogin, {
  clientId: '532996264964-8tfficegp4q2tdavi84c5119cl3jgid0.apps.googleusercontent.com'
})
app.mount('#app')
