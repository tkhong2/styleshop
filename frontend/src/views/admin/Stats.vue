<template>
  <div class="page">
    <!-- Period selector -->
    <div class="period-bar card">
      <span class="period-label"><i class="fas fa-calendar-alt"></i> Khoảng thời gian:</span>
      <div class="period-btns">
        <button v-for="p in periods" :key="p.value" :class="['period-btn', { active: period === p.value }]" @click="period = p.value">
          {{ p.label }}
        </button>
      </div>
    </div>

    <!-- KPI cards -->
    <div class="kpi-grid">
      <div v-for="kpi in kpis" :key="kpi.label" class="kpi-card" :style="{'--c': kpi.color}">
        <div class="kpi-left">
          <p class="kpi-label">{{ kpi.label }}</p>
          <p class="kpi-value">{{ kpi.value }}</p>
          <p class="kpi-change" :class="kpi.up ? 'up' : 'down'">
            <i :class="kpi.up ? 'fas fa-arrow-up' : 'fas fa-arrow-down'"></i>
            {{ kpi.change }} so với kỳ trước
          </p>
        </div>
        <div class="kpi-icon"><i :class="kpi.icon"></i></div>
      </div>
    </div>

    <div class="charts-row">
      <!-- Revenue line chart -->
      <div class="card chart-big">
        <div class="card-header">
          <h3><i class="fas fa-chart-area"></i> Doanh thu theo ngày</h3>
        </div>
        <Line :data="revenueData" :options="lineOpts" />
      </div>

      <!-- Category pie -->
      <div class="card chart-small">
        <div class="card-header">
          <h3><i class="fas fa-chart-pie"></i> Doanh thu theo danh mục</h3>
        </div>
        <Doughnut :data="catData" :options="doughnutOpts" />
        <div class="legend">
          <div v-for="(item, i) in catLegend" :key="i" class="legend-item">
            <span class="dot" :style="{ background: item.color }"></span>
            <span class="leg-label">{{ item.label }}</span>
            <span class="leg-val">{{ item.pct }}%</span>
          </div>
        </div>
      </div>
    </div>

    <div class="charts-row">
      <!-- Orders bar chart -->
      <div class="card chart-big">
        <div class="card-header">
          <h3><i class="fas fa-chart-bar"></i> Số đơn hàng theo ngày</h3>
        </div>
        <Bar :data="ordersData" :options="barOpts" />
      </div>

      <!-- Payment methods -->
      <div class="card chart-small">
        <div class="card-header">
          <h3><i class="fas fa-credit-card"></i> Phương thức thanh toán</h3>
        </div>
        <div class="pay-stats">
          <div v-for="pm in payMethods" :key="pm.label" class="pay-row">
            <div class="pay-info">
              <i :class="pm.icon" :style="{ color: pm.color }"></i>
              <span>{{ pm.label }}</span>
            </div>
            <div class="pay-bar-wrap">
              <div class="pay-bar" :style="{ width: pm.pct + '%', background: pm.color }"></div>
            </div>
            <span class="pay-pct">{{ pm.pct }}%</span>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { Line, Doughnut, Bar } from 'vue-chartjs'
import { Chart as ChartJS, CategoryScale, LinearScale, PointElement, LineElement, BarElement, ArcElement, Tooltip, Legend, Filler } from 'chart.js'

ChartJS.register(CategoryScale, LinearScale, PointElement, LineElement, BarElement, ArcElement, Tooltip, Legend, Filler)

const period = ref('7d')
const periods = [
  { label: '7 ngày', value: '7d' },
  { label: '30 ngày', value: '30d' },
  { label: '3 tháng', value: '3m' },
  { label: '1 năm', value: '1y' },
]

const kpis = [
  { label: 'Tổng doanh thu', value: '48.250.000đ', change: '+12.5%', up: true, icon: 'fas fa-dollar-sign', color: '#3b82f6' },
  { label: 'Tổng đơn hàng', value: '186', change: '+8 đơn', up: true, icon: 'fas fa-box', color: '#10b981' },
  { label: 'Khách hàng mới', value: '34', change: '+5', up: true, icon: 'fas fa-user-plus', color: '#f59e0b' },
  { label: 'Giá trị TB/đơn', value: '259.000đ', change: '+3.2%', up: true, icon: 'fas fa-receipt', color: '#8b5cf6' },
]

const labels7d = ['T2', 'T3', 'T4', 'T5', 'T6', 'T7', 'CN']
const revenueData = {
  labels: labels7d,
  datasets: [
    { label: 'Doanh thu', data: [1200000, 1900000, 1500000, 2800000, 2200000, 3100000, 2400000], borderColor: '#3b82f6', backgroundColor: 'rgba(59,130,246,0.1)', fill: true, tension: 0.4, pointBackgroundColor: '#3b82f6', pointRadius: 4 },
    { label: 'Tuần trước', data: [900000, 1400000, 1200000, 2100000, 1800000, 2600000, 2000000], borderColor: '#94a3b8', backgroundColor: 'rgba(148,163,184,0.05)', fill: true, tension: 0.4, pointBackgroundColor: '#94a3b8', pointRadius: 3 },
  ]
}
const lineOpts = { responsive: true, plugins: { legend: { position: 'bottom' } }, scales: { y: { ticks: { callback: v => (v/1000000).toFixed(1) + 'M' } } } }

const ordersData = {
  labels: labels7d,
  datasets: [{ label: 'Đơn hàng', data: [12, 19, 15, 28, 22, 31, 24], backgroundColor: 'rgba(59,130,246,0.7)', borderRadius: 6 }]
}
const barOpts = { responsive: true, plugins: { legend: { display: false } } }

const catData = {
  labels: ['Áo', 'Quần', 'Váy & Đầm', 'Giày', 'Túi'],
  datasets: [{ data: [38, 18, 22, 12, 10], backgroundColor: ['#3b82f6','#10b981','#ec4899','#f59e0b','#8b5cf6'], borderWidth: 0 }]
}
const doughnutOpts = { responsive: true, plugins: { legend: { display: false } }, cutout: '65%' }
const catLegend = [
  { label: 'Áo', pct: 38, color: '#3b82f6' },
  { label: 'Quần', pct: 18, color: '#10b981' },
  { label: 'Váy & Đầm', pct: 22, color: '#ec4899' },
  { label: 'Giày', pct: 12, color: '#f59e0b' },
  { label: 'Túi', pct: 10, color: '#8b5cf6' },
]

const payMethods = [
  { label: 'Chuyển khoản', pct: 45, color: '#3b82f6', icon: 'fas fa-university' },
  { label: 'COD', pct: 38, color: '#10b981', icon: 'fas fa-money-bill' },
  { label: 'MoMo', pct: 17, color: '#ec4899', icon: 'fas fa-wallet' },
]
</script>

<style scoped>
.page { display: flex; flex-direction: column; gap: 16px; }
.card { background: #fff; border-radius: 12px; padding: 20px; box-shadow: 0 1px 4px rgba(0,0,0,0.06); }
.period-bar { display: flex; align-items: center; gap: 16px; flex-wrap: wrap; }
.period-label { font-size: 13px; font-weight: 600; color: #475569; display: flex; align-items: center; gap: 6px; }
.period-btns { display: flex; gap: 6px; }
.period-btn { padding: 7px 16px; border-radius: 8px; font-size: 13px; font-weight: 500; border: 1.5px solid #e2e8f0; background: #fff; color: #64748b; transition: all 0.15s; }
.period-btn.active { background: #3b82f6; color: #fff; border-color: #3b82f6; }
.period-btn:hover:not(.active) { border-color: #3b82f6; color: #3b82f6; }
.kpi-grid { display: grid; grid-template-columns: repeat(4, 1fr); gap: 14px; }
.kpi-card { background: #fff; border-radius: 12px; padding: 20px; display: flex; justify-content: space-between; align-items: center; box-shadow: 0 1px 4px rgba(0,0,0,0.06); border-top: 3px solid var(--c); }
.kpi-label { font-size: 12px; color: #64748b; margin-bottom: 6px; }
.kpi-value { font-size: 22px; font-weight: 800; color: #1e293b; margin-bottom: 6px; }
.kpi-change { font-size: 12px; display: flex; align-items: center; gap: 4px; }
.kpi-change.up { color: #10b981; } .kpi-change.down { color: #ef4444; }
.kpi-icon { width: 48px; height: 48px; border-radius: 12px; background: color-mix(in srgb, var(--c) 12%, white); color: var(--c); display: flex; align-items: center; justify-content: center; font-size: 20px; }
.charts-row { display: grid; grid-template-columns: 1fr 320px; gap: 16px; }
.card-header { display: flex; align-items: center; margin-bottom: 16px; }
.card-header h3 { font-size: 15px; font-weight: 700; color: #1e293b; display: flex; align-items: center; gap: 8px; }
.legend { display: flex; flex-direction: column; gap: 8px; margin-top: 16px; }
.legend-item { display: flex; align-items: center; gap: 8px; font-size: 13px; }
.dot { width: 10px; height: 10px; border-radius: 50%; flex-shrink: 0; }
.leg-label { flex: 1; color: #475569; }
.leg-val { font-weight: 700; color: #1e293b; }
.pay-stats { display: flex; flex-direction: column; gap: 16px; margin-top: 8px; }
.pay-row { display: flex; align-items: center; gap: 10px; }
.pay-info { display: flex; align-items: center; gap: 8px; min-width: 130px; font-size: 13px; color: #475569; }
.pay-bar-wrap { flex: 1; height: 8px; background: #f1f5f9; border-radius: 4px; overflow: hidden; }
.pay-bar { height: 100%; border-radius: 4px; transition: width 0.5s; }
.pay-pct { font-size: 13px; font-weight: 700; color: #1e293b; min-width: 36px; text-align: right; }
@media (max-width: 1100px) { .kpi-grid { grid-template-columns: 1fr 1fr; } .charts-row { grid-template-columns: 1fr; } }
@media (max-width: 600px) { .kpi-grid { grid-template-columns: 1fr; } }
</style>
