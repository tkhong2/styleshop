<template>
  <div class="page">
    <div class="top-row">
      <div class="card cat-list">
        <div class="card-header">
          <h3><i class="fas fa-tags"></i> Danh mục sản phẩm</h3>
        </div>
        <div class="cat-grid">
          <div v-for="cat in categories" :key="cat.id" class="cat-card" :style="{'--c': cat.color}">
            <div class="cat-icon"><i :class="cat.icon"></i></div>
            <div class="cat-info">
              <p class="cat-name">{{ cat.name }}</p>
              <p class="cat-count">{{ cat.count }} sản phẩm</p>
            </div>
            <div class="cat-bar-wrap">
              <div class="cat-bar" :style="{ width: (cat.count / 40 * 100) + '%' }"></div>
            </div>
            <span class="cat-pct">{{ Math.round(cat.count / 100 * 100) }}%</span>
          </div>
        </div>
      </div>

      <div class="card add-cat">
        <div class="card-header">
          <h3><i class="fas fa-plus-circle"></i> Thêm danh mục</h3>
        </div>
        <form @submit.prevent="addCategory" class="add-form">
          <div class="field">
            <label>Tên danh mục</label>
            <input v-model="newCat.name" type="text" placeholder="VD: Phụ kiện" required />
          </div>
          <div class="field">
            <label>Slug (URL)</label>
            <input v-model="newCat.slug" type="text" placeholder="VD: phu-kien" required />
          </div>
          <div class="field">
            <label>Mô tả</label>
            <textarea v-model="newCat.desc" placeholder="Mô tả danh mục..." rows="3"></textarea>
          </div>
          <button type="submit" class="submit-btn">
            <i class="fas fa-plus"></i> Thêm danh mục
          </button>
        </form>
      </div>
    </div>

    <div class="card">
      <div class="card-header"><h3><i class="fas fa-list"></i> Tất cả danh mục</h3></div>
      <table class="data-table">
        <thead>
          <tr>
            <th>Icon</th><th>Tên danh mục</th><th>Slug</th><th>Số SP</th><th>Giới tính</th><th>Thao tác</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="cat in categories" :key="cat.id">
            <td><div class="tbl-icon" :style="{'background': cat.color + '22', 'color': cat.color}"><i :class="cat.icon"></i></div></td>
            <td class="cat-name-cell">{{ cat.name }}</td>
            <td><code class="slug">{{ cat.slug }}</code></td>
            <td class="center"><strong>{{ cat.count }}</strong></td>
            <td>{{ cat.gender }}</td>
            <td>
              <button class="act-btn edit"><i class="fas fa-edit"></i></button>
              <button class="act-btn del"><i class="fas fa-trash"></i></button>
            </td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'

const newCat = ref({ name: '', slug: '', desc: '' })

const categories = ref([
  { id: 1, name: 'Áo', slug: 'ao', icon: 'fas fa-tshirt', count: 38, color: '#3b82f6', gender: 'Tất cả' },
  { id: 2, name: 'Quần', slug: 'quan', icon: 'fas fa-socks', count: 18, color: '#10b981', gender: 'Tất cả' },
  { id: 3, name: 'Váy & Đầm', slug: 'vay', icon: 'fas fa-female', count: 22, color: '#ec4899', gender: 'Nữ' },
  { id: 4, name: 'Giày', slug: 'giay', icon: 'fas fa-shoe-prints', count: 12, color: '#f59e0b', gender: 'Tất cả' },
  { id: 5, name: 'Túi xách', slug: 'tui', icon: 'fas fa-shopping-bag', count: 10, color: '#8b5cf6', gender: 'Nữ' },
])

function addCategory() {
  categories.value.push({
    id: Date.now(),
    name: newCat.value.name,
    slug: newCat.value.slug,
    icon: 'fas fa-tag',
    count: 0,
    color: '#64748b',
    gender: 'Tất cả',
  })
  newCat.value = { name: '', slug: '', desc: '' }
}
</script>

<style scoped>
.page { display: flex; flex-direction: column; gap: 16px; }
.top-row { display: grid; grid-template-columns: 1fr 320px; gap: 16px; }
.card { background: #fff; border-radius: 12px; padding: 20px; box-shadow: 0 1px 4px rgba(0,0,0,0.06); }
.card-header { display: flex; align-items: center; gap: 8px; margin-bottom: 16px; }
.card-header h3 { font-size: 15px; font-weight: 700; color: #1e293b; display: flex; align-items: center; gap: 8px; }
.cat-grid { display: flex; flex-direction: column; gap: 12px; }
.cat-card { display: flex; align-items: center; gap: 12px; padding: 12px; border-radius: 8px; background: #f8fafc; }
.cat-icon { width: 40px; height: 40px; border-radius: 10px; background: color-mix(in srgb, var(--c) 15%, white); color: var(--c); display: flex; align-items: center; justify-content: center; font-size: 16px; flex-shrink: 0; }
.cat-info { min-width: 100px; }
.cat-name { font-size: 13px; font-weight: 600; color: #1e293b; }
.cat-count { font-size: 11px; color: #64748b; }
.cat-bar-wrap { flex: 1; height: 6px; background: #e2e8f0; border-radius: 3px; overflow: hidden; }
.cat-bar { height: 100%; background: var(--c); border-radius: 3px; transition: width 0.5s; }
.cat-pct { font-size: 12px; font-weight: 700; color: #64748b; min-width: 36px; text-align: right; }
.add-form { display: flex; flex-direction: column; gap: 14px; }
.field { display: flex; flex-direction: column; gap: 5px; }
.field label { font-size: 12px; font-weight: 600; color: #475569; }
.field input, .field textarea { padding: 9px 12px; border: 1.5px solid #e2e8f0; border-radius: 8px; font-size: 13px; outline: none; font-family: inherit; resize: vertical; }
.field input:focus, .field textarea:focus { border-color: #3b82f6; }
.submit-btn { background: #3b82f6; color: #fff; padding: 11px; border-radius: 8px; font-size: 13px; font-weight: 600; display: flex; align-items: center; justify-content: center; gap: 8px; }
.submit-btn:hover { background: #2563eb; }
.data-table { width: 100%; border-collapse: collapse; font-size: 13px; }
.data-table th { text-align: left; padding: 10px 12px; color: #64748b; font-weight: 600; font-size: 11px; text-transform: uppercase; border-bottom: 2px solid #f1f5f9; }
.data-table td { padding: 12px 12px; border-bottom: 1px solid #f8fafc; vertical-align: middle; }
.tbl-icon { width: 34px; height: 34px; border-radius: 8px; display: flex; align-items: center; justify-content: center; font-size: 14px; }
.cat-name-cell { font-weight: 600; }
.slug { background: #f1f5f9; color: #475569; padding: 2px 8px; border-radius: 4px; font-size: 12px; }
.center { text-align: center; }
.act-btn { background: none; padding: 6px 8px; border-radius: 6px; font-size: 13px; margin-right: 4px; }
.act-btn.edit { color: #3b82f6; } .act-btn.edit:hover { background: #eff6ff; }
.act-btn.del { color: #ef4444; } .act-btn.del:hover { background: #fef2f2; }
@media (max-width: 900px) { .top-row { grid-template-columns: 1fr; } }
</style>
