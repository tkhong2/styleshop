<template>
  <div class="container page">
    <h1 class="page-title">Sản phẩm yêu thích ({{ wishlist.items.length }})</h1>
    <div v-if="wishlist.items.length === 0" class="empty">
      <svg width="64" height="64" viewBox="0 0 24 24" fill="none" stroke="#ccc" stroke-width="1.5">
        <path d="M20.84 4.61a5.5 5.5 0 00-7.78 0L12 5.67l-1.06-1.06a5.5 5.5 0 00-7.78 7.78l1.06 1.06L12 21.23l7.78-7.78 1.06-1.06a5.5 5.5 0 000-7.78z"/>
      </svg>
      <p>Chưa có sản phẩm yêu thích</p>
      <RouterLink to="/products" class="btn btn-dark">Khám phá ngay</RouterLink>
    </div>
    <div v-else class="products-grid">
      <ProductCard v-for="p in wishlist.items" :key="p.id" :product="p" />
    </div>
  </div>
</template>

<script setup>
import { useWishlistStore } from '@/stores/wishlist.js'
import ProductCard from '@/components/ProductCard.vue'
const wishlist = useWishlistStore()
</script>

<style scoped>
.page { padding: 40px 20px 80px; }
.page-title { font-size: 24px; font-weight: 700; margin-bottom: 32px; }
.empty { display: flex; flex-direction: column; align-items: center; gap: 16px; padding: 80px 20px; color: #888; }
</style>
