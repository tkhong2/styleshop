<template>
  <Transition name="fade">
    <div v-if="show" class="promo-overlay" @click.self="close">
      <div class="promo-modal">
        <button class="promo-close" @click="close"><i class="fas fa-times"></i></button>
        <div class="promo-content">
          <div class="promo-left">
            <img src="https://images.unsplash.com/photo-1469334031218-e382a71b716b?w=800&q=90" alt="Promo" />
          </div>
          <div class="promo-right">
            <p class="promo-sub">Ưu đãi đặc biệt</p>
            <h2>Giảm <span>15%</span><br/>đơn hàng đầu tiên</h2>
            <p class="promo-desc">Đăng ký nhận thông báo để nhận mã giảm giá độc quyền và cập nhật bộ sưu tập mới nhất.</p>
            <div class="promo-code">
              <span>Mã: </span>
              <strong class="code" @click="copyCode">NEWUSER <i class="fas fa-copy"></i></strong>
            </div>
            <RouterLink to="/products" class="btn btn-dark promo-btn" @click="close">
              Mua sắm ngay
            </RouterLink>
            <button class="promo-skip" @click="close">Không, cảm ơn</button>
          </div>
        </div>
      </div>
    </div>
  </Transition>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useToastStore } from '@/stores/toast.js'

const show = ref(false)
const toast = useToastStore()

onMounted(() => {
  // Chỉ hiện 1 lần mỗi session
  if (!sessionStorage.getItem('promo_shown')) {
    setTimeout(() => { show.value = true }, 3000)
  }
})

function close() {
  show.value = false
  sessionStorage.setItem('promo_shown', '1')
}

function copyCode() {
  navigator.clipboard.writeText('NEWUSER')
  toast.success('Đã copy mã NEWUSER!')
}
</script>

<style scoped>
.promo-overlay { position: fixed; inset: 0; background: rgba(0,0,0,0.6); z-index: 600; display: flex; align-items: center; justify-content: center; padding: 16px; }
.promo-modal { background: #fff; border-radius: 20px; width: 100%; max-width: 1000px; overflow: hidden; position: relative; box-shadow: 0 24px 60px rgba(0,0,0,0.3); }
.promo-close { position: absolute; top: 16px; right: 16px; background: rgba(0,0,0,0.25); color: #fff; border-radius: 50%; width: 40px; height: 40px; display: flex; align-items: center; justify-content: center; z-index: 1; font-size: 16px; }
.promo-close:hover { background: rgba(0,0,0,0.45); }
.promo-content { display: grid; grid-template-columns: 1.1fr 1fr; }
.promo-left img { width: 100%; height: 100%; object-fit: cover; object-position: center top; min-height: 560px; }
.promo-right { padding: 56px 52px; display: flex; flex-direction: column; gap: 20px; justify-content: center; }
.promo-sub { font-size: 13px; font-weight: 700; letter-spacing: 2px; text-transform: uppercase; color: #3b82f6; }
.promo-right h2 { font-size: 42px; font-weight: 800; line-height: 1.15; }
.promo-right h2 span { color: #e53e3e; }
.promo-desc { font-size: 15px; color: #666; line-height: 1.7; }
.promo-code { display: flex; align-items: center; gap: 10px; font-size: 15px; }
.code { background: #f1f5f9; padding: 10px 20px; border-radius: 8px; cursor: pointer; letter-spacing: 2px; font-size: 16px; font-weight: 700; }
.code:hover { background: #e2e8f0; }
.promo-btn { display: block; text-align: center; padding: 16px; font-size: 16px; }
.promo-skip { font-size: 13px; color: #aaa; text-align: center; }
.promo-skip:hover { color: #555; }
.fade-enter-active, .fade-leave-active { transition: opacity 0.3s; }
.fade-enter-from, .fade-leave-to { opacity: 0; }
@media (max-width: 640px) { .promo-content { grid-template-columns: 1fr; } .promo-left { display: none; } .promo-right { padding: 36px 28px; } }
</style>
