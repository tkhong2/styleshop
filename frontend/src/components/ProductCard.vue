<template>
  <div class="product-card" @mouseenter="hovered = true" @mouseleave="hovered = false">
    <div class="card-img-wrap">
      <RouterLink :to="`/products/${product.id}`">
        <img :src="product.image" :alt="product.name" loading="lazy" class="card-img" />
      </RouterLink>

      <!-- Badges -->
      <div class="card-badges">
        <span v-if="product.is_sale" class="badge-sale">-{{ discountPercent(product.original_price, product.price) }}%</span>
        <span v-else-if="product.is_new" class="badge-new">Mới</span>
      </div>

      <!-- Wishlist btn -->
      <button class="wish-btn" :class="{ active: wishlist.isWishlisted(product.id) }"
        @click.prevent="toggleWish" aria-label="Yêu thích">
        <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
          <path d="M20.84 4.61a5.5 5.5 0 00-7.78 0L12 5.67l-1.06-1.06a5.5 5.5 0 00-7.78 7.78l1.06 1.06L12 21.23l7.78-7.78 1.06-1.06a5.5 5.5 0 000-7.78z"/>
        </svg>
      </button>

      <!-- Quick add overlay -->
      <Transition name="fade-up">
        <div v-if="hovered" class="quick-add">
          <button class="quick-view-btn" @click.stop="$emit('quickview', product)">
            <i class="fas fa-eye"></i> Xem nhanh
          </button>
        </div>
      </Transition>
    </div>

    <div class="card-body">
      <!-- Color swatches -->
      <div v-if="product.colors?.length" class="color-swatches">
        <span v-for="c in product.colors.slice(0, 4)" :key="c" class="swatch" :title="c"
          :style="{ background: colorMap[c] || '#ccc' }"></span>
        <span v-if="product.colors.length > 4" class="swatch-more">+{{ product.colors.length - 4 }}</span>
      </div>

      <RouterLink :to="`/products/${product.id}`" class="card-name">{{ product.name }}</RouterLink>

      <div class="card-price">
        <span class="price">{{ formatPrice(product.price) }}</span>
        <span v-if="product.original_price > product.price" class="price-original">{{ formatPrice(product.original_price) }}</span>
      </div>

      <div class="card-rating">
        <span class="stars">★ {{ product.rating }}</span>
        <span class="review-count">({{ product.reviews }})</span>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useWishlistStore } from '@/stores/wishlist.js'
import { useToastStore } from '@/stores/toast.js'
import { formatPrice, discountPercent } from '@/utils/format.js'

const props = defineProps({ product: Object })
const emit = defineEmits(['quickview'])
const wishlist = useWishlistStore()
const toast = useToastStore()
const hovered = ref(false)

const colorMap = {
  'Trắng': '#f5f5f5', 'Trắng kem': '#f5f0e8', 'Đen': '#1a1a1a', 'Xám': '#9e9e9e',
  'Đỏ': '#e53e3e', 'Hồng': '#f9a8d4', 'Xanh': '#3b82f6', 'Xanh navy': '#1e3a5f',
  'Xanh đậm': '#1e40af', 'Xanh nhạt': '#93c5fd', 'Xanh rêu': '#4d7c0f',
  'Nâu': '#92400e', 'Be': '#d4b896', 'Vàng': '#fbbf24', 'Olive': '#6b7280',
  'Kem': '#f5e6c8', 'Bạc': '#d1d5db', 'Vàng đồng': '#b45309',
}

function toggleWish() {
  const added = wishlist.toggle(props.product)
  toast[added ? 'success' : 'info'](added ? 'Đã thêm vào yêu thích' : 'Đã xóa khỏi yêu thích')
}
</script>

<style scoped>
.product-card { display: flex; flex-direction: column; }

.card-img-wrap { position: relative; aspect-ratio: 3/4; overflow: hidden; border-radius: 8px; background: var(--gray); }
.card-img { width: 100%; height: 100%; object-fit: cover; transition: transform 0.4s ease; }
.product-card:hover .card-img { transform: scale(1.04); }

.card-badges { position: absolute; top: 8px; left: 8px; display: flex; flex-direction: column; gap: 4px; }

.wish-btn { position: absolute; top: 8px; right: 8px; background: rgba(255,255,255,0.9); border-radius: 50%; width: 34px; height: 34px; display: flex; align-items: center; justify-content: center; color: #aaa; transition: all 0.2s; opacity: 0; }
.product-card:hover .wish-btn, .wish-btn.active { opacity: 1; }
.wish-btn.active { color: var(--red); }
.wish-btn.active svg { fill: var(--red); stroke: var(--red); }
.wish-btn:hover { background: #fff; color: var(--red); }

.quick-add { position: absolute; bottom: 0; left: 0; right: 0; padding: 10px; }
.quick-view-btn { display: flex; align-items: center; justify-content: center; gap: 6px; width: 100%; background: #1a1a1a; color: #fff; font-size: 12px; font-weight: 600; padding: 11px; border-radius: 4px; border: none; cursor: pointer; transition: background 0.2s; }
.quick-view-btn:hover { background: #333; }

.card-body { padding: 10px 2px 0; display: flex; flex-direction: column; gap: 5px; }

.color-swatches { display: flex; align-items: center; gap: 4px; }
.swatch { width: 14px; height: 14px; border-radius: 50%; border: 1px solid rgba(0,0,0,0.1); flex-shrink: 0; }
.swatch-more { font-size: 11px; color: var(--gray3); }

.card-name { font-size: 13px; font-weight: 500; color: var(--black); line-height: 1.4; display: -webkit-box; -webkit-line-clamp: 2; -webkit-box-orient: vertical; overflow: hidden; }
.card-name:hover { text-decoration: underline; }

.card-price { display: flex; align-items: center; gap: 8px; }
.price { font-size: 14px; font-weight: 700; }
.price-original { font-size: 12px; color: var(--gray3); text-decoration: line-through; }

.card-rating { display: flex; align-items: center; gap: 4px; }
.stars { font-size: 12px; color: #f59e0b; }
.review-count { font-size: 11px; color: var(--gray3); }

.fade-up-enter-active, .fade-up-leave-active { transition: all 0.2s; }
.fade-up-enter-from, .fade-up-leave-to { opacity: 0; transform: translateY(8px); }
</style>
