<template>
  <div class="container products-page">
    <div class="page-header">
      <h1>Sản phẩm</h1>
      <p>{{ filteredProducts.length }} sản phẩm</p>
    </div>
    <div class="layout">
      <aside class="filters">
        <div class="filter-group">
          <h3>Danh mục</h3>
          <label v-for="cat in categories" :key="cat.id">
            <input type="radio" v-model="selectedCategory" :value="cat.id" /> {{ cat.name }}
          </label>
        </div>
        <div class="filter-group">
          <h3>Giới tính</h3>
          <label v-for="g in genders" :key="g.id">
            <input type="radio" v-model="selectedGender" :value="g.id" /> {{ g.name }}
          </label>
        </div>
        <div class="filter-group">
          <h3>Sắp xếp</h3>
          <select v-model="sortBy">
            <option value="default">Mặc định</option>
            <option value="price-asc">Giá tăng dần</option>
            <option value="price-desc">Giá giảm dần</option>
            <option value="rating">Đánh giá cao nhất</option>
          </select>
        </div>
        <div class="filter-group">
          <label><input type="checkbox" v-model="onlySale" /> Chỉ hàng giảm giá</label>
          <label><input type="checkbox" v-model="onlyNew" /> Chỉ hàng mới</label>
        </div>
      </aside>

      <div class="products-area">
        <div v-if="loading" class="loading">Đang tải sản phẩm...</div>
        <div v-else-if="error" class="error">{{ error }}</div>
        <div v-else-if="filteredProducts.length === 0" class="empty">Không tìm thấy sản phẩm phù hợp.</div>
        <div v-else class="products-grid">
          <ProductCard v-for="p in filteredProducts" :key="p.id" :product="p" />
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, watch, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import { useProducts } from '@/composables/useProducts.js'
import ProductCard from '@/components/ProductCard.vue'

const route = useRoute()
const { products, loading, error, fetchProducts } = useProducts()

const categories = [
  { id: 'all', name: 'Tất cả' },
  { id: 'ao', name: 'Áo' },
  { id: 'quan', name: 'Quần' },
  { id: 'vay', name: 'Váy & Đầm' },
]
const genders = [
  { id: 'all', name: 'Tất cả' },
  { id: 'nam', name: 'Nam' },
  { id: 'nu', name: 'Nữ' },
  { id: 'unisex', name: 'Unisex' },
]

const selectedCategory = ref('all')
const selectedGender = ref('all')
const sortBy = ref('default')
const onlySale = ref(false)
const onlyNew = ref(false)

watch(() => route.query, (q) => {
  if (q.gender) selectedGender.value = q.gender
  if (q.category) selectedCategory.value = q.category
  if (q.sale) onlySale.value = true
}, { immediate: true })

onMounted(() => fetchProducts())

const filteredProducts = computed(() => {
  let list = [...products.value]
  if (selectedCategory.value !== 'all') list = list.filter(p => p.category === selectedCategory.value)
  if (selectedGender.value !== 'all') list = list.filter(p => p.gender === selectedGender.value || p.gender === 'unisex')
  if (onlySale.value) list = list.filter(p => p.is_sale)
  if (onlyNew.value) list = list.filter(p => p.is_new)
  if (sortBy.value === 'price-asc') list.sort((a, b) => a.price - b.price)
  else if (sortBy.value === 'price-desc') list.sort((a, b) => b.price - a.price)
  else if (sortBy.value === 'rating') list.sort((a, b) => b.rating - a.rating)
  return list
})
</script>

<style scoped>
.products-page { padding: 40px 20px 80px; }
.page-header { display: flex; justify-content: space-between; align-items: baseline; margin-bottom: 32px; }
.page-header h1 { font-size: 28px; font-weight: 700; }
.page-header p { font-size: 14px; color: #888; }
.layout { display: grid; grid-template-columns: 220px 1fr; gap: 40px; }
.filters { display: flex; flex-direction: column; gap: 28px; }
.filter-group h3 { font-size: 13px; font-weight: 600; text-transform: uppercase; letter-spacing: 1px; margin-bottom: 12px; color: #555; }
.filter-group label { display: flex; align-items: center; gap: 8px; font-size: 14px; cursor: pointer; margin-bottom: 8px; }
.filter-group select { width: 100%; padding: 8px 12px; border: 1.5px solid #ddd; border-radius: 6px; font-size: 14px; background: #fff; }
.products-grid { display: grid; grid-template-columns: repeat(3, 1fr); gap: 20px; }
.loading, .error, .empty { text-align: center; padding: 60px; color: #888; font-size: 16px; }
.error { color: #e53e3e; }
@media (max-width: 1024px) { .products-grid { grid-template-columns: repeat(2, 1fr); } }
@media (max-width: 768px) { .layout { grid-template-columns: 1fr; } .filters { flex-direction: row; flex-wrap: wrap; } }
</style>
