<template>
  <div class="orders-page">
    <!-- Filters -->
    <div class="filters card">
      <div class="search-wrap">
        <i class="fas fa-search search-icon"></i>
        <input v-model="search" type="text" placeholder="Tìm theo mã đơn, nội dung..." class="filter-input with-icon" />
      </div>
      <select v-model="filterStatus" class="filter-select">
        <option value="">Tất cả trạng thái</option>
        <option value="paid">Đã thanh toán</option>
        <option value="waiting">Chờ thanh toán</option>
        <option value="unpaid">Chưa thanh toán</option>
      </select>
      <select v-model="filterMethod" class="filter-select">
        <option value="">Tất cả phương thức</option>
        <option value="bank_transfer">Chuyển khoản</option>
        <option value="momo">MoMo</option>
        <option value="cod">COD</option>
      </select>
      <button class="btn-refresh" @click="load"><i class="fas fa-sync-alt"></i> Làm mới</button>
    </div>

    <!-- Summary -->
    <div class="summary-row">
      <div class="sum-card">
        <p>Tổng đơn</p><strong>{{ orders.length }}</strong>
      </div>
      <div class="sum-card green">
        <p>Đã thanh toán</p><strong>{{ orders.filter(o => o.payment_status === 'paid').length }}</strong>
      </div>
      <div class="sum-card yellow">
        <p>Chờ thanh toán</p><strong>{{ orders.filter(o => o.payment_status === 'waiting').length }}</strong>
      </div>
      <div class="sum-card purple">
        <p>Tổng doanh thu</p><strong>{{ formatPrice(orders.filter(o=>o.payment_status==='paid').reduce((s,o)=>s+o.total,0)) }}</strong>
      </div>
    </div>

    <!-- Table -->
    <div class="card">
      <div v-if="loading" class="loading">Đang tải...</div>
      <div v-else-if="filtered.length === 0" class="empty">Không có đơn hàng nào</div>
      <table v-else class="data-table">
        <thead>
          <tr>
            <th>Mã đơn</th>
            <th>Sản phẩm</th>
            <th>Tổng tiền</th>
            <th>Phương thức</th>
            <th>Nội dung CK</th>
            <th>Thời gian</th>
            <th>Thanh toán</th>
            <th>Trạng thái</th>
            <th>Thao tác</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="order in filtered" :key="order.id" :class="{ 'row-paid': order.payment_status === 'paid' }">
            <td class="order-id">#{{ order.id }}</td>
            <td>
              <div v-for="item in order.items" :key="item.product_id" class="item-line">
                SP#{{ item.product_id }} · {{ item.size }} · {{ item.color }} × {{ item.quantity }}
              </div>
            </td>
            <td class="amount">{{ formatPrice(order.total) }}</td>
            <td><span :class="['method-badge', order.payment_method]">{{ methodLabel(order.payment_method) }}</span></td>
            <td class="transfer-note">{{ order.transfer_note || '—' }}</td>
            <td class="time">{{ formatDate(order.created_at) }}</td>
            <td><span :class="['status-badge', order.payment_status]">{{ payLabel(order.payment_status) }}</span></td>
            <td><span :class="['status-badge', order.status]">{{ statusLabel(order.status) }}</span></td>
            <td>
              <div class="actions">
                <button v-if="order.payment_status === 'waiting'" class="act-btn confirm" @click="markPaid(order.id)" title="Xác nhận đã thanh toán"><i class="fas fa-check-circle"></i></button>
                <button class="act-btn delete" @click="deleteOrder(order.id)" title="Xoá"><i class="fas fa-trash"></i></button>
              </div>
            </td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { orderService } from '@/services/orderService.js'
import { formatPrice } from '@/utils/format.js'
import api from '@/services/api.js'

const orders = ref([])
const loading = ref(false)
const search = ref('')
const filterStatus = ref('')
const filterMethod = ref('')

async function load() {
  loading.value = true
  try { orders.value = await orderService.getMyOrders() } catch {}
  finally { loading.value = false }
}
onMounted(load)

const filtered = computed(() => {
  let list = orders.value
  if (search.value) list = list.filter(o => String(o.id).includes(search.value) || (o.transfer_note || '').toLowerCase().includes(search.value.toLowerCase()))
  if (filterStatus.value) list = list.filter(o => o.payment_status === filterStatus.value)
  if (filterMethod.value) list = list.filter(o => o.payment_method === filterMethod.value)
  return list
})

async function markPaid(id) {
  try {
    await api.patch(`/orders/${id}/mark-paid`)
    await load()
  } catch { /* fallback: update local */ 
    const o = orders.value.find(x => x.id === id)
    if (o) { o.payment_status = 'paid'; o.status = 'confirmed' }
  }
}

function deleteOrder(id) {
  if (!confirm('Xoá đơn hàng này?')) return
  orders.value = orders.value.filter(o => o.id !== id)
}

function formatDate(d) { return d ? new Date(d).toLocaleString('vi-VN') : '' }
function methodLabel(m) { return { bank_transfer: 'CK Ngân hàng', momo: 'MoMo', cod: 'COD' }[m] || m }
function payLabel(s) { return { paid: 'Đã TT', waiting: 'Chờ TT', unpaid: 'Chưa TT' }[s] || s }
function statusLabel(s) { return { pending: 'Chờ xử lý', confirmed: 'Đã xác nhận', shipping: 'Đang giao', done: 'Hoàn thành', cancelled: 'Đã huỷ' }[s] || s }
</script>

<style scoped>
.orders-page { display: flex; flex-direction: column; gap: 16px; }
.card { background: #fff; border-radius: 12px; padding: 20px; box-shadow: 0 1px 4px rgba(0,0,0,0.06); }
.filters { display: flex; gap: 10px; flex-wrap: wrap; align-items: center; }
.search-wrap { position: relative; flex: 1; min-width: 200px; }
.search-icon { position: absolute; left: 12px; top: 50%; transform: translateY(-50%); color: #94a3b8; font-size: 13px; pointer-events: none; }
.filter-input { flex: 1; min-width: 200px; padding: 9px 14px; border: 1.5px solid #e2e8f0; border-radius: 8px; font-size: 13px; outline: none; width: 100%; }
.filter-input.with-icon { padding-left: 36px; }
.filter-input:focus { border-color: #3b82f6; }
.filter-select { padding: 9px 14px; border: 1.5px solid #e2e8f0; border-radius: 8px; font-size: 13px; background: #fff; outline: none; }
.filter-select:focus { border-color: #3b82f6; }
.btn-refresh { padding: 9px 16px; background: #3b82f6; color: #fff; border-radius: 8px; font-size: 13px; font-weight: 600; display: flex; align-items: center; gap: 6px; white-space: nowrap; }
.btn-refresh:hover { background: #2563eb; }

.summary-row { display: grid; grid-template-columns: repeat(4, 1fr); gap: 12px; }
.sum-card { background: #fff; border-radius: 10px; padding: 16px 20px; box-shadow: 0 1px 4px rgba(0,0,0,0.06); border-left: 4px solid #3b82f6; }
.sum-card.green { border-color: #10b981; }
.sum-card.yellow { border-color: #f59e0b; }
.sum-card.purple { border-color: #8b5cf6; }
.sum-card p { font-size: 12px; color: #888; margin-bottom: 4px; }
.sum-card strong { font-size: 20px; font-weight: 800; color: #1e2139; }

.data-table { width: 100%; border-collapse: collapse; font-size: 13px; }
.data-table th { text-align: left; padding: 10px 12px; color: #888; font-weight: 600; font-size: 11px; text-transform: uppercase; border-bottom: 2px solid #f0f0f0; white-space: nowrap; }
.data-table td { padding: 12px 12px; border-bottom: 1px solid #f8f8f8; vertical-align: top; }
.row-paid { background: #f0fdf4; }
.order-id { font-weight: 700; color: #3b82f6; }
.item-line { font-size: 12px; color: #555; margin-bottom: 2px; }
.amount { font-weight: 700; white-space: nowrap; }
.transfer-note { font-family: monospace; font-size: 12px; color: #3b82f6; }
.time { color: #888; font-size: 12px; white-space: nowrap; }

.method-badge { font-size: 11px; font-weight: 600; padding: 3px 8px; border-radius: 4px; white-space: nowrap; }
.method-badge.bank_transfer { background: #ede9fe; color: #3b82f6; }
.method-badge.momo { background: #fce7f3; color: #a50064; }
.method-badge.cod { background: #fef3c7; color: #92400e; }

.status-badge { font-size: 11px; font-weight: 600; padding: 3px 8px; border-radius: 20px; white-space: nowrap; }
.status-badge.paid, .status-badge.confirmed, .status-badge.done { background: #d1fae5; color: #065f46; }
.status-badge.waiting, .status-badge.pending, .status-badge.shipping { background: #fef3c7; color: #92400e; }
.status-badge.unpaid, .status-badge.cancelled { background: #fee2e2; color: #991b1b; }

.actions { display: flex; gap: 6px; }
.act-btn { background: none; font-size: 16px; padding: 4px; border-radius: 4px; transition: background 0.15s; }
.act-btn:hover { background: #f0f0f0; }

.loading, .empty { text-align: center; padding: 40px; color: #888; }
@media (max-width: 900px) { .summary-row { grid-template-columns: 1fr 1fr; } }
</style>
