<template>
  <div class="container cart-page">
    <h1>Giỏ hàng</h1>

    <div v-if="cart.items.length === 0" class="empty">
      <svg width="64" height="64" viewBox="0 0 24 24" fill="none" stroke="#ccc" stroke-width="1.5">
        <path d="M6 2L3 6v14a2 2 0 002 2h14a2 2 0 002-2V6l-3-4z"/>
        <line x1="3" y1="6" x2="21" y2="6"/>
        <path d="M16 10a4 4 0 01-8 0"/>
      </svg>
      <p>Giỏ hàng của bạn đang trống</p>
      <RouterLink to="/products" class="btn btn-dark">Tiếp tục mua sắm</RouterLink>
    </div>

    <div v-else class="layout">
      <!-- Items -->
      <div class="items">
        <div v-for="item in cart.items" :key="`${item.id}-${item.size}-${item.color}`" class="item">
          <img :src="item.image" :alt="item.name" />
          <div class="details">
            <RouterLink :to="`/products/${item.id}`" class="name">{{ item.name }}</RouterLink>
            <p class="meta">{{ item.size }} · {{ item.color }}</p>
            <p class="price">{{ formatPrice(item.price) }}</p>
          </div>
          <div class="qty">
            <button @click="cart.updateQuantity(item.id, item.size, item.color, item.quantity - 1)">−</button>
            <span>{{ item.quantity }}</span>
            <button @click="cart.updateQuantity(item.id, item.size, item.color, item.quantity + 1)">+</button>
          </div>
          <p class="subtotal">{{ formatPrice(item.price * item.quantity) }}</p>
          <button class="remove" @click="cart.removeItem(item.id, item.size, item.color)" aria-label="Xóa">
            <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <polyline points="3 6 5 6 21 6"/>
              <path d="M19 6l-1 14a2 2 0 01-2 2H8a2 2 0 01-2-2L5 6"/>
              <path d="M10 11v6M14 11v6M9 6V4a1 1 0 011-1h4a1 1 0 011 1v2"/>
            </svg>
          </button>
        </div>
      </div>

      <!-- Summary -->
      <div class="summary">
        <h2>Tóm tắt đơn hàng</h2>
        <div class="row"><span>Tạm tính ({{ cart.totalItems }} sp)</span><span>{{ formatPrice(cart.totalPrice) }}</span></div>
        <div class="row"><span>Phí vận chuyển</span><span>{{ cart.totalPrice >= 500000 ? 'Miễn phí' : formatPrice(1000) }}</span></div>
        <div class="divider"></div>
        <div class="row total"><span>Tổng cộng</span><span>{{ formatPrice(finalTotal) }}</span></div>

        <div class="coupon">
          <input v-model="coupon" type="text" placeholder="Mã giảm giá" />
          <button class="btn btn-outline coupon-btn" @click="applyCoupon">Áp dụng</button>
        </div>
        <p v-if="couponMsg" :class="['coupon-msg', couponOk ? 'ok' : 'err']">{{ couponMsg }}</p>

        <button class="btn btn-dark checkout-btn" @click="showPayment = true">
          Tiến hành thanh toán
        </button>
        <RouterLink to="/products" class="continue">← Tiếp tục mua sắm</RouterLink>
      </div>
    </div>

    <!-- Payment Modal -->
    <Transition name="fade">
      <div v-if="showPayment" class="modal-overlay" @click.self="showPayment = false">
        <div class="modal">
          <div class="modal-header">
            <h2>Chọn phương thức thanh toán</h2>
            <button @click="showPayment = false" class="close-btn">
              <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <line x1="18" y1="6" x2="6" y2="18"/><line x1="6" y1="6" x2="18" y2="18"/>
              </svg>
            </button>
          </div>

          <!-- Method selector -->
          <div v-if="!payMethod" class="pay-methods">
            <button class="pay-method-btn" @click="selectMethod('qr')">
              <div class="pay-icon bank-icon"><i class="fas fa-university"></i></div>
              <div>
                <p class="pay-name">Chuyển khoản ngân hàng</p>
                <p class="pay-desc">BIDV · VietQR · Napas 247 · Tất cả ngân hàng</p>
              </div>
              <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="9 18 15 12 9 6"/></svg>
            </button>
            <button class="pay-method-btn" @click="selectCOD">
              <div class="pay-icon cod-icon"><i class="fas fa-hand-holding-usd"></i></div>
              <div>
                <p class="pay-name">Thanh toán khi nhận hàng (COD)</p>
                <p class="pay-desc">Trả tiền mặt khi nhận hàng</p>
              </div>
              <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="9 18 15 12 9 6"/></svg>
            </button>
          </div>

          <!-- QR: Bước 1 - Nhập địa chỉ -->
          <div v-else-if="payMethod === 'qr' && !qrReady" class="pay-cod">
            <button class="back-btn" @click="payMethod = null">← Quay lại</button>
            <div class="shipping-form" style="width:100%">
              <h4><i class="fas fa-map-marker-alt"></i> Thông tin giao hàng</h4>

              <!-- Địa chỉ đã lưu -->
              <div v-if="savedAddresses.length > 0" class="saved-addresses">
                <div
                  v-for="(addr, i) in savedAddresses" :key="i"
                  :class="['saved-addr-item', { selected: selectedAddrIdx === i }]"
                  @click="selectSavedAddress(i)"
                >
                  <div class="saved-addr-radio">
                    <span class="radio-dot" :class="{ active: selectedAddrIdx === i }"></span>
                  </div>
                  <div>
                    <p class="saved-addr-name">{{ addr.name }} · {{ addr.phone }}
                      <span v-if="addr.isDefault" class="default-badge">Mặc định</span>
                    </p>
                    <p class="saved-addr-detail">{{ addr.address }}, {{ addr.district }}, {{ addr.city }}</p>
                  </div>
                </div>
                <button class="add-new-addr-btn" @click="selectedAddrIdx = -1">
                  <i class="fas fa-plus"></i> Dùng địa chỉ khác
                </button>
              </div>

              <!-- Form nhập mới khi chưa có hoặc chọn "dùng địa chỉ khác" -->
              <div v-if="savedAddresses.length === 0 || selectedAddrIdx === -1">
                <div class="form-row">
                  <div class="field">
                    <label>Họ tên *</label>
                    <input v-model="shipping.name" type="text" placeholder="Nguyễn Văn A" />
                  </div>
                  <div class="field">
                    <label>Số điện thoại *</label>
                    <input v-model="shipping.phone" type="tel" placeholder="0912 345 678" />
                  </div>
                </div>
                <div class="field">
                  <label>Địa chỉ *</label>
                  <input v-model="shipping.address" type="text" placeholder="Số nhà, tên đường" />
                </div>
                <div class="form-row">
                  <div class="field">
                    <label>Quận/Huyện</label>
                    <input v-model="shipping.district" type="text" placeholder="Quận 1" />
                  </div>
                  <div class="field">
                    <label>Tỉnh/Thành phố</label>
                    <input v-model="shipping.city" type="text" placeholder="TP. Hồ Chí Minh" />
                  </div>
                </div>
                <div class="field">
                  <label>Ghi chú</label>
                  <textarea v-model="shipping.note" placeholder="Ghi chú cho shipper..." rows="2"></textarea>
                </div>
              </div>
            </div>
            <button class="btn btn-dark confirm-btn"
              :disabled="selectedAddrIdx === -1 ? (!shipping.name || !shipping.phone || !shipping.address) : false"
              @click="proceedToQR">
              Tiếp tục thanh toán →
            </button>
          </div>

          <!-- QR: Bước 2 - Hiện QR -->
          <div v-else-if="payMethod === 'qr' && qrReady" class="pay-qr">
            <button class="back-btn" @click="cancelWaiting">← Quay lại</button>
            <p class="pay-amount-label">Số tiền cần chuyển</p>
            <p class="pay-amount">{{ formatPrice(finalTotal) }}</p>
            <div class="qr-wrap">
              <img :src="qrUrl" alt="QR Code thanh toán" class="qr-img" />
            </div>
            <div class="bank-info">
              <div class="bank-row"><span>Ngân hàng</span><strong>BIDV</strong></div>
              <div class="bank-row"><span>Số tài khoản VA</span><strong class="copy-text" @click="copy('962471OMBS')">962471OMBS 📋</strong></div>
              <div class="bank-row"><span>Chủ tài khoản</span><strong>TRAN KHAC HONG</strong></div>
              <div class="bank-row"><span>Nội dung CK</span>
                <strong class="copy-text" @click="copy(currentTransferNote)">{{ currentTransferNote }} 📋</strong>
              </div>
            </div>
            <p class="qr-note">Quét mã QR bằng app ngân hàng bất kỳ hoặc MoMo, ZaloPay</p>
            <div class="waiting-box">
              <div class="waiting-spinner"></div>
              <p>Đang chờ xác nhận thanh toán...</p>
              <p class="waiting-sub">Hệ thống tự động xác nhận khi nhận được tiền</p>
              <div class="waiting-timer">⏱ {{ waitingSeconds }}s</div>
            </div>
          </div>

          <!-- MoMo -->
          <div v-else-if="payMethod === 'momo'" class="pay-qr">
            <button class="back-btn" @click="cancelWaiting">← Quay lại</button>
            <p class="pay-amount-label">Số tiền cần thanh toán</p>
            <p class="pay-amount momo-color">{{ formatPrice(finalTotal) }}</p>
            <div class="qr-wrap momo-bg">
              <img :src="momoQrUrl" alt="QR MoMo" class="qr-img" />
            </div>
            <div class="bank-info">
              <div class="bank-row"><span>Số điện thoại MoMo</span><strong class="copy-text" @click="copy('0917080222')">0917080222 📋</strong></div>
              <div class="bank-row"><span>Tên tài khoản</span><strong>TRAN KHAC HONG</strong></div>
              <div class="bank-row"><span>Nội dung</span><strong>{{ currentTransferNote }}</strong></div>
            </div>
            <p class="qr-note">Mở app MoMo → Quét mã QR hoặc chuyển tiền theo số điện thoại</p>
            <div class="waiting-box momo-wait">
              <div class="waiting-spinner momo-spin"></div>
              <p>Đang chờ xác nhận từ MoMo...</p>
              <p class="waiting-sub">Hệ thống tự động xác nhận khi nhận được tiền</p>
              <div class="waiting-timer">⏱ {{ waitingSeconds }}s</div>
            </div>
          </div>

          <!-- COD -->
          <div v-else-if="payMethod === 'cod'" class="pay-cod">
            <button class="back-btn" @click="payMethod = null">← Quay lại</button>
            <div class="cod-icon-big"><i class="fas fa-hand-holding-usd"></i></div>
            <h3>Thanh toán khi nhận hàng</h3>
            <p>Bạn sẽ thanh toán <strong>{{ formatPrice(finalTotal) }}</strong> khi nhận được hàng.</p>

            <div class="shipping-form">
              <h4><i class="fas fa-map-marker-alt"></i> Thông tin giao hàng</h4>

              <!-- Địa chỉ đã lưu -->
              <div v-if="savedAddresses.length > 0" class="saved-addresses">
                <div
                  v-for="(addr, i) in savedAddresses" :key="i"
                  :class="['saved-addr-item', { selected: selectedAddrIdx === i }]"
                  @click="selectSavedAddress(i)"
                >
                  <div class="saved-addr-radio">
                    <span class="radio-dot" :class="{ active: selectedAddrIdx === i }"></span>
                  </div>
                  <div>
                    <p class="saved-addr-name">{{ addr.name }} · {{ addr.phone }}
                      <span v-if="addr.isDefault" class="default-badge">Mặc định</span>
                    </p>
                    <p class="saved-addr-detail">{{ addr.address }}, {{ addr.district }}, {{ addr.city }}</p>
                  </div>
                </div>
                <button class="add-new-addr-btn" @click="selectedAddrIdx = -1">
                  <i class="fas fa-plus"></i> Dùng địa chỉ khác
                </button>
              </div>

              <!-- Form nhập mới -->
              <div v-if="savedAddresses.length === 0 || selectedAddrIdx === -1">
                <div class="form-row">
                  <div class="field">
                    <label>Họ tên *</label>
                    <input v-model="shipping.name" type="text" placeholder="Nguyễn Văn A" />
                  </div>
                  <div class="field">
                    <label>Số điện thoại *</label>
                    <input v-model="shipping.phone" type="tel" placeholder="0912 345 678" />
                  </div>
                </div>
                <div class="field">
                  <label>Địa chỉ *</label>
                  <input v-model="shipping.address" type="text" placeholder="Số nhà, tên đường" />
                </div>
                <div class="form-row">
                  <div class="field">
                    <label>Quận/Huyện</label>
                    <input v-model="shipping.district" type="text" placeholder="Quận 1" />
                  </div>
                  <div class="field">
                    <label>Tỉnh/Thành phố</label>
                    <input v-model="shipping.city" type="text" placeholder="TP. Hồ Chí Minh" />
                  </div>
                </div>
                <div class="field">
                  <label>Ghi chú</label>
                  <textarea v-model="shipping.note" placeholder="Ghi chú cho shipper..." rows="2"></textarea>
                </div>
              </div>
            </div>

            <p class="cod-note"><i class="fas fa-info-circle"></i> Shipper sẽ liên hệ trước khi giao. Vui lòng chuẩn bị đúng số tiền.</p>
            <button class="btn btn-dark confirm-btn"
              :disabled="selectedAddrIdx === -1 ? (!shipping.name || !shipping.phone || !shipping.address) : false"
              @click="confirmPayment('cod')">
              Xác nhận đặt hàng COD
            </button>
          </div>
        </div>
      </div>
    </Transition>

    <!-- Success Modal -->
    <Transition name="fade">
      <div v-if="showSuccess" class="modal-overlay">
        <div class="modal success-modal">
          <div class="success-icon">✓</div>
          <h2>Đặt hàng thành công!</h2>
          <p>Mã đơn hàng: <strong>#{{ orderId }}</strong></p>
          <p class="success-sub">Cảm ơn bạn đã mua sắm tại StyleShop. Chúng tôi sẽ liên hệ xác nhận sớm nhất.</p>
          <RouterLink to="/" class="btn btn-dark" @click="showSuccess = false">Về trang chủ</RouterLink>
        </div>
      </div>
    </Transition>
  </div>
</template>

<script setup>
import { ref, computed, onUnmounted } from 'vue'
import { useCartStore } from '@/stores/cart.js'
import { orderService } from '@/services/orderService.js'
import { useToastStore } from '@/stores/toast.js'
import { useAuthStore } from '@/stores/auth.js'
import { formatPrice } from '@/utils/format.js'

const cart = useCartStore()
const toast = useToastStore()
const auth = useAuthStore()

const coupon = ref('')
const couponMsg = ref('')
const couponOk = ref(false)
const discount = ref(0)
const showPayment = ref(false)
const showSuccess = ref(false)
const payMethod = ref(null)
const orderId = ref('')
const shipping = ref({
  name: auth.user?.name || '',
  phone: '',
  address: '',
  district: '',
  city: '',
  note: '',
})

// Địa chỉ đã lưu từ profile
const savedAddresses = ref(JSON.parse(localStorage.getItem('addresses') || '[]'))
const selectedAddrIdx = ref(-2) // -2: chưa init, -1: nhập mới, >=0: chọn từ danh sách

function selectSavedAddress(i) {
  selectedAddrIdx.value = i
  const addr = savedAddresses.value[i]
  shipping.value = { name: addr.name, phone: addr.phone, address: addr.address, district: addr.district || '', city: addr.city || '', note: '' }
}

// Polling state
const waitingPayment = ref(false)
const waitingSeconds = ref(0)
const currentOrderId = ref(null)
const currentTransferNote = ref('')
const qrReady = ref(false)
let pollTimer = null
let secondTimer = null
const MAX_WAIT = 300 // 5 phút

const COUPONS = { 'STYLE10': 10, 'SALE20': 20, 'NEWUSER': 15 }

const finalTotal = computed(() => {
  const shipping = cart.totalPrice >= 500000 ? 0 : 1000
  const disc = Math.round(cart.totalPrice * discount.value / 100)
  return cart.totalPrice + shipping - disc
})

const transferNote = computed(() => `STYLE${Date.now().toString().slice(-6)}`)

const qrUrl = computed(() =>
  `https://img.vietqr.io/image/BIDV-962471OMBS-compact2.png?amount=${finalTotal.value}&addInfo=${encodeURIComponent(currentTransferNote.value || transferNote.value)}&accountName=TRAN%20KHAC%20HONG`
)
const momoQrUrl = computed(() =>
  `https://img.vietqr.io/image/BIDV-962471OMBS-compact2.png?amount=${finalTotal.value}&addInfo=${encodeURIComponent(currentTransferNote.value || transferNote.value)}&accountName=TRAN%20KHAC%20HONG`
)

function applyCoupon() {
  const code = coupon.value.trim().toUpperCase()
  if (COUPONS[code]) {
    discount.value = COUPONS[code]
    couponOk.value = true
    couponMsg.value = `Áp dụng thành công! Giảm ${COUPONS[code]}%`
  } else {
    discount.value = 0
    couponOk.value = false
    couponMsg.value = 'Mã giảm giá không hợp lệ'
  }
}

function copy(text) {
  navigator.clipboard.writeText(text).then(() => toast.success('Đã sao chép!'))
}

// ── COD: xác nhận ngay ───────────────────────────────────────────────────────
function selectCOD() {
  payMethod.value = 'cod'
  savedAddresses.value = JSON.parse(localStorage.getItem('addresses') || '[]')
  const defaultIdx = savedAddresses.value.findIndex(a => a.isDefault)
  if (defaultIdx >= 0) selectSavedAddress(defaultIdx)
  else if (savedAddresses.value.length > 0) selectSavedAddress(0)
  else selectedAddrIdx.value = -1
}
async function confirmPayment(method) {
  try {
    const order = await orderService.create({
      items: cart.items.map(i => ({ product_id: i.id, name: i.name, price: i.price, size: i.size, color: i.color, quantity: i.quantity })),
      total: finalTotal.value,
      coupon: coupon.value || null,
      payment_method: method,
      user_id: auth.user?.email || null,
      shipping: { ...shipping.value },
    })
    orderId.value = order.id
  } catch {
    orderId.value = Math.floor(Math.random() * 90000 + 10000)
  }
  cart.clearCart()
  showPayment.value = false
  payMethod.value = null
  showSuccess.value = true
}

// Chọn phương thức → chỉ set payMethod, chưa tạo đơn
async function selectMethod(method) {
  payMethod.value = method
  qrReady.value = false
  currentOrderId.value = null
  currentTransferNote.value = ''
  // Tự động chọn địa chỉ mặc định nếu có
  if (method === 'qr') {
    savedAddresses.value = JSON.parse(localStorage.getItem('addresses') || '[]')
    const defaultIdx = savedAddresses.value.findIndex(a => a.isDefault)
    if (defaultIdx >= 0) selectSavedAddress(defaultIdx)
    else if (savedAddresses.value.length > 0) selectSavedAddress(0)
    else selectedAddrIdx.value = -1
  }
}

// Sau khi nhập địa chỉ → tạo đơn + hiện QR
async function proceedToQR() {
  try {
    const order = await orderService.create({
      items: cart.items.map(i => ({ product_id: i.id, name: i.name, price: i.price, size: i.size, color: i.color, quantity: i.quantity })),
      total: finalTotal.value,
      coupon: coupon.value || null,
      payment_method: 'qr',
      user_id: auth.user?.email || null,
      shipping: { ...shipping.value },
    })
    currentOrderId.value = order.id
    currentTransferNote.value = order.transfer_note || transferNote.value
  } catch {
    currentTransferNote.value = transferNote.value
  }
  qrReady.value = true
  startPolling()
}

// ── Bắt đầu polling (gọi tự động sau khi tạo đơn) ───────────────────────────
function startPolling() {
  waitingPayment.value = true
  waitingSeconds.value = 0

  secondTimer = setInterval(() => {
    waitingSeconds.value++
    if (waitingSeconds.value >= MAX_WAIT) cancelWaiting()
  }, 1000)

  pollTimer = setInterval(async () => {
    try {
      if (currentOrderId.value) {
        const res = await orderService.getPaymentStatus(currentOrderId.value)
        if (res.payment_status === 'paid') {
          stopPolling()
          orderId.value = currentOrderId.value
          cart.clearCart()
          showPayment.value = false
          payMethod.value = null
          showSuccess.value = true
          toast.success('Thanh toán thành công!')
          return
        }
      }
      // Fallback: check tất cả đơn của user
      const allOrders = await orderService.getMyOrders(auth.user?.email)
      const paidOrder = allOrders.find(o =>
        o.id === currentOrderId.value && o.payment_status === 'paid'
      )
      if (paidOrder) {
        stopPolling()
        orderId.value = paidOrder.id
        cart.clearCart()
        showPayment.value = false
        payMethod.value = null
        showSuccess.value = true
        toast.success('Thanh toán thành công!')
      }
    } catch (e) {
      if (e.message?.includes('404')) {
        // Server restart — đơn mất, vẫn xác nhận
        stopPolling()
        orderId.value = currentOrderId.value || Math.floor(Math.random() * 90000 + 10000)
        cart.clearCart()
        showPayment.value = false
        payMethod.value = null
        showSuccess.value = true
      }
    }
  }, 5000)
}

// Legacy alias (giữ để không lỗi nếu còn ref)
async function startWaiting(method) { startPolling() }

function cancelWaiting() {
  stopPolling()
  payMethod.value = null
  qrReady.value = false
  currentOrderId.value = null
  currentTransferNote.value = ''
}

function stopPolling() {
  waitingPayment.value = false
  clearInterval(pollTimer)
  clearInterval(secondTimer)
  pollTimer = null
  secondTimer = null
}

onUnmounted(() => stopPolling())
</script>

<style scoped>
.cart-page { padding: 40px 20px 80px; }
.cart-page h1 { font-size: 26px; font-weight: 700; margin-bottom: 32px; }

.empty { display: flex; flex-direction: column; align-items: center; gap: 16px; padding: 80px 20px; color: #888; font-size: 15px; }

.layout { display: grid; grid-template-columns: 1fr 360px; gap: 32px; align-items: start; }

.items { display: flex; flex-direction: column; gap: 16px; }
.item { display: grid; grid-template-columns: 90px 1fr auto auto auto; gap: 16px; align-items: center; padding: 16px; background: #fff; border-radius: 10px; border: 1px solid var(--gray2); }
.item img { width: 90px; height: 90px; object-fit: cover; border-radius: 6px; }
.name { font-size: 14px; font-weight: 500; margin-bottom: 4px; display: block; }
.name:hover { text-decoration: underline; }
.meta { font-size: 12px; color: var(--gray3); margin-bottom: 4px; }
.price { font-size: 13px; font-weight: 600; }
.qty { display: flex; align-items: center; gap: 10px; border: 1.5px solid var(--gray2); border-radius: 6px; padding: 5px 10px; }
.qty button { background: none; font-size: 16px; color: #555; width: 22px; height: 22px; display: flex; align-items: center; justify-content: center; }
.qty span { font-size: 14px; font-weight: 500; min-width: 18px; text-align: center; }
.subtotal { font-size: 14px; font-weight: 700; min-width: 90px; text-align: right; }
.remove { background: none; color: #bbb; padding: 4px; } .remove:hover { color: var(--red); }

/* Summary */
.summary { background: #fff; border: 1px solid var(--gray2); border-radius: 10px; padding: 24px; display: flex; flex-direction: column; gap: 14px; position: sticky; top: 80px; }
.summary h2 { font-size: 16px; font-weight: 700; }
.row { display: flex; justify-content: space-between; font-size: 14px; color: #555; }
.divider { border-top: 1px solid var(--gray2); }
.row.total { font-size: 16px; font-weight: 700; color: var(--black); }
.coupon { display: flex; gap: 8px; }
.coupon input { flex: 1; padding: 9px 12px; border: 1.5px solid var(--gray2); border-radius: 6px; font-size: 13px; font-family: var(--font); }
.coupon input:focus { outline: none; border-color: var(--black); }
.coupon-btn { padding: 9px 14px; font-size: 13px; white-space: nowrap; }
.coupon-msg { font-size: 12px; margin-top: -6px; }
.coupon-msg.ok { color: #16a34a; }
.coupon-msg.err { color: var(--red); }
.checkout-btn { width: 100%; padding: 14px; font-size: 14px; }
.continue { text-align: center; font-size: 13px; color: var(--gray3); } .continue:hover { color: var(--black); }

/* Modal */
.modal-overlay { position: fixed; inset: 0; background: rgba(0,0,0,0.5); z-index: 400; display: flex; align-items: center; justify-content: center; padding: 20px; }
.modal { background: #fff; border-radius: 16px; width: 100%; max-width: 480px; max-height: 90vh; overflow-y: auto; }
@media (max-width: 480px) {
  .modal { border-radius: 16px 16px 0 0; max-height: 95vh; margin-top: auto; }
  .modal-overlay { align-items: flex-end; padding: 0; }
}.modal-header { display: flex; justify-content: space-between; align-items: center; padding: 20px 24px; border-bottom: 1px solid var(--gray2); }
.modal-header h2 { font-size: 17px; font-weight: 700; }
.close-btn { background: none; color: #888; padding: 4px; }

/* Payment methods */
.pay-methods { padding: 16px; display: flex; flex-direction: column; gap: 12px; }
.pay-method-btn { display: flex; align-items: center; gap: 14px; padding: 16px; border: 1.5px solid var(--gray2); border-radius: 10px; text-align: left; transition: border-color 0.2s; background: #fff; width: 100%; }
.pay-method-btn:hover { border-color: var(--black); }
.pay-icon { font-size: 28px; flex-shrink: 0; }
.pay-icon { width: 44px; height: 44px; border-radius: 10px; display: flex; align-items: center; justify-content: center; font-size: 20px; flex-shrink: 0; }
.pay-icon.bank-icon { background: #eff6ff; color: #3b82f6; }
.pay-icon.momo-icon { background: #fce7f3; color: #a50064; }
.pay-icon.cod-icon { background: #dcfce7; color: #166534; }
.pay-name { font-size: 14px; font-weight: 600; margin-bottom: 2px; }
.pay-desc { font-size: 12px; color: var(--gray3); }
.pay-method-btn svg { margin-left: auto; flex-shrink: 0; color: var(--gray3); }

/* QR section */
.pay-qr { padding: 20px 24px; display: flex; flex-direction: column; align-items: center; gap: 14px; }
.back-btn { align-self: flex-start; font-size: 13px; color: var(--gray3); background: none; }
.back-btn:hover { color: var(--black); }
.pay-amount-label { font-size: 13px; color: var(--gray3); }
.pay-amount { font-size: 28px; font-weight: 800; color: var(--black); }
.pay-amount.momo-color { color: #a50064; }
.qr-wrap { background: #f0f7ff; border-radius: 16px; padding: 16px; }
.qr-wrap.momo-bg { background: #fdf0f8; }
.qr-img { width: 220px; height: 220px; object-fit: contain; border-radius: 8px; }
.bank-info { width: 100%; background: var(--gray); border-radius: 10px; padding: 14px 16px; display: flex; flex-direction: column; gap: 8px; }
.bank-row { display: flex; justify-content: space-between; font-size: 13px; }
.bank-row span { color: var(--gray3); }
.copy-text { cursor: pointer; color: #2563eb; }
.copy-text:hover { text-decoration: underline; }
.qr-note { font-size: 12px; color: var(--gray3); text-align: center; }
.confirm-btn { width: 100%; padding: 14px; font-size: 14px; margin-top: 8px; }

/* COD */
.pay-cod { padding: 20px 24px; display: flex; flex-direction: column; align-items: center; gap: 12px; text-align: center; }
.cod-icon { font-size: 56px; }
.cod-icon-big { width: 56px; height: 56px; border-radius: 50%; background: #dcfce7; color: #166534; display: flex; align-items: center; justify-content: center; font-size: 24px; }
.pay-cod h3 { font-size: 17px; font-weight: 700; }
.pay-cod > p { font-size: 14px; color: #555; }
.cod-note { font-size: 12px; color: var(--gray3); background: var(--gray); padding: 10px 14px; border-radius: 8px; width: 100%; text-align: left; display: flex; align-items: center; gap: 6px; }
.shipping-form { width: 100%; background: #f8fafc; border-radius: 10px; padding: 16px; text-align: left; box-sizing: border-box; }
.shipping-form h4 { font-size: 13px; font-weight: 700; margin-bottom: 12px; display: flex; align-items: center; gap: 6px; color: #1e293b; }
.form-row { display: grid; grid-template-columns: 1fr 1fr; gap: 10px; }
.shipping-form .field { display: flex; flex-direction: column; gap: 4px; margin-bottom: 10px; min-width: 0; }
.shipping-form label { font-size: 12px; font-weight: 600; color: #475569; }
.shipping-form input, .shipping-form textarea { padding: 8px 12px; border: 1.5px solid #e2e8f0; border-radius: 6px; font-size: 13px; font-family: var(--font); outline: none; resize: none; width: 100%; box-sizing: border-box; }
.shipping-form input:focus, .shipping-form textarea:focus { border-color: var(--black); }
@media (max-width: 480px) { .form-row { grid-template-columns: 1fr; } }

/* Success */
.success-modal { padding: 48px 32px; display: flex; flex-direction: column; align-items: center; gap: 14px; text-align: center; }
.success-icon { width: 64px; height: 64px; background: #22c55e; color: #fff; border-radius: 50%; font-size: 28px; display: flex; align-items: center; justify-content: center; }
.success-modal h2 { font-size: 22px; font-weight: 700; }
.success-modal p { font-size: 14px; color: #555; }
.success-sub { font-size: 13px; color: var(--gray3); }

.fade-enter-active, .fade-leave-active { transition: opacity 0.2s; }
.fade-enter-from, .fade-leave-to { opacity: 0; }

/* Waiting / polling */
.waiting-box { width: 100%; background: #f0f9ff; border: 1.5px solid #bae6fd; border-radius: 10px; padding: 20px; display: flex; flex-direction: column; align-items: center; gap: 8px; text-align: center; }
.waiting-box.momo-wait { background: #fdf0f8; border-color: #f0abdc; }
.waiting-spinner { width: 36px; height: 36px; border: 3px solid #bae6fd; border-top-color: #0284c7; border-radius: 50%; animation: spin 0.8s linear infinite; }
.waiting-spinner.momo-spin { border-color: #f0abdc; border-top-color: #a50064; }
.waiting-box p { font-size: 14px; font-weight: 600; color: #0369a1; }
.waiting-box.momo-wait p { color: #a50064; }
.waiting-sub { font-size: 12px !important; font-weight: 400 !important; color: #64748b !important; }
.waiting-timer { font-size: 13px; color: #94a3b8; font-variant-numeric: tabular-nums; }
.saved-addresses { width: 100%; display: flex; flex-direction: column; gap: 8px; margin-bottom: 14px; }
.saved-addr-item { display: flex; align-items: flex-start; gap: 12px; padding: 12px 14px; border: 1.5px solid #e2e8f0; border-radius: 10px; cursor: pointer; transition: border-color 0.15s; }
.saved-addr-item.selected { border-color: #1a1a1a; background: #f8fafc; }
.saved-addr-radio { padding-top: 2px; }
.radio-dot { display: block; width: 16px; height: 16px; border-radius: 50%; border: 2px solid #cbd5e1; flex-shrink: 0; }
.radio-dot.active { border-color: #1a1a1a; background: #1a1a1a; box-shadow: inset 0 0 0 3px #fff; }
.saved-addr-name { font-size: 13px; font-weight: 600; margin-bottom: 2px; display: flex; align-items: center; gap: 6px; }
.saved-addr-detail { font-size: 12px; color: #666; }
.default-badge { background: #3b82f6; color: #fff; font-size: 10px; font-weight: 600; padding: 1px 7px; border-radius: 10px; }
.add-new-addr-btn { display: flex; align-items: center; gap: 6px; padding: 10px 14px; border: 1.5px dashed #e2e8f0; border-radius: 8px; color: #3b82f6; font-size: 13px; background: none; width: 100%; justify-content: center; }
.add-new-addr-btn:hover { background: #f0f7ff; }

@keyframes spin { to { transform: rotate(360deg); } }

@media (max-width: 900px) { .layout { grid-template-columns: 1fr; } }
@media (max-width: 600px) {
  .cart-page { padding: 16px 14px 100px; }
  .cart-page h1 { font-size: 22px; margin-bottom: 20px; }
  .item { grid-template-columns: 72px 1fr; gap: 10px; padding: 12px; }
  .item img { width: 72px; height: 72px; }
  .qty, .subtotal, .remove { grid-column: 2; }
  .subtotal { font-size: 13px; min-width: unset; text-align: left; }
  .summary { padding: 16px; }
  .checkout-btn { padding: 14px; }
  /* Payment modal full screen on mobile */
  .modal-overlay { padding: 0; align-items: flex-end; }
  .modal { border-radius: 20px 20px 0 0; max-height: 92vh; max-width: 100%; }
  .pay-qr { padding: 16px 18px; }
  .qr-img { width: 180px; height: 180px; }
  .shipping-form .form-row { grid-template-columns: 1fr; }
}
</style>
