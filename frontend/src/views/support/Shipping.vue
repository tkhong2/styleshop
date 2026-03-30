<template>
  <div class="support-page">
    <div class="container">
      <div class="breadcrumb">
        <RouterLink to="/">Trang chủ</RouterLink> / <span>Thanh toán & Giao nhận</span>
      </div>
      <h1 class="page-title"><i class="fas fa-truck"></i> Thanh toán & Giao nhận</h1>

      <div class="content-grid">
        <div class="main-content">
          <!-- Shipping info -->
          <div class="section-card">
            <h2><i class="fas fa-map-marker-alt"></i> Phạm vi giao hàng & Thời gian</h2>
            <div class="shipping-table">
              <div class="sh-row header">
                <span>Khu vực</span><span>Thời gian</span><span>Phí ship</span>
              </div>
              <div class="sh-row" v-for="r in shippingRates" :key="r.area">
                <span>{{ r.area }}</span>
                <span>{{ r.time }}</span>
                <span :class="r.free ? 'free' : ''">{{ r.fee }}</span>
              </div>
            </div>
            <p class="note"><i class="fas fa-info-circle"></i> Miễn phí vận chuyển cho đơn hàng từ <strong>500.000đ</strong></p>
          </div>

          <!-- Payment methods -->
          <div class="section-card">
            <h2><i class="fas fa-credit-card"></i> Phương thức thanh toán</h2>
            <div class="payment-methods">
              <div v-for="pm in paymentMethods" :key="pm.name" class="pm-card">
                <div class="pm-icon" :style="{ background: pm.bg, color: pm.color }">
                  <i :class="pm.icon"></i>
                </div>
                <div>
                  <p class="pm-name">{{ pm.name }}</p>
                  <p class="pm-desc">{{ pm.desc }}</p>
                </div>
              </div>
            </div>
          </div>

          <!-- Shipping process -->
          <div class="section-card">
            <h2><i class="fas fa-route"></i> Quy trình giao hàng</h2>
            <div class="timeline">
              <div v-for="(step, i) in timeline" :key="i" class="tl-item">
                <div class="tl-dot"></div>
                <div class="tl-content">
                  <p class="tl-title">{{ step.title }}</p>
                  <p class="tl-desc">{{ step.desc }}</p>
                </div>
              </div>
            </div>
          </div>
        </div>

        <aside class="sidebar">
          <div class="tip-card">
            <h3><i class="fas fa-headset"></i> Hỗ trợ giao hàng</h3>
            <p>Hotline: <a href="tel:18001162"><strong>091 708 0222</strong></a></p>
            <p class="time">08:00 – 21:00 mỗi ngày</p>
          </div>
          <div class="tip-card">
            <h3><i class="fas fa-exclamation-circle" style="color:#f59e0b"></i> Lưu ý khi nhận hàng</h3>
            <ul>
              <li>Kiểm tra hàng trước khi ký nhận</li>
              <li>Quay video khi mở hộp nếu nghi ngờ</li>
              <li>Không nhận hàng bị móp méo, rách bao bì</li>
              <li>Liên hệ ngay nếu có vấn đề</li>
            </ul>
          </div>
        </aside>
      </div>
    </div>
  </div>
</template>

<script setup>
const shippingRates = [
  { area: 'Nội thành TP.HCM & Hà Nội', time: '1–2 ngày', fee: 'Miễn phí (≥500k)', free: true },
  { area: 'Tỉnh thành khác', time: '3–5 ngày', fee: 'Miễn phí (≥500k)', free: true },
  { area: 'Vùng sâu, vùng xa', time: '5–7 ngày', fee: '30.000đ', free: false },
]

const paymentMethods = [
  { name: 'Chuyển khoản ngân hàng', desc: 'BIDV qua VietQR – Xác nhận tự động qua SePay', icon: 'fas fa-university', bg: '#eff6ff', color: '#3b82f6' },
  { name: 'Ví MoMo', desc: 'Thanh toán nhanh qua ví điện tử MoMo', icon: 'fas fa-wallet', bg: '#fdf0f8', color: '#a50064' },
  { name: 'COD – Thanh toán khi nhận hàng', desc: 'Trả tiền mặt khi nhận hàng, không cần thanh toán trước', icon: 'fas fa-money-bill-wave', bg: '#f0fdf4', color: '#16a34a' },
]

const timeline = [
  { title: 'Đặt hàng thành công', desc: 'Hệ thống xác nhận đơn hàng và gửi email thông báo' },
  { title: 'Xử lý đơn hàng', desc: 'Kho hàng kiểm tra và đóng gói sản phẩm (1–2 giờ)' },
  { title: 'Bàn giao cho đơn vị vận chuyển', desc: 'Đơn hàng được bàn giao cho đối tác vận chuyển' },
  { title: 'Đang vận chuyển', desc: 'Bạn nhận được mã vận đơn để theo dõi' },
  { title: 'Giao hàng thành công', desc: 'Shipper liên hệ trước khi giao, ký nhận và kiểm tra hàng' },
]
</script>

<style scoped>
.support-page { padding: 40px 0 80px; background: #fafafa; min-height: 100vh; }
.breadcrumb { font-size: 13px; color: #888; margin-bottom: 24px; }
.breadcrumb a { color: #888; } .breadcrumb a:hover { color: #1a1a1a; }
.page-title { font-size: 28px; font-weight: 800; margin-bottom: 28px; display: flex; align-items: center; gap: 12px; }
.page-title i { color: #3b82f6; }
.content-grid { display: grid; grid-template-columns: 1fr 260px; gap: 24px; align-items: start; }
.section-card { background: #fff; border-radius: 12px; padding: 24px; margin-bottom: 16px; box-shadow: 0 1px 4px rgba(0,0,0,0.06); }
.section-card h2 { font-size: 16px; font-weight: 700; margin-bottom: 16px; display: flex; align-items: center; gap: 8px; }
.section-card h2 i { color: #3b82f6; }
.shipping-table { border-radius: 8px; overflow: hidden; border: 1px solid #e2e8f0; margin-bottom: 12px; }
.sh-row { display: grid; grid-template-columns: 2fr 1fr 1fr; padding: 12px 16px; font-size: 13px; }
.sh-row.header { background: #1a1a1a; color: #fff; font-weight: 600; font-size: 12px; }
.sh-row:not(.header) { border-bottom: 1px solid #f1f5f9; }
.sh-row:not(.header):hover { background: #f8fafc; }
.free { color: #16a34a; font-weight: 600; }
.note { font-size: 13px; color: #666; display: flex; align-items: center; gap: 6px; }
.note i { color: #3b82f6; }
.payment-methods { display: flex; flex-direction: column; gap: 12px; }
.pm-card { display: flex; align-items: center; gap: 14px; padding: 14px; background: #f8fafc; border-radius: 10px; }
.pm-icon { width: 44px; height: 44px; border-radius: 10px; display: flex; align-items: center; justify-content: center; font-size: 18px; flex-shrink: 0; }
.pm-name { font-size: 14px; font-weight: 600; margin-bottom: 3px; }
.pm-desc { font-size: 12px; color: #666; }
.timeline { display: flex; flex-direction: column; gap: 0; position: relative; padding-left: 24px; }
.timeline::before { content: ''; position: absolute; left: 7px; top: 8px; bottom: 8px; width: 2px; background: #e2e8f0; }
.tl-item { display: flex; gap: 14px; padding-bottom: 20px; position: relative; }
.tl-dot { width: 16px; height: 16px; border-radius: 50%; background: #3b82f6; border: 3px solid #fff; box-shadow: 0 0 0 2px #3b82f6; flex-shrink: 0; margin-top: 2px; position: absolute; left: -24px; }
.tl-title { font-size: 14px; font-weight: 600; margin-bottom: 3px; }
.tl-desc { font-size: 13px; color: #666; }
.sidebar { display: flex; flex-direction: column; gap: 14px; position: sticky; top: 80px; }
.tip-card { background: #fff; border-radius: 12px; padding: 18px; box-shadow: 0 1px 4px rgba(0,0,0,0.06); }
.tip-card h3 { font-size: 14px; font-weight: 700; margin-bottom: 10px; display: flex; align-items: center; gap: 6px; }
.tip-card h3 i { color: #10b981; }
.tip-card p { font-size: 13px; color: #555; margin-bottom: 6px; }
.tip-card a { color: #3b82f6; }
.time { color: #888 !important; font-size: 12px !important; }
.tip-card ul { padding-left: 16px; display: flex; flex-direction: column; gap: 6px; }
.tip-card li { font-size: 13px; color: #555; }
@media (max-width: 900px) { .content-grid { grid-template-columns: 1fr; } .sidebar { position: static; } }
</style>
