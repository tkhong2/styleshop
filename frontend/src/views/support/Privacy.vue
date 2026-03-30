<template>
  <div class="support-page">
    <div class="container">
      <div class="breadcrumb">
        <RouterLink to="/">Trang chủ</RouterLink> / <span>Chính sách bảo mật</span>
      </div>
      <h1 class="page-title"><i class="fas fa-shield-alt"></i> Chính sách bảo mật</h1>
      <p class="updated">Cập nhật lần cuối: 30/03/2026</p>

      <div class="content-grid">
        <div class="main-content">
          <div v-for="section in sections" :key="section.title" class="section-card">
            <h2><i :class="section.icon"></i> {{ section.title }}</h2>
            <div v-for="(block, i) in section.blocks" :key="i">
              <h3 v-if="block.subtitle">{{ block.subtitle }}</h3>
              <p v-if="block.text">{{ block.text }}</p>
              <ul v-if="block.list">
                <li v-for="item in block.list" :key="item">{{ item }}</li>
              </ul>
            </div>
          </div>
        </div>

        <aside class="sidebar">
          <nav class="toc">
            <p class="toc-title">Mục lục</p>
            <a v-for="s in sections" :key="s.title" href="#" class="toc-link">{{ s.title }}</a>
          </nav>
          <div class="tip-card">
            <h3><i class="fas fa-envelope"></i> Liên hệ về bảo mật</h3>
            <p>Email: <a href="mailto:privacy@styleshop.vn">privacy@styleshop.vn</a></p>
          </div>
        </aside>
      </div>
    </div>
  </div>
</template>

<script setup>
const sections = [
  {
    title: '1. Thông tin chúng tôi thu thập', icon: 'fas fa-database',
    blocks: [
      { subtitle: 'Thông tin bạn cung cấp', list: ['Họ tên, địa chỉ email, số điện thoại khi đăng ký tài khoản', 'Địa chỉ giao hàng khi đặt hàng', 'Thông tin thanh toán (không lưu trữ thông tin thẻ)'] },
      { subtitle: 'Thông tin tự động thu thập', list: ['Địa chỉ IP, loại trình duyệt, thiết bị', 'Lịch sử duyệt web và mua sắm trên StyleShop', 'Cookie và dữ liệu phiên làm việc'] },
    ]
  },
  {
    title: '2. Mục đích sử dụng thông tin', icon: 'fas fa-bullseye',
    blocks: [
      { list: ['Xử lý đơn hàng và giao hàng', 'Gửi thông báo về đơn hàng và khuyến mãi', 'Cải thiện trải nghiệm mua sắm', 'Phân tích và nghiên cứu thị trường', 'Tuân thủ các yêu cầu pháp lý'] }
    ]
  },
  {
    title: '3. Chia sẻ thông tin', icon: 'fas fa-share-alt',
    blocks: [
      { text: 'Chúng tôi không bán hoặc cho thuê thông tin cá nhân của bạn. Thông tin chỉ được chia sẻ với:' },
      { list: ['Đối tác vận chuyển để giao hàng', 'Cổng thanh toán để xử lý giao dịch', 'Cơ quan nhà nước khi có yêu cầu pháp lý'] }
    ]
  },
  {
    title: '4. Bảo mật thông tin', icon: 'fas fa-lock',
    blocks: [
      { text: 'Chúng tôi áp dụng các biện pháp bảo mật tiêu chuẩn ngành để bảo vệ thông tin của bạn:' },
      { list: ['Mã hóa SSL/TLS cho tất cả kết nối', 'Không lưu trữ thông tin thẻ tín dụng', 'Kiểm soát truy cập nghiêm ngặt vào dữ liệu', 'Sao lưu dữ liệu định kỳ'] }
    ]
  },
  {
    title: '5. Quyền của bạn', icon: 'fas fa-user-shield',
    blocks: [
      { list: ['Truy cập và xem thông tin cá nhân đã cung cấp', 'Yêu cầu chỉnh sửa thông tin không chính xác', 'Yêu cầu xóa tài khoản và dữ liệu', 'Từ chối nhận email marketing', 'Khiếu nại về việc xử lý dữ liệu'] }
    ]
  },
  {
    title: '6. Cookie', icon: 'fas fa-cookie-bite',
    blocks: [
      { text: 'Chúng tôi sử dụng cookie để cải thiện trải nghiệm của bạn. Cookie giúp ghi nhớ giỏ hàng, tùy chọn và phiên đăng nhập. Bạn có thể tắt cookie trong cài đặt trình duyệt, tuy nhiên một số tính năng có thể không hoạt động.' }
    ]
  },
]
</script>

<style scoped>
.support-page { padding: 40px 0 80px; background: #fafafa; min-height: 100vh; }
.breadcrumb { font-size: 13px; color: #888; margin-bottom: 24px; }
.breadcrumb a { color: #888; } .breadcrumb a:hover { color: #1a1a1a; }
.page-title { font-size: 28px; font-weight: 800; margin-bottom: 8px; display: flex; align-items: center; gap: 12px; }
.page-title i { color: #3b82f6; }
.updated { font-size: 13px; color: #888; margin-bottom: 28px; }
.content-grid { display: grid; grid-template-columns: 1fr 240px; gap: 24px; align-items: start; }
.section-card { background: #fff; border-radius: 12px; padding: 24px; margin-bottom: 16px; box-shadow: 0 1px 4px rgba(0,0,0,0.06); }
.section-card h2 { font-size: 16px; font-weight: 700; margin-bottom: 14px; display: flex; align-items: center; gap: 8px; color: #1a1a1a; }
.section-card h2 i { color: #3b82f6; }
.section-card h3 { font-size: 14px; font-weight: 600; margin: 12px 0 8px; color: #334155; }
.section-card p { font-size: 14px; color: #555; line-height: 1.7; margin-bottom: 8px; }
.section-card ul { padding-left: 20px; display: flex; flex-direction: column; gap: 6px; }
.section-card li { font-size: 14px; color: #555; line-height: 1.6; }
.sidebar { display: flex; flex-direction: column; gap: 14px; position: sticky; top: 80px; }
.toc { background: #fff; border-radius: 12px; padding: 18px; box-shadow: 0 1px 4px rgba(0,0,0,0.06); }
.toc-title { font-size: 12px; font-weight: 700; text-transform: uppercase; letter-spacing: 1px; color: #888; margin-bottom: 10px; }
.toc-link { display: block; font-size: 13px; color: #555; padding: 5px 0; border-bottom: 1px solid #f1f5f9; }
.toc-link:hover { color: #3b82f6; }
.tip-card { background: #fff; border-radius: 12px; padding: 18px; box-shadow: 0 1px 4px rgba(0,0,0,0.06); }
.tip-card h3 { font-size: 14px; font-weight: 700; margin-bottom: 10px; display: flex; align-items: center; gap: 6px; }
.tip-card h3 i { color: #3b82f6; }
.tip-card p { font-size: 13px; color: #555; }
.tip-card a { color: #3b82f6; }
@media (max-width: 900px) { .content-grid { grid-template-columns: 1fr; } .sidebar { position: static; } }
</style>
