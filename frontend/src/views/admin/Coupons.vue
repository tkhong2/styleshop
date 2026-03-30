<template>
  <div class="page">
    <div class="card">
      <div class="card-header">
        <h3><i class="fas fa-ticket-alt"></i> Quản lý mã giảm giá</h3>
        <button class="btn-add" @click="showForm = true">
          <i class="fas fa-plus"></i> Thêm mã
        </button>
      </div>

      <table class="data-table">
        <thead>
          <tr><th>Mã</th><th>Giảm</th><th>Loại</th><th>Đã dùng</th><th>Trạng thái</th><th>Thao tác</th></tr>
        </thead>
        <tbody>
          <tr v-for="c in coupons" :key="c.code">
            <td><code class="code-badge">{{ c.code }}</code></td>
            <td class="amount">{{ c.type === 'percent' ? c.value + '%' : formatPrice(c.value) }}</td>
            <td>{{ c.type === 'percent' ? 'Phần trăm' : 'Số tiền' }}</td>
            <td class="center">{{ c.used }}/{{ c.limit || '∞' }}</td>
            <td><span :class="['status', c.active ? 'active' : 'inactive']">{{ c.active ? 'Hoạt động' : 'Tắt' }}</span></td>
            <td>
              <button class="act-btn" @click="toggleCoupon(c)">
                <i :class="c.active ? 'fas fa-toggle-on' : 'fas fa-toggle-off'"></i>
              </button>
              <button class="act-btn del" @click="deleteCoupon(c.code)">
                <i class="fas fa-trash"></i>
              </button>
            </td>
          </tr>
        </tbody>
      </table>
    </div>

    <!-- Add form -->
    <Transition name="fade">
      <div v-if="showForm" class="modal-overlay" @click.self="showForm = false">
        <div class="modal">
          <div class="modal-header">
            <h3>Thêm mã giảm giá</h3>
            <button @click="showForm = false"><i class="fas fa-times"></i></button>
          </div>
          <form @submit.prevent="addCoupon" class="form">
            <div class="field">
              <label>Mã giảm giá *</label>
              <input v-model="form.code" type="text" placeholder="VD: SUMMER20" required style="text-transform:uppercase" />
            </div>
            <div class="form-row">
              <div class="field">
                <label>Loại</label>
                <select v-model="form.type">
                  <option value="percent">Phần trăm (%)</option>
                  <option value="fixed">Số tiền cố định</option>
                </select>
              </div>
              <div class="field">
                <label>Giá trị *</label>
                <input v-model.number="form.value" type="number" :placeholder="form.type === 'percent' ? '10' : '50000'" required />
              </div>
            </div>
            <div class="field">
              <label>Giới hạn sử dụng (để trống = không giới hạn)</label>
              <input v-model.number="form.limit" type="number" placeholder="100" />
            </div>
            <button type="submit" class="btn-submit">Thêm mã</button>
          </form>
        </div>
      </div>
    </Transition>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useToastStore } from '@/stores/toast.js'
import { formatPrice } from '@/utils/format.js'

const toast = useToastStore()
const showForm = ref(false)

const coupons = ref([
  { code: 'STYLE10', type: 'percent', value: 10, used: 24, limit: null, active: true },
  { code: 'SALE20', type: 'percent', value: 20, used: 8, limit: 50, active: true },
  { code: 'NEWUSER', type: 'percent', value: 15, used: 31, limit: null, active: true },
  { code: 'FREESHIP', type: 'fixed', value: 30000, used: 5, limit: 100, active: false },
])

const form = ref({ code: '', type: 'percent', value: '', limit: '' })

function addCoupon() {
  if (coupons.value.find(c => c.code === form.value.code.toUpperCase())) {
    toast.error('Mã này đã tồn tại!')
    return
  }
  coupons.value.unshift({ ...form.value, code: form.value.code.toUpperCase(), used: 0, active: true })
  form.value = { code: '', type: 'percent', value: '', limit: '' }
  showForm.value = false
  toast.success('Đã thêm mã giảm giá!')
}

function toggleCoupon(c) { c.active = !c.active }
function deleteCoupon(code) {
  if (confirm('Xóa mã này?')) {
    coupons.value = coupons.value.filter(c => c.code !== code)
    toast.info('Đã xóa mã giảm giá')
  }
}
</script>

<style scoped>
.page { display: flex; flex-direction: column; gap: 16px; }
.card { background: #fff; border-radius: 12px; padding: 20px; box-shadow: 0 1px 4px rgba(0,0,0,0.06); }
.card-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 16px; }
.card-header h3 { font-size: 15px; font-weight: 700; color: #1e293b; display: flex; align-items: center; gap: 8px; }
.btn-add { display: flex; align-items: center; gap: 6px; padding: 8px 16px; background: #3b82f6; color: #fff; border-radius: 8px; font-size: 13px; font-weight: 600; }
.data-table { width: 100%; border-collapse: collapse; font-size: 13px; }
.data-table th { text-align: left; padding: 10px 12px; color: #64748b; font-weight: 600; font-size: 11px; text-transform: uppercase; border-bottom: 2px solid #f1f5f9; }
.data-table td { padding: 12px 12px; border-bottom: 1px solid #f8fafc; }
.code-badge { background: #eff6ff; color: #3b82f6; padding: 3px 10px; border-radius: 4px; font-size: 13px; font-weight: 700; letter-spacing: 1px; }
.amount { font-weight: 700; }
.center { text-align: center; }
.status { font-size: 11px; font-weight: 600; padding: 3px 10px; border-radius: 20px; }
.status.active { background: #dcfce7; color: #166534; }
.status.inactive { background: #f1f5f9; color: #64748b; }
.act-btn { background: none; padding: 6px 8px; border-radius: 6px; font-size: 15px; color: #3b82f6; margin-right: 4px; }
.act-btn.del { color: #ef4444; }
.act-btn:hover { background: #f1f5f9; }
.modal-overlay { position: fixed; inset: 0; background: rgba(0,0,0,0.4); z-index: 400; display: flex; align-items: center; justify-content: center; }
.modal { background: #fff; border-radius: 12px; padding: 24px; width: 440px; max-width: 90vw; }
.modal-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 20px; }
.modal-header h3 { font-size: 16px; font-weight: 700; }
.modal-header button { background: none; color: #888; font-size: 16px; }
.form { display: flex; flex-direction: column; gap: 14px; }
.form-row { display: grid; grid-template-columns: 1fr 1fr; gap: 12px; }
.field { display: flex; flex-direction: column; gap: 5px; }
.field label { font-size: 12px; font-weight: 600; color: #475569; }
.field input, .field select { padding: 9px 12px; border: 1.5px solid #e2e8f0; border-radius: 8px; font-size: 13px; outline: none; }
.field input:focus, .field select:focus { border-color: #3b82f6; }
.btn-submit { background: #3b82f6; color: #fff; padding: 12px; border-radius: 8px; font-size: 14px; font-weight: 600; }
.fade-enter-active, .fade-leave-active { transition: opacity 0.2s; }
.fade-enter-from, .fade-leave-to { opacity: 0; }
</style>
