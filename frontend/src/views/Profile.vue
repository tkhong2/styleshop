<template>
  <div class="container page">
    <div class="profile-layout">
      <!-- Sidebar -->
      <aside class="profile-sidebar">
        <div class="avatar">
          <div class="avatar-circle">{{ auth.user?.name?.[0]?.toUpperCase() || 'U' }}</div>
          <div class="user-info">
            <p class="user-name">{{ auth.user?.name || 'Khách hàng' }}</p>
            <p class="user-email">{{ auth.user?.email }}</p>
          </div>
        </div>
        <nav class="profile-nav">
          <button v-for="tab in tabs" :key="tab.id" :class="['pnav-btn', { active: activeTab === tab.id }]" @click="activeTab = tab.id">
            {{ tab.label }}
          </button>
          <button class="pnav-btn logout" @click="handleLogout">Đăng xuất</button>
        </nav>
      </aside>

      <!-- Content -->
      <div class="profile-content">
        <!-- Orders -->
        <div v-if="activeTab === 'orders'">
          <h2 class="content-title">Đơn hàng của tôi</h2>
          <div v-if="orders.length === 0" class="empty-state">
            <p>Bạn chưa có đơn hàng nào</p>
            <RouterLink to="/products" class="btn btn-dark">Mua sắm ngay</RouterLink>
          </div>
          <div v-else class="orders-list">
            <div v-for="order in orders" :key="order.id" class="order-card">
              <div class="order-header">
                <span class="order-id">#{{ order.id }}</span>
                <span :class="['order-status', order.status]">{{ statusLabel(order.status) }}</span>
                <span class="order-date">{{ formatDate(order.created_at) }}</span>
              </div>
              <div class="order-items">
                <p v-for="item in order.items" :key="`${item.product_id}-${item.size}`" class="order-item-row">
                  SP #{{ item.product_id }} · {{ item.size }} · {{ item.color }} × {{ item.quantity }}
                </p>
              </div>
              <div class="order-footer">
                <span>Tổng: <strong>{{ formatPrice(order.total) }}</strong></span>
              </div>
            </div>
          </div>
        </div>

        <!-- Info -->
        <div v-if="activeTab === 'info'">
          <h2 class="content-title">Thông tin tài khoản</h2>
          <form class="info-form" @submit.prevent="saveInfo">
            <div class="field">
              <label>Họ tên</label>
              <input v-model="infoForm.name" type="text" />
            </div>
            <div class="field">
              <label>Email</label>
              <input v-model="infoForm.email" type="email" disabled />
            </div>
            <div class="field">
              <label>Số điện thoại</label>
              <input v-model="infoForm.phone" type="tel" placeholder="0912 345 678" />
            </div>
            <button type="submit" class="btn btn-dark">Lưu thay đổi</button>
          </form>
        </div>

        <!-- Wishlist -->
        <div v-if="activeTab === 'wishlist'">
          <h2 class="content-title">Sản phẩm yêu thích ({{ wishlist.items.length }})</h2>
          <div v-if="wishlist.items.length === 0" class="empty-state"><p>Chưa có sản phẩm yêu thích</p></div>
          <div v-else class="products-grid" style="grid-template-columns: repeat(3,1fr)">
            <ProductCard v-for="p in wishlist.items" :key="p.id" :product="p" />
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth.js'
import { useWishlistStore } from '@/stores/wishlist.js'
import { useToastStore } from '@/stores/toast.js'
import { orderService } from '@/services/orderService.js'
import { formatPrice } from '@/utils/format.js'
import ProductCard from '@/components/ProductCard.vue'

const router = useRouter()
const auth = useAuthStore()
const wishlist = useWishlistStore()
const toast = useToastStore()

if (!auth.isLoggedIn) router.push('/login')

const activeTab = ref('orders')
const orders = ref([])
const tabs = [
  { id: 'orders', label: 'Đơn hàng' },
  { id: 'info', label: 'Thông tin' },
  { id: 'wishlist', label: 'Yêu thích' },
]

const infoForm = ref({ name: auth.user?.name || '', email: auth.user?.email || '', phone: '' })

onMounted(async () => {
  try { orders.value = await orderService.getMyOrders(auth.user?.email) } catch {}
})

function handleLogout() {
  auth.logout()
  toast.info('Đã đăng xuất')
  router.push('/')
}

function saveInfo() { toast.success('Đã lưu thông tin') }

function statusLabel(s) {
  return { pending: 'Chờ xác nhận', confirmed: 'Đã xác nhận', shipping: 'Đang giao', done: 'Hoàn thành' }[s] || s
}

function formatDate(d) {
  return new Date(d).toLocaleDateString('vi-VN')
}
</script>

<style scoped>
.page { padding: 40px 20px 80px; }
.profile-layout { display: grid; grid-template-columns: 240px 1fr; gap: 40px; align-items: start; }
.profile-sidebar { background: #fff; border: 1px solid var(--gray2); border-radius: 12px; padding: 24px; position: sticky; top: 100px; }
.avatar { display: flex; align-items: flex-start; gap: 12px; margin-bottom: 24px; padding-bottom: 24px; border-bottom: 1px solid var(--gray2); }
.avatar-circle { width: 48px; height: 48px; border-radius: 50%; background: var(--black); color: #fff; font-size: 20px; font-weight: 700; display: flex; align-items: center; justify-content: center; flex-shrink: 0; }
.user-info { min-width: 0; flex: 1; overflow: hidden; }
.user-name { font-size: 14px; font-weight: 600; word-break: break-word; }
.user-email { font-size: 12px; color: var(--gray3); word-break: break-all; overflow-wrap: anywhere; }
.profile-nav { display: flex; flex-direction: column; gap: 4px; }
.pnav-btn { text-align: left; padding: 10px 12px; font-size: 14px; border-radius: 6px; transition: background 0.15s; color: var(--black); }
.pnav-btn:hover, .pnav-btn.active { background: var(--gray); font-weight: 600; }
.pnav-btn.logout { color: var(--red); margin-top: 8px; }
.profile-content { background: #fff; border: 1px solid var(--gray2); border-radius: 12px; padding: 32px; }
.content-title { font-size: 20px; font-weight: 700; margin-bottom: 24px; }
.empty-state { text-align: center; padding: 40px; color: var(--gray3); display: flex; flex-direction: column; align-items: center; gap: 16px; }
.orders-list { display: flex; flex-direction: column; gap: 16px; }
.order-card { border: 1px solid var(--gray2); border-radius: 8px; padding: 16px; }
.order-header { display: flex; align-items: center; gap: 12px; margin-bottom: 12px; }
.order-id { font-weight: 700; font-size: 14px; }
.order-status { font-size: 12px; font-weight: 600; padding: 3px 10px; border-radius: 20px; background: #fef3c7; color: #92400e; }
.order-status.done { background: #d1fae5; color: #065f46; }
.order-date { font-size: 12px; color: var(--gray3); margin-left: auto; }
.order-item-row { font-size: 13px; color: #555; margin-bottom: 4px; }
.order-footer { margin-top: 12px; padding-top: 12px; border-top: 1px solid var(--gray2); font-size: 14px; }
.info-form { display: flex; flex-direction: column; gap: 16px; max-width: 400px; }
.field { display: flex; flex-direction: column; gap: 6px; }
.field label { font-size: 13px; font-weight: 600; }
.field input { padding: 11px 14px; border: 1.5px solid var(--gray2); border-radius: 6px; font-size: 14px; font-family: var(--font); }
.field input:focus { outline: none; border-color: var(--black); }
.field input:disabled { background: var(--gray); color: var(--gray3); }
@media (max-width: 768px) { .profile-layout { grid-template-columns: 1fr; } .profile-sidebar { position: static; } }
</style>
