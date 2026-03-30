<template>
  <div class="admin-wrap">
    <aside :class="['sidebar', { collapsed }]">
      <div class="sidebar-logo">
        <div class="logo-icon"><i class="fas fa-store"></i></div>
        <span v-if="!collapsed" class="logo-text">StyleShop</span>
        <button class="collapse-btn" @click="collapsed = !collapsed">
          <i :class="collapsed ? 'fas fa-chevron-right' : 'fas fa-chevron-left'"></i>
        </button>
      </div>

      <nav class="sidebar-nav">
        <p v-if="!collapsed" class="nav-group-label">MAIN</p>
        <RouterLink v-for="item in navItems" :key="item.path" :to="item.path"
          class="nav-item" :class="{ exact: item.exact }" :title="item.label">
          <i :class="['nav-icon', item.icon]"></i>
          <span v-if="!collapsed" class="nav-label">{{ item.label }}</span>
        </RouterLink>

        <p v-if="!collapsed" class="nav-group-label">CATALOG</p>
        <RouterLink v-for="item in catalogItems" :key="item.path" :to="item.path"
          class="nav-item" :title="item.label">
          <i :class="['nav-icon', item.icon]"></i>
          <span v-if="!collapsed" class="nav-label">{{ item.label }}</span>
        </RouterLink>
      </nav>

      <div class="sidebar-footer">
        <RouterLink to="/" class="nav-item" title="Về trang chủ">
          <i class="nav-icon fas fa-home"></i>
          <span v-if="!collapsed" class="nav-label">Về trang chủ</span>
        </RouterLink>
      </div>
    </aside>

    <div class="admin-main">
      <header class="admin-topbar">
        <div class="topbar-left">
          <h1 class="page-title">{{ currentTitle }}</h1>
        </div>
        <div class="topbar-right">
          <div class="search-bar">
            <i class="fas fa-search"></i>
            <input type="text" placeholder="Tìm kiếm..." />
          </div>
          <button class="topbar-icon"><i class="fas fa-bell"></i></button>
          <button class="topbar-icon"><i class="fas fa-cog"></i></button>
          <div class="admin-avatar">A</div>
        </div>
      </header>

      <main class="admin-content">
        <RouterView />
      </main>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { useRoute } from 'vue-router'

const collapsed = ref(false)
const route = useRoute()

const navItems = [
  { path: '/admin', label: 'Dashboard', icon: 'fas fa-chart-pie', exact: true },
  { path: '/admin/orders', label: 'Đơn hàng', icon: 'fas fa-box' },
  { path: '/admin/customers', label: 'Khách hàng', icon: 'fas fa-users' },
]
const catalogItems = [
  { path: '/admin/products', label: 'Sản phẩm', icon: 'fas fa-tshirt' },
  { path: '/admin/categories', label: 'Danh mục', icon: 'fas fa-tags' },
  { path: '/admin/stats', label: 'Thống kê', icon: 'fas fa-chart-line' },
]

const titleMap = {
  '/admin': 'Dashboard',
  '/admin/orders': 'Quản lý đơn hàng',
  '/admin/products': 'Quản lý sản phẩm',
  '/admin/customers': 'Khách hàng',
  '/admin/categories': 'Danh mục',
  '/admin/stats': 'Thống kê',
}
const currentTitle = computed(() => titleMap[route.path] || 'Admin')
</script>

<style scoped>
:root { --admin-blue: #3b82f6; --admin-blue-light: #eff6ff; --admin-dark: #1e293b; }

.admin-wrap { display: flex; min-height: 100vh; background: #f1f5f9; font-family: var(--font); }

.sidebar { width: 240px; background: #1e293b; color: #fff; display: flex; flex-direction: column; transition: width 0.25s; flex-shrink: 0; }
.sidebar.collapsed { width: 64px; }

.sidebar-logo { display: flex; align-items: center; gap: 10px; padding: 18px 16px; border-bottom: 1px solid rgba(255,255,255,0.08); }
.logo-icon { width: 34px; height: 34px; background: #3b82f6; border-radius: 8px; display: flex; align-items: center; justify-content: center; font-size: 15px; flex-shrink: 0; }
.logo-text { font-size: 16px; font-weight: 700; flex: 1; letter-spacing: 0.5px; }
.collapse-btn { background: none; color: rgba(255,255,255,0.4); padding: 4px 6px; margin-left: auto; font-size: 12px; }
.collapse-btn:hover { color: #fff; }

.sidebar-nav { flex: 1; padding: 16px 8px; display: flex; flex-direction: column; gap: 2px; overflow-y: auto; }
.nav-group-label { font-size: 10px; font-weight: 700; letter-spacing: 1.5px; color: rgba(255,255,255,0.3); padding: 8px 10px 4px; }

.nav-item { display: flex; align-items: center; gap: 12px; padding: 10px 12px; border-radius: 8px; color: rgba(255,255,255,0.55); font-size: 13px; font-weight: 500; transition: all 0.15s; text-decoration: none; }
.nav-item:hover { background: rgba(255,255,255,0.08); color: #fff; }
.nav-item.router-link-active { background: #3b82f6; color: #fff; }
.nav-icon { width: 18px; text-align: center; font-size: 14px; flex-shrink: 0; }
.nav-label { flex: 1; white-space: nowrap; }
.sidebar-footer { padding: 12px 8px; border-top: 1px solid rgba(255,255,255,0.08); }

.admin-main { flex: 1; display: flex; flex-direction: column; min-width: 0; }
.admin-topbar { background: #fff; padding: 0 24px; height: 60px; display: flex; align-items: center; justify-content: space-between; border-bottom: 1px solid #e2e8f0; box-shadow: 0 1px 3px rgba(0,0,0,0.04); }
.page-title { font-size: 17px; font-weight: 700; color: #1e293b; }
.topbar-right { display: flex; align-items: center; gap: 8px; }
.search-bar { display: flex; align-items: center; gap: 8px; background: #f8fafc; border: 1px solid #e2e8f0; border-radius: 8px; padding: 7px 14px; }
.search-bar i { color: #94a3b8; font-size: 13px; }
.search-bar input { border: none; background: none; outline: none; font-size: 13px; width: 180px; color: #334155; }
.topbar-icon { background: none; color: #64748b; padding: 8px; border-radius: 6px; font-size: 15px; }
.topbar-icon:hover { background: #f1f5f9; color: #1e293b; }
.admin-avatar { width: 34px; height: 34px; background: #3b82f6; color: #fff; border-radius: 50%; display: flex; align-items: center; justify-content: center; font-weight: 700; font-size: 13px; margin-left: 4px; }
.admin-content { flex: 1; padding: 24px; overflow-y: auto; }
</style>
