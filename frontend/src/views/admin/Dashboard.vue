<template>
  <div class="dashboard">
    <!-- Stats cards -->
    <div class="stats-grid">
      <div v-for="stat in stats" :key="stat.label" class="stat-card" :style="{ '--accent': stat.color }">
        <div class="stat-top">
          <div>
            <p class="stat-label">{{ stat.label }}</p>
            <p class="stat-value">{{ stat.value }}</p>
          </div>
          <div class="stat-icon-wrap" :style="{ background: stat.color + '18', color: stat.color }">
            <i :class="stat.icon"></i>
          </div>
        </div>
        <div class="stat-change" :class="stat.up ? 'up' : 'down'">
          <i :class="stat.up ? 'fas fa-arrow-up' : 'fas fa-arrow-down'"></i>
          {{ stat.change }} so với hôm qua
        </div>
        <div class="stat-chart">
          <svg viewBox="0 0 100 40" preserveAspectRatio="none">
            <polyline :points="stat.sparkline" fill="none" :stroke="stat.color" stroke-width="2" opacity="0.8"/>
            <polyline :points="stat.sparkline + ' 100,40 0,40'" :fill="stat.color" opacity="0.12" stroke="none"/>
          </svg>
        </div>
      </div>
    </div>

    <div class="row-2">
      <!-- Recent orders -->
      <div class="card orders-card">
        <div class="card-header">
          <h3><i class="fas fa-clock"></i> Đơn hàng gần đây</h3>
          <RouterLink to="/admin/orders" class="see-all">Xem tất cả <i class="fas fa-arrow-right"></i></RouterLink>
        </div>
        <table class="data-table">
          <thead>
            <tr>
              <th>#</th><th>Sản phẩm</th><th>Tổng tiền</th><th>Thời gian</th><th>Thanh toán</th><th>Trạng thái</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="order in recentOrders" :key="order.id">
              <td class="order-id">#{{ order.id }}</td>
              <td>{{ order.items?.length }} sản phẩm</td>
              <td class="amount">{{ formatPrice(order.total) }}</td>
              <td class="time">{{ formatDate(order.created_at) }}</td>
              <td><span class="pay-badge">{{ order.payment_method?.toUpperCase() }}</span></td>
              <td><span :class="['status-badge', order.payment_status]">{{ statusLabel(order.payment_status) }}</span></td>
            </tr>
            <tr v-if="recentOrders.length === 0">
              <td colspan="6" class="empty-row">
                <i class="fas fa-inbox"></i> Chưa có đơn hàng nào
              </td>
            </tr>
          </tbody>
        </table>
      </div>

      <!-- Revenue chart -->
      <div class="card chart-card">
        <div class="card-header">
          <h3><i class="fas fa-chart-area"></i> Doanh thu 7 ngày</h3>
        </div>
        <Line :data="chartData" :options="chartOptions" />
      </div>
    </div>

    <div class="row-3">
      <!-- Top products -->
      <div class="card">
        <div class="card-header"><h3><i class="fas fa-fire"></i> Sản phẩm bán chạy</h3></div>
        <div class="product-list">
          <div v-for="(p, i) in topProducts" :key="p.id" class="product-row">
            <span class="rank" :class="i < 3 ? 'top' : ''">{{ i + 1 }}</span>
            <img :src="p.image" :alt="p.name" />
            <div class="product-info">
              <p class="product-name">{{ p.name }}</p>
              <p class="product-cat">{{ p.category }}</p>
            </div>
            <div class="product-stats">
              <p class="product-price">{{ formatPrice(p.price) }}</p>
              <p class="product-reviews"><i class="fas fa-star"></i> {{ p.rating }} ({{ p.reviews }})</p>
            </div>
          </div>
        </div>
      </div>

      <!-- Order status doughnut -->
      <div class="card">
        <div class="card-header"><h3><i class="fas fa-chart-pie"></i> Trạng thái đơn hàng</h3></div>
        <Doughnut :data="doughnutData" :options="doughnutOptions" />
        <div class="legend">
          <div v-for="(item, i) in legendItems" :key="i" class="legend-item">            <span class="legend-dot" :style="{ background: item.color }"></span>
            <span>{{ item.label }}</span>
            <span class="legend-val">{{ item.value }}</span>
          </div>
        </div>
      </div>

      <!-- Quick stats -->
      <div class="card">
        <div class="card-header"><h3><i class="fas fa-tachometer-alt"></i> Tổng quan</h3></div>
        <div class="quick-stats">
          <div v-for="q in quickStats" :key="q.label" class="quick-item">
            <div class="quick-icon-wrap" :style="{ background: q.color + '18', color: q.color }">
              <i :class="q.icon"></i>
            </div>
            <div>
              <p class="quick-val">{{ q.value }}</p>
              <p class="quick-label">{{ q.label }}</p>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { Line, Doughnut } from 'vue-chartjs'
import { Chart as ChartJS, CategoryScale, LinearScale, PointElement, LineElement, ArcElement, Tooltip, Legend, Filler } from 'chart.js'
import { orderService } from '@/services/orderService.js'
import { productService } from '@/services/productService.js'
import { formatPrice } from '@/utils/format.js'

ChartJS.register(CategoryScale, LinearScale, PointElement, LineElement, ArcElement, Tooltip, Legend, Filler)

const recentOrders = ref([])
const allOrders = ref([])
const allProducts = ref([])

onMounted(async () => {
  try {
    allOrders.value = await orderService.getMyOrders()
    recentOrders.value = allOrders.value.slice(0, 6)
  } catch {}
  try {
    allProducts.value = await productService.getAll()
  } catch {}
})

// Stats từ dữ liệu thật
const totalRevenue = computed(() =>
  allOrders.value.filter(o => o.payment_status === 'paid').reduce((s, o) => s + o.total, 0)
)
const totalOrders = computed(() => allOrders.value.length)
const paidOrders = computed(() => allOrders.value.filter(o => o.payment_status === 'paid').length)
const waitingOrders = computed(() => allOrders.value.filter(o => o.payment_status === 'waiting').length)
const codOrders = computed(() => allOrders.value.filter(o => o.payment_method === 'cod').length)

const stats = computed(() => [
  { label: 'Tổng doanh thu', value: formatPrice(totalRevenue.value), change: `${paidOrders.value} đơn paid`, up: true, icon: 'fas fa-dollar-sign', color: '#3b82f6', sparkline: '0,35 15,20 30,28 45,15 60,22 75,10 100,18' },
  { label: 'Đơn hàng', value: String(totalOrders.value), change: `${paidOrders.value} đã TT`, up: true, icon: 'fas fa-box', color: '#f59e0b', sparkline: '0,30 20,25 40,32 60,18 80,22 100,15' },
  { label: 'Sản phẩm', value: String(allProducts.value.length), change: 'trong kho', up: true, icon: 'fas fa-tshirt', color: '#10b981', sparkline: '0,38 25,28 50,32 75,20 100,25' },
  { label: 'Chờ thanh toán', value: String(waitingOrders.value), change: 'đơn pending', up: waitingOrders.value === 0, icon: 'fas fa-clock', color: '#f43f5e', sparkline: '0,20 30,22 60,18 80,20 100,19' },
])

// Chart doanh thu theo ngày (7 ngày gần nhất)
const chartData = computed(() => {
  const days = Array.from({ length: 7 }, (_, i) => {
    const d = new Date()
    d.setDate(d.getDate() - (6 - i))
    return d
  })
  const labels = days.map(d => ['CN','T2','T3','T4','T5','T6','T7'][d.getDay()])
  const data = days.map(d => {
    const dateStr = d.toISOString().slice(0, 10)
    return allOrders.value
      .filter(o => o.payment_status === 'paid' && o.created_at?.slice(0, 10) === dateStr)
      .reduce((s, o) => s + o.total, 0)
  })
  return {
    labels,
    datasets: [{
      label: 'Doanh thu',
      data,
      borderColor: '#3b82f6',
      backgroundColor: 'rgba(59,130,246,0.1)',
      fill: true, tension: 0.4,
      pointBackgroundColor: '#3b82f6', pointRadius: 4,
    }]
  }
})

const chartOptions = { responsive: true, plugins: { legend: { position: 'bottom' } }, scales: { y: { ticks: { callback: v => formatPrice(v) } } } }

// Doughnut từ dữ liệu thật
const doughnutData = computed(() => ({
  labels: ['Đã thanh toán', 'Chờ thanh toán', 'COD'],
  datasets: [{ data: [paidOrders.value, waitingOrders.value, codOrders.value], backgroundColor: ['#10b981', '#f59e0b', '#3b82f6'], borderWidth: 0 }]
}))
const doughnutOptions = { responsive: true, plugins: { legend: { display: false } }, cutout: '70%' }
const legendItems = computed(() => [
  { label: 'Đã thanh toán', value: paidOrders.value, color: '#10b981' },
  { label: 'Chờ thanh toán', value: waitingOrders.value, color: '#f59e0b' },
  { label: 'COD', value: codOrders.value, color: '#3b82f6' },
])

// Top products từ API
const topProducts = computed(() => [...allProducts.value].sort((a, b) => b.reviews - a.reviews).slice(0, 5))

// Quick stats thật
const quickStats = computed(() => [
  { icon: 'fas fa-box', label: 'Tổng đơn hàng', value: String(totalOrders.value), color: '#3b82f6' },
  { icon: 'fas fa-check-circle', label: 'Đã thanh toán', value: String(paidOrders.value), color: '#10b981' },
  { icon: 'fas fa-clock', label: 'Chờ thanh toán', value: String(waitingOrders.value), color: '#f59e0b' },
  { icon: 'fas fa-money-bill', label: 'COD', value: String(codOrders.value), color: '#8b5cf6' },
  { icon: 'fas fa-tshirt', label: 'Sản phẩm', value: String(allProducts.value.length), color: '#06b6d4' },
  { icon: 'fas fa-dollar-sign', label: 'Doanh thu', value: formatPrice(totalRevenue.value), color: '#f43f5e' },
])

function statusLabel(s) { return { paid: 'Đã TT', waiting: 'Chờ TT', unpaid: 'Chưa TT' }[s] || s }
function formatDate(d) { return d ? new Date(d).toLocaleString('vi-VN') : '' }
</script>

<style scoped>
.dashboard { display: flex; flex-direction: column; gap: 20px; }
.stats-grid { display: grid; grid-template-columns: repeat(4, 1fr); gap: 16px; }
.stat-card { background: #fff; border-radius: 12px; padding: 20px; overflow: hidden; box-shadow: 0 1px 4px rgba(0,0,0,0.06); border-top: 3px solid var(--accent); }
.stat-top { display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 8px; }
.stat-label { font-size: 12px; color: #64748b; margin-bottom: 6px; }
.stat-value { font-size: 24px; font-weight: 800; color: #1e293b; }
.stat-icon-wrap { width: 44px; height: 44px; border-radius: 10px; display: flex; align-items: center; justify-content: center; font-size: 18px; }
.stat-change { font-size: 12px; margin-bottom: 12px; display: flex; align-items: center; gap: 4px; }
.stat-change.up { color: #10b981; } .stat-change.down { color: #ef4444; }
.stat-chart { height: 48px; }
.stat-chart svg { width: 100%; height: 100%; }
.row-2 { display: grid; grid-template-columns: 1fr 380px; gap: 16px; }
.row-3 { display: grid; grid-template-columns: repeat(3, 1fr); gap: 16px; }
.card { background: #fff; border-radius: 12px; padding: 20px; box-shadow: 0 1px 4px rgba(0,0,0,0.06); }
.card-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 16px; }
.card-header h3 { font-size: 15px; font-weight: 700; color: #1e293b; display: flex; align-items: center; gap: 8px; }
.see-all { font-size: 12px; color: #3b82f6; display: flex; align-items: center; gap: 4px; }
.data-table { width: 100%; border-collapse: collapse; font-size: 13px; }
.data-table th { text-align: left; padding: 8px 10px; color: #64748b; font-weight: 600; font-size: 11px; text-transform: uppercase; border-bottom: 1px solid #f1f5f9; }
.data-table td { padding: 10px 10px; border-bottom: 1px solid #f8fafc; }
.order-id { font-weight: 700; color: #3b82f6; }
.amount { font-weight: 600; }
.time { color: #94a3b8; font-size: 12px; }
.pay-badge { background: #eff6ff; color: #3b82f6; font-size: 10px; font-weight: 700; padding: 2px 8px; border-radius: 4px; }
.status-badge { font-size: 11px; font-weight: 600; padding: 3px 8px; border-radius: 20px; }
.status-badge.paid { background: #dcfce7; color: #166534; }
.status-badge.waiting { background: #fef3c7; color: #92400e; }
.status-badge.unpaid { background: #fee2e2; color: #991b1b; }
.empty-row { text-align: center; color: #94a3b8; padding: 24px; }
.product-list { display: flex; flex-direction: column; gap: 12px; }
.product-row { display: flex; align-items: center; gap: 10px; }
.rank { width: 22px; height: 22px; border-radius: 50%; background: #f1f5f9; color: #64748b; font-size: 11px; font-weight: 700; display: flex; align-items: center; justify-content: center; flex-shrink: 0; }
.rank.top { background: #fef3c7; color: #92400e; }
.product-row img { width: 40px; height: 40px; object-fit: cover; border-radius: 6px; }
.product-info { flex: 1; }
.product-name { font-size: 13px; font-weight: 500; }
.product-cat { font-size: 11px; color: #94a3b8; }
.product-stats { text-align: right; }
.product-price { font-size: 13px; font-weight: 700; }
.product-reviews { font-size: 11px; color: #f59e0b; }
.legend { display: flex; flex-direction: column; gap: 8px; margin-top: 16px; }
.legend-item { display: flex; align-items: center; gap: 8px; font-size: 13px; }
.legend-dot { width: 10px; height: 10px; border-radius: 50%; flex-shrink: 0; }
.legend-val { margin-left: auto; font-weight: 700; }
.quick-stats { display: flex; flex-direction: column; gap: 10px; }
.quick-item { display: flex; align-items: center; gap: 12px; padding: 10px; background: #f8fafc; border-radius: 8px; }
.quick-icon-wrap { width: 36px; height: 36px; border-radius: 8px; display: flex; align-items: center; justify-content: center; font-size: 14px; flex-shrink: 0; }
.quick-val { font-size: 15px; font-weight: 700; color: #1e293b; }
.quick-label { font-size: 11px; color: #64748b; }
@media (max-width: 1200px) { .stats-grid { grid-template-columns: repeat(2, 1fr); } .row-2 { grid-template-columns: 1fr; } .row-3 { grid-template-columns: 1fr 1fr; } }
@media (max-width: 768px) { .stats-grid { grid-template-columns: 1fr 1fr; } .row-3 { grid-template-columns: 1fr; } }
</style>
