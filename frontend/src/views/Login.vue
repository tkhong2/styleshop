<template>
  <div class="auth-page">
    <div class="auth-card">
      <RouterLink to="/" class="auth-logo">STYLESHOP</RouterLink>

      <div class="auth-tabs">
        <button :class="['auth-tab', { active: mode === 'login' }]" @click="mode = 'login'">Đăng nhập</button>
        <button :class="['auth-tab', { active: mode === 'register' }]" @click="mode = 'register'">Đăng ký</button>
      </div>

      <!-- Google Login - chỉ hiện ở tab đăng nhập -->
      <template v-if="mode === 'login'">
        <GoogleLogin :callback="handleGoogleCallback" :buttonConfig="googleBtnConfig" />
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

const googleBtnConfig = {
  theme: 'outline',
  size: 'large',
  width: 340,
  text: 'continue_with',
  shape: 'rectangular',
  logo_alignment: 'left',
  locale: 'vi',
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

async function handleLogin() {
  loading.value = true; error.value = ''
  try {
    await auth.login(loginForm.value.email, loginForm.value.password)
    toast.success('Chào mừng trở lại!')
    router.push(router.currentRoute.value.query.redirect || '/')
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
.auth-card { background: #fff; border-radius: 16px; padding: 40px; width: 100%; max-width: 420px; box-shadow: 0 4px 32px rgba(0,0,0,0.08); }
.auth-logo { display: block; text-align: center; font-size: 22px; font-weight: 800; letter-spacing: 2px; margin-bottom: 28px; }

.auth-tabs { display: flex; border-bottom: 1px solid var(--gray2); margin-bottom: 24px; }
.auth-tab { flex: 1; padding: 12px; font-size: 14px; font-weight: 600; color: var(--gray3); border-bottom: 2px solid transparent; margin-bottom: -1px; transition: all 0.2s; background: none; }
.auth-tab.active { color: var(--black); border-bottom-color: var(--black); }

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
