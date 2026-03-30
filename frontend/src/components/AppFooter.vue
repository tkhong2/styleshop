<template>
  <footer class="footer">
    <div class="container footer-top">
      <div class="footer-brand">
        <h3>STYLESHOP</h3>
        <p>Thời trang chất lượng cao, phong cách hiện đại cho mọi người.</p>
        <div class="socials">
          <a href="#" aria-label="Facebook">
            <svg width="18" height="18" viewBox="0 0 24 24" fill="currentColor"><path d="M18 2h-3a5 5 0 00-5 5v3H7v4h3v8h4v-8h3l1-4h-4V7a1 1 0 011-1h3z"/></svg>
          </a>
          <a href="#" aria-label="Instagram">
            <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="2" y="2" width="20" height="20" rx="5"/><path d="M16 11.37A4 4 0 1112.63 8 4 4 0 0116 11.37z"/><line x1="17.5" y1="6.5" x2="17.51" y2="6.5"/></svg>
          </a>
          <a href="#" aria-label="TikTok">
            <svg width="18" height="18" viewBox="0 0 24 24" fill="currentColor"><path d="M19.59 6.69a4.83 4.83 0 01-3.77-4.25V2h-3.45v13.67a2.89 2.89 0 01-2.88 2.5 2.89 2.89 0 01-2.89-2.89 2.89 2.89 0 012.89-2.89c.28 0 .54.04.79.1V9.01a6.33 6.33 0 00-.79-.05 6.34 6.34 0 00-6.34 6.34 6.34 6.34 0 006.34 6.34 6.34 6.34 0 006.33-6.34V8.69a8.18 8.18 0 004.78 1.52V6.76a4.85 4.85 0 01-1.01-.07z"/></svg>
          </a>
          <a href="#" aria-label="YouTube">
            <svg width="18" height="18" viewBox="0 0 24 24" fill="currentColor"><path d="M22.54 6.42a2.78 2.78 0 00-1.95-1.96C18.88 4 12 4 12 4s-6.88 0-8.59.46a2.78 2.78 0 00-1.95 1.96A29 29 0 001 12a29 29 0 00.46 5.58A2.78 2.78 0 003.41 19.6C5.12 20 12 20 12 20s6.88 0 8.59-.46a2.78 2.78 0 001.95-1.95A29 29 0 0023 12a29 29 0 00-.46-5.58z"/><polygon points="9.75 15.02 15.5 12 9.75 8.98 9.75 15.02" fill="white"/></svg>
          </a>
        </div>
      </div>

      <div class="footer-col">
        <h4>Sản phẩm</h4>
        <RouterLink to="/products?category=giay">Giày</RouterLink>
        <RouterLink to="/products?category=tui">Túi xách</RouterLink>
        <RouterLink to="/products?category=phu-kien">Phụ kiện</RouterLink>
        <RouterLink to="/products?category=quan-ao">Quần áo</RouterLink>
        <RouterLink to="/products?sale=true">Sale</RouterLink>
      </div>

      <div class="footer-col">
        <h4>Hỗ trợ khách hàng</h4>
        <a href="#">Hướng dẫn chọn size</a>
        <a href="#">Câu hỏi thường gặp</a>
        <a href="#">Chính sách đổi trả</a>
        <a href="#">Thanh toán & giao nhận</a>
        <a href="#">Chính sách bảo mật</a>
      </div>

      <div class="footer-col">
        <h4>Liên hệ</h4>
        <p class="contact-item"><i class="fas fa-phone"></i> <a href="tel:18001162">1800 1162</a> (08:00 - 21:00)</p>
        <p class="contact-item"><i class="fas fa-envelope"></i> <a href="mailto:cskh@styleshop.vn">cskh@styleshop.vn</a></p>
        <p class="contact-item"><i class="fas fa-map-marker-alt"></i> Toàn quốc</p>
        <div class="payment-icons">
          <span class="pay-icon">VISA</span>
          <span class="pay-icon">MC</span>
          <span class="pay-icon">COD</span>
          <span class="pay-icon">MOMO</span>
        </div>
      </div>
    </div>

    <div class="footer-bottom">
      <div class="container footer-bottom-inner">
        <p>© 2026 StyleShop. All rights reserved.</p>
        <p>Được xây dựng với Vue 3 + FastAPI</p>
      </div>
    </div>
  </footer>
</template>

<style scoped>
.footer { background: #111; color: #aaa; margin-top: 0; }
.footer-top { display: grid; grid-template-columns: 2fr 1fr 1fr 1.5fr; gap: 48px; padding: 56px 20px; }
.footer-brand h3 { font-size: 20px; font-weight: 800; color: #fff; letter-spacing: 2px; margin-bottom: 12px; }
.footer-brand p { font-size: 13px; line-height: 1.7; margin-bottom: 20px; }
.socials { display: flex; gap: 12px; }
.socials a { width: 36px; height: 36px; border-radius: 50%; background: #222; color: #aaa; display: flex; align-items: center; justify-content: center; transition: all 0.2s; }
.socials a:hover { background: #fff; color: #111; }
.footer-col { display: flex; flex-direction: column; gap: 10px; }
.footer-col h4 { font-size: 13px; font-weight: 700; color: #fff; text-transform: uppercase; letter-spacing: 1px; margin-bottom: 4px; }
.footer-col a, .contact-item { font-size: 13px; color: #888; transition: color 0.2s; }
.footer-col a:hover { color: #fff; }
.contact-item { display: flex; align-items: center; gap: 8px; }
.contact-item i { color: #3b82f6; width: 14px; flex-shrink: 0; }
.contact-item a { color: #888; }
.contact-item a:hover { color: #fff; }
.payment-icons { display: flex; gap: 8px; flex-wrap: wrap; margin-top: 8px; }
.pay-icon { background: #222; color: #aaa; font-size: 10px; font-weight: 700; padding: 4px 8px; border-radius: 4px; border: 1px solid #333; }
.footer-bottom { border-top: 1px solid #222; }
.footer-bottom-inner { display: flex; justify-content: space-between; align-items: center; padding: 16px 20px; font-size: 12px; color: #555; }
@media (max-width: 900px) { .footer-top { grid-template-columns: 1fr 1fr; gap: 32px; } }
@media (max-width: 480px) { .footer-top { grid-template-columns: 1fr; } .footer-bottom-inner { flex-direction: column; gap: 8px; text-align: center; } }
</style>
