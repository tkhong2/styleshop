# Thanh toán

## Phương thức

### 1. Chuyển khoản ngân hàng (BIDV + SePay)

**Luồng kỹ thuật:**
1. User chọn "Chuyển khoản" → `selectMethod('qr')` tạo đơn ngay
2. Hiển thị QR VietQR + thông tin tài khoản VA
3. User chuyển khoản vào `962471OMBS` với mã `STYLE......`
4. User bấm "Tôi đã chuyển khoản" → bắt đầu polling
5. SePay nhận giao dịch → POST webhook → backend cập nhật
6. Frontend polling 5 giây nhận `payment_status: paid` → thành công

**QR URL:**
```
https://img.vietqr.io/image/BIDV-962471OMBS-compact2.png
  ?amount={total}
  &addInfo={transfer_note}
  &accountName=TRAN%20KHAC%20HONG
```

**Webhook SePay:**
- URL: `https://styleshop-8sdf.onrender.com/api/orders/webhook/sepay`
- Header: `Authorization: Apikey styleshop2026`
- Match: số tiền >= tổng đơn (fallback không cần mã)

### 2. Ví MoMo
- Dùng cùng QR VietQR BIDV (demo)
- Cần tích hợp MoMo Business API cho production

### 3. COD (Thanh toán khi nhận hàng)
- Form nhập: họ tên, SĐT, địa chỉ, quận/huyện, tỉnh/thành, ghi chú
- Đơn hàng xác nhận ngay (`payment_status: paid`)

## Polling

```js
// Polling mỗi 5 giây, tối đa 5 phút
pollTimer = setInterval(async () => {
  const res = await orderService.getPaymentStatus(currentOrderId)
  if (res.payment_status === 'paid') {
    // Hiện thành công
  }
  // Fallback: check tất cả đơn của user
}, 5000)
```

## Mã giảm giá

| Mã | Giảm | Ghi chú |
|----|------|---------|
| STYLE10 | 10% | Mọi đơn hàng |
| SALE20 | 20% | Mọi đơn hàng |
| NEWUSER | 15% | Khách hàng mới |

## Phí vận chuyển
- Đơn < 500.000đ: 30.000đ (test: 1.000đ)
- Đơn ≥ 500.000đ: Miễn phí
