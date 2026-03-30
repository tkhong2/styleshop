<template>
  <div class="page">
    <div class="summary-row">
      <div class="sum-card" v-for="s in summary" :key="s.label" :style="{'--c': s.color}">
        <div class="sum-icon"><i :class="s.icon"></i></div>
        <div>
          <p class="sum-val">{{ s.value }}</p>
          <p class="sum-label">{{ s.label }}</p>
        </div>
      </div>
    </div>

    <div class="card">
      <div class="card-header">
        <h3><i class="fas fa-users"></i> Danh sách khách hàng</h3>
        <input v-model="search" type="text" placeholder="Tìm kiếm..." class="search-input" />
      </div>
      <table class="data-table">
        <thead>
          <tr>
            <th>#</th>
            <th>Khách hàng</th>
            <th>Email</th>
            <th>Đăng nhập qua</th>
            <th>Số đơn</th>
            <th>Tổng chi tiêu</th>
            <th>Trạng thái</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="c in filtered" :key="c.id">
            <td class="cid">#{{ c.id }}</td>
            <td>
              <div class="customer-cell">
                <div class="avatar" :style="{ background: c.color }">{{ c.name[0] }}</div>
                <span>{{ c.name }}</span>
              </div>
            </td>
            <td class="email">{{ c.email }}</td>
            <td>
              <span :class="['provider-badge', c.provider]">
                <i :class="c.provider === 'google' ? 'fab fa-google' : 'fas fa-envelope'"></i>
                {{ c.provider === 'google' ? 'Google' : 'Email' }}
              </span>
            </td>
            <td class="center">{{ c.orders }}</td>
            <td class="amount">{{ formatPrice(c.spent) }}</td>
            <td><span :class="['status', c.active ? 'active' : 'inactive']">{{ c.active ? 'Hoạt động' : 'Không HĐ' }}</span></td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { formatPrice } from '@/utils/format.js'

const search = ref('')

const customers = ref([
  { id: 1, name: 'Nguyễn Văn An', email: 'an@gmail.com', provider: 'google', orders: 5, spent: 2450000, active: true, color: '#3b82f6' },
  { id: 2, name: 'Trần Thị Bình', email: 'binh@gmail.com', provider: 'email', orders: 3, spent: 1200000, active: true, color: '#10b981' },
  { id: 3, name: 'Lê Minh Cường', email: 'cuong@yahoo.com', provider: 'email', orders: 8, spent: 4800000, active: true, color: '#f59e0b' },
  { id: 4, name: 'Phạm Thu Dung', email: 'dung@gmail.com', provider: 'google', orders: 2, spent: 890000, active: false, color: '#ef4444' },
  { id: 5, name: 'Hoàng Văn Em', email: 'em@gmail.com', provider: 'email', orders: 12, spent: 7200000, active: true, color: '#8b5cf6' },
  { id: 6, name: 'Vũ Thị Phương', email: 'phuong@gmail.com', provider: 'google', orders: 1, spent: 350000, active: true, color: '#ec4899' },
  { id: 7, name: 'Đặng Quốc Hùng', email: 'hung@gmail.com', provider: 'email', orders: 6, spent: 3100000, active: true, color: '#06b6d4' },
  { id: 8, name: 'Bùi Thị Lan', email: 'lan@gmail.com', provider: 'google', orders: 4, spent: 1950000, active: false, color: '#84cc16' },
])

const filtered = computed(() =>
  customers.value.filter(c =>
    c.name.toLowerCase().includes(search.value.toLowerCase()) ||
    c.email.toLowerCase().includes(search.value.toLowerCase())
  )
)

const summary = [
  { label: 'Tổng khách hàng', value: '124', icon: 'fas fa-users', color: '#3b82f6' },
  { label: 'Hoạt động', value: '98', icon: 'fas fa-user-check', color: '#10b981' },
  { label: 'Mới tháng này', value: '12', icon: 'fas fa-user-plus', color: '#f59e0b' },
  { label: 'Đăng nhập Google', value: '67', icon: 'fab fa-google', color: '#ef4444' },
]
</script>

<style scoped>
.page { display: flex; flex-direction: column; gap: 16px; }
.summary-row { display: grid; grid-template-columns: repeat(4, 1fr); gap: 14px; }
.sum-card { background: #fff; border-radius: 12px; padding: 18px 20px; display: flex; align-items: center; gap: 14px; box-shadow: 0 1px 4px rgba(0,0,0,0.06); border-left: 4px solid var(--c); }
.sum-icon { width: 42px; height: 42px; border-radius: 10px; background: color-mix(in srgb, var(--c) 15%, white); color: var(--c); display: flex; align-items: center; justify-content: center; font-size: 18px; }
.sum-val { font-size: 22px; font-weight: 800; color: #1e293b; }
.sum-label { font-size: 12px; color: #64748b; }
.card { background: #fff; border-radius: 12px; padding: 20px; box-shadow: 0 1px 4px rgba(0,0,0,0.06); }
.card-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 16px; }
.card-header h3 { font-size: 15px; font-weight: 700; color: #1e293b; display: flex; align-items: center; gap: 8px; }
.search-input { padding: 8px 14px; border: 1.5px solid #e2e8f0; border-radius: 8px; font-size: 13px; outline: none; width: 220px; }
.search-input:focus { border-color: #3b82f6; }
.data-table { width: 100%; border-collapse: collapse; font-size: 13px; }
.data-table th { text-align: left; padding: 10px 12px; color: #64748b; font-weight: 600; font-size: 11px; text-transform: uppercase; border-bottom: 2px solid #f1f5f9; }
.data-table td { padding: 12px 12px; border-bottom: 1px solid #f8fafc; }
.cid { color: #3b82f6; font-weight: 700; }
.customer-cell { display: flex; align-items: center; gap: 10px; }
.avatar { width: 34px; height: 34px; border-radius: 50%; color: #fff; display: flex; align-items: center; justify-content: center; font-weight: 700; font-size: 13px; flex-shrink: 0; }
.email { color: #64748b; font-size: 12px; }
.provider-badge { display: inline-flex; align-items: center; gap: 5px; font-size: 11px; font-weight: 600; padding: 3px 8px; border-radius: 4px; }
.provider-badge.google { background: #fef2f2; color: #dc2626; }
.provider-badge.email { background: #eff6ff; color: #3b82f6; }
.center { text-align: center; font-weight: 600; }
.amount { font-weight: 700; color: #1e293b; }
.status { font-size: 11px; font-weight: 600; padding: 3px 10px; border-radius: 20px; }
.status.active { background: #dcfce7; color: #166534; }
.status.inactive { background: #f1f5f9; color: #64748b; }
@media (max-width: 900px) { .summary-row { grid-template-columns: 1fr 1fr; } }
</style>
