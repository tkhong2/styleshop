<template>
  <div class="support-page">
    <div class="container">
      <div class="breadcrumb">
        <RouterLink to="/">Trang chủ</RouterLink> / <span>Câu hỏi thường gặp</span>
      </div>
      <h1 class="page-title"><i class="fas fa-question-circle"></i> Câu hỏi thường gặp</h1>

      <!-- Search -->
      <div class="faq-search">
        <i class="fas fa-search"></i>
        <input v-model="search" type="text" placeholder="Tìm câu hỏi..." />
      </div>

      <!-- Categories -->
      <div class="faq-cats">
        <button v-for="cat in categories" :key="cat.id"
          :class="['cat-btn', { active: activeCat === cat.id }]"
          @click="activeCat = cat.id">
          <i :class="cat.icon"></i> {{ cat.label }}
        </button>
      </div>

      <!-- FAQ list -->
      <div class="faq-list">
        <div v-for="(item, i) in filtered" :key="i" class="faq-item">
          <button class="faq-q" @click="toggle(i)">
            <span>{{ item.q }}</span>
            <i :class="['fas', openIndex === i ? 'fa-chevron-up' : 'fa-chevron-down']"></i>
          </button>
          <Transition name="slide-down">
            <div v-if="openIndex === i" class="faq-a">
              <p>{{ item.a }}</p>
            </div>
          </Transition>
        </div>
        <div v-if="filtered.length === 0" class="empty">
          <i class="fas fa-search"></i>
          <p>Không tìm thấy câu hỏi phù hợp</p>
        </div>
      </div>

      <div class="still-help">
        <h3>Vẫn cần hỗ trợ?</h3>
        <p>Đội ngũ chăm sóc khách hàng của chúng tôi luôn sẵn sàng giúp đỡ bạn.</p>
        <div class="help-btns">
          <a href="tel:18001162" class="help-btn phone"><i class="fas fa-phone"></i> 091 708 0222</a>
          <a href="mailto:cskh@styleshop.vn" class="help-btn email"><i class="fas fa-envelope"></i> Email</a>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'

const search = ref('')
const activeCat = ref('all')
const openIndex = ref(null)

const categories = [
  { id: 'all', label: 'Tất cả', icon: 'fas fa-list' },
  { id: 'order', label: 'Đặt hàng', icon: 'fas fa-box' },
  { id: 'payment', label: 'Thanh toán', icon: 'fas fa-credit-card' },
  { id: 'shipping', label: 'Vận chuyển', icon: 'fas fa-truck' },
  { id: 'return', label: 'Đổi trả', icon: 'fas fa-undo' },
  { id: 'product', label: 'Sản phẩm', icon: 'fas fa-tshirt' },
]

const faqs = [
  { cat: 'order', q: 'Làm thế nào để đặt hàng?', a: 'Chọn sản phẩm → Thêm vào giỏ hàng → Tiến hành thanh toán → Chọn phương thức thanh toán → Xác nhận đơn hàng. Bạn sẽ nhận được thông báo xác nhận qua email.' },
  { cat: 'order', q: 'Tôi có thể hủy đơn hàng không?', a: 'Bạn có thể hủy đơn hàng trong vòng 2 giờ sau khi đặt hàng bằng cách liên hệ hotline 091 708 0222. Sau thời gian này, đơn hàng đã được xử lý và không thể hủy.' },
  { cat: 'order', q: 'Làm sao để theo dõi đơn hàng?', a: 'Đăng nhập vào tài khoản → Trang cá nhân → Đơn hàng của tôi. Bạn sẽ thấy trạng thái đơn hàng được cập nhật theo thời gian thực.' },
  { cat: 'payment', q: 'StyleShop hỗ trợ những phương thức thanh toán nào?', a: 'Chúng tôi hỗ trợ: Chuyển khoản ngân hàng (BIDV qua VietQR), Ví MoMo, và Thanh toán khi nhận hàng (COD).' },
  { cat: 'payment', q: 'Thanh toán chuyển khoản có an toàn không?', a: 'Hoàn toàn an toàn. Chúng tôi sử dụng hệ thống VietQR và SePay để xác nhận giao dịch tự động. Tiền chỉ được ghi nhận khi chuyển khoản thành công.' },
  { cat: 'payment', q: 'Mã giảm giá áp dụng như thế nào?', a: 'Nhập mã giảm giá vào ô "Mã giảm giá" trong trang giỏ hàng trước khi thanh toán. Mỗi đơn hàng chỉ áp dụng được 1 mã.' },
  { cat: 'shipping', q: 'Thời gian giao hàng là bao lâu?', a: 'Nội thành TP.HCM và Hà Nội: 1–2 ngày. Các tỉnh thành khác: 3–5 ngày làm việc. Thời gian có thể thay đổi tùy theo địa chỉ và tình trạng vận chuyển.' },
  { cat: 'shipping', q: 'Phí vận chuyển là bao nhiêu?', a: 'Miễn phí vận chuyển cho đơn hàng từ 500.000đ. Đơn hàng dưới 500.000đ phí vận chuyển là 30.000đ.' },
  { cat: 'shipping', q: 'Tôi có thể thay đổi địa chỉ giao hàng không?', a: 'Bạn có thể thay đổi địa chỉ giao hàng trước khi đơn hàng được xử lý. Liên hệ hotline 091 708 0222 ngay sau khi đặt hàng.' },
  { cat: 'return', q: 'Chính sách đổi trả như thế nào?', a: 'Chúng tôi chấp nhận đổi trả trong vòng 30 ngày kể từ ngày nhận hàng. Sản phẩm phải còn nguyên tem, nhãn, chưa qua sử dụng và có hóa đơn mua hàng.' },
  { cat: 'return', q: 'Làm thế nào để đổi size?', a: 'Liên hệ hotline 091 708 0222 hoặc email cskh@styleshop.vn với thông tin đơn hàng và size muốn đổi. Chúng tôi sẽ hướng dẫn quy trình đổi hàng.' },
  { cat: 'product', q: 'Sản phẩm có đúng như hình ảnh không?', a: 'Chúng tôi cố gắng chụp ảnh trung thực nhất. Màu sắc có thể hơi khác do điều kiện ánh sáng và màn hình thiết bị. Nếu không hài lòng, bạn có thể đổi trả trong 30 ngày.' },
  { cat: 'product', q: 'Làm sao biết sản phẩm còn hàng không?', a: 'Sản phẩm hiển thị trên website đều còn hàng. Nếu hết size bạn cần, liên hệ hotline để được thông báo khi có hàng trở lại.' },
]

function toggle(i) { openIndex.value = openIndex.value === i ? null : i }

const filtered = computed(() => {
  let list = faqs
  if (activeCat.value !== 'all') list = list.filter(f => f.cat === activeCat.value)
  if (search.value) list = list.filter(f => f.q.toLowerCase().includes(search.value.toLowerCase()) || f.a.toLowerCase().includes(search.value.toLowerCase()))
  return list
})
</script>

<style scoped>
.support-page { padding: 40px 0 80px; background: #fafafa; min-height: 100vh; }
.breadcrumb { font-size: 13px; color: #888; margin-bottom: 24px; }
.breadcrumb a { color: #888; } .breadcrumb a:hover { color: #1a1a1a; }
.page-title { font-size: 28px; font-weight: 800; margin-bottom: 28px; display: flex; align-items: center; gap: 12px; }
.page-title i { color: #3b82f6; }
.faq-search { display: flex; align-items: center; gap: 12px; background: #fff; border: 1.5px solid #e2e8f0; border-radius: 10px; padding: 12px 18px; margin-bottom: 20px; max-width: 500px; }
.faq-search i { color: #94a3b8; }
.faq-search input { flex: 1; border: none; outline: none; font-size: 14px; font-family: inherit; }
.faq-cats { display: flex; gap: 8px; flex-wrap: wrap; margin-bottom: 28px; }
.cat-btn { display: flex; align-items: center; gap: 6px; padding: 8px 16px; border-radius: 20px; border: 1.5px solid #e2e8f0; background: #fff; font-size: 13px; font-weight: 500; color: #555; transition: all 0.15s; }
.cat-btn:hover { border-color: #1a1a1a; color: #1a1a1a; }
.cat-btn.active { background: #1a1a1a; color: #fff; border-color: #1a1a1a; }
.faq-list { display: flex; flex-direction: column; gap: 8px; margin-bottom: 40px; }
.faq-item { background: #fff; border-radius: 10px; overflow: hidden; box-shadow: 0 1px 4px rgba(0,0,0,0.05); }
.faq-q { width: 100%; display: flex; justify-content: space-between; align-items: center; padding: 18px 20px; font-size: 15px; font-weight: 600; text-align: left; background: none; gap: 12px; }
.faq-q:hover { background: #f8fafc; }
.faq-q i { color: #94a3b8; flex-shrink: 0; }
.faq-a { padding: 0 20px 18px; font-size: 14px; color: #555; line-height: 1.7; border-top: 1px solid #f1f5f9; padding-top: 14px; }
.empty { text-align: center; padding: 60px; color: #aaa; display: flex; flex-direction: column; align-items: center; gap: 12px; font-size: 15px; }
.empty i { font-size: 36px; }
.still-help { background: #1a1a1a; color: #fff; border-radius: 16px; padding: 40px; text-align: center; }
.still-help h3 { font-size: 22px; font-weight: 700; margin-bottom: 10px; }
.still-help p { color: #aaa; margin-bottom: 24px; }
.help-btns { display: flex; gap: 12px; justify-content: center; }
.help-btn { display: flex; align-items: center; gap: 8px; padding: 12px 24px; border-radius: 8px; font-size: 14px; font-weight: 600; }
.help-btn.phone { background: #3b82f6; color: #fff; }
.help-btn.email { background: rgba(255,255,255,0.1); color: #fff; border: 1px solid rgba(255,255,255,0.2); }
.slide-down-enter-active, .slide-down-leave-active { transition: all 0.2s; }
.slide-down-enter-from, .slide-down-leave-to { opacity: 0; transform: translateY(-8px); }
</style>
