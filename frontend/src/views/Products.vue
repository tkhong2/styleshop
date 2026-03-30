<template>
  <div class="container products-page">
    <div class="page-header">
      <h1>Sản phẩm</h1>
      <p>{{ filteredProducts.length }} sản phẩm</p>
    </div>
    <div class="layout">
      <!-- Filters sidebar -->
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

        <!-- Price range filter -->
        <div class="filter-group">
          <h3>Khoảng giá</h3>
          <div class="price-range">
            <div class="price-labels">
              <span>{{ formatPrice(priceMin) }}</span>
              <span>{{ formatPrice(priceMax) }}</span>
            </div>
            <input type="range" v-model.number="priceMin" :min="0" :max="priceMax - 50000" step="50000" class="range-slider" />
            <input type="range" v-model.number="priceMax" :min="priceMin + 50000" :max="1500000" step="50000" class="range-slider" />
          </div>
        </div>

        <div class="filter-group">
          <h3>Sắp xếp</h3>
          <select v-model="sortBy">
            <option value="default">Mặc định</option>
            <option value="price-asc">Giá tăng dần</option>
            <option value="price-desc">Giá giảm dần</option>
            <option value="rating">Đánh giá cao nhất</option>
            <option value="newest">Mới nhất</option>
          </select>
        </div>
        <div class="filter-group">
          <label><input type="checkbox" v-model="onlySale" /> Chỉ hàng giảm giá</label>
          <label><input type="checkbox" v-model="onlyNew" /> Chỉ hàng mới</label>
        </div>

        <button v-if="hasActiveFilter" class="reset-btn" @click="resetFilters">
          <i class="fas fa-times"></i> Xóa bộ lọc
        </button>
      </aside>

      <div class="products-area">
        <div v-if="loading" class="loading">
          <div class="skeleton-grid">
            <div v-for="i in 6" :key="i" class="skeleton-card"></div>
          </div>
        </div>
        <div v-else-if="error" class="error">{{ error }}</div>
        <div v-else-if="filteredProducts.length === 0" class="empty">
          <i class="fas fa-search" style="font-size:40px;color:#ddd;margin-bottom:12px"></i>
          <p>Không tìm thấy sản phẩm phù hợp.</p>
          <button class="btn btn-outline" @click="resetFilters">Xóa bộ lọc</button>
        </div>
        <div v-else class="products-grid">
          <ProductCard v-for="p in pagedProducts" :key="p.id" :product="p" @quickview="openQuickView" />
        </div>

        <!-- Pagination -->
        <div v-if="totalPages > 1" class="pagination">
          <button :disabled="page === 1" @click="page--; scrollTop()">
            <i class="fas fa-chevron-left"></i>
          </button>
          <template v-for="n in totalPages" :key="n">
            <button v-if="n === 1 || n === totalPages || Math.abs(n - page) <= 1"
              :class="{ active: page === n }" @click="page = n; scrollTop()">{{ n }}</button>
            <span v-else-if="Math.abs(n - page) === 2" class="page-dots">...</span>
          </template>
          <button :disabled="page === totalPages" @click="page++; scrollTop()">
            <i class="fas fa-chevron-right"></i>
          </button>
        </div>
      </div>
    </div>

    <!-- Recently viewed -->
    <div v-if="history.items.length > 0" class="recently-viewed">
      <h2 class="section-title">Đã xem gần đây</h2>
      <div class="recent-grid">
        <ProductCard v-for="p in history.items.slice(0,5)" :key="p.id" :product="p" @quickview="openQuickView" />
      </div>
    </div>

    <!-- Quick View -->
    <QuickView :product="qvProduct" @close="qvProduct = null" />
    <!-- Quick View -->
    <QuickView :product="qvProduct" @close="qvProduct = null" />
  </div>
</template>

<script setup>
import { ref, computed, watch, onMounted, inject } from 'vue'
import { useRoute } from 'vue-router'
import { useProducts } from '@/composables/useProducts.js'
import { useHistoryStore } from '@/stores/history.js'
import { formatPrice } from '@/utils/format.js'
import ProductCard from '@/components/ProductCard.vue'
import QuickView from '@/components/QuickView.vue'

const route = useRoute()
const { products, loading, error, fetchProducts } = useProducts()
const history = useHistoryStore()

const categories = [
  { id: 'all', name: 'Tất cả' },
  { id: 'ao', name: 'Áo' },
  { id: 'quan', name: 'Quần' },
  { id: 'vay', name: 'Váy & Đầm' },
  { id: 'giay', name: 'Giày' },
  { id: 'tui', name: 'Túi' },
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
const priceMin = ref(0)
const priceMax = ref(1500000)
const page = ref(1)
const PER_PAGE = 12
const qvProduct = ref(null)

const hasActiveFilter = computed(() =>
  selectedCategory.value !== 'all' || selectedGender.value !== 'all' ||
  onlySale.value || onlyNew.value || priceMin.value > 0 || priceMax.value < 1500000
)

function resetFilters() {
  selectedCategory.value = 'all'
  selectedGender.value = 'all'
  onlySale.value = false
  onlyNew.value = false
  priceMin.value = 0
  priceMax.value = 1500000
  sortBy.value = 'default'
  page.value = 1
}

function openQuickView(product) { qvProduct.value = product }
watch(() => route.query, (q) => {
  if (q.gender) selectedGender.value = q.gender
  if (q.category) selectedCategory.value = q.category
  if (q.sale) onlySale.value = true
  if (q.new) onlyNew.value = true
  if (q.q) {} // search handled by backend
  page.value = 1
}, { immediate: true })

watch([selectedCategory, selectedGender, sortBy, onlySale, onlyNew, priceMin, priceMax], () => { page.value = 1 })

onMounted(() => fetchProducts())

const filteredProducts = computed(() => {
  let list = [...products.value]
  if (selectedCategory.value !== 'all') list = list.filter(p => p.category === selectedCategory.value)
  if (selectedGender.value !== 'all') list = list.filter(p => p.gender === selectedGender.value || p.gender === 'unisex')
  if (onlySale.value) list = list.filter(p => p.is_sale)
  if (onlyNew.value) list = list.filter(p => p.is_new)
  list = list.filter(p => p.price >= priceMin.value && p.price <= priceMax.value)
  if (sortBy.value === 'price-asc') list.sort((a, b) => a.price - b.price)
  else if (sortBy.value === 'price-desc') list.sort((a, b) => b.price - a.price)
  else if (sortBy.value === 'rating') list.sort((a, b) => b.rating - a.rating)
  else if (sortBy.value === 'newest') list.sort((a, b) => (b.is_new ? 1 : 0) - (a.is_new ? 1 : 0))
  return list
})

const totalPages = computed(() => Math.ceil(filteredProducts.value.length / PER_PAGE))
const pagedProducts = computed(() => filteredProducts.value.slice((page.value - 1) * PER_PAGE, page.value * PER_PAGE))

function scrollTop() { window.scrollTo({ top: 0, behavior: 'smooth' }) }
</script>

<style scoped>
.products-page { padding: 40px 20px 80px; }
.page-header { display: flex; justify-content: space-between; align-items: baseline; margin-bottom: 32px; }
.page-header h1 { font-size: 28px; font-weight: 700; }
.page-header p { font-size: 14px; color: #888; }
.layout { display: grid; grid-template-columns: 220px 1fr; gap: 40px; }

/* Filters */
.filters { display: flex; flex-direction: column; gap: 24px; }
.filter-group h3 { font-size: 11px; font-weight: 700; text-transform: uppercase; letter-spacing: 1px; margin-bottom: 12px; color: #555; }
.filter-group label { display: flex; align-items: center; gap: 8px; font-size: 13px; cursor: pointer; margin-bottom: 8px; }
.filter-group select { width: 100%; padding: 8px 12px; border: 1.5px solid #ddd; border-radius: 6px; font-size: 13px; background: #fff; }

/* Price range */
.price-range { display: flex; flex-direction: column; gap: 8px; }
.price-labels { display: flex; justify-content: space-between; font-size: 12px; font-weight: 600; color: #333; }
.range-slider { width: 100%; accent-color: var(--black); }

.reset-btn { display: flex; align-items: center; gap: 6px; padding: 8px 14px; border: 1.5px solid #ddd; border-radius: 6px; font-size: 13px; color: #555; background: #fff; transition: all 0.15s; }
.reset-btn:hover { border-color: var(--red); color: var(--red); }

/* Products */
.products-grid { display: grid; grid-template-columns: repeat(3, 1fr); gap: 20px; }
.loading, .error, .empty { text-align: center; padding: 60px; color: #888; font-size: 15px; display: flex; flex-direction: column; align-items: center; gap: 12px; }
.error { color: #e53e3e; }

/* Skeleton */
.skeleton-grid { display: grid; grid-template-columns: repeat(3, 1fr); gap: 20px; }
.skeleton-card { aspect-ratio: 3/4; background: linear-gradient(90deg, #f0f0f0 25%, #e8e8e8 50%, #f0f0f0 75%); background-size: 200% 100%; animation: shimmer 1.5s infinite; border-radius: 8px; }
@keyframes shimmer { 0% { background-position: 200% 0; } 100% { background-position: -200% 0; } }

/* Pagination */
.pagination { display: flex; align-items: center; justify-content: center; gap: 6px; margin-top: 40px; flex-wrap: wrap; }
.pagination button { min-width: 36px; height: 36px; border-radius: 8px; border: 1.5px solid var(--gray2); background: #fff; font-size: 13px; font-weight: 500; color: #555; transition: all 0.15s; padding: 0 10px; }
.pagination button:hover:not(:disabled) { border-color: var(--black); color: var(--black); }
.pagination button.active { background: var(--black); color: #fff; border-color: var(--black); }
.pagination button:disabled { opacity: 0.4; cursor: not-allowed; }
.page-dots { color: #aaa; padding: 0 4px; }

/* Recently viewed */
.recently-viewed { margin-top: 60px; padding-top: 40px; border-top: 1px solid var(--gray2); }
.section-title { font-size: 20px; font-weight: 700; margin-bottom: 24px; }
.recent-grid { display: grid; grid-template-columns: repeat(5, 1fr); gap: 16px; }

@media (max-width: 1024px) { .products-grid { grid-template-columns: repeat(2, 1fr); } .recent-grid { grid-template-columns: repeat(3, 1fr); } }
@media (max-width: 768px) { .layout { grid-template-columns: 1fr; } .filters { flex-direction: row; flex-wrap: wrap; } .recent-grid { grid-template-columns: repeat(2, 1fr); } }
</style>
