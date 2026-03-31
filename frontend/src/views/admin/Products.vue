<template>
  <div class="products-page">
    <div class="toolbar card">
      <div class="search-wrap">
        <i class="fas fa-search search-icon"></i>
        <input v-model="search" type="text" placeholder="Tìm sản phẩm..." class="filter-input with-icon" />
      </div>
      <select v-model="filterCat" class="filter-select">
        <option value="">Tất cả danh mục</option>
        <option value="ao">Áo</option>
        <option value="quan">Quần</option>
        <option value="vay">Váy & Đầm</option>
        <option value="giay">Giày</option>
        <option value="tui">Túi</option>
      </select>
      <select v-model="filterGender" class="filter-select">
        <option value="">Tất cả</option>
        <option value="nam">Nam</option>
        <option value="nu">Nữ</option>
        <option value="unisex">Unisex</option>
      </select>
      <span class="total-count">{{ filtered.length }} sản phẩm</span>
      <RouterLink to="/admin/products/new" class="btn-add">
        <i class="fas fa-plus"></i> Thêm sản phẩm
      </RouterLink>
    </div>

    <div class="card">
      <table class="data-table">
        <thead>
          <tr>
            <th>ID</th>
            <th>Ảnh</th>
            <th>Tên sản phẩm</th>
            <th>Danh mục</th>
            <th>Giới tính</th>
            <th>Giá</th>
            <th>Đánh giá</th>
            <th>Tags</th>
            <th></th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="p in paginated" :key="p.id">
            <td class="pid">#{{ p.id }}</td>
            <td><img :src="p.image" :alt="p.name" class="prod-img" /></td>
            <td class="prod-name">{{ p.name }}</td>
            <td><span class="cat-badge">{{ catLabel(p.category) }}</span></td>
            <td>{{ genderLabel(p.gender) }}</td>
            <td>
              <div class="price-col">
                <span class="price">{{ formatPrice(p.price) }}</span>
                <span v-if="p.original_price > p.price" class="orig">{{ formatPrice(p.original_price) }}</span>
              </div>
            </td>
            <td>
              <span class="rating">★ {{ p.rating }}</span>
              <span class="reviews">({{ p.reviews }})</span>
            </td>
            <td>
              <span v-if="p.is_new" class="tag new">Mới</span>
              <span v-if="p.is_sale" class="tag sale">Sale</span>
            </td>
            <td>
              <RouterLink :to="`/admin/products/${p.id}/edit`" class="act-edit">
                <i class="fas fa-edit"></i>
              </RouterLink>
            </td>
          </tr>
        </tbody>
      </table>

      <!-- Pagination -->
      <div class="pagination">
        <button :disabled="page === 1" @click="page--">‹</button>
        <span>Trang {{ page }} / {{ totalPages }}</span>
        <button :disabled="page === totalPages" @click="page++">›</button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { productService } from '@/services/productService.js'
import { formatPrice } from '@/utils/format.js'

const allProducts = ref([])
const search = ref('')
const filterCat = ref('')
const filterGender = ref('')
const page = ref(1)
const PER_PAGE = 15

onMounted(async () => {
  try { allProducts.value = await productService.getAll() } catch {}
})

const filtered = computed(() => {
  let list = allProducts.value
  if (search.value) list = list.filter(p => p.name.toLowerCase().includes(search.value.toLowerCase()))
  if (filterCat.value) list = list.filter(p => p.category === filterCat.value)
  if (filterGender.value) list = list.filter(p => p.gender === filterGender.value)
  return list
})

const totalPages = computed(() => Math.max(1, Math.ceil(filtered.value.length / PER_PAGE)))
const paginated = computed(() => filtered.value.slice((page.value - 1) * PER_PAGE, page.value * PER_PAGE))

function catLabel(c) { return { ao: 'Áo', quan: 'Quần', vay: 'Váy', giay: 'Giày', tui: 'Túi' }[c] || c }
function genderLabel(g) { return { nam: 'Nam', nu: 'Nữ', unisex: 'Unisex' }[g] || g }
</script>

<style scoped>
.products-page { display: flex; flex-direction: column; gap: 16px; }
.card { background: #fff; border-radius: 12px; padding: 20px; box-shadow: 0 1px 4px rgba(0,0,0,0.06); }
.toolbar { display: flex; gap: 10px; flex-wrap: wrap; align-items: center; }
.search-wrap { position: relative; flex: 1; min-width: 200px; }
.search-icon { position: absolute; left: 12px; top: 50%; transform: translateY(-50%); color: #94a3b8; font-size: 13px; pointer-events: none; }
.filter-input { width: 100%; padding: 9px 14px; border: 1.5px solid #e2e8f0; border-radius: 8px; font-size: 13px; outline: none; }
.filter-input.with-icon { padding-left: 36px; }
.filter-input:focus { border-color: #3b82f6; }
.filter-select { padding: 9px 14px; border: 1.5px solid #e2e8f0; border-radius: 8px; font-size: 13px; background: #fff; outline: none; }
.filter-select:focus { border-color: #3b82f6; }
.total-count { font-size: 13px; color: #888; margin-left: auto; }
.data-table { width: 100%; border-collapse: collapse; font-size: 13px; }
.data-table th { text-align: left; padding: 10px 12px; color: #888; font-weight: 600; font-size: 11px; text-transform: uppercase; border-bottom: 2px solid #f0f0f0; }
.data-table td { padding: 10px 12px; border-bottom: 1px solid #f8f8f8; vertical-align: middle; }
.pid { color: #3b82f6; font-weight: 700; }
.prod-img { width: 44px; height: 44px; object-fit: cover; border-radius: 6px; }
.prod-name { font-weight: 500; max-width: 200px; }
.cat-badge { background: #ede9fe; color: #3b82f6; font-size: 11px; font-weight: 600; padding: 2px 8px; border-radius: 4px; }
.price-col { display: flex; flex-direction: column; gap: 2px; }
.price { font-weight: 700; font-size: 13px; }
.orig { font-size: 11px; color: #aaa; text-decoration: line-through; }
.rating { color: #f59e0b; font-size: 12px; }
.reviews { font-size: 11px; color: #aaa; }
.tag { font-size: 10px; font-weight: 700; padding: 2px 6px; border-radius: 3px; margin-right: 4px; }
.tag.new { background: #1e2139; color: #fff; }
.tag.sale { background: #ef4444; color: #fff; }
.act-edit { display: inline-flex; align-items: center; justify-content: center; width: 30px; height: 30px; border-radius: 6px; color: #3b82f6; background: #eff6ff; font-size: 13px; }
.act-edit:hover { background: #dbeafe; }
.btn-add { display: flex; align-items: center; gap: 6px; padding: 9px 16px; background: #3b82f6; color: #fff; border-radius: 8px; font-size: 13px; font-weight: 600; white-space: nowrap; text-decoration: none; margin-left: auto; }
.btn-add:hover { background: #2563eb; }
.pagination { display: flex; align-items: center; justify-content: center; gap: 16px; margin-top: 16px; font-size: 13px; color: #555; }
.pagination button { padding: 6px 14px; border: 1.5px solid #eee; border-radius: 6px; background: #fff; font-size: 16px; }
.pagination button:disabled { opacity: 0.4; cursor: not-allowed; }
.pagination button:not(:disabled):hover { border-color: #3b82f6; color: #3b82f6; }
</style>
