<template>
  <nav class="bottom-nav">
    <RouterLink to="/" class="nav-item" exact-active-class="active">
      <i class="fas fa-home"></i>
      <span>Trang chủ</span>
    </RouterLink>
    <RouterLink to="/products" class="nav-item" active-class="active">
      <i class="fas fa-th-large"></i>
      <span>Sản phẩm</span>
    </RouterLink>
    <button class="nav-item cart-center" @click="cart.isOpen = true">
      <div class="cart-bubble">
        <i class="fas fa-shopping-bag"></i>
        <span v-if="cart.totalItems > 0" class="cart-badge">{{ cart.totalItems }}</span>
      </div>
    </button>
    <RouterLink to="/wishlist" class="nav-item" active-class="active">
      <i class="fas fa-heart"></i>
      <span>Yêu thích</span>
    </RouterLink>
    <RouterLink v-if="auth.isLoggedIn" to="/profile" class="nav-item" active-class="active">
      <i class="fas fa-user"></i>
      <span>Tài khoản</span>
    </RouterLink>
    <RouterLink v-else to="/login" class="nav-item" active-class="active">
      <i class="fas fa-user"></i>
      <span>Đăng nhập</span>
    </RouterLink>
  </nav>
</template>

<script setup>
import { useCartStore } from '@/stores/cart.js'
import { useAuthStore } from '@/stores/auth.js'
const cart = useCartStore()
const auth = useAuthStore()
</script>

<style scoped>
.bottom-nav {
  display: none;
  position: fixed;
  bottom: 0; left: 0; right: 0;
  background: #fff;
  border-top: 1px solid #e2e8f0;
  z-index: 90;
  padding: 6px 0 env(safe-area-inset-bottom, 6px);
  box-shadow: 0 -4px 16px rgba(0,0,0,0.08);
}

.nav-item {
  flex: 1;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 3px;
  padding: 6px 4px;
  color: #94a3b8;
  font-size: 10px;
  font-weight: 500;
  background: none;
  border: none;
  cursor: pointer;
  transition: color 0.15s;
  text-decoration: none;
}

.nav-item i { font-size: 20px; }
.nav-item.active { color: #1a1a1a; }
.nav-item.active i { color: #1a1a1a; }

/* Center cart button */
.cart-center {
  flex: 1;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 0;
  margin-top: -16px;
}

.cart-bubble {
  width: 52px;
  height: 52px;
  background: #1a1a1a;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  position: relative;
  box-shadow: 0 4px 12px rgba(0,0,0,0.25);
}

.cart-bubble i { font-size: 20px; color: #fff; }

.cart-badge {
  position: absolute;
  top: -2px; right: -2px;
  background: #ef4444;
  color: #fff;
  font-size: 9px;
  font-weight: 700;
  width: 18px; height: 18px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  border: 2px solid #fff;
}

@media (max-width: 768px) {
  .bottom-nav { display: flex; }
}
</style>
