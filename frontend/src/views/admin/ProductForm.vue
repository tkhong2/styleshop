<template>
  <div class="page">
    <div class="page-header">
      <RouterLink to="/admin/products" class="back-btn">
        <i class="fas fa-arrow-left"></i> Quay lại
      </RouterLink>
      <h1>{{ isEdit ? 'Sửa sản phẩm' : 'Thêm sản phẩm mới' }}</h1>
    </div>

    <form @submit.prevent="save" class="form-grid">
      <!-- Left -->
      <div class="form-main">
        <div class="card">
          <h3><i class="fas fa-info-circle"></i> Thông tin cơ bản</h3>
          <div class="field">
            <label>Tên sản phẩm *</label>
            <input v-model="form.name" type="text" placeholder="VD: Áo Thun Basic Cotton" required />
          </div>
          <div class="field">
            <label>Mô tả *</label>
            <textarea v-model="form.description" rows="4" placeholder="Mô tả chi tiết sản phẩm..." required></textarea>
          </div>
          <div class="form-row">
            <div class="field">
              <label>Giá bán (đ) *</label>
              <input v-model.number="form.price" type="number" min="0" step="1000" required />
            </div>
            <div class="field">
              <label>Giá gốc (đ)</label>
              <input v-model.number="form.original_price" type="number" min="0" step="1000" />
            </div>
          </div>
        </div>

        <div class="card">
          <h3><i class="fas fa-tags"></i> Phân loại</h3>
          <div class="form-row">
            <div class="field">
              <label>Danh mục *</label>
              <select v-model="form.category" required>
                <option value="">Chọn danh mục</option>
                <option value="ao">Áo</option>
                <option value="quan">Quần</option>
                <option value="vay">Váy & Đầm</option>
                <option value="giay">Giày</option>
                <option value="tui">Túi</option>
              </select>
            </div>
            <div class="field">
              <label>Giới tính *</label>
              <select v-model="form.gender" required>
                <option value="">Chọn giới tính</option>
                <option value="nam">Nam</option>
                <option value="nu">Nữ</option>
                <option value="unisex">Unisex</option>
              </select>
            </div>
          </div>
          <div class="form-row">
            <div class="field">
              <label>Sizes (cách nhau bởi dấu phẩy)</label>
              <input v-model="sizesStr" type="text" placeholder="S, M, L, XL" />
            </div>
            <div class="field">
              <label>Màu sắc (cách nhau bởi dấu phẩy)</label>
              <input v-model="colorsStr" type="text" placeholder="Đen, Trắng, Xám" />
            </div>
          </div>
        </div>

        <div class="card">
          <h3><i class="fas fa-image"></i> Hình ảnh</h3>
          <div class="field">
            <label>URL ảnh chính *</label>
            <input v-model="form.image" type="url" placeholder="https://..." required />
          </div>
          <div v-if="form.image" class="img-preview">
            <img :src="form.image" alt="Preview" />
          </div>
          <div class="field">
            <label>URL ảnh phụ (mỗi dòng 1 URL)</label>
            <textarea v-model="imagesStr" rows="3" placeholder="https://...&#10;https://..."></textarea>
          </div>
        </div>
      </div>

      <!-- Right sidebar -->
      <div class="form-side">
        <div class="card">
          <h3><i class="fas fa-cog"></i> Trạng thái</h3>
          <label class="toggle-label">
            <input type="checkbox" v-model="form.is_new" />
            <span>Sản phẩm mới</span>
          </label>
          <label class="toggle-label">
            <input type="checkbox" v-model="form.is_sale" />
            <span>Đang giảm giá</span>
          </label>
        </div>

        <div class="card">
          <h3><i class="fas fa-star"></i> Đánh giá</h3>
          <div class="form-row">
            <div class="field">
              <label>Rating (1-5)</label>
              <input v-model.number="form.rating" type="number" min="1" max="5" step="0.1" />
            </div>
            <div class="field">
              <label>Số lượt đánh giá</label>
              <input v-model.number="form.reviews" type="number" min="0" />
            </div>
          </div>
        </div>

        <div class="card actions-card">
          <button type="submit" class="btn-primary-full" :disabled="saving">
            <i class="fas fa-save"></i>
            {{ saving ? 'Đang lưu...' : (isEdit ? 'Cập nhật' : 'Thêm sản phẩm') }}
          </button>
          <RouterLink to="/admin/products" class="btn-cancel">Hủy</RouterLink>
        </div>
      </div>
    </form>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { productService } from '@/services/productService.js'
import { useToastStore } from '@/stores/toast.js'

const route = useRoute()
const router = useRouter()
const toast = useToastStore()

const isEdit = computed(() => !!route.params.id)
const saving = ref(false)

const form = ref({
  name: '', description: '', price: 0, original_price: 0,
  category: '', gender: '', image: '', images: [],
  sizes: [], colors: [], rating: 4.5, reviews: 0,
  is_new: false, is_sale: false,
})

const sizesStr = computed({
  get: () => form.value.sizes.join(', '),
  set: (v) => { form.value.sizes = v.split(',').map(s => s.trim()).filter(Boolean) }
})
const colorsStr = computed({
  get: () => form.value.colors.join(', '),
  set: (v) => { form.value.colors = v.split(',').map(s => s.trim()).filter(Boolean) }
})
const imagesStr = computed({
  get: () => form.value.images.join('\n'),
  set: (v) => { form.value.images = v.split('\n').map(s => s.trim()).filter(Boolean) }
})

onMounted(async () => {
  if (isEdit.value) {
    try {
      const p = await productService.getById(route.params.id)
      form.value = { ...p }
    } catch { toast.error('Không tìm thấy sản phẩm') }
  }
})

async function save() {
  if (!form.value.original_price) form.value.original_price = form.value.price
  if (!form.value.images.length) form.value.images = [form.value.image]
  saving.value = true
  try {
    // Gọi API tạo/cập nhật (backend cần implement endpoint này)
    toast.success(isEdit.value ? 'Đã cập nhật sản phẩm!' : 'Đã thêm sản phẩm!')
    router.push('/admin/products')
  } catch (e) { toast.error('Lỗi: ' + e.message) }
  finally { saving.value = false }
}
</script>

<style scoped>
.page { display: flex; flex-direction: column; gap: 20px; }
.page-header { display: flex; align-items: center; gap: 16px; }
.back-btn { display: flex; align-items: center; gap: 6px; font-size: 13px; color: #64748b; padding: 8px 12px; border-radius: 8px; background: #fff; border: 1px solid #e2e8f0; }
.back-btn:hover { background: #f8fafc; }
.page-header h1 { font-size: 22px; font-weight: 700; color: #1e293b; }
.form-grid { display: grid; grid-template-columns: 1fr 280px; gap: 20px; align-items: start; }
.form-main { display: flex; flex-direction: column; gap: 16px; }
.form-side { display: flex; flex-direction: column; gap: 16px; position: sticky; top: 80px; }
.card { background: #fff; border-radius: 12px; padding: 20px; box-shadow: 0 1px 4px rgba(0,0,0,0.06); }
.card h3 { font-size: 14px; font-weight: 700; color: #1e293b; margin-bottom: 16px; display: flex; align-items: center; gap: 8px; }
.card h3 i { color: #3b82f6; }
.form-row { display: grid; grid-template-columns: 1fr 1fr; gap: 14px; }
.field { display: flex; flex-direction: column; gap: 5px; margin-bottom: 12px; }
.field label { font-size: 12px; font-weight: 600; color: #475569; }
.field input, .field select, .field textarea { padding: 10px 14px; border: 1.5px solid #e2e8f0; border-radius: 8px; font-size: 13px; outline: none; font-family: inherit; resize: vertical; }
.field input:focus, .field select:focus, .field textarea:focus { border-color: #3b82f6; }
.img-preview { margin: -4px 0 12px; }
.img-preview img { width: 100%; max-height: 200px; object-fit: cover; border-radius: 8px; }
.toggle-label { display: flex; align-items: center; gap: 10px; font-size: 14px; cursor: pointer; margin-bottom: 10px; }
.toggle-label input { width: 16px; height: 16px; }
.actions-card { display: flex; flex-direction: column; gap: 10px; }
.btn-primary-full { width: 100%; padding: 13px; background: #3b82f6; color: #fff; border-radius: 8px; font-size: 14px; font-weight: 600; display: flex; align-items: center; justify-content: center; gap: 8px; }
.btn-primary-full:disabled { opacity: 0.6; cursor: not-allowed; }
.btn-cancel { display: block; text-align: center; padding: 11px; border: 1.5px solid #e2e8f0; border-radius: 8px; font-size: 14px; color: #64748b; }
.btn-cancel:hover { background: #f8fafc; }
@media (max-width: 900px) { .form-grid { grid-template-columns: 1fr; } .form-side { position: static; } }
</style>
