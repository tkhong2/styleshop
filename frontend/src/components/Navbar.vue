<template>
  <div class="header-wrap">
    <!-- Top bar -->
    <div class="topbar">
      <div class="container topbar-inner">
        <span><i class="fas fa-truck"></i> Miễn phí vận chuyển cho đơn từ 500.000đ</span>
        <span>Hotline: <a href="tel:0917080222">091 708 0222</a> (08:00 - 21:00)</span>
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
                    <i :class="sub.icon"></i>
                    <span>{{ sub.label }}</span>
                  </RouterLink>
                </div>
                <div v-if="item.banner" class="mega-banner">
                  <RouterLink :to="item.href" @click="activeMenu = null">
                    <img :src="item.banner" :alt="item.label" />
                    <div class="banner-cta">Xem tất cả {{ item.label }} →</div>
                  </RouterLink>
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
          <RouterLink to="/wishlist" class="icon-btn hide-on-mobile" aria-label="Yêu thích">
            <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <path d="M20.84 4.61a5.5 5.5 0 00-7.78 0L12 5.67l-1.06-1.06a5.5 5.5 0 00-7.78 7.78l1.06 1.06L12 21.23l7.78-7.78 1.06-1.06a5.5 5.5 0 000-7.78z"/>
            </svg>
            <span v-if="wishlist.items.length > 0" class="icon-badge">{{ wishlist.items.length }}</span>
          </RouterLink>
          <RouterLink v-if="auth.isLoggedIn" to="/profile" class="icon-btn hide-on-mobile" aria-label="Tài khoản">
            <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <path d="M20 21v-2a4 4 0 00-4-4H8a4 4 0 00-4 4v2"/><circle cx="12" cy="7" r="4"/>
            </svg>
          </RouterLink>
          <RouterLink v-else to="/login" class="icon-btn hide-on-mobile" aria-label="Đăng nhập">
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
    <div v-if="searchOpen" class="search-overlay" @click.self="closeSearch">
      <div class="search-box">
        <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="#888" stroke-width="2">
          <circle cx="11" cy="11" r="8"/><line x1="21" y1="21" x2="16.65" y2="16.65"/>
        </svg>
        <input ref="searchInput" v-model="searchQuery" type="text"
          placeholder="Tìm kiếm sản phẩm..."
          @input="onSearchInput"
          @keyup.enter="goSearch"
          @keyup.esc="closeSearch" />
        <button @click="closeSearch">
          <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="#888" stroke-width="2">
            <line x1="18" y1="6" x2="6" y2="18"/><line x1="6" y1="6" x2="18" y2="18"/>
          </svg>
        </button>
      </div>

      <!-- Suggestions -->
      <div v-if="suggestions.length > 0" class="suggestions">
        <RouterLink v-for="p in suggestions" :key="p.id" :to="`/products/${p.id}`"
          class="suggestion-item" @click="closeSearch">
          <img :src="p.image" :alt="p.name" />
          <div class="sug-info">
            <p class="sug-name">{{ p.name }}</p>
            <p class="sug-price">{{ formatPrice(p.price) }}</p>
          </div>
          <span v-if="p.is_sale" class="sug-badge">Sale</span>
        </RouterLink>
        <RouterLink :to="`/products?q=${encodeURIComponent(searchQuery)}`"
          class="sug-all" @click="closeSearch">
          Xem tất cả kết quả cho "<strong>{{ searchQuery }}</strong>" →
        </RouterLink>
      </div>
      <div v-else-if="searchQuery.length > 1 && !searching" class="suggestions">
        <p class="sug-empty">Không tìm thấy sản phẩm phù hợp</p>
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
import { productService } from '@/services/productService.js'
import { formatPrice } from '@/utils/format.js'

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
const suggestions = ref([])
const searching = ref(false)
let debounceTimer = null

watch(searchOpen, async (v) => {
  if (v) { await nextTick(); searchInput.value?.focus() }
  else { suggestions.value = []; searchQuery.value = '' }
})

function closeSearch() {
  searchOpen.value = false
  suggestions.value = []
  searchQuery.value = ''
}

async function onSearchInput() {
  const q = searchQuery.value.trim()
  if (q.length < 2) { suggestions.value = []; return }
  clearTimeout(debounceTimer)
  debounceTimer = setTimeout(async () => {
    searching.value = true
    try {
      const results = await productService.getAll({ q, limit: 5 })
      suggestions.value = results
    } catch { suggestions.value = [] }
    finally { searching.value = false }
  }, 300)
}

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
    banner: 'https://images.unsplash.com/photo-1543163521-1bf539c55dd2?w=400&q=80',
    children: [
      { title: 'Theo kiểu dáng', items: [
        { label: 'Giày xăng đan', href: '/products?sub=sandal', icon: 'fas fa-shoe-prints' },
        { label: 'Giày cao gót', href: '/products?sub=cao-got', icon: 'fas fa-shoe-prints' },
        { label: 'Giày búp bê', href: '/products?sub=bup-be', icon: 'fas fa-shoe-prints' },
        { label: 'Giày sneakers', href: '/products?sub=sneakers', icon: 'fas fa-shoe-prints' },
        { label: 'Dép guốc', href: '/products?sub=dep-guoc', icon: 'fas fa-shoe-prints' },
      ]},
      { title: 'Nổi bật', items: [
        { label: 'Hàng mới về', href: '/products?category=giay&new=true', icon: 'fas fa-star' },
        { label: 'Đang giảm giá', href: '/products?category=giay&sale=true', icon: 'fas fa-tag' },
      ]},
    ]
  },
  {
    label: 'Túi', href: '/products?category=tui',
    banner: 'https://images.unsplash.com/photo-1548036328-c9fa89d128fa?w=400&q=80',
    children: [
      { title: 'Theo kích cỡ', items: [
        { label: 'Túi cỡ nhỏ', href: '/products?sub=tui-nho', icon: 'fas fa-shopping-bag' },
        { label: 'Túi cỡ trung', href: '/products?sub=tui-trung', icon: 'fas fa-shopping-bag' },
        { label: 'Túi cỡ lớn', href: '/products?sub=tui-lon', icon: 'fas fa-shopping-bag' },
        { label: 'Balo', href: '/products?sub=balo', icon: 'fas fa-backpack' },
        { label: 'Ví - Clutch', href: '/products?sub=vi-clutch', icon: 'fas fa-wallet' },
      ]},
      { title: 'Nổi bật', items: [
        { label: 'Hàng mới về', href: '/products?category=tui&new=true', icon: 'fas fa-star' },
        { label: 'Đang giảm giá', href: '/products?category=tui&sale=true', icon: 'fas fa-tag' },
      ]},
    ]
  },
  {
    label: 'Phụ Kiện', href: '/products?category=phu-kien',
    banner: 'https://images.unsplash.com/photo-1523779105320-d1cd346ff52b?w=400&q=80',
    children: [
      { title: 'Danh mục', items: [
        { label: 'Mắt kính', href: '/products?sub=mat-kinh', icon: 'fas fa-glasses' },
        { label: 'Nón', href: '/products?sub=non', icon: 'fas fa-hat-cowboy' },
        { label: 'Móc khóa', href: '/products?sub=moc-khoa', icon: 'fas fa-key' },
        { label: 'Vớ', href: '/products?sub=vo', icon: 'fas fa-socks' },
      ]},
    ]
  },
  {
    label: 'Quần Áo', href: '/products?category=quan-ao',
    banner: 'https://images.unsplash.com/photo-1558618666-fcd25c85cd64?w=400&q=80',
    children: [
      { title: 'Trang phục nữ', items: [
        { label: 'Đầm & Jumpsuit', href: '/products?sub=dam', icon: 'fas fa-female' },
        { label: 'Váy', href: '/products?sub=vay', icon: 'fas fa-female' },
        { label: 'Áo nữ', href: '/products?sub=ao&gender=nu', icon: 'fas fa-tshirt' },
      ]},
      { title: 'Trang phục nam', items: [
        { label: 'Áo nam', href: '/products?sub=ao&gender=nam', icon: 'fas fa-tshirt' },
        { label: 'Quần', href: '/products?sub=quan', icon: 'fas fa-male' },
        { label: 'Áo khoác', href: '/products?sub=khoac', icon: 'fas fa-tshirt' },
      ]},
      { title: 'Nổi bật', items: [
        { label: 'Hàng mới về', href: '/products?is_new=true', icon: 'fas fa-star' },
        { label: 'Đang giảm giá', href: '/products?sale=true', icon: 'fas fa-tag' },
      ]},
    ]
  },
  {
    label: 'Bộ Sưu Tập', href: '/collections',
    banner: 'https://images.unsplash.com/photo-1483985988355-763728e1935b?w=400&q=80',
    children: [
      { title: 'BST mới nhất', items: [
        { label: 'Summer Wanted', href: '/collections/summer', icon: 'fas fa-sun' },
        { label: 'Dazzling Aura', href: '/collections/dazzling', icon: 'fas fa-star' },
        { label: "Juno's Club", href: '/collections/club', icon: 'fas fa-crown' },
        { label: 'The Sweetest Spring', href: '/collections/spring', icon: 'fas fa-leaf' },
        { label: 'Jingle All Twinkle', href: '/collections/winter', icon: 'fas fa-snowflake' },
        { label: 'Áo Dài Giai Duyên', href: '/collections/aodai', icon: 'fas fa-heart' },
      ]},
    ]
  },
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
.mega-menu { position: fixed; left: 0; right: 0; top: 96px; background: #fff; border-top: 2px solid var(--black); box-shadow: 0 12px 40px rgba(0,0,0,0.12); z-index: 200; }
.mega-inner { display: flex; gap: 40px; padding: 28px 20px; align-items: flex-start; }
.mega-col { display: flex; flex-direction: column; gap: 4px; min-width: 150px; }
.mega-title { font-size: 10px; font-weight: 700; text-transform: uppercase; letter-spacing: 1.5px; color: var(--gray3); margin-bottom: 8px; padding-bottom: 8px; border-bottom: 1px solid var(--gray2); }
.mega-link { display: flex; align-items: center; gap: 8px; font-size: 13px; color: #444; padding: 6px 8px; border-radius: 6px; transition: all 0.15s; }
.mega-link:hover { color: var(--black); background: var(--gray); font-weight: 500; }
.mega-link i { width: 14px; color: var(--gray3); font-size: 12px; }
.mega-link:hover i { color: var(--black); }
.mega-banner { margin-left: auto; flex-shrink: 0; }
.mega-banner a { display: block; position: relative; border-radius: 10px; overflow: hidden; }
.mega-banner img { width: 220px; height: 220px; object-fit: cover; display: block; transition: transform 0.3s; }
.mega-banner a:hover img { transform: scale(1.04); }
.banner-cta { position: absolute; bottom: 0; left: 0; right: 0; background: linear-gradient(transparent, rgba(0,0,0,0.7)); color: #fff; font-size: 13px; font-weight: 600; padding: 24px 14px 14px; }

.nav-actions { display: flex; align-items: center; gap: 4px; margin-left: auto; }
.icon-btn { position: relative; padding: 8px; color: var(--black); border-radius: 4px; transition: background 0.15s; display: flex; align-items: center; }
.icon-btn:hover { background: var(--gray); }
.icon-badge { position: absolute; top: 2px; right: 2px; background: var(--black); color: #fff; font-size: 9px; font-weight: 700; width: 16px; height: 16px; border-radius: 50%; display: flex; align-items: center; justify-content: center; }
.icon-badge.red { background: var(--red); }

/* Search overlay */
.search-overlay { position: fixed; inset: 0; background: rgba(0,0,0,0.5); z-index: 300; display: flex; flex-direction: column; align-items: center; padding-top: 80px; }
.search-box { background: #fff; border-radius: 12px 12px 0 0; display: flex; align-items: center; gap: 12px; padding: 16px 20px; width: 600px; max-width: 90vw; box-shadow: 0 4px 20px rgba(0,0,0,0.15); }
.search-box input { flex: 1; border: none; outline: none; font-size: 16px; font-family: var(--font); }
.suggestions { background: #fff; width: 600px; max-width: 90vw; border-radius: 0 0 12px 12px; border-top: 1px solid var(--gray2); overflow: hidden; box-shadow: 0 8px 24px rgba(0,0,0,0.12); }
.suggestion-item { display: flex; align-items: center; gap: 12px; padding: 10px 16px; transition: background 0.15s; text-decoration: none; color: inherit; }
.suggestion-item:hover { background: var(--gray); }
.suggestion-item img { width: 44px; height: 44px; object-fit: cover; border-radius: 6px; flex-shrink: 0; }
.sug-name { font-size: 13px; font-weight: 500; margin-bottom: 2px; }
.sug-price { font-size: 12px; color: var(--gray3); }
.sug-badge { margin-left: auto; background: var(--red); color: #fff; font-size: 10px; font-weight: 700; padding: 2px 6px; border-radius: 3px; flex-shrink: 0; }
.sug-all { display: block; padding: 12px 16px; font-size: 13px; color: #3b82f6; border-top: 1px solid var(--gray2); text-decoration: none; }
.sug-all:hover { background: #eff6ff; }
.sug-empty { padding: 16px; text-align: center; color: var(--gray3); font-size: 13px; }

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
  .nav-inner { gap: 8px; }
  .logo { font-size: 17px; letter-spacing: 1px; }
}

@media (max-width: 768px) {
  /* Ẩn wishlist + profile icon vì đã có bottom nav */
  .hide-on-mobile { display: none !important; }
  .topbar { display: none; }
}
</style>
