<template>
  <div class="container detail-page">
    <div v-if="loading" class="loading">Đang tải...</div>
    <div v-else-if="error" class="error">{{ error }}</div>
    <template v-else-if="product">
      <div class="breadcrumb">
        <RouterLink to="/">Trang chủ</RouterLink> /
        <RouterLink to="/products">Sản phẩm</RouterLink> /
        <span>{{ product.name }}</span>
      </div>
      <div class="layout">
        <div class="images">
          <div class="main-img">
            <img :src="activeImage" :alt="product.name" />
          </div>
          <div class="thumbs">
            <img v-for="(img, i) in product.images" :key="i" :src="img"
              :class="{ active: activeImage === img }" @click="activeImage = img" :alt="`${product.name} ${i+1}`" />
          </div>
        </div>

        <div class="info">
          <div class="badges">
            <span v-if="product.is_new" class="badge new">Mới</span>
            <span v-if="product.is_sale" class="badge sale">Sale</span>
          </div>
          <h1>{{ product.name }}</h1>
          <div class="rating">
            <span class="stars">★ {{ product.rating }}</span>
            <span class="reviews">{{ product.reviews }} đánh giá</span>
          </div>
          <div class="price-row">
            <span class="price">{{ formatPrice(product.price) }}</span>
            <span v-if="product.original_price > product.price" class="original">{{ formatPrice(product.original_price) }}</span>
            <span v-if="product.is_sale" class="discount">-{{ discountPercent(product.original_price, product.price) }}%</span>
          </div>
          <p class="desc">{{ product.description }}</p>

          <div class="option-group">
            <p class="opt-label">Màu sắc: <strong>{{ selectedColor }}</strong></p>
            <div class="opts">
              <button v-for="c in product.colors" :key="c" :class="['opt-btn', { active: selectedColor === c }]" @click="selectedColor = c">{{ c }}</button>
            </div>
          </div>

          <div class="option-group">
            <p class="opt-label">Kích thước: <strong>{{ selectedSize }}</strong></p>
            <div class="opts">
              <button v-for="s in product.sizes" :key="s" :class="['opt-btn', { active: selectedSize === s }]" @click="selectedSize = s">{{ s }}</button>
            </div>
          </div>

          <div class="action-row">
            <button class="btn btn-dark add-btn" @click="addToCart" :disabled="!selectedSize || !selectedColor">
              <i class="fas fa-shopping-cart"></i> Thêm vào giỏ hàng
            </button>
            <button :class="['wish-toggle', { active: wishlist.isWishlisted(product.id) }]" @click="toggleWish" aria-label="Yêu thích">
              <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <path d="M20.84 4.61a5.5 5.5 0 00-7.78 0L12 5.67l-1.06-1.06a5.5 5.5 0 00-7.78 7.78l1.06 1.06L12 21.23l7.78-7.78 1.06-1.06a5.5 5.5 0 000-7.78z"/>
              </svg>
            </button>
          </div>

          <div class="meta">
            <p>Danh mục: <span>{{ product.category }}</span></p>
            <p>Miễn phí vận chuyển cho đơn từ 500.000đ</p>
          </div>
        </div>
      </div>
    </template>
  </div>
</template>

<script setup>
import { ref, watch } from 'vue'
import { useRoute } from 'vue-router'
import { useProduct } from '@/composables/useProducts.js'
import { useCartStore } from '@/stores/cart.js'
import { useWishlistStore } from '@/stores/wishlist.js'
import { useToastStore } from '@/stores/toast.js'
import { formatPrice, discountPercent } from '@/utils/format.js'

const route = useRoute()
const cart = useCartStore()
const wishlist = useWishlistStore()
const toast = useToastStore()
const { product, loading, error, fetchProduct } = useProduct()

const activeImage = ref('')
const selectedSize = ref('')
const selectedColor = ref('')

watch(product, (p) => {
  if (p) {
    activeImage.value = p.images?.[0] || p.image
    selectedSize.value = p.sizes?.[0] || ''
    selectedColor.value = p.colors?.[0] || ''
  }
}, { immediate: true })

watch(() => route.params.id, (id) => fetchProduct(id), { immediate: true })

function addToCart() {
  if (!selectedSize.value || !selectedColor.value) return
  cart.addItem(product.value, selectedSize.value, selectedColor.value)
  toast.success('Đã thêm vào giỏ hàng!')
}

function toggleWish() {
  const added = wishlist.toggle(product.value)
  toast[added ? 'success' : 'info'](added ? 'Đã thêm vào yêu thích' : 'Đã xóa khỏi yêu thích')
}
</script>

<style scoped>
.detail-page { padding: 32px 20px 80px; }
.loading, .error { text-align: center; padding: 80px; color: #888; }
.error { color: #e53e3e; }
.breadcrumb { font-size: 13px; color: #888; margin-bottom: 32px; }
.breadcrumb a { color: #888; } .breadcrumb a:hover { color: #1a1a1a; } .breadcrumb span { color: #1a1a1a; }
.layout { display: grid; grid-template-columns: 1fr 1fr; gap: 60px; }
.images { display: flex; flex-direction: column; gap: 12px; }
.main-img { border-radius: 12px; overflow: hidden; aspect-ratio: 3/4; }
.main-img img { width: 100%; height: 100%; object-fit: cover; }
.thumbs { display: flex; gap: 10px; }
.thumbs img { width: 72px; height: 72px; object-fit: cover; border-radius: 8px; cursor: pointer; border: 2px solid transparent; transition: border-color 0.2s; }
.thumbs img.active { border-color: #1a1a1a; }
.info { display: flex; flex-direction: column; gap: 20px; }
.badges { display: flex; gap: 8px; }
.badge { padding: 4px 10px; border-radius: 4px; font-size: 12px; font-weight: 600; }
.badge.new { background: #1a1a1a; color: #fff; } .badge.sale { background: #e53e3e; color: #fff; }
.info h1 { font-size: 28px; font-weight: 700; line-height: 1.2; }
.rating { display: flex; align-items: center; gap: 8px; }
.stars { color: #f59e0b; font-size: 15px; } .reviews { font-size: 14px; color: #888; }
.price-row { display: flex; align-items: center; gap: 12px; }
.price { font-size: 26px; font-weight: 700; }
.original { font-size: 18px; color: #aaa; text-decoration: line-through; }
.discount { background: #fef2f2; color: #e53e3e; font-size: 13px; font-weight: 600; padding: 3px 8px; border-radius: 4px; }
.desc { font-size: 15px; color: #555; line-height: 1.7; }
.opt-label { font-size: 14px; margin-bottom: 10px; }
.opts { display: flex; flex-wrap: wrap; gap: 8px; }
.opt-btn { padding: 8px 16px; border-radius: 6px; font-size: 13px; font-weight: 500; border: 1.5px solid #ddd; background: #fff; transition: all 0.2s; }
.opt-btn.active { border-color: #1a1a1a; background: #1a1a1a; color: #fff; }
.add-btn { flex: 1; padding: 14px; font-size: 15px; }
.add-btn:disabled { opacity: 0.5; cursor: not-allowed; }
.action-row { display: flex; gap: 10px; }
.wish-toggle { width: 50px; height: 50px; border: 1.5px solid var(--gray2); border-radius: 6px; display: flex; align-items: center; justify-content: center; color: #aaa; transition: all 0.2s; background: #fff; flex-shrink: 0; }
.wish-toggle:hover { border-color: var(--red); color: var(--red); }
.wish-toggle.active { border-color: var(--red); color: var(--red); background: #fff5f5; }
.wish-toggle.active svg { fill: var(--red); }
.meta { font-size: 13px; color: #888; display: flex; flex-direction: column; gap: 6px; }
.meta span { color: #1a1a1a; }
@media (max-width: 768px) { .layout { grid-template-columns: 1fr; gap: 32px; } }
</style>
