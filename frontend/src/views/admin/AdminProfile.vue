<template>
  <div class="profile-page">
    <div class="profile-grid">
      <!-- Left: Info card -->
      <div class="info-card">
        <div class="avatar-section">
          <div class="big-avatar">{{ auth.user?.name?.[0]?.toUpperCase() || 'A' }}</div>
          <h2>{{ auth.user?.name }}</h2>
          <span class="role-badge"><i class="fas fa-shield-alt"></i> Quản trị viên</span>
          <p class="email">{{ auth.user?.email }}</p>
        </div>
        <div class="stats-row">
          <div class="stat-item">
            <p class="stat-val">{{ totalOrders }}</p>
            <p class="stat-label">Đơn hàng</p>
          </div>
          <div class="stat-item">
            <p class="stat-val">{{ formatPrice(totalRevenue) }}</p>
            <p class="stat-label">Doanh thu</p>
          </div>
          <div class="stat-item">
            <p class="stat-val">{{ paidOrders }}</p>
            <p class="stat-label">Đã thanh toán</p>
          </div>
        </div>
      </div>

      <!-- Right: Settings -->
      <div class="settings-col">
        <!-- Account info -->
        <div class="card">
          <h3><i class="fas fa-user-edit"></i> Thông tin tài khoản</h3>
          <form @submit.prevent="saveInfo" class="form">
            <div class="form-row">
              <div class="field">
                <label>Họ tên</label>
                <input v-model="form.name" type="text" />
              </div>
              <div class="field">
                <label>Email</label>
                <input v-model="form.email" type="email" disabled />
              </div>
            </div>
            <div class="form-row">
              <div class="field">
                <label>Số điện thoại</label>
                <input v-model="form.phone" type="tel" placeholder="0912 345 678" />
              </div>
              <div class="field">
                <label>Chức vụ</label>
                <input value="Quản trị viên" disabled />
              </div>
            </div>
            <button type="submit" class="btn-save">
              <i class="fas fa-save"></i> Lưu thay đổi
            </button>
          </form>
        </div>

        <!-- Change password -->
        <div class="card">
          <h3><i class="fas fa-lock"></i> Đổi mật khẩu</h3>
          <form @submit.prevent="changePassword" class="form">
            <div class="field">
              <label>Mật khẩu hiện tại</label>
              <input v-model="pwForm.current" type="password" placeholder="••••••••" />
            </div>
            <div class="form-row">
              <div class="field">
                <label>Mật khẩu mới</label>
                <input v-model="pwForm.newPw" type="password" placeholder="Tối thiểu 6 ký tự" minlength="6" />
              </div>
              <div class="field">
                <label>Xác nhận mật khẩu</label>
                <input v-model="pwForm.confirm" type="password" placeholder="Nhập lại mật khẩu" />
              </div>
            </div>
            <button type="submit" class="btn-save">
              <i class="fas fa-key"></i> Đổi mật khẩu
            </button>
          </form>
        </div>

        <!-- Activity log -->
        <div class="card">
          <h3><i class="fas fa-history"></i> Hoạt động gần đây</h3>
          <div class="activity-list">
            <div v-for="a in activities" :key="a.id" class="activity-item">
              <div class="act-icon" :style="{ background: a.color + '18', color: a.color }">
                <i :class="a.icon"></i>
              </div>
              <div class="act-body">
                <p class="act-title">{{ a.title }}</p>
                <p class="act-time">{{ a.time }}</p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import { useAuthStore } from '@/stores/auth.js'
import { useToastStore } from '@/stores/toast.js'
import { orderService } from '@/services/orderService.js'
import { formatPrice } from '@/utils/format.js'

const auth = useAuthStore()
const toast = useToastStore()

const form = ref({ name: auth.user?.name || '', email: auth.user?.email || '', phone: '' })
const pwForm = ref({ current: '', newPw: '', confirm: '' })

const orders = ref([])
onMounted(async () => {
  try { orders.value = await orderService.getMyOrders() } catch {}
})

const totalOrders = computed(() => orders.value.length)
const paidOrders = computed(() => orders.value.filter(o => o.payment_status === 'paid').length)
const totalRevenue = computed(() => orders.value.filter(o => o.payment_status === 'paid').reduce((s, o) => s + o.total, 0))

function saveInfo() { toast.success('Đã lưu thông tin!') }
function changePassword() {
  if (pwForm.value.newPw !== pwForm.value.confirm) { toast.error('Mật khẩu xác nhận không khớp'); return }
  toast.success('Đã đổi mật khẩu!')
  pwForm.value = { current: '', newPw: '', confirm: '' }
}

const activities = [
  { id: 1, title: 'Đăng nhập hệ thống', time: 'Vừa xong', icon: 'fas fa-sign-in-alt', color: '#3b82f6' },
  { id: 2, title: 'Xác nhận đơn hàng #10', time: '5 phút trước', icon: 'fas fa-check-circle', color: '#10b981' },
  { id: 3, title: 'Xem báo cáo thống kê', time: '1 giờ trước', icon: 'fas fa-chart-line', color: '#f59e0b' },
  { id: 4, title: 'Cập nhật mã giảm giá', time: '2 giờ trước', icon: 'fas fa-ticket-alt', color: '#8b5cf6' },
]
</script>

<style scoped>
.profile-page { display: flex; flex-direction: column; gap: 0; }
.profile-grid { display: grid; grid-template-columns: 280px 1fr; gap: 24px; align-items: start; }

/* Info card */
.info-card { background: #fff; border-radius: 16px; padding: 28px; box-shadow: 0 1px 4px rgba(0,0,0,0.06); text-align: center; position: sticky; top: 80px; }
.avatar-section { display: flex; flex-direction: column; align-items: center; gap: 10px; margin-bottom: 24px; }
.big-avatar { width: 80px; height: 80px; background: linear-gradient(135deg, #3b82f6, #1d4ed8); color: #fff; border-radius: 50%; display: flex; align-items: center; justify-content: center; font-size: 32px; font-weight: 800; }
.info-card h2 { font-size: 18px; font-weight: 700; color: #1e293b; }
.role-badge { background: #eff6ff; color: #3b82f6; font-size: 12px; font-weight: 600; padding: 4px 12px; border-radius: 20px; display: flex; align-items: center; gap: 5px; }
.email { font-size: 13px; color: #94a3b8; word-break: break-all; }
.stats-row { display: grid; grid-template-columns: repeat(3, 1fr); gap: 12px; border-top: 1px solid #f1f5f9; padding-top: 20px; }
.stat-item { text-align: center; }
.stat-val { font-size: 18px; font-weight: 800; color: #1e293b; }
.stat-label { font-size: 11px; color: #94a3b8; margin-top: 2px; }

/* Settings */
.settings-col { display: flex; flex-direction: column; gap: 20px; }
.card { background: #fff; border-radius: 16px; padding: 24px; box-shadow: 0 1px 4px rgba(0,0,0,0.06); }
.card h3 { font-size: 15px; font-weight: 700; color: #1e293b; margin-bottom: 20px; display: flex; align-items: center; gap: 8px; }
.card h3 i { color: #3b82f6; }
.form { display: flex; flex-direction: column; gap: 14px; }
.form-row { display: grid; grid-template-columns: 1fr 1fr; gap: 14px; }
.field { display: flex; flex-direction: column; gap: 5px; }
.field label { font-size: 12px; font-weight: 600; color: #475569; }
.field input { padding: 10px 14px; border: 1.5px solid #e2e8f0; border-radius: 8px; font-size: 13px; outline: none; font-family: inherit; }
.field input:focus { border-color: #3b82f6; }
.field input:disabled { background: #f8fafc; color: #94a3b8; }
.btn-save { display: flex; align-items: center; gap: 8px; padding: 11px 20px; background: #3b82f6; color: #fff; border-radius: 8px; font-size: 13px; font-weight: 600; width: fit-content; }
.btn-save:hover { background: #2563eb; }

/* Activity */
.activity-list { display: flex; flex-direction: column; gap: 12px; }
.activity-item { display: flex; align-items: center; gap: 12px; padding: 10px; background: #f8fafc; border-radius: 8px; }
.act-icon { width: 36px; height: 36px; border-radius: 8px; display: flex; align-items: center; justify-content: center; font-size: 14px; flex-shrink: 0; }
.act-title { font-size: 13px; font-weight: 500; color: #1e293b; }
.act-time { font-size: 11px; color: #94a3b8; }

@media (max-width: 900px) { .profile-grid { grid-template-columns: 1fr; } .info-card { position: static; } .form-row { grid-template-columns: 1fr; } }
</style>
