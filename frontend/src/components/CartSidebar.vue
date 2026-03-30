<template>
  <Transition name="slide">
    <div v-if="cart.isOpen" class="overlay" @click.self="cart.isOpen = false">
      <div class="sidebar">
        <div class="header">
          <h2>Giỏ hàng ({{ cart.totalItems }})</h2>
          <button @click="cart.isOpen = false" aria-label="Đóng">
            <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <line x1="18" y1="6" x2="6" y2="18"/><line x1="6" y1="6" x2="18" y2="18"/>
            </svg>
          </button>
        </div>

        <div v-if="cart.items.length === 0" class="empty">
          <p>Giỏ hàng trống</p>
          <RouterLink to="/products" class="btn btn-dark" @click="cart.isOpen = false">Mua sắm ngay</RouterLink>
        </div>

        <div v-else class="items">
          <div v-for="item in cart.items" :key="`${item.id}-${item.size}-${item.color}`" class="item">
            <img :src="item.image" :alt="item.name" />
            <div class="item-info">
              <p class="name">{{ item.name }}</p>
              <p class="meta">{{ item.size }} · {{ item.color }}</p>
              <p class="price">{{ formatPrice(item.price) }}</p>
              <div class="qty">
                <button @click="cart.updateQuantity(item.id, item.size, item.color, item.quantity - 1)">−</button>
                <span>{{ item.quantity }}</span>
                <button @click="cart.updateQuantity(item.id, item.size, item.color, item.quantity + 1)">+</button>
              </div>
            </div>
            <button class="remove" @click="cart.removeItem(item.id, item.size, item.color)" aria-label="Xóa">
              <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <line x1="18" y1="6" x2="6" y2="18"/><line x1="6" y1="6" x2="18" y2="18"/>
              </svg>
            </button>
          </div>
        </div>

        <div v-if="cart.items.length > 0" class="footer">
          <div class="total-row">
            <span>Tổng cộng</span>
            <span class="total">{{ formatPrice(cart.totalPrice) }}</span>
          </div>
          <RouterLink to="/cart" class="btn btn-dark checkout-btn" @click="cart.isOpen = false">
            Xem giỏ hàng & Thanh toán
          </RouterLink>
        </div>
      </div>
    </div>
  </Transition>
</template>

<script setup>
import { useCartStore } from '@/stores/cart.js'
import { formatPrice } from '@/utils/format.js'
const cart = useCartStore()
</script>

<style scoped>
.overlay { position: fixed; inset: 0; background: rgba(0,0,0,0.4); z-index: 200; display: flex; justify-content: flex-end; }
.sidebar { width: 400px; max-width: 100vw; background: #fff; height: 100%; display: flex; flex-direction: column; }
.header { display: flex; justify-content: space-between; align-items: center; padding: 20px 24px; border-bottom: 1px solid #eee; }
.header h2 { font-size: 18px; font-weight: 600; }
.header button { background: none; color: #555; }
.empty { flex: 1; display: flex; flex-direction: column; align-items: center; justify-content: center; gap: 16px; color: #888; }
.items { flex: 1; overflow-y: auto; padding: 16px 24px; display: flex; flex-direction: column; gap: 16px; }
.item { display: flex; gap: 12px; position: relative; }
.item img { width: 80px; height: 80px; object-fit: cover; border-radius: 8px; }
.item-info { flex: 1; }
.name { font-size: 14px; font-weight: 500; margin-bottom: 4px; }
.meta { font-size: 12px; color: #888; margin-bottom: 4px; }
.price { font-size: 14px; font-weight: 600; margin-bottom: 8px; }
.qty { display: flex; align-items: center; gap: 10px; }
.qty button { background: #f0f0f0; width: 26px; height: 26px; border-radius: 4px; font-size: 16px; display: flex; align-items: center; justify-content: center; }
.qty span { font-size: 14px; font-weight: 500; }
.remove { background: none; color: #aaa; align-self: flex-start; padding: 4px; }
.footer { padding: 20px 24px; border-top: 1px solid #eee; }
.total-row { display: flex; justify-content: space-between; margin-bottom: 16px; font-size: 16px; }
.total { font-weight: 700; }
.checkout-btn { display: block; text-align: center; width: 100%; padding: 13px; font-size: 14px; font-weight: 600; background: var(--black); color: #fff; border-radius: 4px; transition: background 0.2s; }
.checkout-btn:hover { background: #333; }
.slide-enter-active, .slide-leave-active { transition: opacity 0.25s; }
.slide-enter-from, .slide-leave-to { opacity: 0; }
.slide-enter-from .sidebar, .slide-leave-to .sidebar { transform: translateX(100%); }
.slide-enter-active .sidebar, .slide-leave-active .sidebar { transition: transform 0.25s ease; }
</style>
