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

        <!-- Address -->
        <div v-if="activeTab === 'address'">
          <h2 class="content-title">Địa chỉ giao hàng</h2>
          <div class="address-list">
            <div v-for="(addr, i) in addresses" :key="i" class="address-card" :class="{ default: addr.isDefault }">
              <div class="addr-header">
                <span class="addr-name">{{ addr.name }}</span>
                <span v-if="addr.isDefault" class="default-badge">Mặc định</span>
              </div>
              <p class="addr-detail">{{ addr.phone }}</p>
              <p class="addr-detail">{{ addr.address }}, {{ addr.district }}, {{ addr.city }}</p>
              <div class="addr-actions">
                <button class="addr-btn" @click="editAddress(i)"><i class="fas fa-edit"></i> Sửa</button>
                <button v-if="!addr.isDefault" class="addr-btn" @click="setDefault(i)">Đặt mặc định</button>
                <button class="addr-btn del" @click="removeAddress(i)"><i class="fas fa-trash"></i></button>
              </div>
            </div>
            <button class="add-addr-btn" @click="showAddrForm = !showAddrForm">
              <i class="fas fa-plus"></i> Thêm địa chỉ mới
            </button>
          </div>

          <div v-if="showAddrForm" class="addr-form">
            <h3>{{ editIdx >= 0 ? 'Sửa địa chỉ' : 'Thêm địa chỉ mới' }}</h3>
            <div class="form-row-2">
              <div class="field"><label>Họ tên *</label><input v-model="addrForm.name" type="text" /></div>
              <div class="field"><label>Số điện thoại *</label><input v-model="addrForm.phone" type="tel" /></div>
            </div>
            <div class="field"><label>Địa chỉ *</label><input v-model="addrForm.address" type="text" placeholder="Số nhà, tên đường" /></div>
            <div class="form-row-2">
              <div class="field"><label>Quận/Huyện</label><input v-model="addrForm.district" type="text" /></div>
              <div class="field"><label>Tỉnh/Thành phố</label><input v-model="addrForm.city" type="text" /></div>
            </div>
            <label class="check-label"><input type="checkbox" v-model="addrForm.isDefault" /> Đặt làm địa chỉ mặc định</label>
            <div class="addr-form-btns">
              <button class="btn btn-dark" @click="saveAddress">Lưu địa chỉ</button>
              <button class="btn btn-outline" @click="showAddrForm = false; editIdx = -1">Hủy</button>
            </div>
          </div>
        </div>
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
import { ref, computed, onMounted } from 'vue'
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

const ADMIN_EMAILS = ['khachong2102005@gmail.com']
const isAdmin = computed(() => ADMIN_EMAILS.includes(auth.user?.email))

if (!auth.isLoggedIn) router.push('/login')

const activeTab = ref('orders')
const orders = ref([])
const tabs = [
  { id: 'orders', label: '📦 Đơn hàng' },
  { id: 'address', label: '📍 Địa chỉ' },
  { id: 'info', label: '👤 Thông tin' },
  { id: 'wishlist', label: '❤️ Yêu thích' },
]

const infoForm = ref({ name: auth.user?.name || '', email: auth.user?.email || '', phone: '' })

// Địa chỉ giao hàng
const addresses = ref(JSON.parse(localStorage.getItem('addresses') || '[]'))
const showAddrForm = ref(false)
const editIdx = ref(-1)
const addrForm = ref({ name: auth.user?.name || '', phone: '', address: '', district: '', city: '', isDefault: false })

function saveAddress() {
  if (!addrForm.value.name || !addrForm.value.phone || !addrForm.value.address) return
  if (addrForm.value.isDefault) addresses.value.forEach(a => a.isDefault = false)
  if (editIdx.value >= 0) addresses.value[editIdx.value] = { ...addrForm.value }
  else addresses.value.push({ ...addrForm.value })
  localStorage.setItem('addresses', JSON.stringify(addresses.value))
  showAddrForm.value = false; editIdx.value = -1
  addrForm.value = { name: auth.user?.name || '', phone: '', address: '', district: '', city: '', isDefault: false }
}
function editAddress(i) { editIdx.value = i; addrForm.value = { ...addresses.value[i] }; showAddrForm.value = true }
function removeAddress(i) { addresses.value.splice(i, 1); localStorage.setItem('addresses', JSON.stringify(addresses.value)) }
function setDefault(i) { addresses.value.forEach((a, idx) => a.isDefault = idx === i); localStorage.setItem('addresses', JSON.stringify(addresses.value)) }

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
.pnav-btn.admin-link { color: #3b82f6; display: flex; align-items: center; gap: 6px; margin-top: 4px; }
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
.address-list { display: flex; flex-direction: column; gap: 12px; margin-bottom: 16px; }
.address-card { border: 1.5px solid var(--gray2); border-radius: 10px; padding: 16px; }
.address-card.default { border-color: #3b82f6; background: #f0f7ff; }
.addr-header { display: flex; align-items: center; gap: 10px; margin-bottom: 6px; }
.addr-name { font-size: 14px; font-weight: 600; }
.default-badge { background: #3b82f6; color: #fff; font-size: 11px; font-weight: 600; padding: 2px 8px; border-radius: 10px; }
.addr-detail { font-size: 13px; color: #555; margin-bottom: 3px; }
.addr-actions { display: flex; gap: 8px; margin-top: 10px; }
.addr-btn { font-size: 12px; padding: 5px 10px; border: 1px solid #e2e8f0; border-radius: 6px; background: #fff; color: #555; display: flex; align-items: center; gap: 4px; }
.addr-btn:hover { background: #f8fafc; }
.addr-btn.del { color: #ef4444; border-color: #fecaca; }
.add-addr-btn { display: flex; align-items: center; gap: 8px; padding: 12px 16px; border: 1.5px dashed #e2e8f0; border-radius: 10px; color: #3b82f6; font-size: 14px; font-weight: 500; background: none; width: 100%; justify-content: center; }
.add-addr-btn:hover { background: #f0f7ff; }
.addr-form { background: #f8fafc; border-radius: 10px; padding: 20px; margin-top: 8px; }
.addr-form h3 { font-size: 15px; font-weight: 700; margin-bottom: 14px; }
.form-row-2 { display: grid; grid-template-columns: 1fr 1fr; gap: 12px; margin-bottom: 12px; }
.check-label { display: flex; align-items: center; gap: 8px; font-size: 13px; cursor: pointer; margin: 8px 0; }
.addr-form-btns { display: flex; gap: 10px; margin-top: 14px; }
.field { display: flex; flex-direction: column; gap: 6px; }
.field label { font-size: 13px; font-weight: 600; }
.field input { padding: 11px 14px; border: 1.5px solid var(--gray2); border-radius: 6px; font-size: 14px; font-family: var(--font); }
.field input:focus { outline: none; border-color: var(--black); }
.field input:disabled { background: var(--gray); color: var(--gray3); }
@media (max-width: 768px) { .profile-layout { grid-template-columns: 1fr; } .profile-sidebar { position: static; } }
</style>
