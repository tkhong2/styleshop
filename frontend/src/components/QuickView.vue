<template>
  <Transition name="fade">
    <div v-if="product" class="qv-overlay" @click.self="$emit('close')">
      <div class="qv-modal">
        <button class="qv-close" @click="$emit('close')">
          <i class="fas fa-times"></i>
        </button>
        <div class="qv-layout">
          <div class="qv-img">
            <img :src="activeImg" :alt="product.name" />
            <div class="qv-thumbs">
              <img v-for="(img, i) in product.images" :key="i" :src="img"
                :class="{ active: activeImg === img }" @click="activeImg = img" />
            </div>
          </div>
          <div class="qv-info">
            <div class="badges">
              <span v-if="product.is_new" class="badge-new">Mới</span>
              <span v-if="product.is_sale" class="badge-sale">Sale</span>
            </div>
            <h2>{{ product.name }}</h2>
            <div class="rating">
              <span class="stars">★ {{ product.rating }}</span>
              <span class="reviews">({{ product.reviews }} đánh giá)</span>
            </div>
            <div class="price-row">
              <span class="price">{{ formatPrice(product.price) }}</span>
              <span v-if="product.original_price > product.price" class="original">{{ formatPrice(product.original_price) }}</span>
              <span v-if="product.is_sale" class="discount">-{{ discountPercent(product.original_price, product.price) }}%</span>
            </div>
            <p class="desc">{{ product.description }}</p>

            <div class="opt-group">
              <p class="opt-label">Màu: <strong>{{ selectedColor }}</strong></p>
              <div class="opts">
                <button v-for="c in product.colors" :key="c"
                  :class="['opt-btn', { active: selectedColor === c }]" @click="selectedColor = c">{{ c }}</button>
              </div>
            </div>
            <div class="opt-group">
              <p class="opt-label">Size: <strong>{{ selectedSize }}</strong></p>
              <div class="opts">
                <button v-for="s in product.sizes" :key="s"
                  :class="['opt-btn', { active: selectedSize === s }]" @click="selectedSize = s">{{ s }}</button>
              </div>
            </div>

            <div class="qv-actions">
              <button class="btn btn-dark add-btn" @click="addToCart">
                <i class="fas fa-shopping-cart"></i> Thêm vào giỏ
              </button>
              <RouterLink :to="`/products/${product.id}`" class="btn btn-outline" @click="$emit('close')">
                Xem chi tiết
              </RouterLink>
            </div>
          </div>
        </div>
      </div>
    </div>
  </Transition>
</template>

<script setup>
import { ref, watch } from 'vue'
import { useCartStore } from '@/stores/cart.js'
import { useToastStore } from '@/stores/toast.js'
import { formatPrice, discountPercent } from '@/utils/format.js'

const props = defineProps({ product: Object })
const emit = defineEmits(['close'])
const cart = useCartStore()
const toast = useToastStore()

const activeImg = ref('')
const selectedSize = ref('')
const selectedColor = ref('')

watch(() => props.product, (p) => {
  if (p) {
    activeImg.value = p.images?.[0] || p.image
    selectedSize.value = p.sizes?.[0] || ''
    selectedColor.value = p.colors?.[0] || ''
  }
}, { immediate: true })

function addToCart() {
  cart.addItem(props.product, selectedSize.value, selectedColor.value)
  toast.success('Đã thêm vào giỏ hàng!')
  emit('close')
}
</script>

<style scoped>
.qv-overlay { position: fixed; inset: 0; background: rgba(0,0,0,0.5); z-index: 500; display: flex; align-items: center; justify-content: center; padding: 20px; }
.qv-modal { background: #fff; border-radius: 16px; width: 100%; max-width: 860px; max-height: 90vh; overflow-y: auto; position: relative; }
.qv-close { position: absolute; top: 16px; right: 16px; background: #f1f5f9; border-radius: 50%; width: 36px; height: 36px; display: flex; align-items: center; justify-content: center; color: #555; z-index: 1; }
.qv-close:hover { background: #e2e8f0; }
.qv-layout { display: grid; grid-template-columns: 1fr 1fr; gap: 0; }
.qv-img { padding: 24px; }
.qv-img > img { width: 100%; aspect-ratio: 3/4; object-fit: cover; border-radius: 10px; }
.qv-thumbs { display: flex; gap: 8px; margin-top: 10px; }
.qv-thumbs img { width: 56px; height: 56px; object-fit: cover; border-radius: 6px; cursor: pointer; border: 2px solid transparent; }
.qv-thumbs img.active { border-color: var(--black); }
.qv-info { padding: 24px 24px 24px 0; display: flex; flex-direction: column; gap: 14px; }
.badges { display: flex; gap: 6px; }
.qv-info h2 { font-size: 20px; font-weight: 700; line-height: 1.3; }
.rating { display: flex; align-items: center; gap: 6px; }
.stars { color: #f59e0b; } .reviews { font-size: 13px; color: #888; }
.price-row { display: flex; align-items: center; gap: 10px; }
.price { font-size: 22px; font-weight: 800; }
.original { font-size: 15px; color: #aaa; text-decoration: line-through; }
.discount { background: #fef2f2; color: var(--red); font-size: 12px; font-weight: 700; padding: 2px 8px; border-radius: 4px; }
.desc { font-size: 13px; color: #555; line-height: 1.6; }
.opt-label { font-size: 13px; margin-bottom: 8px; }
.opts { display: flex; flex-wrap: wrap; gap: 6px; }
.opt-btn { padding: 6px 14px; border-radius: 6px; font-size: 12px; font-weight: 500; border: 1.5px solid #ddd; background: #fff; transition: all 0.15s; }
.opt-btn.active { border-color: var(--black); background: var(--black); color: #fff; }
.qv-actions { display: flex; gap: 10px; margin-top: 4px; }
.add-btn { flex: 1; padding: 12px; font-size: 14px; display: flex; align-items: center; justify-content: center; gap: 8px; }
.fade-enter-active, .fade-leave-active { transition: opacity 0.2s; }
.fade-enter-from, .fade-leave-to { opacity: 0; }
@media (max-width: 640px) { .qv-layout { grid-template-columns: 1fr; } .qv-info { padding: 0 16px 24px; } }
</style>
