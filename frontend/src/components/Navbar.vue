<template>
  <div class="header-wrap">
    <!-- Top bar -->
    <div class="topbar">
      <div class="container topbar-inner">
        <span><i class="fas fa-truck"></i> Miễn phí vận chuyển cho đơn từ 500.000đ</span>
        <span>Hotline: <a href="tel:18001162">1800 1162</a> (08:00 - 21:00)</span>
      </div>
    </div>

    <!-- Main nav -->
    <nav class="navbar" :class="{ scrolled: isScrolled }">
      <div class="container nav-inner">
        <!-- Mobile menu btn -->
        <button class="icon-btn mobile-only" @click="mobileOpen = true" aria-label="Menu">
          <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <line x1="3" y1="6" x2="21" y2="6"/><line x1="3" y1="12" x2="21" y2="12"/><line x1="3" y1="18" x2="21" y2="18"/>
          </svg>
        </button>

        <RouterLink to="/" class="logo">STYLESHOP</RouterLink>

        <!-- Desktop menu -->
        <ul class="nav-menu desktop-only">
          <li v-for="item in menu" :key="item.label" class="nav-item"
            @mouseenter="activeMenu = item.label" @mouseleave="activeMenu = null">
            <RouterLink :to="item.href" class="nav-link">
              {{ item.label }}
              <svg v-if="item.children" width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><polyline points="6 9 12 15 18 9"/></svg>
            </RouterLink>
            <!-- Mega dropdown -->
            <div v-if="item.children && activeMenu === item.label" class="mega-menu">
              <div class="container mega-inner">
                <div v-for="col in item.children" :key="col.title" class="mega-col">
                  <p class="mega-title">{{ col.title }}</p>
                  <RouterLink v-for="sub in col.items" :key="sub.label" :to="sub.href" class="mega-link" @click="activeMenu = null">
                    {{ sub.label }}
                  </RouterLink>
                </div>
                <div v-if="item.banner" class="mega-banner">
                  <img :src="item.banner" :alt="item.label" />
                </div>
              </div>
            </div>
          </li>
        </ul>

        <!-- Right actions -->
        <div class="nav-actions">
          <button class="icon-btn" @click="searchOpen = true" aria-label="Tìm kiếm">
            <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <circle cx="11" cy="11" r="8"/><line x1="21" y1="21" x2="16.65" y2="16.65"/>
            </svg>
          </button>
          <RouterLink to="/wishlist" class="icon-btn" aria-label="Yêu thích">
            <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <path d="M20.84 4.61a5.5 5.5 0 00-7.78 0L12 5.67l-1.06-1.06a5.5 5.5 0 00-7.78 7.78l1.06 1.06L12 21.23l7.78-7.78 1.06-1.06a5.5 5.5 0 000-7.78z"/>
            </svg>
            <span v-if="wishlist.items.length > 0" class="icon-badge">{{ wishlist.items.length }}</span>
          </RouterLink>
          <RouterLink v-if="auth.isLoggedIn" to="/profile" class="icon-btn" aria-label="Tài khoản">
            <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <path d="M20 21v-2a4 4 0 00-4-4H8a4 4 0 00-4 4v2"/><circle cx="12" cy="7" r="4"/>
            </svg>
          </RouterLink>
          <RouterLink v-else to="/login" class="icon-btn" aria-label="Đăng nhập">
            <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <path d="M20 21v-2a4 4 0 00-4-4H8a4 4 0 00-4 4v2"/><circle cx="12" cy="7" r="4"/>
            </svg>
          </RouterLink>
          <button class="icon-btn cart-btn" @click="cart.isOpen = true" aria-label="Giỏ hàng">
            <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <path d="M6 2L3 6v14a2 2 0 002 2h14a2 2 0 002-2V6l-3-4z"/><line x1="3" y1="6" x2="21" y2="6"/><path d="M16 10a4 4 0 01-8 0"/>
            </svg>
            <span v-if="cart.totalItems > 0" class="icon-badge red">{{ cart.totalItems }}</span>
          </button>
        </div>
      </div>
    </nav>
  </div>

  <!-- Search overlay -->
  <Transition name="fade">
    <div v-if="searchOpen" class="search-overlay" @click.self="searchOpen = false">
      <div class="search-box">
        <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="#888" stroke-width="2">
          <circle cx="11" cy="11" r="8"/><line x1="21" y1="21" x2="16.65" y2="16.65"/>
        </svg>
        <input ref="searchInput" v-model="searchQuery" type="text" placeholder="Tìm kiếm sản phẩm..."
          @keyup.enter="goSearch" @keyup.esc="searchOpen = false" />
        <button @click="searchOpen = false">
          <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="#888" stroke-width="2">
            <line x1="18" y1="6" x2="6" y2="18"/><line x1="6" y1="6" x2="18" y2="18"/>
          </svg>
        </button>
      </div>
    </div>
  </Transition>

  <!-- Mobile drawer -->
  <Transition name="slide-left">
    <div v-if="mobileOpen" class="mobile-overlay" @click.self="mobileOpen = false">
      <div class="mobile-drawer">
        <div class="drawer-header">
          <span class="logo">STYLESHOP</span>
          <button @click="mobileOpen = false">
            <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <line x1="18" y1="6" x2="6" y2="18"/><line x1="6" y1="6" x2="18" y2="18"/>
            </svg>
          </button>
        </div>
        <div class="drawer-body">
          <div v-for="item in menu" :key="item.label" class="drawer-item">
            <RouterLink :to="item.href" @click="mobileOpen = false" class="drawer-link">{{ item.label }}</RouterLink>
          </div>
          <div class="drawer-divider"></div>
          <RouterLink to="/login" @click="mobileOpen = false" class="drawer-link">Đăng nhập</RouterLink>
          <RouterLink to="/wishlist" @click="mobileOpen = false" class="drawer-link">Yêu thích</RouterLink>
        </div>
      </div>
    </div>
  </Transition>
</template>

<script setup>
import { ref, watch, nextTick, onMounted, onUnmounted } from 'vue'
import { useRouter } from 'vue-router'
import { useCartStore } from '@/stores/cart.js'
import { useWishlistStore } from '@/stores/wishlist.js'
import { useAuthStore } from '@/stores/auth.js'

const cart = useCartStore()
const wishlist = useWishlistStore()
const auth = useAuthStore()
const router = useRouter()

const activeMenu = ref(null)
const mobileOpen = ref(false)
const searchOpen = ref(false)
const searchQuery = ref('')
const searchInput = ref(null)
const isScrolled = ref(false)

watch(searchOpen, async (v) => {
  if (v) { await nextTick(); searchInput.value?.focus() }
})

function goSearch() {
  if (searchQuery.value.trim()) {
    router.push(`/products?q=${encodeURIComponent(searchQuery.value.trim())}`)
    searchOpen.value = false
    searchQuery.value = ''
  }
}

function onScroll() { isScrolled.value = window.scrollY > 60 }
onMounted(() => window.addEventListener('scroll', onScroll))
onUnmounted(() => window.removeEventListener('scroll', onScroll))

const menu = [
  {
    label: 'Giày', href: '/products?category=giay',
    banner: 'https://images.unsplash.com/photo-1543163521-1bf539c55dd2?w=300&q=80',
    children: [
      { title: 'Theo kiểu dáng', items: [
        { label: 'Giày xăng đan', href: '/products?sub=sandal' },
        { label: 'Giày cao gót', href: '/products?sub=cao-got' },
        { label: 'Giày búp bê', href: '/products?sub=bup-be' },
        { label: 'Giày sneakers', href: '/products?sub=sneakers' },
        { label: 'Dép guốc', href: '/products?sub=dep-guoc' },
      ]},
    ]
  },
  {
    label: 'Túi', href: '/products?category=tui',
    banner: 'https://images.unsplash.com/photo-1548036328-c9fa89d128fa?w=300&q=80',
    children: [
      { title: 'Theo kích cỡ', items: [
        { label: 'Túi cỡ nhỏ', href: '/products?sub=tui-nho' },
        { label: 'Túi cỡ trung', href: '/products?sub=tui-trung' },
        { label: 'Túi cỡ lớn', href: '/products?sub=tui-lon' },
        { label: 'Balo', href: '/products?sub=balo' },
        { label: 'Ví - Clutch', href: '/products?sub=vi-clutch' },
      ]},
    ]
  },
  {
    label: 'Phụ Kiện', href: '/products?category=phu-kien',
    children: [
      { title: 'Danh mục', items: [
        { label: 'Mắt kính', href: '/products?sub=mat-kinh' },
        { label: 'Nón', href: '/products?sub=non' },
        { label: 'Móc khóa', href: '/products?sub=moc-khoa' },
        { label: 'Vớ', href: '/products?sub=vo' },
      ]},
    ]
  },
  {
    label: 'Quần Áo', href: '/products?category=quan-ao',
    children: [
      { title: 'Danh mục', items: [
        { label: 'Đầm & Jumpsuit', href: '/products?sub=dam' },
        { label: 'Áo', href: '/products?sub=ao' },
        { label: 'Quần', href: '/products?sub=quan' },
        { label: 'Váy', href: '/products?sub=vay' },
        { label: 'Khoác', href: '/products?sub=khoac' },
      ]},
    ]
  },
  { label: 'Bộ Sưu Tập', href: '/collections' },
  { label: 'Sale', href: '/products?sale=true' },
]
</script>

<style scoped>
.header-wrap { position: sticky; top: 0; z-index: 100; }

.topbar { background: var(--black); color: #fff; font-size: 12px; }
.topbar-inner { display: flex; justify-content: space-between; align-items: center; height: 36px; }
.topbar a { color: #fff; }

.navbar { background: #fff; border-bottom: 1px solid var(--gray2); transition: box-shadow 0.2s; }
.navbar.scrolled { box-shadow: 0 2px 12px rgba(0,0,0,0.08); }

.nav-inner { display: flex; align-items: center; height: 60px; gap: 32px; }
.logo { font-size: 20px; font-weight: 800; letter-spacing: 2px; flex-shrink: 0; }

.nav-menu { display: flex; gap: 4px; flex: 1; }
.nav-item { position: static; }
.nav-link { display: flex; align-items: center; gap: 4px; padding: 8px 12px; font-size: 13px; font-weight: 600; color: var(--black); border-radius: 4px; transition: background 0.15s; white-space: nowrap; }
.nav-link:hover, .nav-link.router-link-active { background: var(--gray); }

/* Mega menu */
.mega-menu { position: fixed; left: 0; right: 0; top: 96px; background: #fff; border-top: 2px solid var(--black); box-shadow: 0 8px 32px rgba(0,0,0,0.1); z-index: 200; }
.mega-inner { display: flex; gap: 48px; padding: 32px 20px; }
.mega-col { display: flex; flex-direction: column; gap: 8px; min-width: 140px; }
.mega-title { font-size: 11px; font-weight: 700; text-transform: uppercase; letter-spacing: 1px; color: var(--gray3); margin-bottom: 4px; }
.mega-link { font-size: 13px; color: #444; transition: color 0.15s; }
.mega-link:hover { color: var(--black); font-weight: 500; }
.mega-banner { margin-left: auto; }
.mega-banner img { width: 200px; height: 200px; object-fit: cover; border-radius: 8px; }

.nav-actions { display: flex; align-items: center; gap: 4px; margin-left: auto; }
.icon-btn { position: relative; padding: 8px; color: var(--black); border-radius: 4px; transition: background 0.15s; display: flex; align-items: center; }
.icon-btn:hover { background: var(--gray); }
.icon-badge { position: absolute; top: 2px; right: 2px; background: var(--black); color: #fff; font-size: 9px; font-weight: 700; width: 16px; height: 16px; border-radius: 50%; display: flex; align-items: center; justify-content: center; }
.icon-badge.red { background: var(--red); }

/* Search overlay */
.search-overlay { position: fixed; inset: 0; background: rgba(0,0,0,0.5); z-index: 300; display: flex; align-items: flex-start; justify-content: center; padding-top: 100px; }
.search-box { background: #fff; border-radius: 8px; display: flex; align-items: center; gap: 12px; padding: 16px 20px; width: 600px; max-width: 90vw; box-shadow: 0 8px 32px rgba(0,0,0,0.2); }
.search-box input { flex: 1; border: none; outline: none; font-size: 16px; font-family: var(--font); }

/* Mobile */
.mobile-only { display: none; }
.desktop-only { display: flex; }

.mobile-overlay { position: fixed; inset: 0; background: rgba(0,0,0,0.4); z-index: 300; }
.mobile-drawer { position: absolute; left: 0; top: 0; bottom: 0; width: 300px; background: #fff; display: flex; flex-direction: column; }
.drawer-header { display: flex; justify-content: space-between; align-items: center; padding: 20px; border-bottom: 1px solid var(--gray2); }
.drawer-body { padding: 16px; display: flex; flex-direction: column; gap: 4px; overflow-y: auto; }
.drawer-link { display: block; padding: 12px 8px; font-size: 15px; font-weight: 500; border-radius: 4px; }
.drawer-link:hover { background: var(--gray); }
.drawer-divider { border-top: 1px solid var(--gray2); margin: 8px 0; }

.fade-enter-active, .fade-leave-active { transition: opacity 0.2s; }
.fade-enter-from, .fade-leave-to { opacity: 0; }
.slide-left-enter-active, .slide-left-leave-active { transition: opacity 0.25s; }
.slide-left-enter-from, .slide-left-leave-to { opacity: 0; }
.slide-left-enter-active .mobile-drawer, .slide-left-leave-active .mobile-drawer { transition: transform 0.25s ease; }
.slide-left-enter-from .mobile-drawer, .slide-left-leave-to .mobile-drawer { transform: translateX(-100%); }

@media (max-width: 900px) {
  .mobile-only { display: flex; }
  .desktop-only { display: none; }
  .nav-inner { gap: 12px; }
}
</style>
