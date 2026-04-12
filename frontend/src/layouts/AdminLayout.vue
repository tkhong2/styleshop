<template>
  <div class="admin-wrap">
    <aside :class="['sidebar', { collapsed }]">
      <div class="sidebar-logo">
        <div v-if="!collapsed" class="logo-icon"><i class="fas fa-store"></i></div>
        <span v-if="!collapsed" class="logo-text">StyleShop</span>
        <button class="collapse-btn" @click="collapsed = !collapsed" :title="collapsed ? 'Mở menu' : 'Thu gọn'">
          <i :class="collapsed ? 'fas fa-bars' : 'fas fa-chevron-left'"></i>
        </button>
      </div>

      <nav class="sidebar-nav">
        <p v-if="!collapsed" class="nav-group-label">MAIN</p>
        <RouterLink v-for="item in navItems" :key="item.path" :to="item.path" class="nav-item" :title="item.label">
          <i :class="['nav-icon', item.icon]"></i>
          <span v-if="!collapsed" class="nav-label">{{ item.label }}</span>
          <span v-if="!collapsed && item.badge" class="nav-badge">{{ item.badge }}</span>
        </RouterLink>
        <p v-if="!collapsed" class="nav-group-label">CATALOG</p>
        <RouterLink v-for="item in catalogItems" :key="item.path" :to="item.path" class="nav-item" :title="item.label">
          <i :class="['nav-icon', item.icon]"></i>
          <span v-if="!collapsed" class="nav-label">{{ item.label }}</span>
        </RouterLink>
      </nav>

      <div class="sidebar-footer">
      </div>
    </aside>

    <div class="admin-main">
      <!-- Topbar -->
      <header class="admin-topbar">
        <div class="topbar-left">
          <h1 class="page-title">{{ currentTitle }}</h1>
        </div>
        <div class="topbar-right">
          <!-- Search -->
          <div class="search-wrap" v-click-outside="() => showSearch = false">
            <div class="search-bar" :class="{ focused: showSearch }">
              <i class="fas fa-search"></i>
              <input v-model="searchQ" type="text" placeholder="Tìm kiếm..."
                @focus="showSearch = true" @input="doSearch" />
              <button v-if="searchQ" class="clear-btn" @click="searchQ = ''; searchResults = []">
                <i class="fas fa-times"></i>
              </button>
            </div>
            <div v-if="showSearch && searchResults.length > 0" class="search-dropdown">
              <RouterLink v-for="r in searchResults" :key="r.path" :to="r.path"
                class="search-result" @click="showSearch = false; searchQ = ''">
                <i :class="r.icon"></i>
                <div>
                  <p class="sr-title">{{ r.title }}</p>
                  <p class="sr-sub">{{ r.sub }}</p>
                </div>
              </RouterLink>
            </div>
            <div v-else-if="showSearch && searchQ.length > 1" class="search-dropdown">
              <p class="sr-empty">Không tìm thấy kết quả</p>
            </div>
          </div>

          <!-- Notifications -->
          <div class="notif-wrap" v-click-outside="() => showNotif = false">
            <button class="topbar-icon" :class="{ active: showNotif }" @click="showNotif = !showNotif">
              <i class="fas fa-bell"></i>
              <span v-if="unreadCount > 0" class="notif-dot">{{ unreadCount }}</span>
            </button>
            <div v-if="showNotif" class="notif-dropdown">
              <div class="notif-header">
                <span>Thông báo</span>
                <button @click="markAllRead" class="mark-read">Đánh dấu đã đọc</button>
              </div>
              <div class="notif-list">
                <div v-for="n in notifications" :key="n.id" :class="['notif-item', { unread: !n.read }]" @click="n.read = true">
                  <div class="notif-icon" :style="{ background: n.color + '18', color: n.color }">
                    <i :class="n.icon"></i>
                  </div>
                  <div class="notif-body">
                    <p class="notif-title">{{ n.title }}</p>
                    <p class="notif-time">{{ n.time }}</p>
                  </div>
                  <div v-if="!n.read" class="unread-dot"></div>
                </div>
              </div>
              <RouterLink to="/admin/orders" class="notif-footer" @click="showNotif = false">
                Xem tất cả đơn hàng →
              </RouterLink>
            </div>
          </div>

          <!-- Profile dropdown -->
          <div class="profile-wrap" v-click-outside="() => showProfile = false">
            <button class="admin-avatar-btn" @click="showProfile = !showProfile">
              <div class="admin-avatar">{{ auth.user?.name?.[0]?.toUpperCase() || 'A' }}</div>
              <div class="avatar-info">
                <p class="avatar-name">{{ auth.user?.name || 'Admin' }}</p>
                <p class="avatar-role">Quản trị viên</p>
              </div>
              <i class="fas fa-chevron-down" style="font-size:11px;color:#94a3b8"></i>
            </button>
            <div v-if="showProfile" class="profile-dropdown">
              <div class="pd-header">
                <div class="pd-avatar">{{ auth.user?.name?.[0]?.toUpperCase() || 'A' }}</div>
                <div>
                  <p class="pd-name">{{ auth.user?.name }}</p>
                  <p class="pd-email">{{ auth.user?.email }}</p>
                </div>
              </div>
              <div class="pd-divider"></div>
              <RouterLink to="/admin/profile" class="pd-item" @click="showProfile = false">
                <i class="fas fa-user"></i> Trang cá nhân
              </RouterLink>
              <div class="pd-divider"></div>
              <button class="pd-item logout" @click="handleLogout">
                <i class="fas fa-sign-out-alt"></i> Đăng xuất
              </button>
            </div>
          </div>
        </div>
      </header>

      <main class="admin-content">
        <RouterView />
      </main>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth.js'
import { useToastStore } from '@/stores/toast.js'
import { orderService } from '@/services/orderService.js'

const collapsed = ref(false)
const route = useRoute()
const router = useRouter()
const auth = useAuthStore()
const toast = useToastStore()

// Search
const searchQ = ref('')
const showSearch = ref(false)
const searchResults = ref([])

const searchIndex = [
  { title: 'Dashboard', sub: 'Tổng quan hệ thống', path: '/admin', icon: 'fas fa-chart-pie' },
  { title: 'Đơn hàng', sub: 'Quản lý đơn hàng', path: '/admin/orders', icon: 'fas fa-box' },
  { title: 'Sản phẩm', sub: 'Quản lý sản phẩm', path: '/admin/products', icon: 'fas fa-tshirt' },
  { title: 'Khách hàng', sub: 'Danh sách khách hàng', path: '/admin/customers', icon: 'fas fa-users' },
  { title: 'Danh mục', sub: 'Quản lý danh mục', path: '/admin/categories', icon: 'fas fa-tags' },
  { title: 'Mã giảm giá', sub: 'Quản lý coupon', path: '/admin/coupons', icon: 'fas fa-ticket-alt' },
  { title: 'Thống kê', sub: 'Báo cáo doanh thu', path: '/admin/stats', icon: 'fas fa-chart-line' },
]

function doSearch() {
  if (searchQ.value.length < 1) { searchResults.value = []; return }
  const q = searchQ.value.toLowerCase()
  searchResults.value = searchIndex.filter(i =>
    i.title.toLowerCase().includes(q) || i.sub.toLowerCase().includes(q)
  )
}

// Notifications
const showNotif = ref(false)
const notifications = ref([
  { id: 1, title: 'Đơn hàng mới #10', time: '2 phút trước', icon: 'fas fa-box', color: '#3b82f6', read: false },
  { id: 2, title: 'Thanh toán thành công #9', time: '15 phút trước', icon: 'fas fa-check-circle', color: '#10b981', read: false },
  { id: 3, title: 'Đơn hàng chờ xác nhận #8', time: '1 giờ trước', icon: 'fas fa-clock', color: '#f59e0b', read: true },
  { id: 4, title: 'Khách hàng mới đăng ký', time: '2 giờ trước', icon: 'fas fa-user-plus', color: '#8b5cf6', read: true },
])

const unreadCount = computed(() => notifications.value.filter(n => !n.read).length)
function markAllRead() { notifications.value.forEach(n => n.read = true) }

// Load real notifications from orders
onMounted(async () => {
  try {
    const orders = await orderService.getMyOrders()
    const waiting = orders.filter(o => o.payment_status === 'waiting')
    if (waiting.length > 0) {
      notifications.value.unshift({
        id: Date.now(), read: false, color: '#f59e0b', icon: 'fas fa-exclamation-circle',
        title: `${waiting.length} đơn hàng chờ thanh toán`,
        time: 'Vừa xong',
      })
    }
  } catch {}
})

// Profile dropdown
const showProfile = ref(false)
function handleLogout() {
  auth.logout()
  toast.info('Đã đăng xuất')
  router.push('/login')
}

// Click outside directive
const vClickOutside = {
  mounted(el, binding) {
    el._clickOutside = (e) => { if (!el.contains(e.target)) binding.value(e) }
    document.addEventListener('click', el._clickOutside)
  },
  unmounted(el) { document.removeEventListener('click', el._clickOutside) }
}

const navItems = [
  { path: '/admin', label: 'Dashboard', icon: 'fas fa-chart-pie' },
  { path: '/admin/orders', label: 'Đơn hàng', icon: 'fas fa-box' },
  { path: '/admin/customers', label: 'Khách hàng', icon: 'fas fa-users' },
]
const catalogItems = [
  { path: '/admin/products', label: 'Sản phẩm', icon: 'fas fa-tshirt' },
  { path: '/admin/categories', label: 'Danh mục', icon: 'fas fa-tags' },
  { path: '/admin/coupons', label: 'Mã giảm giá', icon: 'fas fa-ticket-alt' },
  { path: '/admin/stats', label: 'Thống kê', icon: 'fas fa-chart-line' },
]

const titleMap = {
  '/admin': 'Dashboard', '/admin/orders': 'Quản lý đơn hàng',
  '/admin/products': 'Quản lý sản phẩm', '/admin/customers': 'Khách hàng',
  '/admin/categories': 'Danh mục', '/admin/stats': 'Thống kê',
  '/admin/coupons': 'Mã giảm giá', '/admin/profile': 'Trang cá nhân',
}
const currentTitle = computed(() => titleMap[route.path] || 'Admin')
</script>

<style scoped>
.admin-wrap { display: flex; min-height: 100vh; background: #f1f5f9; font-family: var(--font); }

/* Sidebar */
.sidebar { width: 240px; background: #1e293b; color: #fff; display: flex; flex-direction: column; transition: width 0.25s; flex-shrink: 0; }
.sidebar.collapsed { width: 64px; }
.sidebar-logo { display: flex; align-items: center; gap: 10px; padding: 18px 16px; border-bottom: 1px solid rgba(255,255,255,0.08); }
.sidebar.collapsed .sidebar-logo { justify-content: center; padding: 18px 8px; }
.logo-icon { width: 34px; height: 34px; background: #3b82f6; border-radius: 8px; display: flex; align-items: center; justify-content: center; font-size: 15px; flex-shrink: 0; }
.logo-text { font-size: 16px; font-weight: 700; flex: 1; }
.collapse-btn { background: none; color: rgba(255,255,255,0.4); padding: 4px 6px; margin-left: auto; font-size: 14px; border-radius: 6px; transition: all 0.15s; }
.sidebar.collapsed .collapse-btn { margin-left: 0; }
.collapse-btn:hover { color: #fff; background: rgba(255,255,255,0.1); }
.sidebar-nav { flex: 1; padding: 16px 8px; display: flex; flex-direction: column; gap: 2px; overflow-y: auto; }
.nav-group-label { font-size: 10px; font-weight: 700; letter-spacing: 1.5px; color: rgba(255,255,255,0.3); padding: 8px 10px 4px; }
.nav-item { display: flex; align-items: center; gap: 12px; padding: 10px 12px; border-radius: 8px; color: rgba(255,255,255,0.55); font-size: 13px; font-weight: 500; transition: all 0.15s; text-decoration: none; }
.nav-item:hover { background: rgba(255,255,255,0.08); color: #fff; }
.nav-item.router-link-active { background: #3b82f6; color: #fff; }
.nav-icon { width: 18px; text-align: center; font-size: 14px; flex-shrink: 0; }
.nav-label { flex: 1; white-space: nowrap; }
.nav-badge { background: #ef4444; color: #fff; font-size: 10px; font-weight: 700; padding: 1px 6px; border-radius: 10px; }
.sidebar-footer { padding: 12px 8px; border-top: 1px solid rgba(255,255,255,0.08); }
.logout-btn { width: 100%; color: rgba(255,255,255,0.55); }
.logout-btn:hover { background: rgba(239,68,68,0.15); color: #ef4444; }

/* Main */
.admin-main { flex: 1; display: flex; flex-direction: column; min-width: 0; }
.admin-topbar { background: #fff; padding: 0 20px; height: 64px; display: flex; align-items: center; justify-content: space-between; border-bottom: 1px solid #e2e8f0; box-shadow: 0 1px 3px rgba(0,0,0,0.04); gap: 16px; }
.page-title { font-size: 17px; font-weight: 700; color: #1e293b; white-space: nowrap; }
.topbar-right { display: flex; align-items: center; gap: 6px; }

/* Search */
.search-wrap { position: relative; }
.search-bar { display: flex; align-items: center; gap: 8px; background: #f8fafc; border: 1.5px solid #e2e8f0; border-radius: 10px; padding: 8px 14px; transition: border-color 0.2s; }
.search-bar.focused { border-color: #3b82f6; background: #fff; }
.search-bar i { color: #94a3b8; font-size: 13px; flex-shrink: 0; }
.search-bar input { border: none; background: none; outline: none; font-size: 13px; width: 200px; color: #334155; }
.clear-btn { background: none; color: #94a3b8; font-size: 12px; padding: 0 2px; }
.search-dropdown { position: absolute; top: calc(100% + 8px); left: 0; right: 0; background: #fff; border-radius: 10px; box-shadow: 0 8px 24px rgba(0,0,0,0.12); border: 1px solid #e2e8f0; overflow: hidden; z-index: 100; min-width: 280px; }
.search-result { display: flex; align-items: center; gap: 12px; padding: 12px 16px; text-decoration: none; color: inherit; transition: background 0.15s; }
.search-result:hover { background: #f8fafc; }
.search-result i { width: 32px; height: 32px; background: #eff6ff; color: #3b82f6; border-radius: 8px; display: flex; align-items: center; justify-content: center; font-size: 13px; flex-shrink: 0; }
.sr-title { font-size: 13px; font-weight: 600; color: #1e293b; }
.sr-sub { font-size: 11px; color: #94a3b8; }
.sr-empty { padding: 16px; text-align: center; color: #94a3b8; font-size: 13px; }

/* Notifications */
.notif-wrap { position: relative; }
.topbar-icon { background: none; color: #64748b; padding: 8px; border-radius: 8px; font-size: 15px; position: relative; transition: all 0.15s; }
.topbar-icon:hover, .topbar-icon.active { background: #f1f5f9; color: #1e293b; }
.notif-dot { position: absolute; top: 4px; right: 4px; background: #ef4444; color: #fff; font-size: 9px; font-weight: 700; width: 16px; height: 16px; border-radius: 50%; display: flex; align-items: center; justify-content: center; border: 2px solid #fff; }
.notif-dropdown { position: absolute; top: calc(100% + 8px); right: 0; width: 320px; background: #fff; border-radius: 12px; box-shadow: 0 8px 32px rgba(0,0,0,0.12); border: 1px solid #e2e8f0; z-index: 100; overflow: hidden; }
.notif-header { display: flex; justify-content: space-between; align-items: center; padding: 14px 16px; border-bottom: 1px solid #f1f5f9; font-size: 14px; font-weight: 700; }
.mark-read { font-size: 12px; color: #3b82f6; background: none; }
.notif-list { max-height: 280px; overflow-y: auto; }
.notif-item { display: flex; align-items: center; gap: 12px; padding: 12px 16px; cursor: pointer; transition: background 0.15s; position: relative; }
.notif-item:hover { background: #f8fafc; }
.notif-item.unread { background: #f0f7ff; }
.notif-icon { width: 36px; height: 36px; border-radius: 10px; display: flex; align-items: center; justify-content: center; font-size: 14px; flex-shrink: 0; }
.notif-title { font-size: 13px; font-weight: 500; color: #1e293b; margin-bottom: 2px; }
.notif-time { font-size: 11px; color: #94a3b8; }
.unread-dot { width: 8px; height: 8px; background: #3b82f6; border-radius: 50%; flex-shrink: 0; margin-left: auto; }
.notif-footer { display: block; text-align: center; padding: 12px; font-size: 13px; color: #3b82f6; border-top: 1px solid #f1f5f9; text-decoration: none; }
.notif-footer:hover { background: #f8fafc; }

/* Profile */
.profile-wrap { position: relative; }
.admin-avatar-btn { display: flex; align-items: center; gap: 8px; padding: 6px 10px; border-radius: 10px; background: none; transition: background 0.15s; }
.admin-avatar-btn:hover { background: #f1f5f9; }
.admin-avatar { width: 34px; height: 34px; background: #3b82f6; color: #fff; border-radius: 50%; display: flex; align-items: center; justify-content: center; font-weight: 700; font-size: 13px; flex-shrink: 0; }
.avatar-info { text-align: left; }
.avatar-name { font-size: 13px; font-weight: 600; color: #1e293b; line-height: 1.2; }
.avatar-role { font-size: 11px; color: #94a3b8; }
.profile-dropdown { position: absolute; top: calc(100% + 8px); right: 0; width: 220px; background: #fff; border-radius: 12px; box-shadow: 0 8px 32px rgba(0,0,0,0.12); border: 1px solid #e2e8f0; z-index: 100; overflow: hidden; }
.pd-header { display: flex; align-items: center; gap: 10px; padding: 14px 16px; }
.pd-avatar { width: 40px; height: 40px; background: #3b82f6; color: #fff; border-radius: 50%; display: flex; align-items: center; justify-content: center; font-weight: 700; font-size: 16px; flex-shrink: 0; }
.pd-name { font-size: 13px; font-weight: 600; color: #1e293b; }
.pd-email { font-size: 11px; color: #94a3b8; word-break: break-all; }
.pd-divider { height: 1px; background: #f1f5f9; }
.pd-item { display: flex; align-items: center; gap: 10px; padding: 11px 16px; font-size: 13px; color: #475569; text-decoration: none; transition: background 0.15s; width: 100%; text-align: left; background: none; }
.pd-item:hover { background: #f8fafc; color: #1e293b; }
.pd-item i { width: 16px; color: #94a3b8; }
.pd-item.logout { color: #ef4444; }
.pd-item.logout i { color: #ef4444; }

.admin-content { flex: 1; padding: 24px; overflow-y: auto; }
</style>
