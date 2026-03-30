<template>
  <div class="support-page">
    <div class="container">
      <div class="breadcrumb">
        <RouterLink to="/">Trang chủ</RouterLink> / <span>Chính sách đổi trả</span>
      </div>
      <h1 class="page-title"><i class="fas fa-undo"></i> Chính sách đổi trả</h1>

      <div class="content-grid">
        <div class="main-content">
          <!-- Highlights -->
          <div class="highlight-row">
            <div v-for="h in highlights" :key="h.title" class="highlight-card" :style="{'--c': h.color}">
              <i :class="h.icon"></i>
              <p class="hl-title">{{ h.title }}</p>
              <p class="hl-desc">{{ h.desc }}</p>
            </div>
          </div>

          <div v-for="section in sections" :key="section.title" class="section-card">
            <h2><i :class="section.icon"></i> {{ section.title }}</h2>
            <ul>
              <li v-for="item in section.items" :key="item">{{ item }}</li>
            </ul>
          </div>

          <!-- Process -->
          <div class="section-card">
            <h2><i class="fas fa-list-ol"></i> Quy trình đổi trả</h2>
            <div class="steps">
              <div v-for="(step, i) in steps" :key="i" class="step">
                <div class="step-num">{{ i + 1 }}</div>
                <div>
                  <p class="step-title">{{ step.title }}</p>
                  <p class="step-desc">{{ step.desc }}</p>
                </div>
              </div>
            </div>
          </div>
        </div>

        <aside class="sidebar">
          <div class="tip-card">
            <h3><i class="fas fa-phone"></i> Liên hệ đổi trả</h3>
            <p>Hotline: <a href="tel:18001162"><strong>091 708 0222</strong></a></p>
            <p>Email: <a href="mailto:cskh@styleshop.vn">cskh@styleshop.vn</a></p>
            <p class="time">Thứ 2 – Chủ nhật: 8:00 – 21:00</p>
          </div>
          <div class="tip-card">
            <h3><i class="fas fa-exclamation-triangle" style="color:#f59e0b"></i> Lưu ý</h3>
            <ul>
              <li>Giữ lại hóa đơn mua hàng</li>
              <li>Không giặt/sử dụng sản phẩm trước khi đổi</li>
              <li>Chụp ảnh sản phẩm lỗi trước khi gửi</li>
            </ul>
          </div>
        </aside>
      </div>
    </div>
  </div>
</template>

<script setup>
const highlights = [
  { icon: 'fas fa-calendar-check', title: '30 ngày đổi trả', desc: 'Kể từ ngày nhận hàng', color: '#3b82f6' },
  { icon: 'fas fa-shipping-fast', title: 'Miễn phí đổi', desc: 'Lỗi từ nhà sản xuất', color: '#10b981' },
  { icon: 'fas fa-shield-alt', title: 'Bảo hành chất lượng', desc: 'Cam kết chính hãng', color: '#f59e0b' },
]

const sections = [
  {
    title: 'Điều kiện đổi trả', icon: 'fas fa-check-circle',
    items: [
      'Sản phẩm còn nguyên tem, nhãn mác, chưa qua sử dụng',
      'Có hóa đơn mua hàng hoặc xác nhận đơn hàng',
      'Trong vòng 30 ngày kể từ ngày nhận hàng',
      'Sản phẩm không bị hư hỏng do lỗi của khách hàng',
    ]
  },
  {
    title: 'Trường hợp được đổi trả miễn phí', icon: 'fas fa-gift',
    items: [
      'Sản phẩm bị lỗi từ nhà sản xuất (đường may, vải, khóa...)',
      'Giao sai sản phẩm, sai màu sắc, sai size so với đơn hàng',
      'Sản phẩm bị hư hỏng trong quá trình vận chuyển',
    ]
  },
  {
    title: 'Trường hợp không được đổi trả', icon: 'fas fa-times-circle',
    items: [
      'Sản phẩm đã qua sử dụng, giặt, hoặc bị bẩn',
      'Sản phẩm đã bị cắt tem, nhãn mác',
      'Quá 30 ngày kể từ ngày nhận hàng',
      'Sản phẩm thuộc danh mục sale cuối mùa (ghi rõ không đổi trả)',
    ]
  },
]

const steps = [
  { title: 'Liên hệ hỗ trợ', desc: 'Gọi hotline 091 708 0222 hoặc email để thông báo yêu cầu đổi trả' },
  { title: 'Xác nhận yêu cầu', desc: 'Nhân viên xác nhận điều kiện và hướng dẫn gửi hàng' },
  { title: 'Gửi hàng về', desc: 'Đóng gói cẩn thận và gửi về địa chỉ kho của StyleShop' },
  { title: 'Kiểm tra hàng', desc: 'Chúng tôi kiểm tra trong 1–2 ngày làm việc' },
  { title: 'Hoàn tất', desc: 'Gửi hàng mới hoặc hoàn tiền trong 3–5 ngày làm việc' },
]
</script>

<style scoped>
.support-page { padding: 40px 0 80px; background: #fafafa; min-height: 100vh; }
.breadcrumb { font-size: 13px; color: #888; margin-bottom: 24px; }
.breadcrumb a { color: #888; } .breadcrumb a:hover { color: #1a1a1a; }
.page-title { font-size: 28px; font-weight: 800; margin-bottom: 28px; display: flex; align-items: center; gap: 12px; }
.page-title i { color: #3b82f6; }
.content-grid { display: grid; grid-template-columns: 1fr 260px; gap: 24px; align-items: start; }
.highlight-row { display: grid; grid-template-columns: repeat(3, 1fr); gap: 14px; margin-bottom: 20px; }
.highlight-card { background: #fff; border-radius: 12px; padding: 20px; text-align: center; box-shadow: 0 1px 4px rgba(0,0,0,0.06); border-top: 3px solid var(--c); }
.highlight-card i { font-size: 28px; color: var(--c); margin-bottom: 10px; }
.hl-title { font-size: 14px; font-weight: 700; margin-bottom: 4px; }
.hl-desc { font-size: 12px; color: #888; }
.section-card { background: #fff; border-radius: 12px; padding: 24px; margin-bottom: 16px; box-shadow: 0 1px 4px rgba(0,0,0,0.06); }
.section-card h2 { font-size: 16px; font-weight: 700; margin-bottom: 14px; display: flex; align-items: center; gap: 8px; }
.section-card h2 i { color: #3b82f6; }
.section-card ul { padding-left: 20px; display: flex; flex-direction: column; gap: 8px; }
.section-card li { font-size: 14px; color: #444; line-height: 1.6; }
.steps { display: flex; flex-direction: column; gap: 16px; }
.step { display: flex; gap: 14px; align-items: flex-start; }
.step-num { width: 32px; height: 32px; background: #1a1a1a; color: #fff; border-radius: 50%; display: flex; align-items: center; justify-content: center; font-size: 13px; font-weight: 700; flex-shrink: 0; }
.step-title { font-size: 14px; font-weight: 600; margin-bottom: 3px; }
.step-desc { font-size: 13px; color: #666; }
.sidebar { display: flex; flex-direction: column; gap: 14px; position: sticky; top: 80px; }
.tip-card { background: #fff; border-radius: 12px; padding: 18px; box-shadow: 0 1px 4px rgba(0,0,0,0.06); }
.tip-card h3 { font-size: 14px; font-weight: 700; margin-bottom: 10px; display: flex; align-items: center; gap: 6px; }
.tip-card h3 i { color: #10b981; }
.tip-card p { font-size: 13px; color: #555; margin-bottom: 6px; }
.tip-card a { color: #3b82f6; }
.time { color: #888 !important; font-size: 12px !important; }
.tip-card ul { padding-left: 16px; display: flex; flex-direction: column; gap: 6px; }
.tip-card li { font-size: 13px; color: #555; }
@media (max-width: 900px) { .content-grid { grid-template-columns: 1fr; } .highlight-row { grid-template-columns: 1fr; } .sidebar { position: static; } }
</style>
