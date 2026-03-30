<template>
  <div class="home">
    <!-- Hero Slider -->
    <section class="hero">
      <div class="hero-slides">
        <div v-for="(slide, i) in slides" :key="i" class="hero-slide" :class="{ active: currentSlide === i }">
          <img :src="slide.img" :alt="slide.title" />
          <div class="hero-overlay">
            <div class="container">
              <div class="hero-content">
                <p class="hero-sub">{{ slide.sub }}</p>
                <h1>{{ slide.title }}</h1>
                <p class="hero-desc">{{ slide.desc }}</p>
                <RouterLink :to="slide.href" class="btn btn-dark">{{ slide.cta }}</RouterLink>
              </div>
            </div>
          </div>
        </div>
      </div>
      <div class="hero-dots">
        <button v-for="(_, i) in slides" :key="i" :class="['dot', { active: currentSlide === i }]" @click="currentSlide = i"></button>
      </div>
      <button class="hero-arrow prev" @click="prevSlide">‹</button>
      <button class="hero-arrow next" @click="nextSlide">›</button>
    </section>

    <!-- Flash Sale -->
    <section class="flash-sale section">
      <div class="container">
        <div class="section-header">
          <div class="flash-title">
            <span class="flash-icon"><i class="fas fa-bolt"></i></span>
            <span class="section-title">FLASH SALE</span>
            <div class="countdown">
              <span class="cd-block">{{ pad(countdown.h) }}</span>:
              <span class="cd-block">{{ pad(countdown.m) }}</span>:
              <span class="cd-block">{{ pad(countdown.s) }}</span>
            </div>
          </div>
          <RouterLink to="/products?sale=true" class="view-all">Xem tất cả →</RouterLink>
        </div>
        <div class="products-grid">
          <ProductCard v-for="p in saleProducts" :key="p.id" :product="p" />
        </div>
      </div>
    </section>

    <!-- Category icons -->
    <section class="cat-icons section">
      <div class="container">
        <div class="cat-icon-grid">
          <RouterLink v-for="cat in catIcons" :key="cat.label" :to="cat.href" class="cat-icon-item">
            <div class="cat-icon-img">
              <img :src="cat.img" :alt="cat.label" />
            </div>
            <span>{{ cat.label }}</span>
          </RouterLink>
        </div>
      </div>
    </section>

    <!-- New arrivals -->
    <section class="section">
      <div class="container">
        <div class="section-header">
          <h2 class="section-title">HÀNG MỚI VỀ</h2>
          <RouterLink to="/products" class="view-all">Xem tất cả →</RouterLink>
        </div>
        <div v-if="loading" class="loading-grid">
          <div v-for="i in 5" :key="i" class="skeleton-card"></div>
        </div>
        <div v-else class="products-grid">
          <ProductCard v-for="p in newProducts" :key="p.id" :product="p" />
        </div>
      </div>
    </section>

    <!-- Banner strip -->
    <section class="banner-strip">
      <div class="container banner-strip-inner">
        <RouterLink to="/products?category=giay" class="banner-item">
          <img src="https://images.unsplash.com/photo-1543163521-1bf539c55dd2?w=600&q=80" alt="Giày" />
          <div class="banner-label"><span>GIÀY</span><small>Khám phá ngay →</small></div>
        </RouterLink>
        <RouterLink to="/products?category=tui" class="banner-item">
          <img src="https://images.unsplash.com/photo-1548036328-c9fa89d128fa?w=600&q=80" alt="Túi" />
          <div class="banner-label"><span>TÚI XÁCH</span><small>Khám phá ngay →</small></div>
        </RouterLink>
        <RouterLink to="/products?category=quan-ao" class="banner-item">
          <img src="https://images.unsplash.com/photo-1558618666-fcd25c85cd64?w=600&q=80" alt="Quần áo" />
          <div class="banner-label"><span>QUẦN ÁO</span><small>Khám phá ngay →</small></div>
        </RouterLink>
      </div>
    </section>

    <!-- Products by category tabs -->
    <section class="section">
      <div class="container">
        <div class="tab-header">
          <button v-for="tab in tabs" :key="tab.id" :class="['tab-btn', { active: activeTab === tab.id }]" @click="activeTab = tab.id">
            {{ tab.label }}
          </button>
          <RouterLink :to="`/products?category=${activeTab}`" class="view-all" style="margin-left:auto">Xem tất cả →</RouterLink>
        </div>
        <div class="products-grid">
          <ProductCard v-for="p in tabProducts" :key="p.id" :product="p" />
        </div>
      </div>
    </section>

    <!-- Collections -->
    <section class="section collections-section">
      <div class="container">
        <div class="section-header">
          <h2 class="section-title">BỘ SƯU TẬP</h2>
          <RouterLink to="/collections" class="view-all">Xem tất cả BST →</RouterLink>
        </div>
        <div class="collections-grid">
          <RouterLink v-for="col in collections" :key="col.title" :to="col.href" class="col-card">
            <img :src="col.img" :alt="col.title" />
            <div class="col-overlay">
              <p class="col-sub">{{ col.sub }}</p>
              <h3>{{ col.title }}</h3>
              <span class="col-cta">KHÁM PHÁ NGAY</span>
            </div>
          </RouterLink>
        </div>
      </div>
    </section>

    <!-- Benefits -->
    <section class="benefits">
      <div class="container benefits-grid">
        <div v-for="b in benefits" :key="b.title" class="benefit-item">
          <div class="benefit-icon"><i :class="b.icon"></i></div>
          <div>
            <p class="benefit-title">{{ b.title }}</p>
            <p class="benefit-desc">{{ b.desc }}</p>
          </div>
        </div>
      </div>
    </section>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted } from 'vue'
import { useProducts } from '@/composables/useProducts.js'
import ProductCard from '@/components/ProductCard.vue'

const { products, loading, fetchProducts } = useProducts()
onMounted(() => fetchProducts())

// Slider
const slides = [
  { img: 'https://images.unsplash.com/photo-1483985988355-763728e1935b?w=1400&q=80', sub: 'Bộ sưu tập mới 2026', title: 'Phong cách của bạn, câu chuyện của bạn', desc: 'Khám phá hàng trăm mẫu thời trang chất lượng cao', href: '/products', cta: 'Mua sắm ngay' },
  { img: 'https://images.unsplash.com/photo-1558618666-fcd25c85cd64?w=1400&q=80', sub: 'Flash Sale hôm nay', title: 'Giảm đến 50% toàn bộ sản phẩm', desc: 'Ưu đãi có hạn - Nhanh tay kẻo lỡ', href: '/products?sale=true', cta: 'Xem ngay' },
  { img: 'https://images.unsplash.com/photo-1490578474895-699cd4e2cf59?w=1400&q=80', sub: 'Thời trang nam', title: 'Phong cách hiện đại & lịch lãm', desc: 'Bộ sưu tập thời trang nam mới nhất', href: '/products?gender=nam', cta: 'Khám phá' },
]
const currentSlide = ref(0)
let slideTimer = null
function nextSlide() { currentSlide.value = (currentSlide.value + 1) % slides.length }
function prevSlide() { currentSlide.value = (currentSlide.value - 1 + slides.length) % slides.length }
onMounted(() => { slideTimer = setInterval(nextSlide, 5000) })
onUnmounted(() => clearInterval(slideTimer))

// Countdown
const countdown = ref({ h: 5, m: 30, s: 0 })
let cdTimer = null
function pad(n) { return String(n).padStart(2, '0') }
onMounted(() => {
  cdTimer = setInterval(() => {
    if (countdown.value.s > 0) countdown.value.s--
    else if (countdown.value.m > 0) { countdown.value.m--; countdown.value.s = 59 }
    else if (countdown.value.h > 0) { countdown.value.h--; countdown.value.m = 59; countdown.value.s = 59 }
  }, 1000)
})
onUnmounted(() => clearInterval(cdTimer))

const saleProducts = computed(() => products.value.filter(p => p.is_sale).slice(0, 5))
const newProducts = computed(() => products.value.filter(p => p.is_new).slice(0, 5))

const tabs = [
  { id: 'ao', label: 'Áo' },
  { id: 'quan', label: 'Quần' },
  { id: 'vay', label: 'Váy & Đầm' },
]
const activeTab = ref('ao')
const tabProducts = computed(() => products.value.filter(p => p.category === activeTab.value).slice(0, 5))

const catIcons = [
  { label: 'Giày', href: '/products?category=giay', img: 'https://images.unsplash.com/photo-1543163521-1bf539c55dd2?w=200&q=80' },
  { label: 'Túi', href: '/products?category=tui', img: 'https://images.unsplash.com/photo-1548036328-c9fa89d128fa?w=200&q=80' },
  { label: 'Phụ kiện', href: '/products?category=phu-kien', img: 'https://images.unsplash.com/photo-1523779105320-d1cd346ff52b?w=200&q=80' },
  { label: 'Quần áo', href: '/products?category=quan-ao', img: 'https://images.unsplash.com/photo-1558618666-fcd25c85cd64?w=200&q=80' },
  { label: 'Sale', href: '/products?sale=true', img: 'https://images.unsplash.com/photo-1607082348824-0a96f2a4b9da?w=200&q=80' },
  { label: 'Mới về', href: '/products?new=true', img: 'https://images.unsplash.com/photo-1483985988355-763728e1935b?w=200&q=80' },
]

const collections = [
  { title: 'Summer Wanted', sub: 'Bộ sưu tập', img: 'https://images.unsplash.com/photo-1496747611176-843222e1e57c?w=600&q=80', href: '/collections/summer' },
  { title: 'Dazzling Aura', sub: 'Bộ sưu tập', img: 'https://images.unsplash.com/photo-1572804013309-59a88b7e92f1?w=600&q=80', href: '/collections/dazzling' },
  { title: 'Juno\'s Club', sub: 'Bộ sưu tập', img: 'https://images.unsplash.com/photo-1551028719-00167b16eac5?w=600&q=80', href: '/collections/club' },
]

const benefits = [
  { icon: 'fas fa-truck', title: 'Miễn phí vận chuyển', desc: 'Cho đơn hàng từ 500.000đ' },
  { icon: 'fas fa-undo', title: 'Đổi trả dễ dàng', desc: 'Trong vòng 30 ngày' },
  { icon: 'fas fa-shield-alt', title: 'Bảo hành chính hãng', desc: 'Cam kết chất lượng' },
  { icon: 'fas fa-credit-card', title: 'Thanh toán an toàn', desc: 'Nhiều phương thức' },
]
</script>

<style scoped>
/* Hero */

.hero { position: relative; height: 560px; overflow: hidden; }
.hero-slides { position: relative; height: 100%; }
.hero-slide { position: absolute; inset: 0; opacity: 0; transition: opacity 0.6s; }
.hero-slide.active { opacity: 1; }
.hero-slide img { width: 100%; height: 100%; object-fit: cover; }
.hero-overlay { position: absolute; inset: 0; background: linear-gradient(to right, rgba(0,0,0,0.6) 0%, transparent 65%); display: flex; align-items: center; }
.hero-overlay .container { width: 100%; }
.hero-content { color: #fff; max-width: 520px; padding: 0; }
.hero-sub { font-size: 13px; font-weight: 600; letter-spacing: 3px; text-transform: uppercase; opacity: 0.8; margin-bottom: 16px; }
.hero-content h1 { font-size: 48px; font-weight: 800; line-height: 1.15; margin-bottom: 16px; }
.hero-desc { font-size: 15px; opacity: 0.85; margin-bottom: 28px; }
.hero-dots { position: absolute; bottom: 20px; left: 50%; transform: translateX(-50%); display: flex; gap: 8px; }
.dot { width: 8px; height: 8px; border-radius: 50%; background: rgba(255,255,255,0.5); transition: all 0.2s; }
.dot.active { background: #fff; width: 24px; border-radius: 4px; }
.hero-arrow { position: absolute; top: 50%; transform: translateY(-50%); background: rgba(255,255,255,0.2); color: #fff; width: 44px; height: 44px; border-radius: 50%; font-size: 24px; display: flex; align-items: center; justify-content: center; transition: background 0.2s; }
.hero-arrow:hover { background: rgba(255,255,255,0.4); }
.hero-arrow.prev { left: 20px; }
.hero-arrow.next { right: 20px; }

/* Flash sale */
.flash-title { display: flex; align-items: center; gap: 12px; }
.flash-icon { font-size: 20px; }
.countdown { display: flex; align-items: center; gap: 4px; font-size: 13px; font-weight: 700; }
.cd-block { background: var(--black); color: #fff; padding: 4px 8px; border-radius: 4px; min-width: 32px; text-align: center; }

/* Category icons */
.cat-icon-grid { display: grid; grid-template-columns: repeat(6, 1fr); gap: 16px; }
.cat-icon-item { display: flex; flex-direction: column; align-items: center; gap: 10px; font-size: 13px; font-weight: 500; }
.cat-icon-img { width: 80px; height: 80px; border-radius: 50%; overflow: hidden; border: 2px solid var(--gray2); transition: border-color 0.2s; }
.cat-icon-item:hover .cat-icon-img { border-color: var(--black); }
.cat-icon-img img { width: 100%; height: 100%; object-fit: cover; }

/* Banner strip */
.banner-strip { background: var(--gray); }
.banner-strip-inner { display: grid; grid-template-columns: repeat(3, 1fr); gap: 2px; }
.banner-item { position: relative; aspect-ratio: 4/3; overflow: hidden; display: block; }
.banner-item img { width: 100%; height: 100%; object-fit: cover; transition: transform 0.4s; }
.banner-item:hover img { transform: scale(1.04); }
.banner-label { position: absolute; bottom: 0; left: 0; right: 0; background: linear-gradient(transparent, rgba(0,0,0,0.6)); color: #fff; padding: 32px 20px 20px; }
.banner-label span { display: block; font-size: 18px; font-weight: 700; letter-spacing: 1px; }
.banner-label small { font-size: 12px; opacity: 0.8; }

/* Tabs */
.tab-header { display: flex; align-items: center; gap: 4px; margin-bottom: 28px; border-bottom: 1px solid var(--gray2); padding-bottom: 0; }
.tab-btn { padding: 10px 20px; font-size: 13px; font-weight: 600; color: var(--gray3); border-bottom: 2px solid transparent; margin-bottom: -1px; transition: all 0.2s; }
.tab-btn.active { color: var(--black); border-bottom-color: var(--black); }
.tab-btn:hover { color: var(--black); }

/* Collections */
.collections-grid { display: grid; grid-template-columns: repeat(3, 1fr); gap: 16px; }
.col-card { position: relative; aspect-ratio: 3/4; overflow: hidden; border-radius: 8px; display: block; }
.col-card img { width: 100%; height: 100%; object-fit: cover; transition: transform 0.4s; }
.col-card:hover img { transform: scale(1.04); }
.col-overlay { position: absolute; inset: 0; background: linear-gradient(transparent 40%, rgba(0,0,0,0.7)); display: flex; flex-direction: column; justify-content: flex-end; padding: 24px; color: #fff; }
.col-sub { font-size: 11px; letter-spacing: 2px; text-transform: uppercase; opacity: 0.7; margin-bottom: 6px; }
.col-overlay h3 { font-size: 22px; font-weight: 700; margin-bottom: 12px; }
.col-cta { font-size: 12px; font-weight: 600; letter-spacing: 1px; border-bottom: 1px solid rgba(255,255,255,0.6); padding-bottom: 2px; width: fit-content; }

/* Benefits */
.benefits { background: var(--gray); padding: 32px 0; }
.benefits-grid { display: grid; grid-template-columns: repeat(4, 1fr); gap: 24px; }
.benefit-item { display: flex; align-items: center; gap: 14px; }
.benefit-icon { width: 48px; height: 48px; background: rgba(0,0,0,0.08); border-radius: 12px; display: flex; align-items: center; justify-content: center; font-size: 20px; color: #1a1a1a; flex-shrink: 0; }
.benefit-title { font-size: 13px; font-weight: 700; margin-bottom: 2px; }
.benefit-desc { font-size: 12px; color: var(--gray3); }

/* Skeleton */
.loading-grid { display: grid; grid-template-columns: repeat(5, 1fr); gap: 16px; }
.skeleton-card { aspect-ratio: 3/4; background: linear-gradient(90deg, #f0f0f0 25%, #e0e0e0 50%, #f0f0f0 75%); background-size: 200% 100%; animation: shimmer 1.5s infinite; border-radius: 8px; }
@keyframes shimmer { 0% { background-position: 200% 0; } 100% { background-position: -200% 0; } }

@media (max-width: 900px) {
  .hero-content h1 { font-size: 32px; }
  .cat-icon-grid { grid-template-columns: repeat(3, 1fr); }
  .banner-strip-inner { grid-template-columns: 1fr; }
  .collections-grid { grid-template-columns: 1fr 1fr; }
  .benefits-grid { grid-template-columns: 1fr 1fr; }
  .loading-grid { grid-template-columns: repeat(2, 1fr); }
}

@media (max-width: 600px) {
  .hero { height: 400px; }
  .hero-content h1 { font-size: 26px; }
  .cat-icon-grid { grid-template-columns: repeat(3, 1fr); gap: 10px; }
  .collections-grid { grid-template-columns: 1fr; }
  .benefits-grid { grid-template-columns: 1fr; }
}
</style>
