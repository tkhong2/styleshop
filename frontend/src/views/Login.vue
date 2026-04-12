<template>
  <div class="auth-page">
    <RouterLink to="/" class="back-home">
      <i class="fas fa-arrow-left"></i> Về trang chủ
    </RouterLink>
    <div class="auth-card">
      <RouterLink to="/" class="auth-logo">STYLESHOP</RouterLink>

      <div class="auth-tabs">
        <button :class="['auth-tab', { active: mode === 'login' }]" @click="mode = 'login'">Đăng nhập</button>
        <button :class="['auth-tab', { active: mode === 'register' }]" @click="mode = 'register'">Đăng ký</button>
      </div>

      <!-- Google Login - chỉ hiện ở tab đăng nhập -->
      <template v-if="mode === 'login'">
        <button class="google-btn" @click="handleGoogleClick">
          <svg width="18" height="18" viewBox="0 0 24 24">
            <path fill="#4285F4" d="M22.56 12.25c0-.78-.07-1.53-.2-2.25H12v4.26h5.92c-.26 1.37-1.04 2.53-2.21 3.31v2.77h3.57c2.08-1.92 3.28-4.74 3.28-8.09z"/>
            <path fill="#34A853" d="M12 23c2.97 0 5.46-.98 7.28-2.66l-3.57-2.77c-.98.66-2.23 1.06-3.71 1.06-2.86 0-5.29-1.93-6.16-4.53H2.18v2.84C3.99 20.53 7.7 23 12 23z"/>
            <path fill="#FBBC05" d="M5.84 14.09c-.22-.66-.35-1.36-.35-2.09s.13-1.43.35-2.09V7.07H2.18C1.43 8.55 1 10.22 1 12s.43 3.45 1.18 4.93l2.85-2.22.81-.62z"/>
            <path fill="#EA4335" d="M12 5.38c1.62 0 3.06.56 4.21 1.64l3.15-3.15C17.45 2.09 14.97 1 12 1 7.7 1 3.99 3.47 2.18 7.07l3.66 2.84c.87-2.6 3.3-4.53 6.16-4.53z"/>
          </svg>
          Tiếp tục với Google
        </button>
        <div class="divider"><span>hoặc</span></div>
      </template>

      <!-- Login form -->
      <form v-if="mode === 'login'" @submit.prevent="handleLogin" class="auth-form">
        <div class="field">
          <label>Email</label>
          <input v-model="loginForm.email" type="email" placeholder="email@example.com" required />
        </div>
        <div class="field">
          <label>Mật khẩu</label>
          <div class="pass-wrap">
            <input v-model="loginForm.password" :type="showPass ? 'text' : 'password'" placeholder="••••••••" required />
            <button type="button" class="eye-btn" @click="showPass = !showPass">{{ showPass ? '🙈' : '👁️' }}</button>
          </div>
        </div>
        <p v-if="error" class="error-msg">{{ error }}</p>
        <button type="submit" class="btn btn-dark submit-btn" :disabled="loading">
          <span v-if="loading" class="spinner"></span>
          {{ loading ? 'Đang xử lý...' : 'Đăng nhập' }}
        </button>
      </form>

      <!-- Register form -->
      <form v-else @submit.prevent="handleRegister" class="auth-form">
        <div class="field">
          <label>Họ tên</label>
          <input v-model="regForm.name" type="text" placeholder="Nguyễn Văn A" required />
        </div>
        <div class="field">
          <label>Email</label>
          <input v-model="regForm.email" type="email" placeholder="email@example.com" required />
        </div>
        <div class="field">
          <label>Mật khẩu</label>
          <div class="pass-wrap">
            <input v-model="regForm.password" :type="showPass ? 'text' : 'password'" placeholder="Tối thiểu 6 ký tự" required minlength="6" />
            <button type="button" class="eye-btn" @click="showPass = !showPass">{{ showPass ? '🙈' : '👁️' }}</button>
          </div>
        </div>
        <div class="field">
          <label>Số điện thoại <span class="optional">(tuỳ chọn)</span></label>
          <input v-model="regForm.phone" type="tel" placeholder="0912 345 678" />
        </div>
        <p v-if="error" class="error-msg">{{ error }}</p>
        <button type="submit" class="btn btn-dark submit-btn" :disabled="loading">
          <span v-if="loading" class="spinner"></span>
          {{ loading ? 'Đang xử lý...' : 'Tạo tài khoản' }}
        </button>
      </form>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { GoogleLogin, decodeCredential } from 'vue3-google-login'
import { useAuthStore } from '@/stores/auth.js'
import { useToastStore } from '@/stores/toast.js'

const router = useRouter()
const auth = useAuthStore()
const toast = useToastStore()

const mode = ref('login')
const loading = ref(false)
const error = ref('')
const showPass = ref(false)
const loginForm = ref({ email: '', password: '' })
const regForm = ref({ name: '', email: '', password: '', phone: '' })

const GOOGLE_CLIENT_ID = '532996264964-8tfficegp4q2tdavi84c5119cl3jgid0.apps.googleusercontent.com'
const googleLoginRef = ref(null)

function handleGoogleClick() {
  // Dùng Google Identity Services popup trực tiếp
  if (window.google?.accounts?.oauth2) {
    const client = window.google.accounts.oauth2.initTokenClient({
      client_id: GOOGLE_CLIENT_ID,
      scope: 'openid email profile',
      callback: async (tokenResponse) => {
        if (tokenResponse.access_token) {
          try {
            const res = await fetch('https://www.googleapis.com/oauth2/v3/userinfo', {
              headers: { Authorization: `Bearer ${tokenResponse.access_token}` }
            })
            const userData = await res.json()
            auth.loginWithGoogle({ name: userData.name, email: userData.email, avatar: userData.picture, provider: 'google' })
            toast.success(`Chào mừng ${userData.name}!`)
            const redirect = router.currentRoute.value.query.redirect
            if (redirect) router.push(redirect)
            else if (ADMIN_EMAILS.includes(userData.email)) router.push('/admin')
            else router.push('/')
          } catch { toast.error('Đăng nhập Google thất bại') }
        }
      }
    })
    client.requestAccessToken()
  } else {
    // Fallback: load GIS script rồi thử lại
    const script = document.createElement('script')
    script.src = 'https://accounts.google.com/gsi/client'
    script.onload = () => handleGoogleClick()
    document.head.appendChild(script)
  }
}

// Called when Google returns credential
function handleGoogleCallback(response) {
  try {
    const userData = decodeCredential(response.credential)
    auth.loginWithGoogle({
      name: userData.name,
      email: userData.email,
      avatar: userData.picture,
      provider: 'google',
    })
    toast.success(`Chào mừng ${userData.name}!`)
    router.push(router.currentRoute.value.query.redirect || '/')
  } catch (e) {
    toast.error('Đăng nhập Google thất bại')
  }
}

const ADMIN_EMAILS = ['khachong2102005@gmail.com']

async function handleLogin() {
  loading.value = true; error.value = ''
  try {
    await auth.login(loginForm.value.email, loginForm.value.password)
    toast.success('Chào mừng trở lại!')
    const redirect = router.currentRoute.value.query.redirect
    if (redirect) router.push(redirect)
    else if (ADMIN_EMAILS.includes(loginForm.value.email)) router.push('/admin')
    else router.push('/')
  } catch (e) { error.value = e.message }
  finally { loading.value = false }
}

async function handleRegister() {
  loading.value = true; error.value = ''
  try {
    await auth.register(regForm.value.name, regForm.value.email, regForm.value.password)
    toast.success('Đăng ký thành công! Chào mừng bạn.')
    router.push('/')
  } catch (e) { error.value = e.message }
  finally { loading.value = false }
}
</script>

<style scoped>
.auth-page { min-height: 100vh; display: flex; align-items: center; justify-content: center; background: var(--gray); padding: 20px; }
.back-home { position: fixed; top: 20px; left: 20px; display: flex; align-items: center; gap: 8px; font-size: 13px; font-weight: 500; color: #555; background: #fff; padding: 8px 14px; border-radius: 8px; box-shadow: 0 2px 8px rgba(0,0,0,0.08); transition: all 0.2s; text-decoration: none; }
.back-home:hover { color: #1a1a1a; box-shadow: 0 4px 12px rgba(0,0,0,0.12); transform: translateX(-2px); }
.auth-card { background: #fff; border-radius: 16px; padding: 40px; width: 100%; max-width: 420px; box-shadow: 0 4px 32px rgba(0,0,0,0.08); }
.auth-logo { display: block; text-align: center; font-size: 22px; font-weight: 800; letter-spacing: 2px; margin-bottom: 28px; }

.auth-tabs { display: flex; border-bottom: 1px solid var(--gray2); margin-bottom: 24px; }
.auth-tab { flex: 1; padding: 12px; font-size: 14px; font-weight: 600; color: var(--gray3); border-bottom: 2px solid transparent; margin-bottom: -1px; transition: all 0.2s; background: none; }
.auth-tab.active { color: var(--black); border-bottom-color: var(--black); }

.google-btn { width: 100%; display: flex; align-items: center; justify-content: center; gap: 10px; padding: 12px; border: 1.5px solid #e2e8f0; border-radius: 8px; font-size: 14px; font-weight: 500; background: #fff; transition: border-color 0.2s, box-shadow 0.2s; cursor: pointer; color: #1a1a1a; }
.google-btn:hover { border-color: #aaa; box-shadow: 0 2px 8px rgba(0,0,0,0.08); }

.divider { display: flex; align-items: center; gap: 12px; margin: 20px 0; color: var(--gray3); font-size: 13px; }
.divider::before, .divider::after { content: ''; flex: 1; height: 1px; background: var(--gray2); }

.auth-form { display: flex; flex-direction: column; gap: 16px; }
.field { display: flex; flex-direction: column; gap: 6px; }
.field label { font-size: 13px; font-weight: 600; }
.optional { font-weight: 400; color: var(--gray3); }
.field input { padding: 11px 14px; border: 1.5px solid var(--gray2); border-radius: 8px; font-size: 14px; font-family: var(--font); transition: border-color 0.2s; }
.field input:focus { outline: none; border-color: var(--black); }
.pass-wrap { position: relative; }
.pass-wrap input { width: 100%; padding-right: 44px; }
.eye-btn { position: absolute; right: 12px; top: 50%; transform: translateY(-50%); background: none; font-size: 16px; }

.error-msg { font-size: 13px; color: var(--red); background: #fef2f2; padding: 8px 12px; border-radius: 6px; }
.submit-btn { width: 100%; padding: 13px; font-size: 14px; display: flex; align-items: center; justify-content: center; gap: 8px; margin-top: 4px; }
.submit-btn:disabled { opacity: 0.6; cursor: not-allowed; }
.spinner { width: 16px; height: 16px; border: 2px solid rgba(255,255,255,0.3); border-top-color: #fff; border-radius: 50%; animation: spin 0.7s linear infinite; }
@keyframes spin { to { transform: rotate(360deg); } }
.demo-hint { font-size: 12px; color: var(--gray3); text-align: center; background: #fffbeb; padding: 8px; border-radius: 6px; }
</style>
